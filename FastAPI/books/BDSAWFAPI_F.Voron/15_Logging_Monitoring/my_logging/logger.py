import add_packages
import logging
import sys
from loguru import logger

# Removes a previously defined sink
logger.remove() 

#* Defines new sinks. Specifies how log calls should be handled

# Only logs messages with a WARNING level
logger.add(sys.stdout, level="WARNING")

# Logs all messages, remove old logs after 1 day
logger.add("./logged_data/file.log", rotation="1 day")

# Extra is a dictionary where Loguru stores all values added in context
LOG_LEVEL = "DEBUG"
logger.add(
  sys.stdout,
  level=LOG_LEVEL,
  format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    " - {extra}"
)

class InterceptHandler(logging.Handler):
  """
  Forwards standard log calls to Loguru by retrieving log level and original 
  caller information from the call stack
  """
  def emit(self, record):
    # Get corresponding Loguru level if it exists.
    try:
      level = logger.level(record.levelname).name
    except ValueError:
      level = record.levelno

    # Find caller from where originated the logged message.
    frame, depth = sys._getframe(6), 6
    while frame and frame.f_code.co_filename == logging.__file__:
      frame = frame.f_back
      depth += 1

    logger.opt(depth=depth, exception=record.exc_info).log(
      level, record.getMessage()
    )

# Set custom interception handler
# All log calls made with root logger will be handled by Loguru
# If using other libraries with their own loggers like Uvicorn, determine the 
# logger's name in the source code.
logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True) 

for other_logger_name in ["uvicorn.error", "uvicorn.access"]:
  other_logger = logging.getLogger(other_logger_name)
  other_logger.propagate = False
  other_logger.handlers = [InterceptHandler()]


"""
`all` is a special variable in Python that specifies which variables are 
publicly available when importing the module. 
Exposing logger from Loguru allows for easy importing throughout the project.
"""
# __all__ = ["logger"]