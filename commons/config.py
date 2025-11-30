from argparse import ArgumentParser
from configparser import ConfigParser
import os
from dotenv import load_dotenv

load_dotenv()

SECRETS_CONFIG_FILE_NAME = ".conf"
GLOBAL_CONFIG_NAME = "GLOBAL"
STAGE_NAME = os.environ["STAGE"]


class CustomConfigParser(ConfigParser):

    def optionxform(self, optionstr: str) -> str:
        # configparser by default converts keys to lowercase, I want to make sure keys are read as is.
        return optionstr


def load_app_config():
    config = CustomConfigParser()

    config.read(SECRETS_CONFIG_FILE_NAME)

    if not config.sections():
        raise ValueError(
            f'No valid configuration found. Please add {SECRETS_CONFIG_FILE_NAME} file to the root of project')

    PROFILES = [GLOBAL_CONFIG_NAME, STAGE_NAME]

    for profile in PROFILES:
        if profile not in config:
            raise KeyError(
                f'Stage "{profile}" does not exist in configuration.')

        for key, value in config[profile].items():
            os.environ[key] = value


def parse_arguments():
    parser = ArgumentParser(description='Not Bot')
    parser.add_argument(
        '--stage', help=f'STAGE for running the application. Expects in env by default', default=None)

    args = parser.parse_args()
    if args.stage and isinstance(args.stage, str) and len(args.stage) > 0:
        os.environ['STAGE'] = args.stage
    return parser
