from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from lib.log import logger


class BuscarElementos:
    def __init__(
        self,
        driver,
        locator: tuple,
        excecao: bool = True,
        lista_de_um: bool = False
    ) -> None:
        """
        Classe para busca de elementos no DOM de uma página Web.
        :args
            {driver} - WebDriver (Navegador baseado no Chrome).
            {locator} [tuple] - Parâmetros da busca (Método, 'argumento para busca').
            {excecao} [bool] - Se tratará ou não caso ocorra uma exceção (padrão: True).
            {lista_de_um} [bool] - Se retorna uma string com o texto do elemento encontrado na primeira posição da lista (padrão: False).        
        :methods
            buscar()

        """
        self.__driver = driver
        self.__locator: tuple = locator
        self.__excecao: bool = excecao
        self.__lista_de_um: bool = lista_de_um

    @property
    def driver(self):
        return self.__driver

    @property
    def locator(self):
        return self.__locator

    @property
    def excecao(self):
        return self.__excecao

    @property
    def lista_de_um(self):
        return self.__lista_de_um

    def buscar(self):
        """
        Busca no DOM por elementos, aguardando até que todos estejam visiveis.
        :args
            {driver} - WebDriver (Navegador baseado no Chrome).
            {locator} - Tupla com (By.CLASSE, elemento) para a pesquisa.
        :returns
            {busca}:
                    None - se a busca falhar,
                    Webelement - o resultado da busca,
                    Lista de webelements - com os resultados encontrados.
        """
        wait = WebDriverWait(self.driver, 20)

        # Variável com o conteúdo da chave elemento para utilização no except
        elemento = self.locator[1]

        try:
            busca = wait.until(
                EC.visibility_of_all_elements_located(self.locator)
            )
        except TimeoutException as erro:
            if not self.excecao:
                pass
            else:
                logger.critical(
                    f'Tempo expirou... o elemento [{elemento}] não existe ou não ficou visível na página. Erro: {erro}.')
                self.driver.quit()
        except NoSuchElementException as erro:
            if not self.excecao:
                pass
            else:
                logger.critical(
                    f'Elemento [{elemento}] não encontrado na página. Erro: {erro}.')
                self.driver.quit()
        except Exception as erro:
            if not self.excecao:
                pass
            else:
                logger.critical(
                    f'Falha ao encontrar o elemento [{elemento}] na página. Erro: {erro}')
                self.driver.quit()
        else:
            if len(busca) < 2:
                if not self.lista_de_um:
                    return busca[0]
            return busca


class ArquivoDownload:
    def __init__(self, driver) -> str:
        """
        Classe que captura o nome do último arquivo baixado pelo WebDriver.
        :args
            {driver} - WebDriver (Navegador Chrome).
        :returns
            [str] - Nome e extensão do arquivo baixado.
        :methods
            arquivo()
        """
        self.__driver = driver

    @property
    def driver(self):
        return self.__driver

    def arquivo(self) -> str:
        """
        Captura o nome do arquivo baixado, por meio de script na página download (chrome://downloads/).
        :args
            Nenhum.
        :returns
            Nome do arquivo baixado.
        """
        try:
            self.driver.get('chrome://downloads/')
            arquivo = self.driver.execute_script(
                'return document.querySelector("downloads-manager").shadowRoot.querySelector("#downloadsList downloads-item").shadowRoot.querySelector("#file-link").text'
            )
        except Exception as e:
            logger.critical(
                f'Erro ao capturar o arquivo de Download: {e}'
            )
            self.driver.quit()
        else:
            return arquivo
