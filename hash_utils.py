import bcrypt
import hashlib
import passlib.hash
import secrets
from argon2 import PasswordHasher

pepper = "8fa1921c"


# Store the password in plaintext! This is so much dangerous
def plain(password):
    return "$0$" + password


# Basic and Simple SHA-256 hashing, no salt, no rounds, no protection
def sha256(password):
    res = hashlib.sha256(password.encode('utf-8')).hexdigest()
    # print(res)
    return "$5$" + res

def verify_sha256(password, hash):
    res = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return "$5$" + res == hash

# Advanced SHA-512 hashing, with salt, peppr, rounds and provides more protection!
def sha512(password):
    salt = secrets.token_hex(4) + pepper
    rounds = secrets.randbelow(100000) + 50000
    res = passlib.hash.sha512_crypt.using(salt=salt, rounds=rounds).hash(password)
    res = res.replace(pepper, '', 1)
    return res

def verify_sha512(password, hash):
    idx = hash.rfind('$')
    hash =  hash[:idx] + pepper + hash[idx:]
    # print(hash)
    res = passlib.hash.sha512_crypt.verify(password, hash)
    # print(res)
    return res


def bcrypt_enc(password):
    password = password.encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    # print(hashed)

def verify_bcrypt(password, hash):
    return bcrypt.checkpw(password, hash)


def argon2_enc(password):
    ph = PasswordHasher()
    hash = ph.hash(password)
    # print(hash)
    return hash

def verify_argon2(password, hash):
    ph = PasswordHasher()
    try:
        return ph.verify(password, hash)
    except:
        return False 

def verify(password, hash):
    # print(hash)
    type = hash.find('$', 1)
    type = hash[1: type]
    # print(type)

    if type == "0":
        return password == hash[3:]
    elif type == "5":
        return verify_sha256(password, hash)
    elif type == "6":
        return verify_sha512(password, hash)
    elif type == "2b":
        return verify_bcrypt(password, hash)
    elif type == "argon2id":
        return verify_argon2(password, hash)    
    