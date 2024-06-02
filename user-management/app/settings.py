from starlette.config import Config
from starlette.datastructures import Secret
from cryptography.hazmat.primitives.serialization import load_pem_private_key

try: 
    config = Config(".env")

except FileNotFoundError:
    config = Config()


DATABASE_URL_USERS = config("DATABASE_URL_USERS", cast=Secret)
# TEST_DATABASE_URL = config("TEST_DATABASE_URL", cast=Secret)
SECRET_KEY = str(config("SECRET_KEY", cast=Secret))
ALGORITHM = str(config("ALGORITHM", cast=Secret))

USERNAME = str(config("USERNAME", cast=Secret))
PASSWORD = str(config("PASSWORD", cast=Secret))
