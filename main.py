from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine, Base
import controllers as ctrl
from typing import Optional

# cria tabelas ORM
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Manutencao Micros")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# header name for supervisor checks
SUPERVISORA_HEADER = "X-Supervisora"

# helper dependency to require supervisora header and validate it exists and is supervisor
def require_supervisora(x_supervisora: Optional[str] = Header(None), db: Session = Depends(get_db)):
    if not x_supervisora:
        raise HTTPException(status_code=401, detail="Cabeçalho X-Supervisora é obrigatório")
    sup = db.query(models.Tecnico).filter(models.Tecnico.nome == x_supervisora.strip(), models.Tecnico.is_supervisor == True).first()
    if not sup:
        raise HTTPException(status_code=401, detail="Supervisora inválida ou sem permissão")
    return sup

# root
@app.get("/")
def root():
    return {"status": "API Manutencao Micros funcionando"}

# ----------------- Rotas de administrador (somente supervisora) -----------------
@app.post("/tipopeca", response_model=schemas.TipoPecaOut)
def criar_tipo_peca(data: schemas.TipoPecaCreate, sup: models.Tecnico = Depends(require_supervisora), db: Session = Depends(get_db)):
    return ctrl.criar_tipo_peca(db, data.nome)

@app.post("/estoque/novo")
def adicionar_estoque_novo(data: schemas.EstoqueNovoCreate, sup: models.Tecnico = Depends(require_supervisora), db: Session = Depends(get_db)):
    return ctrl.adicionar_estoque_novo(db, data.nome_peca, data.quantidade)

@app.post("/tecnico", response_model=schemas.TecnicoOut)
def criar_tecnico(data: schemas.TecnicoCreate, sup: models.Tecnico = Depends(require_supervisora), db: Session = Depends(get_db)):
    return ctrl.criar_tecnico(db, data.nome)

@app.post("/troca/{peca_defeituosa_id}")
def realizar_troca(peca_defeituosa_id: int, sup: models.Tecnico = Depends(require_supervisora), db: Session = Depends(get_db)):
    return ctrl.realizar_troca(db, peca_defeituosa_id, sup.nome)

# ----------------- Rotas abertas (consultas / tecnico registra defeito) -----------------
@app.get("/estoque/novo")
def ver_estoque_novo(db: Session = Depends(get_db)):
    return ctrl.listar_estoque_novo(db)

@app.post("/peca_defeituosa")
def reg_peca_defeituosa(data: schemas.PecaDefeituosaCreate, db: Session = Depends(get_db)):
    return ctrl.registrar_peca_defeituosa(db, data)

@app.get("/trocas/serie/{numero_serie}")
def trocas_por_serie(numero_serie: str, db: Session = Depends(get_db)):
    return ctrl.consultar_trocas_por_numero(db, numero_serie)

@app.get("/pecas_defeituosas", response_model=list[schemas.PecaDefeituosaOut])
def listar_defeituosas(db: Session = Depends(get_db)):
    return ctrl.listar_pecas_defeituosas(db)
