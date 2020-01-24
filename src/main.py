from src.json_filter import filtro_json
from src.auxiliar import erro_diretorio_inexistente


def get_arqs_pesquisa():
    """
    Na pasta 'input_output' tem um txt que contem o nome dos arquivos que queremos pesquisar.
    Essa função vai ler o caminho (strirng) que direciona os arquivos de pesquisa e adicioná-los a uma lista.
    :return: lista contendo o caminho (string) dos arquivos de pesquisa.
    """
    entrada_pesquisa = 'input_output/arquivos_pesquisa.txt'
    try:
        arqs_pesquisa = open(entrada_pesquisa, encoding='utf-8')
    except FileNotFoundError:
        erro_diretorio_inexistente(entrada_pesquisa)
    else:
        lista_pesquisa = arqs_pesquisa.readlines()
        lista_pesquisa = list(map(lambda string: 'material_de_provas/' + string.replace('\n', ''), lista_pesquisa))
        arqs_pesquisa.close()
        return lista_pesquisa


def main():
    lista_arquivos_pesquisa = get_arqs_pesquisa()
    for pesquisa in lista_arquivos_pesquisa:
        filtro_json(pesquisa)


if __name__ == '__main__':
    main()
