from src import parametro_global
from src.auxiliar import erro_diretorio_inexistente
import json


def encontrar_data_documento(documento):
    """
    Procedimento resposável por encontrar a data (geralmente a data de aplicação da prova) do documento passado como
    parâmetro.
    :param documento: documento que será feita a pesquisa.
    :return: dicionário contendo as informações dia, mes e ano do documento
    """
    pegar_data = lambda data_string: list(map(int, data_string.split('/')))
    parametro_de_busca = 'Belo Horizonte'  # A data está na mesma linha em que 'Belo Horizonte' está
    for frase in documento:
        if parametro_de_busca in frase:
            inicio_slice = frase.find(',') + 1
            fim_slice = frase.find('\\')
            string_data = frase[inicio_slice:fim_slice:].strip()
            lista_data = pegar_data(string_data)
            dict_data = dict(dia=lista_data[0], mes=lista_data[1], ano=lista_data[2])
            return dict_data
    return None


def pegar_semestre(documento):
    """
    Procedimento que irá retornar o semestre de aplicação da prova/lista (por exemplo 2018.1)
    :param documento: documento que será feita a pesquisa.
    :return: Float que indica o semestre do documento.
    """
    data_documento = encontrar_data_documento(documento)
    if 1 <= data_documento['mes'] <= 6:  # Se está entre janeiro e junho, então é .1
        return float(str(data_documento['ano']) + '.1')
    else:  # Senão é .2
        return float(str(data_documento['ano']) + '.2')


def encontrar_tipo_da_questao(string_questao):
    if '\\choice' in string_questao:
        return 'multiplechoice'  # Questão aberta
    return 'open'  # Questão fechada


def encontrar_questoes(documento):
    """
    Procedimento que encontra todas as questões de um documento.
    :param documento: documento que será feita a pesquisa.
    :return: Lista de questões do documento informado como parâmetro
    """
    lista_questoes = []
    for i in range(len(documento)):
        string_questao = ''
        if documento[i].strip() == '\\begin{question}':
            string_questao += documento[i]
            while documento[i].strip() != '\\end{question}':
                i += 1
                string_questao += documento[i]
            tipo_quest = encontrar_tipo_da_questao(string_questao)
            lista_questoes.append(dict(corpo=string_questao, type=tipo_quest))
    return lista_questoes


def informacoes_para_por_no_json(veio_do_arquivo):
    """
    Esse procedimento vai retornar um json formatado de acordo com o arquivo tex recebido como parâmetro.
    :param nome_arquivo_pesquisa: Informações do arquivo tex.
    :return: json formatado.
    """
    initial_doc = veio_do_arquivo.index('\\begin{document}\n')  # O documento inicia a partir do \begin
    setup = [veio_do_arquivo[i] for i in range(initial_doc)]  # O setup são as definições que precedem o documento
    documento = [veio_do_arquivo[i] for i in
                 range(initial_doc, len(veio_do_arquivo))]  # O documento está após o setup
    semestre_documento = pegar_semestre(documento)
    questoes_documento = encontrar_questoes(documento)
    return dict(steup_inicial=setup, semestre=semestre_documento, questoes=questoes_documento)


def gerar_saida(info_json):
    """
    Escreve no arquivo json de saída
    :param info_json: informações no formato json
    :return: None
    """
    parametro_global.param += 1  # Acrescenta 1 para gerar outro json
    name_arq_json = 'json' + str(parametro_global.param)
    diretorio_saida = 'input_output/json_outputs/' + name_arq_json + '.json'
    try:
        arquivo_saida = open(diretorio_saida, 'a')
    except FileNotFoundError:
        erro_diretorio_inexistente(diretorio_saida)
    else:
        arquivo_saida.write(info_json)
        arquivo_saida.close()


def filtro_json(nome_arquivo_pesquisa: str):
    try:
        arq_pesquisa = open(nome_arquivo_pesquisa, encoding='utf-8')
    except FileNotFoundError:
        erro_diretorio_inexistente(nome_arquivo_pesquisa)
    else:
        veio_do_arquivo = arq_pesquisa.readlines()  # Lê tudo que tem dentro do .tex
        info_json = json.dumps(informacoes_para_por_no_json(veio_do_arquivo))
        gerar_saida(info_json)
