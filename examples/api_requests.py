import requests
import cv2
import numpy as np

# define you api url here
api_url = "http://192.168.11.10:8000"


def request_image(item_id: int):
    url = api_url + "/image/" + str(item_id)
    response = requests.get(url)

    if response.status_code == 200:
        image_array = np.frombuffer(response.content, np.uint8)
        res_image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        return res_image
    else:
        return None


def get_ids_for_label(labels: list[str]):
    url = api_url + f"/search?labels={labels}"
    response = requests.get(url)
    request_ids = []
    for item in response.json():
        request_ids.append(item['id'])
    return request_ids
