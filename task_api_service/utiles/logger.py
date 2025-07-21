from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, format="{time} {level} {message}", level="INFO")
# logger.add(
#     "logs/task_queue.log",  # log file path
#     rotation="500 KB",      # rotate log files after they hit 500KB
#     retention="10 days",    # keep old logs for 10 days
#     level="DEBUG",          # minimum log level to record
#     enqueue=True,           # async / multiprocessing
#     backtrace=True,         # show complete error traces
#     diagnose=True,          # give better error diagnostics
#     format="{time} {level} {message}",
# )
