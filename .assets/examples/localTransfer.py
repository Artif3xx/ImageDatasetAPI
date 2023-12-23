"""
:detail: this file contains an example for a local transfer of the content of one dataset to another
:author: Castox
"""

import os

import cv2

from DatasetAPI import API, deleteFile


import_server = API("http://import.com")
export_server = API("http://export.com")


def main():
    """
    main function of the script
    """
    # get all items from the import server
    item_ids = import_server.get_ids_for_label([])
    # iterate over all items
    for item_id in item_ids:
        print('processing item', item_id, end=' ... ')
        # get the image data from the import server
        image_data = import_server.get_image_data(item_id)
        # get the image from the import server
        image = import_server.get_image(item_id)

        cv2.imwrite(f"image_{item_id}.jpg", image)

        image_data['labels'].append('Zahn Nahaufnahme')
        # send the image to the export server
        new_item = export_server.send_image(f"image_{item_id}.jpg", image_data['labels'])
        deleteFile(f"image_{item_id}.jpg")
        export_server.update_metadata(new_item['id'], image_data['imageMetadata'])
        print('done', 'new item id:', new_item['id'])


if __name__ == "__main__":
    main()
    print("done")
