# this file should become a script that transfers images from one dataset to another
import os
import json
import cv2 as cv
from tqdm import tqdm

from DatasetAPI import API


def importImages(saveFolder: os.path, apiURL: str, searchLabels: list[str] = None):
    api = API(apiURL)

    if searchLabels is None:
        searchLabels = []
    all_image_ids = api.get_ids_for_label(searchLabels)
    print(len(all_image_ids), " images found")

    # create a folder for the image
    contentFolder = os.path.join(saveFolder, "content")
    if not os.path.exists(contentFolder):
        os.mkdir(contentFolder)

    for image_id in tqdm(all_image_ids, unit='images'):
        itemFolder = os.path.join(contentFolder, str(image_id))
        if os.path.exists(itemFolder):
            print('Folder ', itemFolder, ' already exists. Skipping the id: ', image_id)
            continue
        os.mkdir(itemFolder)
        # request the image and save it in the saveFolder
        img = api.request_image(image_id)
        data = api.get_image_data(image_id)
        filename = data['path'].split('/')[-1].removeprefix(str(image_id) + '-')
        savePath = os.path.join(itemFolder, filename)
        cv.imwrite(savePath, img)
        # save the Image Data from the Database in a json file
        json.dump(data, open(os.path.join(itemFolder, 'data.json'), "w"))


def exportImages(contentFolder: str, apiULR: str):
    api = API(apiULR)
    for itemFolder in tqdm(os.listdir(contentFolder), unit='images'):
        itemPath = os.path.join(contentFolder, itemFolder)
        if os.path.isdir(itemPath):
            image_id = int(itemFolder)
            data = json.load(open(os.path.join(itemPath, 'data.json'), "r"))
            imageMetadata = data['imageMetadata']
            labels = data['labels']
            filepath = os.path.join(itemPath, data['path'].split('/')[-1].removeprefix(str(image_id) + '-'))

            item = api.send_image(filepath, labels)
            item_id = item['id']
            api.update_metadata(item_id, imageMetadata)
            # print(item_id, api.get_image_data(item_id))


if __name__ == "__main__":
    target_folder = "Path to your folder"
    api_url = "Your Server URL"

    # importImages(saveFolder=target_folder, apiURL=api_url, searchLabels=[])
    exportImages(contentFolder=target_folder, apiULR=api_url)
