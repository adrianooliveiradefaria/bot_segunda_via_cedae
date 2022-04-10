from lib.util import ArquivoConfig
from lib.secret import Criptografia
from lib.log import logger


def config_smtp():
    """
    Configura o servidor SMTP para envio de e-mails.
    :args
    :returns
    """
    while True:
        print(
            '''
            ------------------------------
            Configuração do servidor SMTP
            ------------------------------

            Informe os dados do seu servidor de envio de e-mail.
            Execute este processo com atenção para não ter problemas com o envio de e-mails.

            ''')
        smtp_dict = dict()
        smtp_dict['host'] = input('HOST (exemplo: smtp.gamail.com): ')
        smtp_dict['porta'] = input('PORTA (exemplo: 465): ')
        smtp_dict['usuario'] = input(
            'USUÁRIO (exemplo: seu_usuario@gmail.com): ')
        smtp_dict['senha'] = input('SENHA (será criptografada em seguida): ')
        senha_confirmada = input('CONFIRME A SENHA: ')

        if not smtp_dict['senha'] == senha_confirmada:
            input(
                '\nAtenção! As senhas precisam ser iguais. Pressione qualquer tecla para tentar novamente...')
            continue
        else:
            confirma = input('\nConfirma dados fornecidos (S/N)? ')

            if confirma.lower().strip() == 's':
                for chave, valor in smtp_dict.items():
                    if not valor:
                        input(
                            f'\n<<< {chave.upper()} >>> parâmetro não informado ou inválido!\
                            \nPressione qualquer tecla para tentar novamente ou CTRL + C para desistir...')
                try:
                    porta_int = int(smtp_dict['porta'])
                    smtp_dict['porta'] = porta_int
                except ValueError:
                    input(
                        f'\nO valor do parâmetro <<< PORTA >>> não é um número inteiro!\
                        \nPressione qualquer tecla para tentar novamente ou CTRL + C para desistir...')

                # Criptografa a senha informada
                smtp_dict['senha'] = Criptografia(
                ).encriptar(smtp_dict['senha'])

                #  Salva os parâmetros no arquivo de configuração
                if ArquivoConfig('smtp.yaml').gravar_arquivo(smtp_dict):
                    logger.info(
                        'Arquivo de configuração do servidor SMTP gravado com sucesso!')
                    break
                else:
                    logger.error(
                        'Falha ao gravar o arquivo de parâmetros do servidor SMTP.')
                    break
            else:
                logger.critical(
                    'Parâmetros do servidor SMTP não configurados.')
                break
