# Bot 2a Via de Conta D'Água
    
## Descrição do Projeto
    A automação acessa a página da Companhia Estadual de Água e Esgoto (CEDAE), e utiliza-se dos dados contidos na planilha AGUA.xlsx para ingressar no site e extrair a segunda via de todos os vencimentos do mês corrente.

## Status do Projeto
  Em desenvolvimento

## Funcionalidades
    
## Tecnologias utilizadas
   - Python
   - Sellenium
   - autopep8
   - isort

## Pŕe-requisitos
   - Python 3
   - Editor de arquivos xlsx para alterar a planilha fonte de dados
   - Arquivo AGUA.xlsx com os dados de acesso dos clientes
   - [WebDriver](https://chromedriver.chromium.org/downloads) compatível com sua versão do Google Chrome
   - WebDriver descompatado na raiz do diretório da aplicação e renomeado como chromedriver_linux

## Como rodar a aplicação
 1. Cerfique-se de estar no diretório onde a aplicação foi descompactada
 2. Instale as dependências
   pip install -r requirements.txt
 3. Gere sua pŕopria chave criptográfica privada com o comando
   python agua.py --conf-pk
 4. Configure os parâmetro de envio de e-mail
   python agua.py --conf-smtp
 4. Criptografe seus dados de usuário e senha para envio de e-mail
 5. Configure o SMTP para envio dos PDFs por e-mail
 6. Execute no diretório da aplicação
   python3 agua.py
    
## Desenvolvedor
   Adriano Faria

## Licença
   - GNU

## Conclusão
