import logging
from config_data.config import Config, load_config

# Load the config
config = load_config()
log_config = config.LogConfig

# Set up the logger
logger = logging.getLogger(__name__)
logger.propagate = False
logger.setLevel(logging.DEBUG)

# Set the log message formatter
formatter = logging.Formatter(
    '[{asctime}] #{levelname:8} {filename}:'
    '{lineno} - function:{funcName} - {message}',
    style='{'
)


# Add console handler if console logging is enabled
if log_config.console_on == 1:
    console_handler = logging.StreamHandler()
    console_level = log_config.level_info_console
    console_handler.setLevel(console_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


# Add file handler if file logging is enabled
if log_config.file_on == 1:
    file_path = log_config.filepath
    file_level = log_config.level_info_file
    file_handler = logging.FileHandler(file_path, encoding='utf-8')
    file_handler.setLevel(file_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def get_log_state(config: Config) -> None:
    "Prints current log settings: console_on, filepath, and so on"
    log_config = config.LogConfig
    print("*" * 50)
    print("CURRENT LOG SETTINGS".center(10))
    print(f"LOG_CONSOLE_ON = {log_config.console_on}")
    print(f"LOG_FILE_ON = {log_config.file_on}")
    print(f"LOG_FILEPATH = {log_config.filepath}")
    print(f"LOG_LEVEL_INFO_CONSOLE = {log_config.level_info_console}")
    print(f"LOG_LEVEL_INFO_FILE = {log_config.level_info_file}")
    print("*" * 50)
