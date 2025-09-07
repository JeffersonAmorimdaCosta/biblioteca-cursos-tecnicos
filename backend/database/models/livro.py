from sqlalchemy import Column, ForeignKey, Integer, String

from . import Model


class Livro(Model):
    __tablename__ = 'livros'

    id = Column(Integer, primary_key=True)
    titulo = Column(String(200), nullable=False)
    link = Column(String(200), nullable=False)
    disciplina_id = Column(Integer, ForeignKey('disciplinas.id'), nullable=False)

    @classmethod
    def get_all(cls, session):
        """Retorna todos os livros."""
        return session.query(cls).all()

    @classmethod
    def get_by_id(cls, session, livro_id):
        """Busca um livro pelo ID."""
        return session.query(cls).filter(cls.id == livro_id).first()

    @classmethod
    def get_by_disciplina(cls, session, disciplina_id):
        """Retorna livros de uma disciplina específica."""
        return session.query(cls).filter(cls.disciplina_id == disciplina_id).all()

    @classmethod
    def create(cls, session, titulo, link, disciplina_id):
        """Cria um novo livro."""
        livro = cls(titulo=titulo, link=link, disciplina_id=disciplina_id)
        session.add(livro)
        session.flush()
        return livro

    @classmethod
    def update(cls, session, livro_id, titulo=None, link=None, disciplina_id=None):
        """Atualiza um livro."""
        livro = cls.get_by_id(session, livro_id)
        if not livro:
            return None
        if titulo is not None:
            livro.titulo = titulo
        if link is not None:
            livro.link = link
        if disciplina_id is not None:
            livro.disciplina_id = disciplina_id
        return livro

    @classmethod
    def delete(cls, session, livro_id):
        """Deleta um livro."""
        livro = cls.get_by_id(session, livro_id)
        if livro:
            session.delete(livro)
            return True
        return False

    def __repr__(self):
        return f'<Livro {self.titulo}>'

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'link': self.link,
            'disciplina_id': self.disciplina_id
        }
