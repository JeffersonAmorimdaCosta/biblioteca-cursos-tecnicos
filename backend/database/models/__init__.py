from sqlalchemy.ext.declarative import declarative_base

# Importar todos os modelos para garantir que sejam registrados
from .curso import Curso
from .disciplina import Disciplina
from .livro import Livro
from .map_curso_disciplina import MapCursoDisciplina

Model = declarative_base()

__all__ = ['Model', 'Curso', 'Disciplina', 'Livro', 'MapCursoDisciplina']
