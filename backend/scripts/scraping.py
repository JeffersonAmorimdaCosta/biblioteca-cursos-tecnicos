if __name__ == '__main__':
    # Imports
    from urllib.parse import urljoin

    import requests
    from bs4 import BeautifulSoup

    URL_BASE = 'https://estudante.ifpb.edu.br/'
    LINK_PAGINA_CURSOS_TECNICOS = 'https://estudante.ifpb.edu.br/cursos/?' \
        'cidade=8&modalidade=&nome=&formacao=&nivel_formacao=TECNICO&turno=&' \
        'forma_acesso='

    links_cursos_tecnicos = []

    try:
        pagina_cursos = requests.get(
            LINK_PAGINA_CURSOS_TECNICOS, timeout=10)
        pagina_cursos.raise_for_status()
    except requests.exceptions.Timeout:
        print('O servidor demorou para responder.')
    except requests.exceptions.RequestException:
        print('Erro na requisição.')
    else:
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

    if links_cursos_tecnicos:
        print(links_cursos_tecnicos)
    else:
        print('Erro na requisição.')
