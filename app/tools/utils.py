import base64
import uuid
from fastapi import UploadFile
from random import Random

async def generate_user_code(name:str):
    random_num = str(Random().randint(a=1000,b=9999))
    random_name = name[0:4].upper()
    user_code = random_name+random_num
    return user_code

async def generate_uuid_id():
    return str(uuid.uuid4())

async def to_base64(file: UploadFile):
    file = await file.read()
    b64_img = base64.b64encode(file).decode("utf-8")
    return b64_img