import logging
import os
from random import randrange

class Log:
    """Class for generating program logs"""
        
    LOG_DIR = os.path.join("Logs")

    @classmethod
    def check_Log_Dir(cls):
        """Checks that the logs directory already exists, if not it creates it"""
        if not os.path.exists(cls.LOG_DIR):
            os.mkdir(cls.LOG_DIR)

    @classmethod
    def __generateLoggerCode(cls) -> str:
        securityCode:str = ""
        for i in range(8):
            #Se genera un numero aleatorio
            randNum = randrange(1,10)
            securityCode += str(randNum)
        return securityCode

    @classmethod
    def debug(cls, logName, message):
        "Logs a Debug message on the specified log"
        cls.check_Log_Dir()
        logger = logging.getLogger(cls.__generateLoggerCode())
        logger.setLevel(logging.DEBUG)

        #File where the logs will be saved
        fileHandler = logging.FileHandler(os.path.join(cls.LOG_DIR, f"{logName}.log"))
        #Format for the log messages on the file
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        fileHandler.setFormatter(formatter)
        
        logger.addHandler(fileHandler)
        logger.debug(message)

    @classmethod
    def info(cls, logName, message):
        "Logs a Info message on the specified log"
        cls.check_Log_Dir()
        logger = logging.getLogger(cls.__generateLoggerCode())
        logger.setLevel(logging.INFO)

        fileHandler = logging.FileHandler(os.path.join(cls.LOG_DIR, f"{logName}.log"))
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        fileHandler.setFormatter(formatter)

        logger.addHandler(fileHandler)
        logger.info(message)

    @classmethod
    def warning(cls, logName, message):
        "Logs a Warning message on the specified log"
        cls.check_Log_Dir()
        logger = logging.getLogger(cls.__generateLoggerCode())

        fileHandler = logging.FileHandler(os.path.join(cls.LOG_DIR, f"{logName}.log"))
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        fileHandler.setFormatter(formatter)

        logger.addHandler(fileHandler)
        logger.warning(message)

    @classmethod
    def error(cls, logName, message):
        "Logs a Error message on the specified log"
        cls.check_Log_Dir()
        logger = logging.getLogger(cls.__generateLoggerCode())

        fileHandler = logging.FileHandler(os.path.join(cls.LOG_DIR, f"{logName}.log"))
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        fileHandler.setFormatter(formatter)
        
        logger.addHandler(fileHandler)
        logger.error(message)

    @classmethod
    def critical(cls, logName, message):
        "Logs a Critical message on the specified log"
        cls.check_Log_Dir()
        logger = logging.getLogger(cls.__generateLoggerCode())

        fileHandler = logging.FileHandler(os.path.join(cls.LOG_DIR, f"{logName}.log"))
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        fileHandler.setFormatter(formatter)
        
        logger.addHandler(fileHandler)
        logger.critical(message)

    @classmethod
    def exception(cls, logName, message):
        "Logs an Exception stack trace and message on the specified log"
        cls.check_Log_Dir()
        logger = logging.getLogger(cls.__generateLoggerCode())
        
        fileHandler = logging.FileHandler(os.path.join(cls.LOG_DIR, f"{logName}.log"))
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        fileHandler.setFormatter(formatter)
        
        logger.addHandler(fileHandler)
        logger.exception(message)

    @classmethod
    def get_Log_Files(cls) -> list:
        "Returns all the log files to send them or check them"
        log_Files = list()
        for element in os.listdir(cls.LOG_DIR):
            if os.path.isfile(os.path.join(cls.LOG_DIR, element)):
                log_Files.append(os.path.join(cls.LOG_DIR, element))
        return log_Files