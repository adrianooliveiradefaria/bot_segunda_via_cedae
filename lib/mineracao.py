from typing import Dict, List

from openpyxl import load_workbook

from controle.matricula_processada import retornar_processada
from lib.log import logger


def pegar_cadastro_prestadora(arquivo) -> List[Dict[str, str]]:
    """
        Extrai da planilha de cadastro de clientes, das linhas que estiverem completas, as informações necessárias para a solicitação da segunda via.
        A planilha de dados deve se chamar AGUA.xlsx.
            A primeira linha deve conter o título das colunas [Cliente, CNPJ/CPF, Documento].
            A partir da segunda linha, as colunas devem conter:
                Coluna A = Nome do cliente
                Coluna B = Número da matrícula
                Coluna C = Número do documento (CPF/CNPJ)
                Coluna D = Endereço e e-mail para envio da conta
        :args
            {arquivo} [str] - Nome da planilha de dados localizada na raiz da aplicação.
        :returns
            Uma lista de dicionários do cadastro.
            [
                {'cliente': 'NomeDoCliente'},
                {'matricula': 'NumeroDaMatricula'},
                {'documento': 'NumeroDocumento'}
            ]
    """
    try:
        arquivo_planilha = load_workbook(arquivo)
        planilha = arquivo_planilha.active
        # Deleta a linha de títulos da matriz
        planilha.delete_rows(1)
        cadastro_temp: List[Dict[str, list]] = list()
        # Na planilha, os dados de acesso correspondem as seguintes colunas:
        # cliente[0], matricula[1], documento[2], e-mail[3]

        # Ignora dados incompletos na [lista] como os dados da planilha
        for dado in planilha.values:
            if dado[0] and dado[1] and dado[2] and dado[3]:
                dic_dado = {
                    'cliente': dado[0],
                    'matricula': dado[1],
                    'documento': dado[2],
                    'email': dado[3]
                }
                cadastro_temp.append(dic_dado)
        matriculas_processadas = retornar_processada()
        cadastro_prestadora = list(filter(
            lambda x: x['matricula'] not in matriculas_processadas, cadastro_temp)
        )
        return cadastro_prestadora
    except Exception as e:
        logger.critical(
            f'Erro na mineração de dados da planilha: {arquivo}. O arquivo não existe no diretório da aplicação.'
        )
        return list()
