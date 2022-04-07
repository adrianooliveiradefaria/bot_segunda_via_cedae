import logging

# Criando Logger e setando Level
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Criando Handlers e setando Level
# Console Handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# File Handler
fh = logging.FileHandler('log/log.log')
fh.setLevel(logging.INFO)

# Criando Formatter e setando os handlers
formatter_ch = logging.Formatter(
    fmt='''%(asctime)s => %(levelname)s: %(message)s''',
    datefmt='%d-%m-%Y %H:%M:%S'
)
formatter_fh = logging.Formatter(
    fmt='''%(asctime)s => %(levelname)s: módulo:%(module)s função:%(funcName)s linha:%(lineno)d
    %(message)s''',
    datefmt='%d-%m-%Y %H:%M:%S'
)
ch.setFormatter(formatter_ch)
fh.setFormatter(formatter_fh)

# Adicionando Handler ao Logger
logger.addHandler(ch)
logger.addHandler(fh)
