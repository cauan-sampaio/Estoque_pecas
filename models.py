
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class TipoPeca(Base):
    __tablename__ = "tipos_peca"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False, unique=True)

class Tecnico(Base):
    __tablename__ = "tecnicos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False, unique=True)
    is_supervisor = Column(Boolean, nullable=False, default=False)

class EstoqueNovo(Base):
    __tablename__ = "estoque_novo"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo_peca_id = Column(Integer, ForeignKey("tipos_peca.id"), nullable=False)
    quantidade = Column(Integer, nullable=False, default=0)

    tipo = relationship("TipoPeca")

class EstoqueDefeituoso(Base):
    __tablename__ = "estoque_defeituoso"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo_peca_id = Column(Integer, ForeignKey("tipos_peca.id"), nullable=False)
    quantidade = Column(Integer, nullable=False, default=0)

    tipo = relationship("TipoPeca")

class PecaDefeituosa(Base):
    __tablename__ = "pecas_defeituosas"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo_peca_id = Column(Integer, ForeignKey("tipos_peca.id"), nullable=False)
    numero_serie = Column(String(50), nullable=False, unique=True)
    tecnico_id = Column(Integer, ForeignKey("tecnicos.id"), nullable=False)
    data_hora = Column(DateTime, default=datetime.utcnow)

    tipo = relationship("TipoPeca")
    tecnico = relationship("Tecnico")

class Troca(Base):
    __tablename__ = "trocas"
    id = Column(Integer, primary_key=True, autoincrement=True)
    peca_defeituosa_id = Column(Integer, ForeignKey("pecas_defeituosas.id"), nullable=False)
    tipo_peca_id = Column(Integer, ForeignKey("tipos_peca.id"), nullable=False)
    supervisora_id = Column(Integer, ForeignKey("tecnicos.id"), nullable=False)  # refere-se à supervisora que executou
    data_hora = Column(DateTime, default=datetime.utcnow)

    peca_defeituosa = relationship("PecaDefeituosa")
    tipo = relationship("TipoPeca")
    supervisora = relationship("Tecnico", foreign_keys=[supervisora_id])
