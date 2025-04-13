from random import Random

async def generate_user_code(name:str):
    random_num = str(Random().randint(a=1000,b=9999))
    random_name = name[0:4].upper()
    user_code = random_name+random_num
    return user_code