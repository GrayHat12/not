from commons.config import parse_arguments, load_app_config
from commons.logging import setup_application_logger, setup_discord_logger
import os

if __name__ == "__main__":
    parse_arguments()
    load_app_config()
    setup_application_logger()

    from bot import client
    setup_discord_logger()
    client.run(os.environ["BOT_TOKEN"], log_handler=None)
