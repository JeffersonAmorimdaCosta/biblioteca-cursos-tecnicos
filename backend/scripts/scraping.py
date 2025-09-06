# Imports
import requests
from bs4 import BeautifulSoup


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


if __name__ == '__main__':
    links_cursos_tecnicos = [
        'https://estudante.ifpb.edu.br/cursos/155/',  # Edificações
        'https://estudante.ifpb.edu.br/cursos/90/',  # Informática
        'https://estudante.ifpb.edu.br/cursos/85/',  # Mineração
        'https://estudante.ifpb.edu.br/cursos/88/',  # Petróleo e Gás
        'https://estudante.ifpb.edu.br/cursos/154/',  # Química
    ]

    for link in links_cursos_tecnicos:
        pagina = fazer_requisicao_get(link)
        pagina_parsed = BeautifulSoup(pagina.text, 'html.parser')

        nome = pagina_parsed.select_one('h2.titulo.azul-petroleo')
        print(nome.text)
