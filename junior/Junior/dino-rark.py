
import requests
import uuid
import time

def dino():
    for i in range(0,50):
        response = requests.get(f"http://127.0.0.1:5000/add?key={str(uuid.uuid4().hex)}&value=rark")
        time.sleep(10)

dino()
