def erro_diretorio_inexistente(caminho):
    """
    Procedimento resposável por alertar que houve um erro, encerrando o programa.
    :param caminho: Caminho informado não existente.
    :return: None
    """
    print('\033[1;31mErro! O caminho \033[m', end=f'\033[0;33m{caminho} \033[m')
    print('\033[1;31mnão existe\033[m')
    exit(1)
