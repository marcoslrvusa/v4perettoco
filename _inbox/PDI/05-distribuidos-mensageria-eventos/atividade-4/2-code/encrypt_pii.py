from cryptography.fernet import Fernet
key = Fernet.generate_key()
def encrypt(value: str) -> str:
    return Fernet(key).encrypt(value.encode()).decode()
def decrypt(token: str) -> str:
    return Fernet(key).decrypt(token.encode()).decode()
