from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..database.models import Model
from . import get_logger

class DataBase:
    def __init__(self):
        self.engine = create_engine('sqlite:///backend/database/biblioteca.db', echo=False)
        Model.metadata.create_all(self.engine)
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)()
        self.logger = get_logger('database')
        self.logger.info('Database session created')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.session.rollback()
            self.logger.error(f'Database transaction rolled back: {exc_val}')
        else:
            self.session.commit()
            self.logger.info('Database transaction committed')
        self.session.close()

    def close(self):
        """Fecha a sessão do banco de dados."""
        self.session.close()
        self.logger.info('Database session closed')

if __name__ == '__main__':
    # Testando a conexão com o banco de dados
    with DataBase() as db:
        print("Database connected and session started.")