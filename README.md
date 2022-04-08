# Bot 2a Via de Conta D'Água
    
## Descrição do Projeto
    A automação acessa a página da Companhia Estadual de Água e Esgoto (CEDAE), e utiliza-se dos dados contidos na planilha AGUA.xlsx para ingressar no site e extrair a segunda via de todos os vencimentos do mês corrente.

## Status do Projeto
    Em desenvolvimento

## Funcionalidades
    
## Tecnologias utilizadas
    - Python
    - Sellenium

## Pŕe-requisitos
    - Python 3
    - Editor de arquivos xlsx para alterar a planilha fonte de dados
    - Arquivo AGUA.xlsx com os dados de acesso dos clientes
    - [WebDriver](https://chromedriver.chromium.org/downloads) compatível com sua versão do Google Chrome
    - WebDriver descompatado na raiz do diretório da aplicação e renomeado como chromedriver_linux

## Como rodar a aplicação
    1. Instalar as dependências
        pip install -r requirements.txt
    2. No diretório da aplicação executar o arquivo agua.py
        python3 agua.py 
    
## Desenvolvedor
    Adriano Faria

## Licença
    - GNU

## Conclusão
