import random, string





def generate_sk():
    
    alphabet = string.ascii_letters + string.digits
    code = ''.join(random.choice(alphabet) for i in range(20))

    sk = f"sk_{code}"

    return sk