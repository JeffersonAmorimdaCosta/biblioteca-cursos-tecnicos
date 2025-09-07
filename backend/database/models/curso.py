from sqlalchemy import Column, Integer, String

from . import Model


class Curso(Model):
    __tablename__ = 'cursos'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)

    @classmethod
    def get_all(cls, session):
        """Retorna todos os cursos."""
        return session.query(cls).all()

    @classmethod
    def get_by_id(cls, session, curso_id):
        """Busca um curso pelo ID."""
        return session.query(cls).filter(cls.id == curso_id).first()

    @classmethod
    def create(cls, session, id, nome):
        """Cria um novo curso."""
        curso_exists = session.query(cls).filter(cls.id == id).first()
        if curso_exists:
            return curso_exists
        curso = cls(id=id, nome=nome)
        session.add(curso)
        return curso

    def delete(self, session):
        """Deleta um curso."""
        session.delete(self)
        return True

    def __repr__(self):
        return f'<Curso {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome
        }
