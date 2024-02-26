import random
import string






def unique_id():
    
    alphabet = string.ascii_letters + string.digits
    code = ''.join(random.choice(alphabet) for i in range(15))

    return code
