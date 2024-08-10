from starlette.config import Config
from starlette.datastructures import Secret
from cryptography.hazmat.primitives.serialization import load_pem_private_key

try: 
    config = Config(".env")

except FileNotFoundError:
    config = Config()


PAYMENT_DATABASE = config("PAYMENT_DATABASE", cast=Secret)
