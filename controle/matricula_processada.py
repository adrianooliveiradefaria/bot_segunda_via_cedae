from datetime import datetime
from pathlib import Path
from typing import List

import yaml

from lib.log import logger


ARQUIVO_YAML = Path('controle/matricula_processada.yaml')


def __verificar_data_arquivo_controle() -> None:
    """
    Calcula se o mês e ano corrente são maiores que o da última modificação do arquivo.
    Se verdadeiro, cria um novo arquivo para o controle do mês corrente. 
    Se o arquivo não existir, cria.
    :args
        Nenhum.
    :return
        Nenhum.
    """
    if not ARQUIVO_YAML.is_file():
        __criar_processada()
    else:
        hoje = datetime.today()
        dt_criacao_arquivo_yaml = datetime.fromtimestamp(
            ARQUIVO_YAML.stat().st_mtime)  # data da última modificação no arquivo.
        calculo = (hoje.month + hoje.year) > (dt_criacao_arquivo_yaml.month +
                                              dt_criacao_arquivo_yaml.year)
        if calculo:
            __criar_processada()
        return


def __criar_processada() -> None:
    """
    Cria, no diretório controle, o arquivo matricula_processadas.yaml, que armazena as matrículas já processadas no mês.
    """
    # Chave raiz do arquivo
    ctrl = {'processada':  list()}
    # Regrava o arquivo existente ou cria um novo
    with open(ARQUIVO_YAML, 'w+') as arq_ctrl:
        try:
            yaml.dump(
                ctrl,
                arq_ctrl,
                default_flow_style=False,
                explicit_start=True,
                explicit_end=True,
                version=(1, 2),
                sort_keys=False
            )
        except yaml.YAMLError as erro:
            logger.error(
                f'Erro na criação do arquivo de controle de matrículas processadas. {erro}')
    return


def inserir_processada(matricula: str, cliente: str, documento: str) -> None:
    """
    Lê o arquivo matricula_processada.yaml, adiciona à lista de valores o novo dicionário com o s daados processados.
    :args
        {matricula} - Número da matrícula do cliente.
        {cliente} - Nome do cliente.
        {documento} - Número do documento do cliente.
    :returns
        Nenhum.
    """
    # Lê o conteúdo original do arquivo
    with open(ARQUIVO_YAML) as arq_controle:
        try:
            conteudo = yaml.safe_load(arq_controle)
        except yaml.YAMLError as erro:
            logger.error(f'Erro ao abrir o arquivo {arq_controle}: {erro}')
        else:
            # Novo dicionário à adicionar
            novo = {
                'matricula': matricula,
                'cliente': cliente,
                'documento': documento,
                'execucao': datetime.today(),
            }
            # Adiciona o novo dicionário na lista de valores do controle
            conteudo['processada'].append(novo)

    # Abre o arquivo e regrava com o conteúdo adicionado
    with open(ARQUIVO_YAML, 'w+') as arq_ctrl:
        try:
            yaml.dump(
                conteudo,
                arq_ctrl,
                default_flow_style=False,
                explicit_start=True,
                explicit_end=True,
                version=(1, 2),
                sort_keys=False
            )
        except yaml.YAMLError as erro:
            logger.error(f'Erro ao gravar o arquivo atualizado! {erro}')
    return


def retornar_processada() -> List[str]:
    """
    Retorna o controle das matrículas que já foram processadas para não haver repetição.
    :args
        Nenhum.
    :returns
        Lista das matrículas já processadas no mês.
    """
    __verificar_data_arquivo_controle()
    with open(ARQUIVO_YAML) as arq_controle:
        try:
            controle = yaml.safe_load(arq_controle)
        except yaml.YAMLError as erro:
            logger.error(f'Erro ao abrir o arquivo {arq_controle}: {erro}')
        else:
            for valores in controle.values():
                controle_executados: list = [
                    valor['matricula'] for valor in valores
                ]
            return controle_executados
