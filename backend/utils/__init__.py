import logging

import colorlog
import requests
from bs4 import BeautifulSoup

from ..database.models import Curso as Curso
from ..database.models import Disciplina as Disciplina
from ..database.models import Livro as Livro
from ..database.models import MapCursoDisciplina as MapCursoDisciplina

BASE_URL = 'https://estudante.ifpb.edu.br'
CURSOS_URL = f'{BASE_URL}/cursos/'
CURSOS = {
    155: 'Edificações',
    90: 'Informática',
    85: 'Mineração',
    88: 'Petróleo e Gás',
    154: 'Química'
}


def get_logger(name: str) -> logging.Logger:
    """
    Configura e retorna um logger colorido.

    Args:
        name (str): Nome do logger.

    Returns:
        logging.Logger: Logger configurado com cores.
    """
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        handler = colorlog.StreamHandler()
        formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    return logger
