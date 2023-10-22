import requests
import cv2
import numpy as np
import os
import json

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


def update_labels(item_id: int, newLabels: list[str]):
    url = api_url + "/item/" + str(item_id) + "/update"
    labels = json.dumps({"labels": newLabels})
    response = requests.post(url, data=labels)
    return response.json()


def get_image_data(item_id: int):
    url = api_url + "/item/" + str(item_id)
    response = requests.get(url)
    return response.json()


def get_ids_for_label(labels: list[str]):
    url = api_url + f"/search?labels={labels}"
    response = requests.get(url)
    request_ids = []
    for item in response.json():
        request_ids.append(item['id'])
    return request_ids


def send_image(filepath: str, labels: list[str]):
    with open(filepath, "rb") as file:
        files = {"file": (filepath.split('/')[-1], file)}
        url = api_url + f'/upload?labels={labels}'
        response = requests.post(url, files=files)
        print(response.json())


def send_images_in_folder(folder: str, labels: list[str]):
    for filename in os.listdir(folder):
        if filename.endswith(('.jpeg', '.png', '.jpg')):
            image_path = os.path.join(folder, filename)
            send_image(image_path, labels=labels)
            # print(image_path)
            deleteFile(image_path)


def deleteFile(filepath: str) -> bool:
    try:
        os.remove(filepath)
        return True
    except FileNotFoundError:
        return False
    except PermissionError:
        return False
    except IsADirectoryError:
        return False


if __name__ == "__main__":
    # myLabels = ["label1", "label2"]
    # send_images_in_folder('upload', myLabels)

    myLabels = ["label1", "label2"]

    for i in range(1539, 1554):
        # data = get_image_data(i)
        data = update_labels(i, myLabels)
        print(i, data['labels'])
