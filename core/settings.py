from os import getenv

from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

email_sender = getenv("EMAIL_SENDER")
email_password = getenv("EMAIL_PASSWORD")

DATABASE_PASSWORD = getenv("DATABASE_PASSWORD")
DATABASE_NAME = getenv("DATABASE_NAME")

PORT = getenv("PORT")
HOST = getenv('localhost')
