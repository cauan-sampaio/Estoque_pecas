from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException
import models, schemas
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, func
from datetime import datetime

# Helper constants
SUPERVISORA_NOME = "Elisangela"

# ---------- Tipo de peça ----------
def criar_tipo_peca(db: Session, nome: str):
    nome = nome.strip()
    if not nome:
        raise HTTPException(status_code=400, detail="Nome da peça inválido")
    existing = db.query(models.TipoPeca).filter(func.lower(models.TipoPeca.nome) == nome.lower()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Tipo de peça já existe")
    tp = models.TipoPeca(nome=nome)
    db.add(tp)
    try:
        db.commit()
        db.refresh(tp)
        return tp
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# ---------- Estoque Novo ----------
def adicionar_estoque_novo(db: Session, nome_peca: str, quantidade: int):
    if quantidade <= 0:
        raise HTTPException(status_code=400, detail="Quantidade deve ser maior que zero")
    # resolve tipo_peca pelo nome
    tp = db.query(models.TipoPeca).filter(func.lower(models.TipoPeca.nome) == nome_peca.strip().lower()).first()
    if not tp:
        raise HTTPException(status_code=404, detail="Tipo de peça não encontrado (crie antes)")
    est = db.query(models.EstoqueNovo).filter(models.EstoqueNovo.tipo_peca_id == tp.id).first()
    if est:
        est.quantidade += quantidade
    else:
        est = models.EstoqueNovo(tipo_peca_id=tp.id, quantidade=quantidade)
        db.add(est)
    db.commit()
    db.refresh(est)
    return est

def listar_estoque_novo(db: Session):
    # return list of (tipo_nome, quantidade)
    rows = db.query(models.EstoqueNovo, models.TipoPeca).join(models.TipoPeca, models.EstoqueNovo.tipo_peca_id == models.TipoPeca.id).all()
    out = []
    for est, tp in rows:
        out.append({"tipo_peca": tp.nome, "quantidade": est.quantidade})
    return out

# ---------- Estoque Defeituoso ----------
def get_or_create_estoque_defeituoso(db: Session, tipo_id: int):
    estd = db.query(models.EstoqueDefeituoso).filter(models.EstoqueDefeituoso.tipo_peca_id == tipo_id).first()
    if not estd:
        estd = models.EstoqueDefeituoso(tipo_peca_id=tipo_id, quantidade=0)
        db.add(estd)
        db.commit()
        db.refresh(estd)
    return estd

# ---------- Tecnico ----------
def criar_tecnico(db: Session, nome: str):
    nome = nome.strip()
    if not nome:
        raise HTTPException(status_code=400, detail="Nome inválido")
    if nome == SUPERVISORA_NOME:
        raise HTTPException(status_code=400, detail="Nome reservado para a supervisora")
    existing = db.query(models.Tecnico).filter(func.lower(models.Tecnico.nome) == nome.lower()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Técnico já existe")
    t = models.Tecnico(nome=nome, is_supervisor=False)
    db.add(t)
    try:
        db.commit()
        db.refresh(t)
        return t
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# ---------- Registrar peça defeituosa (feito por técnico) ----------
def registrar_peca_defeituosa(db: Session, dto: schemas.PecaDefeituosaCreate):
    # resolve tipo_peca
    tp = db.query(models.TipoPeca).filter(func.lower(models.TipoPeca.nome) == dto.nome_peca.strip().lower()).first()
    if not tp:
        raise HTTPException(status_code=404, detail="Tipo de peça não encontrado (crie antes)")

    # resolve tecnico: if not exists, create automatically (or error - here we create)
    tecnico = db.query(models.Tecnico).filter(func.lower(models.Tecnico.nome) == dto.tecnico_nome.strip().lower()).first()
    if not tecnico:
        tecnico = models.Tecnico(nome=dto.tecnico_nome.strip(), is_supervisor=False)
        db.add(tecnico)
        try:
            db.commit()
            db.refresh(tecnico)
        except IntegrityError:
            db.rollback()
            tecnico = db.query(models.Tecnico).filter(func.lower(models.Tecnico.nome) == dto.tecnico_nome.strip().lower()).first()

    # create peca defeituosa and increment estoque_defeituoso
    try:
        p = models.PecaDefeituosa(tipo_peca_id=tp.id, numero_serie=dto.numero_serie.strip(), tecnico_id=tecnico.id)
        db.add(p)
        db.commit()
        db.refresh(p)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Número de série já registrado")

    # increment defective stock
    estd = get_or_create_estoque_defeituoso(db, tp.id)
    estd.quantidade += 1
    db.commit()
    db.refresh(estd)

    return {
        "id": p.id,
        "nome_peca": tp.nome,
        "numero_serie": p.numero_serie,
        "tecnico_nome": tecnico.nome,
        "data_hora": p.data_hora
    }

# ---------- Realizar troca (apenas supervisora) ----------
def realizar_troca(db: Session, peca_defeituosa_id: int, supervisora_nome: str):
    # verify supervisora exists and is supervisor
    sup = db.query(models.Tecnico).filter(func.lower(models.Tecnico.nome) == supervisora_nome.strip().lower(), models.Tecnico.is_supervisor == True).first()
    if not sup:
        raise HTTPException(status_code=401, detail="Supervisora inválida ou não encontrada")

    # transaction: check defective piece exists
    p = db.query(models.PecaDefeituosa).filter(models.PecaDefeituosa.id == peca_defeituosa_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Peça defeituosa não encontrada")

    tp_id = p.tipo_peca_id

    # lock estoque_novo row
    est_novo = db.query(models.EstoqueNovo).filter(models.EstoqueNovo.tipo_peca_id == tp_id).with_for_update().first()
    if not est_novo or est_novo.quantidade <= 0:
        raise HTTPException(status_code=400, detail="Estoque insuficiente para realizar a troca")

    try:
        # decrement new stock
        est_novo.quantidade -= 1
        # ensure defective stock incremented (the defective piece may already be recorded via registrar_peca_defeituosa;
        # but business rule requires piece defeituosa to be added to defective stock upon registration and on trade we also ensure it's present)
        est_def = get_or_create_estoque_defeituoso(db, tp_id)
        est_def.quantidade += 1

        # insert troca
        troca = models.Troca(peca_defeituosa_id=p.id, tipo_peca_id=tp_id, supervisora_id=sup.id, data_hora=datetime.utcnow())
        db.add(troca)
        db.commit()
        db.refresh(troca)
        db.refresh(est_novo)
        db.refresh(est_def)

        # prepare output: include readable names
        tecnico_entregou = db.query(models.Tecnico).filter(models.Tecnico.id == p.tecnico_id).first()
        tipo = db.query(models.TipoPeca).filter(models.TipoPeca.id == tp_id).first()

        return {
            "id": troca.id,
            "numero_serie": p.numero_serie,
            "nome_peca": tipo.nome,
            "tecnico_que_entregou": tecnico_entregou.nome if tecnico_entregou else None,
            "supervisora": sup.nome,
            "data_hora": troca.data_hora
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# ---------- Consultas ----------
def consultar_trocas_por_numero(db: Session, numero_serie: str):
    # find defective piece by serial
    p = db.query(models.PecaDefeituosa).filter(models.PecaDefeituosa.numero_serie == numero_serie.strip()).first()
    if not p:
        return []
    # find related troca(s)
    trocas = db.query(models.Troca).filter(models.Troca.peca_defeituosa_id == p.id).all()
    out = []
    tipo = db.query(models.TipoPeca).filter(models.TipoPeca.id == p.tipo_peca_id).first()
    tecnico_entregou = db.query(models.Tecnico).filter(models.Tecnico.id == p.tecnico_id).first()
    for t in trocas:
        sup = db.query(models.Tecnico).filter(models.Tecnico.id == t.supervisora_id).first()
        out.append({
            "troca_id": t.id,
            "numero_serie": p.numero_serie,
            "nome_peca": tipo.nome if tipo else None,
            "tecnico_que_entregou": tecnico_entregou.nome if tecnico_entregou else None,
            "supervisora": sup.nome if sup else None,
            "data_hora": t.data_hora
        })
    return out

def listar_pecas_defeituosas(db: Session):
    query = text("""
        SELECT 
            p.id AS id,
            t.nome AS tipo_peca,
            p.numero_serie AS numero_serie,
            tec.nome AS tecnico,
            p.data_hora AS data_hora
        FROM pecas_defeituosas p
        INNER JOIN tipos_peca t ON t.id = p.tipo_peca_id
        INNER JOIN tecnicos tec ON tec.id = p.tecnico_id
        ORDER BY p.data_hora DESC;
    """)

    return db.execute(query).mappings().all()
