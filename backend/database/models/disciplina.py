from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from . import Model

class Disciplina(Model):
    __tablename__ = 'disciplinas'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    tec = Column(Boolean, nullable=False)
    ementa = Column(String(200), nullable=False)
    serie = Column(Integer, nullable=False)

    @classmethod
    def get_all(cls, session):
        """Retorna todas as disciplinas."""
        return session.query(cls).all()

    @classmethod
    def get_by_id(cls, session, disciplina_id):
        """Busca uma disciplina pelo ID."""
        return session.query(cls).filter(cls.id == disciplina_id).first()

    @classmethod
    def get_by_curso(cls, session, curso_id):
        """Retorna disciplinas de um curso específico."""
        from .map_curso_disciplina import MapCursoDisciplina
        return (session.query(cls)
                .join(MapCursoDisciplina, cls.id == MapCursoDisciplina.disciplina_id)
                .filter(MapCursoDisciplina.curso_id == curso_id)
                .all())
    
    @classmethod
    def create(cls, session, nome, tec, ementa, serie):
        """Cria uma nova disciplina."""
        disci_exists = session.query(cls).filter(cls.nome == nome, cls.serie == serie).first()
        if disci_exists:
            return disci_exists
        
        disciplina = cls(nome=nome, tec=tec, ementa=ementa, serie=serie)
        session.add(disciplina)
        session.flush()
        return disciplina

    def update(self, session, nome=None, tec=None, ementa=None, serie=None):
        """Atualiza uma disciplina."""
        if nome is not None:
            self.nome = nome
        if tec is not None:
            self.tec = tec
        if ementa is not None:
            self.ementa = ementa
        if serie is not None:
            self.serie = serie
        return self

    def delete(self, session):
        """Deleta uma disciplina."""
        session.delete(self)
        return True

    def __repr__(self):
        return f'<Disciplina {self.nome}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'tec': self.tec,
            'ementa': self.ementa,
            'serie': self.serie
        }