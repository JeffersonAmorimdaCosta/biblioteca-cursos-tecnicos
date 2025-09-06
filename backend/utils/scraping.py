# Imports
from . import (requests,
               BeautifulSoup,
               get_logger,
               BASE_URL,
               CURSOS_URL,
               CURSOS)

logger = get_logger("Scraping")

def fazer_requisicao_get(url: str) -> requests.Response:
    """
    Realiza uma requisição HTTP GET e retorna o Response.

    Args:
        url (str): URL da página a ser acessada.

    Raises:
        RuntimeError: se a requisição falhar.
    """
    try:
        pag = requests.get(url, timeout=10)
        pag.raise_for_status()
        return pag
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f'Ocorreu um erro na requisição: {e}') from e

def extrair_disciplinas(pagina: str) -> list[dict]:
    """
    Extrai a lista de disciplinas de uma página HTML.

    Args:
        pagina (str): Conteúdo HTML da página.

    Returns:
        list[dict]: Lista de dicionários com 'nome' e 'link' das disciplinas.
    """
    soup = BeautifulSoup(pagina, 'html.parser')
    disciplinas = []

    links_disciplinas = soup.select('a[href*="/disciplina/"][href$=".pdf"]')

    for disciplina in links_disciplinas:
        nome = disciplina.get_text(strip=True)
        link = disciplina.get('href')
        
        if link and link.startswith('/'):
            link = BASE_URL + link

        disciplinas.append({
            'nome': nome,
            'link': link
        })

    return disciplinas

if __name__ == '__main__':
    links_cursos_tecnicos = [
        f'{CURSOS_URL}{id}/' for id in CURSOS.keys()
    ]

    for link in links_cursos_tecnicos:
        pagina = fazer_requisicao_get(link)
        pagina_parsed = BeautifulSoup(pagina.text, 'html.parser')
        
        nome_curso = pagina_parsed.select_one('h2.titulo.azul-petroleo')
        logger.info(f"Curso: {nome_curso.text if nome_curso else 'Nome não encontrado'}")
        
        disciplinas = extrair_disciplinas(pagina.text)
        logger.info(f"Disciplinas encontradas: {len(disciplinas)}")
        
        for disciplina in disciplinas:
            logger.info(f"  - Nome: {disciplina['nome']}")
            logger.info(f"    Link: {disciplina['link']}")
        
        logger.info("-" * 50)
