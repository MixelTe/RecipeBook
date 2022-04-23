import logging
from datetime import datetime, timedelta


def customTime(*args):
    utc_dt = datetime.utcnow()
    utc_dt += timedelta(hours=3)
    return utc_dt.timetuple()


class InfoFilter(logging.Filter):
    def filter(self, rec):
        return rec.levelno == logging.INFO and rec.name == "root"


class ErrorFilter(logging.Filter):
    def filter(self, rec):
        return rec.name != "other"


class OtherFilter(logging.Filter):
    def filter(self, rec):
        return rec.name == "other"


def setLogging():
    logging.basicConfig(
        level=logging.DEBUG,
        filename='RecipeBook.log',
        format='%(asctime)s %(levelname)-8s %(name)s     %(message)s',
        encoding="utf-8"
    )
    logging.Formatter.converter = customTime

    log_formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(name)s     %(message)s')
    log_formatter2 = logging.Formatter('%(asctime)s %(levelname)-8s     %(message)s')

    file_handler_error = logging.FileHandler("RecipeBook-errors.log", mode='w')
    file_handler_error.setFormatter(log_formatter)
    file_handler_error.setLevel(logging.WARNING)
    file_handler_error.encoding = "utf-8"
    logging.getLogger().addHandler(file_handler_error)

    file_handler_info = logging.FileHandler("RecipeBook-info.log", mode='w')
    file_handler_info.setFormatter(log_formatter2)
    file_handler_info.addFilter(InfoFilter())
    file_handler_info.encoding = "utf-8"
    logging.getLogger().addHandler(file_handler_info)

    otherLogger = logging.getLogger("other")
    file_handler_other = logging.FileHandler("RecipeBook-other.log", mode='w')
    file_handler_other.setFormatter(log_formatter2)
    file_handler_other.addFilter(OtherFilter())
    file_handler_other.encoding = "utf-8"
    otherLogger.addHandler(file_handler_other)
