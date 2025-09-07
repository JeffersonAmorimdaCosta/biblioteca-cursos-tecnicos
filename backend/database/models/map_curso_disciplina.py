from sqlalchemy import Column, Integer

from . import Model


class MapCursoDisciplina(Model):
    __tablename__ = 'map_curso_disciplina'
    curso_id = Column(Integer, primary_key=True)
    disciplina_id = Column(Integer, primary_key=True)

    @classmethod
    def create(cls, session, curso_id, disciplina_id):
        """Cria um mapeamento entre curso e disciplina, se ainda não existir."""
        existing = cls.get_by_curso_disciplina(session, curso_id, disciplina_id)
        if existing:
            return existing
        map_obj = cls(curso_id=curso_id, disciplina_id=disciplina_id)
        session.add(map_obj)
        return map_obj

    @classmethod
    def get_by_curso_disciplina(cls, session, curso_id, disciplina_id):
        """Busca um mapeamento específico."""
        return (session.query(cls)
                .filter(cls.curso_id == curso_id, cls.disciplina_id == disciplina_id)
                .first())

    def delete(self, session):
        """Deleta um mapeamento."""
        session.delete(self)
        return True

    def __repr__(self):
        return f'<MapCursoDisciplina curso_id={self.curso_id} disciplina_id={self.disciplina_id}>'

    def to_dict(self):
        return {
            'curso_id': self.curso_id,
            'disciplina_id': self.disciplina_id
        }
