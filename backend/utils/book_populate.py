from . import Livro, Disciplina, get_logger
from .database import DataBase
from .scraping import scraping_main
import pdfplumber
import requests
from io import BytesIO
import re

logger = get_logger('book_populate')

def populate_books():

    with DataBase() as db:
        try:
            disciplinas = get_disciplinas(session=db.session)
            
            update_ementas(disciplinas, session=db.session)
            livros = extrair_livros(disciplinas)
            if livros:
                for livro in livros:
                    livro_obj = Livro.create(db.session, titulo=livro['titulo'], link='', disciplina_id=livro['disciplina_id'])
                    logger.info(f'Livro criado: {livro_obj.titulo}')
                db.session.commit()
            else:
                logger.info('Nenhum livro para popular.')
        except Exception as e:
            db.session.rollback()
            logger.error(f'Erro ao popular livros: {e}')
        

def ementa_to_text(link: str) -> str:
    """Extrai a ementa de uma disciplina a partir do link fornecido."""
    try:
        response = requests.get(link)
        response.raise_for_status()
        with pdfplumber.open(BytesIO(response.content)) as pdf:
            ementa = ''
            for page in pdf.pages:
                ementa += page.extract_text()
            return ementa
    except requests.RequestException as e:
        logger.error(f'Erro ao acessar {link}: {e}')
        return 'Erro ao acessar a página da disciplina.'

def limpar_referencias(texto):
    """
    Limpa e separa as referências bibliográficas baseado no padrão de ano.
    
    Args:
        texto (str): Texto com referências bibliográficas
        
    Returns:
        list: Lista de referências limpas
    """
    if not texto or not texto.strip():
        return []
    
    # Regex: captura qualquer coisa até um ano no formato XXXX seguido de ponto ou ponto e vírgula
    pattern = re.compile(r'.+?\d{4}[.;]', re.DOTALL)
    refs = pattern.findall(texto)
    
    # Remove espaços e quebras de linha extras
    referencias_limpas = []
    for ref in refs:
        ref_limpa = re.sub(r'\s+', ' ', ref).strip()
        # Valida se tem pelo menos 10 caracteres e contém um ano
        if len(ref_limpa) > 10 and re.search(r'\d{4}', ref_limpa):
            referencias_limpas.append(ref_limpa)
    
    return referencias_limpas

def extrair_bibliografia(ementa_texto):
    """
    Extrai e organiza a bibliografia de uma ementa.
    
    Args:
        ementa_texto (str): Texto completo da ementa
        
    Returns:
        str: String com todas as referências bibliográficas separadas por "#"
    """
    if not ementa_texto:
        return ""
    
    # Busca pela seção de Bibliografia
    match_bibliografia = re.search(r'Bibliografia\s*(.+)', ementa_texto, re.DOTALL | re.IGNORECASE)
    
    if not match_bibliografia:
        logger.warning("Seção 'Bibliografia' não encontrada na ementa")
        return ""
    
    bibliografia_texto = match_bibliografia.group(1)
    
    # Tenta separar Bibliografia Básica e Complementar
    pattern_divisao = re.compile(r'Básica\s*(.+?)\s*Complementar\s*(.+)', re.DOTALL | re.IGNORECASE)
    match_divisao = pattern_divisao.search(bibliografia_texto)
    
    todas_referencias = []
    
    if match_divisao:
        basica_texto = match_divisao.group(1)
        complementar_texto = match_divisao.group(2)

        refs_basicas = limpar_referencias(basica_texto)
        refs_complementares = limpar_referencias(complementar_texto)
        
        todas_referencias.extend(refs_basicas)
        todas_referencias.extend(refs_complementares)

        if len(todas_referencias) > 20:
            breakpoint()
        
        logger.info(f"Bibliografia extraída: {len(refs_basicas)} básicas, {len(refs_complementares)} complementares")
    else:
        # Se não conseguir separar, pega tudo como uma bibliografia única
        todas_referencias = limpar_referencias(bibliografia_texto)
        logger.info(f"Bibliografia extraída (sem divisão): {len(todas_referencias)} referências")

    # Retorna todas as referências separadas por "#"
    return "#".join(todas_referencias)

def get_disciplinas(session):
    return Disciplina.get_all(session)

def update_ementas(disciplinas, session):
    try:
        logger.info(f'Obtendo ementas')
        logger.info(f'Total de disciplinas: {len(disciplinas)}')

        for disciplina in disciplinas:
            ementa = ementa_to_text(disciplina.ementa)
            if ementa:
                logger.info(f'Obtida ementa para {disciplina.nome}')
                bibliografia = extrair_bibliografia(ementa)
                if bibliografia:
                    Disciplina.update(session=session, id=disciplina.id, ementa=ementa, bibliografia=str(bibliografia))
                    logger.info(f'Atualizada ementa e bibliografia para {disciplina.nome}')
                else:
                    logger.warning(f'Sem bibliografia para {disciplina.nome}')
            else:
                logger.warning(f'Sem ementa para {disciplina.nome}')
        session.commit()
        logger.info('Ementas atualizadas')

    except Exception as e:
        logger.error(f'Erro ao obter disciplinas: {e}')
        return None
    
def extrair_livros(disciplinas):
    livros = []
    try:
        for disciplina in disciplinas:
            bibliografia = disciplina.bibliografia
            if bibliografia:
                livros.extend({'titulo': livro.strip(), 'disciplina_id': disciplina.id } for livro in bibliografia.split('#') if livro.strip())
        logger.info(f'Total de livros extraídos: {len(livros)}')
        return livros
    except Exception as e:
        logger.error(f'Erro ao mapear livros: {e}')    

if __name__ == '__main__':
    scraping_main()
    populate_books()


