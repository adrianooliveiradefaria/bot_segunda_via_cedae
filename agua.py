import os
import sys
from argparse import ArgumentParser
from datetime import datetime
from platform import system
from random import uniform
from textwrap import dedent
from time import sleep
from typing import Dict, List

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from lib.ambiente_inicial import config_smtp
from controle.matricula_processada import inserir_processada
from lib.elemento_web import ArquivoDownload, BuscarElementos
from lib.envio_email import Email
from lib.log import logger
from lib.mineracao import pegar_cadastro_prestadora
from lib.secret import Criptografia
from lib.util import ArquivoConfig, SiteOn


class BotAguaSegundaVia(object):
    def __init__(self) -> None:
        """
        Classe para emissão de segunda via de contas da Companhia Estadual de Água e Esgoto (CEDAE/RJ).
        :methods
            baixar_segunda_via()
            verificar_conteudo_pagina()
            processar_vencimento()
        """
        self.__dir_download: str = os.path.expanduser(
            '~') + os.sep + 'Downloads' + os.sep

        # Definição do Browser
        config_chrome: webdriver = webdriver.ChromeOptions()

        preferencias_chrome: dict = {
            'download.default_directory': self.dir_download,
            # 'directory_upgrade': True,
            # 'safebrowsing, enable': True
        }

        config_chrome.add_experimental_option('prefs', preferencias_chrome)
        # Define o path do driver de acordo com sistema operacional
        if system() == 'Linux':
            path_driver: object = Service(
                os.getcwd()+os.sep+'chromedriver_linux')
        elif system() == 'Windows':
            path_driver: object = Service(
                os.getcwd()+os.sep+'chromedriver_win.exe')

        logger.info(f'Sistema operacional: {system()}')
        self.__driver: object = webdriver.Chrome(
            service=path_driver,
            options=config_chrome
        )

        self.driver.maximize_window()

    @property
    def dir_download(self):
        return self.__dir_download

    @property
    def driver(self):
        return self.__driver

    def baixar_segunda_via(self, url: str) -> bool:
        """
        Abre o navegador na página de emissão de segunda via da prestadora,
        baixa a segunda via da conta, renomeia o arquivo com o padrão:
        NomeDoCliente-NúmeroDaMatrícula-DataDeVencimento.pdf, envia por e-mail
        e registra o processamento no controle para não haver repetição de envio.
        :args
            {url} [str] - Endereço da URL para testar se o serviço está respondendo.
        :returns
            Booleano [bool] se obteve sucesso na emissão.
        """
        # Testa se o site está no ar
        if not SiteOn(url).verificar():
            logger.critical(
                'Erro ao carregar a URL. 1) ela pode ter mudado ou 2) o serviço pode estar momentâneamente indisponível.')
            self.driver.quit()
            return False
        logger.info('Carregando dados da planilha de cadastro...')
        # Retorna, da planilha, o cadastro dos clientes na prestadora
        cadastro_clientes: List[Dict[str, str]
                                ] = pegar_cadastro_prestadora(arquivo='AGUA.xlsx')
        if not cadastro_clientes:
            self.driver.quit()
            return False
        for self.cadastro in cadastro_clientes:
            logger.info(
                f'Processando matrícula de {self.cadastro["cliente"]}...')
            # O site não é a página principal por ser um iFrame. Trabalhar direto na página de emissão é mais produtivo.
            self.driver.get(url)
            """
            Além da documentação oficial, o site
            http://pythonclub.com.br/selenium-parte-4.html
            é uma boa consulta sobre função de espera.
            """
            # Elemento MATRICULA
            try:
                matricula = BuscarElementos(
                    driver=self.driver,
                    locator=(By.ID, 'MATRICULA')
                ).buscar()
            except:
                pass
            else:
                matricula.send_keys(self.cadastro['matricula'])
            # Elemento DOCUMENTO
            if self.cadastro['documento']:
                try:
                    documento = BuscarElementos(
                        driver=self.driver,
                        locator=(By.ID, 'FC01_CPF')
                    ).buscar()
                except:
                    pass
                else:
                    documento.send_keys(self.cadastro['documento'])
            # Elemento BOTÃO SOLICITAR
            try:
                botao_solicitar = BuscarElementos(
                    driver=self.driver,
                    locator=(By.ID, 'btncpfvalida')
                ).buscar()
            except:
                pass
            else:
                botao_solicitar.click()
                alerta = Alert(self.driver)
                try:
                    texto = alerta.text
                except:
                    pass
                else:
                    logger.error(
                        'A página emitiu um alerta de documento inválido!')
                    if texto:
                        alerta.accept()
                        BotAguaSegundaVia.__exibir_resumo(
                            self.cadastro['cliente'],
                            self.cadastro['matricula'],
                            self.cadastro['documento'],
                            status='FALHA! Alerta de Documento inválido.'
                        )
                        continue
                    else:
                        pass
            # Verificar se há vencimento ou se página está em branco
            sem_dados_a_processar = self.verificar_conteudo_pagina()
            if sem_dados_a_processar:
                # Retorna pro loop e processa o próximo
                continue
            # Processar vencimentos na página
            try:
                self.processar_vencimento()
            except:
                pass
        self.driver.quit()
        return True

    def verificar_conteudo_pagina(self):
        """
        Verifica se a página tem dados à processar ou apenas a mensagem Continuação...
        """
        dados_pagina = BuscarElementos(
            driver=self.driver,
            locator=(By.CLASS_NAME, 'colVenc'),
            excecao=False
        ).buscar()
        if len(dados_pagina) < 2:
            # Página sem vencimentos ou apenas com o título 'Continuação...'
            return True
        else:
            return False

    def processar_vencimento(self):
        """
        Processa todos os vencimentos cujos mês/ano sejam iguais aos da data atual.
        """
        # Busca todas as colunas de vencimento na página
        while True:
            try:
                vencimentos = BuscarElementos(
                    driver=self.driver,
                    locator=(By.CLASS_NAME, 'colVenc')
                ).buscar()
            except:
                pass
            else:
                hoje = datetime.today()
                data_vencimento = ''
                for i, vencimento in enumerate(vencimentos):
                    try:
                        vencimento_date = datetime.strptime(
                            vencimento.text, '%d/%m/%y').date()
                    except:
                        continue
                    else:
                        try:
                            if vencimento_date.month == hoje.month and vencimento_date.year == hoje.year:
                                linha_continuacao = BuscarElementos(
                                    driver=self.driver,
                                    locator=(By.ID, 'linha_continuacao'),
                                    excecao=False
                                ).buscar()
                                linha_vencimento = i
                                if linha_continuacao:
                                    linha_vencimento += 1
                                data_vencimento = vencimento.text
                                elemento_motivo = 'DRLMOTIVO' + \
                                    str(linha_vencimento)
                            else:
                                continue
                        except:
                            continue
                        else:
                            # Elemento MOTIVO
                            try:
                                wait = WebDriverWait(self.driver, 20)
                                motivo = Select(
                                    wait.until(
                                        EC.visibility_of_element_located(
                                            (By.NAME, elemento_motivo))
                                    )
                                )
                                motivo.select_by_index(1)
                            except:
                                pass
                            else:
                                # Elemento BAIXAR DOCUMENTO
                                elemento_baixar: str = ''
                                if self.cadastro['documento']:
                                    elemento_baixar: str = 'EPortalLinkImp' + \
                                        str(linha_vencimento)
                                else:
                                    elemento_baixar: str = 'LinkBar' + \
                                        str(linha_vencimento)
                                # Elemento BAIXAR
                                try:
                                    baixar = wait.until(
                                        EC.visibility_of_element_located(
                                            (By.ID, elemento_baixar)
                                        )
                                    )
                                except Exception as e:
                                    print(f'Erro: {e}')
                                else:
                                    baixar.click()
                                    logger.info('Gerando arquivo PDF...')
                                    arquivo_conta = self.__renomear_arquivo(
                                        cliente=self.cadastro['cliente'],
                                        matricula=self.cadastro['matricula'],
                                        vencimento=data_vencimento
                                    )
                                    # Envia e-mail da conta
                                    logger.info('Enviando e-mail...')
                                    conf_smtp = ArquivoConfig(
                                        'smtp.yaml').carregar_arquivo()
                                    enviar_email: Email = Email(
                                        host=conf_smtp['host'],
                                        port=conf_smtp['porta'],
                                        user=conf_smtp['usuario'],
                                        pwd=Criptografia().decriptar(
                                            conf_smtp['senha']
                                        ),
                                        de='robo@conectasolucoes.com.br',
                                        para=[self.cadastro['email']],
                                        assunto=f'Segunda via CEDAE <-> {self.cadastro["cliente"]}-{self.cadastro["matricula"].replace("-", "")}',
                                        corpo_html='config/corpo_email.html',
                                        anexo=arquivo_conta
                                    ).enviar()
                                    if not enviar_email:
                                        self.driver.quit()
                                        return False
                                    else:
                                        logger.info(
                                            'Registrando matrícula no controle de dados processados.')
                                        inserir_processada(
                                            matricula=self.cadastro['matricula'],
                                            cliente=self.cadastro['cliente'],
                                            documento=self.cadastro['documento'])
                                        # Exibe resumo da tarefa
                                        BotAguaSegundaVia.__exibir_resumo(
                                            cliente=self.cadastro['cliente'],
                                            matricula=self.cadastro['matricula'],
                                            documento=self.cadastro['documento'],
                                            vencimento=data_vencimento,
                                            email=self.cadastro['email'],
                                            status='Concluída com sucesso!')
                                        logger.info(
                                            'Processamento da matrícula finalizado.')
            # Pausa randômica anti-bloqueio
            sleep(uniform(1, 5))
            # Avança para próxima página, se houver
            try:
                proxima_pagina = BuscarElementos(
                    driver=self.driver,
                    locator=(By.ID, 'Proxima1'),
                    excecao=False
                ).buscar()
            except:
                break
            else:
                proxima_pagina.click()

    def __renomear_arquivo(
        self,
        cliente: str,
        matricula: str,
        vencimento: str
    ) -> str:
        """
        Renomeia o arquivo baixado para o padrão definido.
        :args
            {cliente} [str] - Nome do cliente na planilha de dados.
            {matricula} [str] - Número da matrícula na planilha de dados.
            {vencimento} [str] - Data de vencimento da conta extraído do site da prestadora.
        :returns
            [str] - Nome do arquivo com seu caminho absoluto.

            O nome final do arquivo será:
            NomeCliente-NúmeroMatrícula-DataVencimento.pdf
        """
        try:
            matricula_replace: str = matricula.replace('-', '')
            vencimento_replace: str = vencimento.replace('/', '-')
            nome_arquivo: str = cliente + '-' + \
                matricula_replace + '-' + vencimento_replace + '.pdf'
            conta: str = self.dir_download + \
                ArquivoDownload(self.driver).arquivo()
            conta_renomeada: str = self.dir_download + nome_arquivo
            os.replace(conta, conta_renomeada)
            logger.info(f'Arquivo {conta_renomeada} processado com sucesso!')
            return conta_renomeada
        except Exception as e:
            logger.error(f'Erro ao processar o arquivo PDF: {e}')
            return ''

    @staticmethod
    def __exibir_resumo(
        cliente: str,
        matricula: str,
        documento: str = '',
        vencimento: str = '',
        email: str = '',
        status: str = ''
    ) -> None:
        """
        Exibe no terminal o resumo do processamento da matrícula.
        :args
            {cliente} [str] - Nome do cliente na planilha de dados..
            {matricula} [str] - Número da matrícula na planilha de dados..
            {documento} [str] - Número do documento na planilha de dados..
            {vencimento} [str] - Vencimento extraído do site da prestadora.
            {email} [str] - E-mail cadastrado na planilha de dados.
            {status} [str] - Mensagem à exibir.
        :returns
            Nenhum.
        """
        print(dedent(
            f'''
            ============================================================
                            Emissão de segunda via de conta
            ============================================================

            Cliente: {cliente}
            Matrícula: {matricula}
            Documento: {documento}
            Vencimento: {vencimento}
            Data: {datetime.today().strftime('%d/%m/%Y %H:%M:%S')}
            E-mail: Enviado com sucesso para:
                    {email}
            Status: {status}            
            ------------------------------------------------------------
            ''')
        )


parser = ArgumentParser(
    usage='python agua.py [args]'
)
parser.add_argument(
    '--config_pk',
    action='store_true',
    help='Cria uma chave privada para criptografia do sistema.'
)
parser.add_argument(
    '--config_smtp',
    action='store_true',
    help='Chama o configurador do servidor SMTP para envio de e-mail.'
)

args = parser.parse_args()


if __name__ == '__main__':
    if args.config_pk:
        logger.info('Gerando chave criptográfica privada, aguarde...')
        if Criptografia().gerar_chave_cripto():
            logger.info(
                '''Chave gerada com sucesso!
                Agora é preciso configurar os dados do SMTP para o envio de e-mail.
                Execute python agua.py --config_smtp''')
            sys.exit(0)
    elif args.config_smtp:
        config_smtp()
        sys.exit(0)
    bot_segunda_via = BotAguaSegundaVia()
    if bot_segunda_via.baixar_segunda_via(
            'https://seguro.cedae.com.br/segunda_via_web/pages/SegundaVia/ENTRADA.aspx'):
        logger.info('*** Envio das contas concluído com sucesso ;)')
    else:
        logger.info(
            'FALHA na rotina de envio das contas... Entre em contato com o suporte técnico :(')
