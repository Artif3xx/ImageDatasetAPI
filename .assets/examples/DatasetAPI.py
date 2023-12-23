import requests
import cv2
import numpy as np
import os
import json


class API:
    def __init__(self, api_url):
        self.api_url = api_url

    def get_info(self):
        url = self.api_url + "/info"
        response = requests.get(url)
        return response.json()

    def get_image(self, item_id: int):
        url = self.api_url + "/image/id/" + str(item_id)
        response = requests.get(url)

        if response.status_code == 200:
            image_array = np.frombuffer(response.content, np.uint8)
            res_image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

            return res_image
        else:
            return None

    def update_labels(self, item_id: int, newLabels: list[str]):
        url = self.api_url + "/item/id/" + str(item_id) + "/update"
        labels = json.dumps({"labels": newLabels})
        response = requests.post(url, data=labels)
        return response.json()

    def update_metadata(self, item_id: int, newMetadata: dict):
        url = self.api_url + "/item/id/" + str(item_id) + "/update"
        metadata = json.dumps({"imageMetadata": newMetadata})
        response = requests.post(url, data=metadata)
        return response.json()

    def get_image_data(self, item_id: int):
        url = self.api_url + "/item/id/" + str(item_id)
        response = requests.get(url)
        return response.json()

    def get_ids_for_label(self, labels: list[str]):
        url = self.api_url + f"/search?labels={labels}"
        response = requests.get(url)
        request_ids = []
        for item in response.json():
            request_ids.append(item['id'])
        return request_ids

    def send_image(self, filepath: str, labels: list[str]):
        with open(filepath, "rb") as file:
            files = {"file": (filepath.split('/')[-1], file)}
            url = self.api_url + f'/upload?labels={labels}'
            response = requests.post(url, files=files)
            return response.json()

    def send_images_in_folder(self, folder: str, labels: list[str], deleteFiles = False):
        for filename in os.listdir(folder):
            if filename.endswith(('.jpeg', '.png', '.jpg')):
                image_path = os.path.join(folder, filename)
                self.send_image(image_path, labels=labels)
                if deleteFiles:
                    deleteFile(image_path)

    def delete_image(self, item_id: int):
        url = self.api_url + f"/item/id/{item_id}/delete"
        response = requests.delete(url)
        return response.json()


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


def writeFile(filepath: str, content) -> bool:
    try:
        with open(filepath, "w") as file:
            file.write(content)
        return True
    except FileNotFoundError:
        return False
    except PermissionError:
        return False
    except IsADirectoryError:
        return False


if __name__ == "__main__":
    api = API("http://portainer.local.com")
    print(api.get_image_data(1))
    exit(0)
