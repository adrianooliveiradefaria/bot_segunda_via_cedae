from pathlib import Path
from typing import Dict

import requests
import yaml

from lib.log import logger


class SiteOn:
    def __init__(self, url) -> bool:
        """
        Classe que verifica a resposta de acesso a um site.
        :args
            {url} [str] - URL de acesso.
        :returns
            True/False.
        :methods
            verificar()
        """
        self.__url = url

    @property
    def url(self):
        return self.__url

    def verificar(self) -> bool:
        """
        Verifica se a página está com seus recursos disponíveis.
        :args
            {url} - String com a URL a carregar.
        :returns
            True/False.
        """
        # https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Status
        try:
            site_online = requests.get(self.url)
            logger.info(f'{self.url} <=> {site_online}')
        except Exception as e:
            logger.critical(f'''URL indisponível!
            Retorno: {site_online}
            Erro: {e}''')
        finally:
            if site_online.status_code > 199 and site_online.status_code < 299:
                return True
            else:
                return False


class ArquivoConfig(object):
    def __init__(self, arquivo) -> None:
        """
        Classe para manipulação de um arquivo de configuração no padrão YAML.
        :args
            {arquivo} - Nome do arquivo à manipular. O diretório padrão é config.
        :returns
            Nenhum.
        :methods
            Nenhum.
        """
        self.__arquivo = arquivo

    @property
    def arquivo(self):
        return self.__verificar_arquivo()

    def __verificar_arquivo(self) -> str:
        path_config = Path.cwd().joinpath('config')

        try:
            if Path(self.path_config).exists() \
                    and Path(path_config.joinpath(self.__arquivo)).exists():
                return path_config.joinpath(self.__arquivo)
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            caminho = path_config.joinpath(self.__arquivo)
            logger.critical(
                f'Falha ao acessar o arquivo de configuração: {caminho}. Erro: FileNotFoundError.')
            return ''

    def gravar_arquivo(self, conteudo: dict) -> bool:
        """
        Grava o conteúdo informado no arquivo (YAML) da instância de ArquivoConfig().
        :args
            {conteudo} [dict] - Dicionário com o conteúdo do arquivo.
        :returns
            True/False.
        """
        with open(self.arquivo, 'w') as arq_conf:
            try:
                yaml.dump(
                    conteudo,
                    arq_conf,
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

    def carregar_arquivo(self) -> Dict[str, str]:
        """
        Carrega o arquivo (YAML) da instância de ArquivoConfig().
        :returns
            Dicionário com o conteúdo do arquivo ou vazio em caso de erro.
        """
        try:
            with open(self.arquivo) as f:
                conteudo = yaml.safe_load(f)
                return conteudo
        except yaml.YAMLError as e:
            logger.critical(
                f'Falha ao ler o arquivo {self.arquivo}. Erro: {e}')
            return dict()


class Arquivo(object):
    def __init__(
        self,
        arquivo,
        caminho=Path.cwd()
    ) -> None:
        """
        Classe para manipular arquivos.
        :args
            {caminho} - Path absoluto. Por padrão assume o path atual.
            {arquivo} - nome do arquivo para manipulação.
        :returns
            Nenhum.
        :methods
            verificar()
        """
        self.__caminho = caminho
        self.__arquivo = arquivo

    @property
    def arquivo(self):
        caminho_arquivo = self.caminho.joinpath(self.__arquivo)
        return caminho_arquivo

    @property
    def caminho(self):
        return self.__caminho

    def verificar(self):
        """
        Verifica se o arquivo existe.
        :args
            Nenhum.
        :returns
            True/False.
        """
        try:
            if Path(self.arquivo).exists():
                return
            else:
                raise FileNotFoundError
        except FileNotFoundError as e:
            logger.critical(
                f'Falha ao acessar o arquivo: {self.arquivo}. Erro: FileNotFoundError.')
            return False
