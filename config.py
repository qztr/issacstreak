import os

from dotenv import load_dotenv

load_dotenv()


class Config(object):

    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SECRET_KEY = os.getenv("secret_key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIRECT_URI = "https://isaac-streak.fun/loged_in"  # куда редиректить после успешной авторизации
    # REDIRECT_URI = "http://localhost:8001/loged_in" # куда редиректить после успешной авторизации

    CATEGORIES = ["all_chapter", "mother", "blue_baby", "lost", "t_lost"]
    SCOPES = "bits:read"  # так как мне не нужны никакие разрешения, беру безобидное. если генерить новый SECRET_OAUTH с новыми SCOPES, то не забыть поменять оба значения тут!

    CLIENT_ID = os.getenv("CLIENT_ID")  # https://dev.twitch.tv/console/apps/<client_id>

    SECRET_OAUTH = os.environ.get(
        "SECRET_OAUTH"
    )  # generated here: https://twitchtokengenerator.com/

    KEY_FOR_API = os.environ.get(
        "KEY_FOR_API"
    )  # по этому ключу верфицировать запрос. только бот знает ключ

    CLIENT_SECRET = os.environ.get(
        "CLIENT_SECRET"
    )  # этот код генерится 1 раз на странице https://dev.twitch.tv/console/apps/<client_id>

    TWITCH_LOGIN = f"https://id.twitch.tv/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope={SCOPES}&force_verify=true"  # ссылка для авторизации

    PATH_TO_LOGFILE = os.environ.get("PATH_TO_LOGFILE")

    GENERATED_CLIENT_ID = os.environ.get("GENERATED_CLIENT_ID")

    AUTH_LOG = os.getenv(
        "AUTH_LOG"
    )  # full path to file: .txt or .csv include file + .txt/.csv

    PATH_TO_CSV = os.environ.get("PATH_TO_CSV")
