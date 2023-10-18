import requests
import cv2
import numpy as np


def request_image(item_id: int):
    url = "http://192.168.11.10:8000/image/" + str(item_id)
    response = requests.get(url)

    if response.status_code == 200:
        image_array = np.frombuffer(response.content, np.uint8)
        res_image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        return res_image
    else:
        return None
