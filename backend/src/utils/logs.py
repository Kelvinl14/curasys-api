import logging
import colorlog

def get_logger(name: str = "app"):
    """Cria e retorna um logger configurado com cores"""
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        }
    ))

    logger = logging.getLogger(name)

    # evita adicionar múltiplos handlers se o logger já existir
    if not logger.handlers:
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

    return logger


# Função simples para reuso
def log(level: str, message: str):
    logger = get_logger()
    level = level.lower()

    if level == "debug":
        logger.debug(message)
    elif level == "info":
        logger.info(message)
    elif level == "warning":
        logger.warning(message)
    elif level == "error":
        logger.error(message)
    elif level == "critical":
        logger.critical(message)
    else:
        logger.info(message)
