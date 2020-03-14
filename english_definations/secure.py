import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet


def read_password():
    dirname, _ = os.path.split(os.path.abspath(__file__))
    password_file = os.path.join(os.path.dirname(dirname), ".password.txt")
    if os.path.exists(password_file):
        with open(password_file, "r") as file:
            password = file.read()

        if len(password) <= 0:
            raise ValueError(".password.txt is empty")

        return password
    raise FileNotFoundError(".password.txt file not found")


def get_key(password):
    password = password.encode()  # convert the string password to bytes
    salt = b'\x8f\x7fDN\x1d*\xda\x06Gff-\xf2\xf8\x13\x00'  # generate a salt using os.random(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=10000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key


def encrypt_file(password, filename):
    if not os.path.exists(filename):
        _, _filename = os.path.split(filename + ".enc")
        if _filename.endswith(".enc"):
            print("{0} is already encrypted".format(_filename))
            return
        raise FileNotFoundError("{0} not exists".format(filename))

    _, _filename = os.path.split(filename)
    if _filename.endswith(".enc"):
        print("{0} is already encrypted".format(_filename))
        return

    key = get_key(password=password)
    with open(filename, 'rb') as file:
        data = file.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data=data)

    with open("{0}.enc".format(filename), 'wb') as file:
        file.write(encrypted)

    if os.path.exists(filename):
        os.remove(filename)


def decrypt_file_and_read(password, filename):
    if not os.path.exists(filename):
        raise FileNotFoundError("{0} not exists".format(filename))

    key = get_key(password=password)
    with open(filename, 'rb') as file:
        data = file.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(token=data)
    return decrypted.decode()


if __name__ == "__main__":
    password = read_password()
    dirname, _ = os.path.split(os.path.abspath(__file__))
    filename = os.path.join(dirname, "oxford_api_key")

    encrypt_file(password=password, filename=filename)

    filename = "{0}.enc".format(filename)
    decrypt_file_and_read(password, filename)
