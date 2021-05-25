from cryptography.fernet import Fernet

"""
API DE PÓS-VENDA/RATING DO LIVRO
ARQUIVO DE CONFIGURAÇÃO DA CRIPTOGRAFIA
"""


def encrypt(content: str, key: str) -> str:
    key = bytes(key.encode())
    f = Fernet(key)
    token = f.encrypt(bytes(content.encode()))
    return str(token.decode())


def is_encrypted(content: str, key: str) -> bool:
    try:
        decrypt(content, key)
    except:
        return False
    return True


def decrypt(content: str, key: str) -> str:
    f = Fernet(bytes(key.encode()))
    return str(f.decrypt(bytes(content.encode())).decode())