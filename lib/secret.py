from pathlib import Path

from cryptography.fernet import Fernet

from lib.log import logger

path_secret = Path.cwd().joinpath('config')
arq_secret = 'secret.key'


class Criptografia:
    # Este método precisa estar em um local remoto para garantir a autenticidade da cópia
    def gerar_chave_cripto(self) -> bool:
        """
        Gera uma chave criptográfica para string ou byte e salva no arquivo (config/secrets.key).
        :args
            Nenhum
        :return
            O sucesso da operação True/False.
        """
        if not Path.exists(path_secret):
            logger.info(f'Criando diretório não encontrado: {path_secret}!')
            try:
                Path.mkdir(path_secret)
            except Exception as e:
                logger.critical(
                    f'Falha ao criar o diretório {path_secret}. Erro: {e}')
                return False
        try:
            chave = Fernet.generate_key()
            arquivo = open(path_secret.joinpath(arq_secret), 'wb')
            arquivo.write(chave)
            arquivo.close()
            return True
        except Exception as e:
            logger.critical(
                f'Falha ao salvar a chave criptográfica em {path_secret}. Erro: {e}')
            return False

    def ler_chave_cripto(self) -> str:
        """
        Busca no arquivo (config/secret.key), a chave criptográfica.
        :args
            Nenhum
        :return
            A chave no formato byte, se encontrada, ou um erro.
        """
        try:
            with open(path_secret.joinpath(arq_secret), 'rb') as arquivo:
                chave = arquivo.read()
                return chave
        except Exception as e:
            logger.critical(
                f'Chave criptográfica privada não encontrada! Erro: {e}')
            return ''

    def encriptar(self, senha: str) -> str:
        """
        Criptografa a string fornecida utilizando a chave privada.
        :args
            {senha} - Senha a ser criptografada.
        :return
            Senha no formato string.
        """
        try:
            senha_byte = str.encode(senha, 'utf-8')
            SECRET_KEY = self.ler_chave_cripto()
            hash_senha = Fernet(SECRET_KEY).encrypt(senha_byte)
            return hash_senha.decode('utf-8')
        except Exception as e:
            logger.critical(f'Falha ao encriptar a string! Erro: {e}')
            return ''

    def decriptar(self, hash_senha: str) -> str:
        """
        Descriptografa o hash da string.
        :args
            {hash_senha} - String para conversão.
        :return
            Senha descriptografada em formato string.
        """
        try:
            hash_byte = str.encode(hash_senha, 'utf-8')
            SECRET_KEY = self.ler_chave_cripto()
            senha_byte = Fernet(SECRET_KEY).decrypt(hash_byte)
            return senha_byte.decode('utf-8')
        except Exception as e:
            logger.critical(f'Falha ao descriptografar a string! Erro: {e}')
            return ''
