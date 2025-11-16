from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Tipo de peça (apenas nome na API)
class TipoPecaCreate(BaseModel):
    nome: str

class TipoPecaOut(BaseModel):
    id: int
    nome: str
    class Config:
        orm_mode = True

# Estoque novo
class EstoqueNovoCreate(BaseModel):
    nome_peca: str
    quantidade: int

class EstoqueNovoOut(BaseModel):
    id: int
    tipo_peca_id: int
    quantidade: int
    class Config:
        orm_mode = True

# Estoque defeituoso (leitura)
class EstoqueDefeituosoOut(BaseModel):
    id: int
    tipo_peca_id: int
    quantidade: int
    class Config:
        orm_mode = True

# Tecnico
class TecnicoCreate(BaseModel):
    nome: str

class TecnicoOut(BaseModel):
    id: int
    nome: str
    is_supervisor: bool
    class Config:
        orm_mode = True

# Registrar peça defeituosa (input uses names)
class PecaDefeituosaCreate(BaseModel):
    nome_peca: str
    numero_serie: str
    tecnico_nome: str

class PecaDefeituosaOut(BaseModel):
    id: int
    nome_peca: str
    numero_serie: str
    tecnico_nome: str
    data_hora: datetime
    class Config:
        orm_mode = True

# Troca output: returns readable fields (names)
class TrocaOut(BaseModel):
    id: int
    numero_serie: str
    nome_peca: str
    tecnico_que_entregou: str
    supervisora: str
    data_hora: datetime
    class Config:
        orm_mode = True
class PecaDefeituosaOut(BaseModel):
    id: int
    tipo_peca: str
    numero_serie: str
    tecnico: str
    data_hora: datetime

    class Config:
        orm_mode = True
