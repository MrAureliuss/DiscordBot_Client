import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), 'config.env')
load_dotenv(dotenv_path)

settings = {
    'token': os.environ.get("TOKEN"),
    'bot': os.environ.get("BOT_NAME"),
    'id': os.environ.get("ID"),
    'command_prefix': '*'
}