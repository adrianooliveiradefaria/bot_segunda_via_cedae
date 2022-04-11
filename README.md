# Bot 2a Via de Conta D'Água
    
## Descrição do Projeto
O robô viabiliza a automação do recebimento da segunda via da conta da Companhia Estadual de Água e Esgoto (CEDAE), que tem o péssimo costume de entregar faturas com até 3 meses de antecedência, o que resulta num alto custo (tempo e dinheiro) para gerenciamento (agendamento) ou esquecimento do pagamento (sumiço depois de meses da entrega).

A fonte de dados para ingresso no site da companhia e extração dos vencimentos está contida na planilha **AGUA.xlsx**. 

Após minerar a tabela de vencimentos, são extraídos somente os do mês corrente, e o e-mail cadastrado recebe a segunda via em formato PDF, para impressão e arquivamento, ou pagamento por aplicativos de bancos, que já reconhecem boletos neste formato - versões futuras preveem o envio direto para um aplicativo mensageiro, o que facilitará o pagamento direto do celular.

Como há um controle das matrículas já processadas no mês, o robô pode ser agendado para rodar duas ou mais vezes no mês para a verificação dos vencimentos sem gerar duplicidade. Confira a conclusão...

## Status do Projeto
   Em desenvolvimento.

## Funcionalidades
    
## Tecnologias utilizadas
   - Python
   - Sellenium
   - autopep8
   - isort

## Pŕe-requisitos
   - Python 3
   - Editor de arquivos xlsx para alterar a planilha fonte de dados
   - Arquivo **AGUA.xlsx** com os dados de acesso dos clientes
   - [WebDriver](https://chromedriver.chromium.org/downloads) compatível com sua versão do Google Chrome
   - WebDriver descompatado na raiz do diretório da aplicação e renomeado como chromedriver_linux ou chromedriver_win.exe (para Windows)

## Como rodar a aplicação
   1. Cerfique-se de estar no diretório onde a aplicação foi descompactada
   2. Instale as dependências
      `pip install -r requirements.txt`
   3. Gere sua pŕopria chave criptográfica privada com o comando
      `python agua.py --config_pk`
   4. Configure o SMTP para envio dos PDFs por e-mail
      `python agua.py --config_smtp`
   5. Edite a planilha **AGUA.xlsx** e cadastre os dados das contas que deseja
      Siga o modelo informado de exemplo.
   6. Execute no diretório da aplicação
      `python3 agua.py`
    
## Desenvolvedor
   Adriano Faria

## Licença
   GNU General Public License v3.0 (GNU GPLv3)

## Conclusão
Este robô tem um relevante papel no ganho de mão de obra em administradoras de imóveis, onde dezenas ou centenas de contas precisam ser gerenciadas e/ou solicitadas a companhia pessoalmente, todo mês, pelos mais diversos motivos. Utilize o robô e ganhe mais tempo com quem você ama e com o que te leva ao aperfeiçoamento ;)
