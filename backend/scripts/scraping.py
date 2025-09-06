# Imports
from urllib.parse import urljoin

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
    URL_BASE = 'https://estudante.ifpb.edu.br/'
    LINK_PAGINA_CURSOS_TECNICOS = 'https://estudante.ifpb.edu.br/cursos/?' \
        'cidade=8&modalidade=&nome=&formacao=&nivel_formacao=TECNICO&turno=&' \
        'forma_acesso='

    links_cursos_tecnicos = []

    pagina_cursos = fazer_requisicao_get(LINK_PAGINA_CURSOS_TECNICOS)

    pagina_cursos_parsed = BeautifulSoup(pagina_cursos.text, 'html.parser')
    cursos_tecnicos = pagina_cursos_parsed.find_all(
        'a', class_='list-group-item thumbnail'
    )

    nomes_cursos_tecnicos = ['Edificações', 'Informática',
                             'Mineração', 'Petróleo e Gás', 'Química']

    for curso in cursos_tecnicos:
        nome_curso = curso.select_one('p').text.strip()
        eh_integrado = 'Integrado' in curso.select_one('li').text.split()

        if nome_curso in nomes_cursos_tecnicos and eh_integrado:
            links_cursos_tecnicos.append(
                urljoin(URL_BASE, curso.get('href')))

    for link in links_cursos_tecnicos:
        pagina = fazer_requisicao_get(link)
        pagina_parsed = BeautifulSoup(pagina.text, 'html.parser')

        nome = pagina_parsed.select_one('h2.titulo.azul-petroleo')
        print(nome.text)
