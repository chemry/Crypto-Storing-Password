import bcrypt
import hashlib
import passlib.hash
import secrets

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
    return res == hash

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



def verify(password, hash):
    # print(hash)
    type = hash.find('$', 1)
    type = hash[1: type]
    # print(type)

    if type == "0":
        return password == hash[3:]
    elif type == "5":
        return verify_sha256(password, hash[3:])
    elif type == "6":
        return verify_sha512(password, hash)
