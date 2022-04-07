import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
from pathlib import Path

from lib.log import logger


class Email(object):
    def __init__(self, **kwargs) -> bool:
        """
        Classe para envio de e-mail com corpo em arquivo HTML e anexo (opcional).
        :args
            {host} - Endereço do servidor SMTP.
            {port} - Porta de conexão SSL.
            {user} - Usuário de autenticação.
            {pwd} - Senha de autenticação.
            {de} - E-mail de origem.
            {para} - Lista dos destinatários.
            {assunto} - Assunto da mensagem.
            {corpo_html} - Arquivo HTML com o corpo da mensagem.
            {anexo} - Caminho completo e nome do arquivo para anexar.
        :returns
            True/False - Indicando o sucesso da tarefa.
        """
        self.__host = kwargs.get('host')
        self.__port = kwargs.get('port', 465)  # SSL
        self.__user = kwargs.get('user')
        self.__pwd = kwargs.get('pwd')
        self.__de = kwargs.get('de')
        self.__para = kwargs.get('para')
        self.__assunto = kwargs.get('assunto')
        self.__corpo_html = kwargs.get('corpo_html')
        self.__anexo = kwargs.get('anexo', None)

    @property
    def host(self):
        return self.__host

    @property
    def port(self):
        return self.__port

    @property
    def user(self):
        return self.__user

    @property
    def pwd(self):
        return self.__pwd

    @property
    def de(self):
        return self.__de

    @property
    def para(self):
        return self.__para

    @property
    def assunto(self):
        return self.__assunto

    @property
    def corpo_html(self):
        return Path.cwd().joinpath(self.__corpo_html)

    @property
    def anexo(self):
        return self.__anexo

    def enviar(self) -> bool:
        """ Envia e-mail. """
        # Instância do objeto e-mail
        mensagem = MIMEMultipart()

        # Configuração de envio
        mensagem['From'] = self.de
        mensagem['To'] = ', '.join(self.para)
        mensagem['Subject'] = self.assunto

        # Texto da mensagem
        try:
            arquivo = open(self.corpo_html, 'r')
            corpo_email = arquivo.read()
        except Exception as e:
            logger.critical(f'Erro ao abrir {self.corpo_html} => {e}')
            return False
        else:
            mensagem.attach(
                MIMEText(_text=corpo_email, _subtype='html', _charset='utf-8')
            )

        # Anexo
        try:
            with open(self.anexo, 'rb') as carregar_arquivo:
                anexar = MIMEBase('application', 'octet-stream')
                anexar.set_payload((carregar_arquivo).read())
                encoders.encode_base64(anexar)
                anexar.add_header('Content-Disposition',
                                  "attachment; filename= %s" % basename(self.anexo).replace(' ', '_'))
                mensagem.attach(anexar)
        except Exception as e:
            logger.critical(
                f'Erro ao processar o arquivo de anexo: {self.anexo} => {e}')
            arquivo.close()
            return False

        # Servidor SMTP SSL
        try:
            servidor_smtp = smtplib.SMTP_SSL(self.host, self.port)
            servidor_smtp.login(self.user, self.pwd)
        except Exception as e:
            logger.error(
                f'Falha de conexão com o servidor SSL: {self.host} => {e}')
            return False
        else:
            servidor_smtp.sendmail(self.de, self.para, mensagem.as_string())
            return True
        finally:
            arquivo.close()
            servidor_smtp.quit()
