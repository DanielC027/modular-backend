from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Float,
    CheckConstraint,
    UniqueConstraint,
    LargeBinary,
)
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)


class Escrito(Base):
    __tablename__ = "escrito"

    id_escrito = Column(Integer, primary_key=True, index=True)
    fecha = Column(String, nullable=False)
    huella_digital = Column(LargeBinary, nullable=False)
    # Relacion con analisis
    analisis = relationship("Analisis", back_populates="escrito", cascade="all, delete")


class Analisis(Base):
    __tablename__ = "analisis"

    id_analisis = Column(Integer, primary_key=True, index=True)
    id_escrito = Column(
        Integer, ForeignKey("escrito.id_escrito", ondelete="CASCADE"), nullable=False
    )

    escrito = relationship("Escrito", back_populates="analisis")
    emociones = relationship(
        "ListaEmociones", back_populates="analisis", cascade="all, delete"
    )


class Emocion(Base):
    __tablename__ = "emocion"

    id_emocion = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)

    analisis = relationship("ListaEmociones", back_populates="emocion")


class ListaEmociones(Base):
    __tablename__ = "lista_emociones"

    id_lista_emociones = Column(Integer, primary_key=True, index=True)

    id_analisis = Column(
        Integer, ForeignKey("analisis.id_analisis", ondelete="CASCADE"), nullable=False
    )
    id_emocion = Column(
        Integer, ForeignKey("emocion.id_emocion", ondelete="RESTRICT"), nullable=False
    )

    porcentaje_emocion = Column(Float, nullable=False)

    __table_args__ = (
        CheckConstraint("porcentaje_emocion >= 0 AND porcentaje_emocion <= 100"),
        UniqueConstraint("id_analisis", "id_emocion"),
    )

    analisis = relationship("Analisis", back_populates="emociones")
    emocion = relationship("Emocion", back_populates="analisis")
