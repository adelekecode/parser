import string
import random

def generate_password():
    a = []
    for _ in range(3):
        a.append(random.choice(string.ascii_lowercase))
        a.append(random.choice(string.ascii_uppercase))
        a.append(random.choice(string.digits))
        a.append(random.choice(["@","!","$","#","="]))
    random.shuffle(a)
    return "".join(a)


def generate_code(n):
    
    alphabet = string.ascii_letters + string.digits
    code = ''.join(random.choice(alphabet) for i in range(n))
    return code






def generate_sk():
    
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(38))

    return "sk_" + random_string
