import argon2


def hash(inp):
    return argon2.hash_password(bytes(inp, 'utf-8'))

def check_hash(hash, inp):
    try:
        return argon2.verify_password(hash, bytes(inp, 'utf-8'))
    except:
        return False

if __name__ == '__main__':
    print(hash('123456'))
    
    print(check_hash(hash('123456'), '123456'))


