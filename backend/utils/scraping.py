from . import (
    BASE_URL,
    CURSOS,
    CURSOS_URL,
    BeautifulSoup,
    Curso,
    Disciplina,
    MapCursoDisciplina,
    get_logger,
    requests,
)
from .database import DataBase

logger = get_logger("Scraping")


def main():
    disciplinas_por_curso = scrape_cursos()
    save_data(disciplinas_por_curso)


def save_data(data) -> None:
    """
    Função placeholder para salvar os dados extraídos.

    Args:
        data (dict): Dicionário com os dados a serem salvos.
    """
    cursos_obj = set()
    disciplinas_obj = set()

    with DataBase() as db:
        try:
            for id, nome in CURSOS.items():
                curso_obj = Curso.create(db.session, id, nome)
                cursos_obj.add(curso_obj.nome)
                logger.info(f"Salvo curso: {curso_obj.to_dict()}")

                for disciplina, link in data[nome]:
                    disc_obj = Disciplina.create(
                        db.session,
                        nome=disciplina,
                        tec=False,
                        ementa=link,
                        serie=0
                    )

                    if not MapCursoDisciplina.get_by_curso_disciplina(db.session, curso_obj.id, disc_obj.id):
                        MapCursoDisciplina.create(db.session, curso_obj.id, disc_obj.id)
                    disciplinas_obj.add(disc_obj.nome)
                    logger.info(f"Salvo disciplina: {disc_obj.to_dict()}")
                    logger.info(f"Mapeamento curso-disciplina criado:\n{curso_obj.id} -> {disc_obj.id}")

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao salvar dados: {e}")
            raise

    logger.info(f"Total de cursos salvos: {len(cursos_obj)}")
    logger.info(f"Total de disciplinas salvas: {len(disciplinas_obj)}")


def scrape_cursos():
    """
    Realiza o scraping dos cursos técnicos do IFPB.

    Returns:
        dict: Dicionário com IDs e nomes dos cursos.
    """
    links_cursos_tecnicos = {curso: f'{CURSOS_URL}{id}/' for id, curso in CURSOS.items()}
    logger.info(f"Links dos cursos técnicos: {links_cursos_tecnicos}")
    disciplinas_cursos = {}

    for curso, link in links_cursos_tecnicos.items():
        pagina = fazer_requisicao_get(link)

        disciplinas = extrair_disciplinas(pagina)
        logger.info(f"Disciplinas encontradas: {len(disciplinas)}")

        disciplinas_cursos[curso] = disciplinas

    return disciplinas_cursos


def fazer_requisicao_get(url: str) -> str:
    """
    Realiza uma requisição HTTP GET e retorna o conteúdo da página.

    Args:
        url (str): URL da página a ser acessada.

    Raises:
        RuntimeError: se a requisição falhar.
    """
    try:
        pag = requests.get(url, timeout=10)
        pag.raise_for_status()
        return pag.text
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f'Ocorreu um erro na requisição: {e}') from e


def extrair_disciplinas(pagina: str) -> set[dict]:
    """
    Extrai a lista de disciplinas de uma página HTML.

    Args:
        pagina (str): Conteúdo HTML da página.

    Returns:
        list[dict]: Lista de dicionários com 'nome' e 'link' das disciplinas.
    """
    soup = BeautifulSoup(pagina, 'html.parser')
    disciplinas = set()

    links_disciplinas = soup.select('a[href*="/disciplina/"][href$=".pdf"]')

    for disciplina in links_disciplinas:
        nome = disciplina.get_text(strip=True)
        link = disciplina.get('href')

        if link and link.startswith('/'):
            link = BASE_URL + link

        disciplinas.add((nome, link))

    return disciplinas


if __name__ == '__main__':
    main()
