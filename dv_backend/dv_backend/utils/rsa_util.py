import base64
from pathlib import Path
from django.conf import settings
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from loguru import logger

PRIVATE_KEY_PATH = Path(settings.BASE_DIR) / 'private_key.pem'


def load_private_key():
    with open(PRIVATE_KEY_PATH, 'rb') as f:
        return serialization.load_pem_private_key(f.read(), password=None)


def rsa_decrypt(encrypted_text: str) -> str:
    try:
        private_key = load_private_key()
        encrypted_bytes = base64.b64decode(encrypted_text)
        decrypted = private_key.decrypt(
            encrypted_bytes,
            padding.PKCS1v15()
        )
        return decrypted.decode('utf-8')
    except Exception as e:
        logger.warning(f"RSA解密失败: {e}")
        return encrypted_text
