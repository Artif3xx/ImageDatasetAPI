# ImageDatasetAPI

A simple docker based application to store and label images. Metadata of images will automatically be extracted and
stored as well. The api is build with FastAPI and uses a sqlite database to store the data. Images will be saved in the 
filesystem. The purpose of the project is to collect and label images for a machine learning model. To train the model,
you can simply request an image from the api. You can see the available endpoints below. 

There is also a custom frontend to manage the dataset, update labels and metadata. More information coming soon!

--- 

###  Table of Contents

1. [Collection Images](https://github.com/Artif3xx/ImageDatasetAPI/tree/master#collection-images)
2. [API Endpoints](https://github.com/Artif3xx/ImageDatasetAPI/tree/master#api-endpoints)
3. [Labels](https://github.com/Artif3xx/ImageDatasetAPI/tree/master#labels)
4. [Metadata](https://github.com/Artif3xx/ImageDatasetAPI/tree/master#metadata)

### Framework

The whole API is build with [FastAPI](https://fastapi.tiangolo.com/). Docs are available and can be accessed 
here if the service is running: 
- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/redoc`

### Docker

You can run the api with docker. The dockerfile can be downloaded from releases or build by yourself. More instructions
coming soon.

↪ [ImageDatasetAPI Releases](https://github.com/Artif3xx/ImageDatasetAPI/releases)

---

## Collection Images

To be able to classify images we save as much incoming metadata as possible. Location 
information and other useless stuff will be ignored. We focus on the camera settings and
other information about how the image was taken.

### Apple Shortcuts

The simples way is to use a shortcut for this. You simply need to select an image 
and send it to the api. The Metadata will be extracted on the server. You can find some example
shortcuts in the `shortcuts` folder.

↪ [Apple Shortcuts for ImageDatasetAPI](https://github.com/Artif3xx/ImageDatasetAPI/tree/master/shortcuts) 

## API Endpoints

To request an image, you simply need to send a get request to the api. You can choose 
between two different endpoints.

### Get `/info`

returns information about the used api version.

#### Example  

```http request:
http://127.0.0.1:8000/info
```

---

### Get `/item/{item_id: int}`

Get the database item of the given id. The item contains the image path, metadata and labels.

#### Path Params

- `item_id` - the id of the image as integer

#### Example

```http request:
http://127.0.0.1:8000/item/42
```

---

### Post `/item/{item_id: int}/update`

Update the item of the given id. The item in the body must contains at least an empty metadata dict and a 
labels string list.

#### Path Params

- `item_id` - the id of the image as integer

#### Body

```json:
newItem = {
  "metadata": {},
  "labels": []
}
```

#### Example

```http request:
http://127.0.0.1:8000/item/42/update data=newItem
```

---

### Delete `/item/{item_id: int}/delete`

Delete the item of the given id. The image will be deleted from the server and the database.

#### Path Params

- `item_id` - the id of the image as integer

#### Example

```http request:
http://127.0.0.2:8000/deleteInfo?imageID=42
```

---

### Get `/image/{item_id: int}`

return an image by id

#### Path Params

- `item_id` - the id of the image as integer

#### Example

```http request:
http://127.0.0.1:8000/image/42
```

---

### Get `/image/random`

returns a random image from the dataset

#### Query Params

- `?labels` - (optional) the label of the image as string in a list. If no label is given, a random image
will be returned. You can select as many labels as you want, the minimum is one. 

```
Example:
http://127.0.0.1:8000/random?labels=['iPhone 15']
```

---

### Get `/search`

you can search the database for images with specific labels. The labels must be given as a list of strings. The 
endpoint returns all the available items in the database.

#### Query Params

- `?labels` - the label of the image as string in a list. There must be at least one label to search for
- `?onlyOne` - (optional) boolean value. if true, images containing only one of the search labels will be returned.
the default value is false. This means the item must contain all the labels in the string list.

#### Example

```http request:
http://127.0.0.1:8000/search?labels=['iPhone 15', 'iPhone 16']&onlyOne=true
http://127.0.0.1:8000/search?labels=['iPhone 15', 'iPhone 16']
```

---

## Labels

You can add labels to an image. The labels are saved as a list of strings. You can add as many labels as you want. 
Those can be used to search for images. You can also update the labels of an image.

## Metadata

You can save and request metadata from an image. If an image is sent to the api, all available metadata will be 
extracted and saved. You can also update the metadata of an image. The metadata is saved as a dict and can be parsed 
into a json object.
