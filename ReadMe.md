# ImageDatasetAPI

A simple api to save and serve images. The purpose is to separate data
from a machine learning model. To train the model, you can simply 
request an image from the api. The api will return a random image from
the dataset. You can read some more information about the api and how to use it below.

#### TLDR: Usage

Use Apple Shortcuts or any other script to send and collect data. Request labeled images to train a 
machine learning model. Update the labels or metadata of an image to improve the dataset.

### Framework

The whole API is build with [FastAPI](https://fastapi.tiangolo.com/). Docs are available and can be accessed 
here if the service is running: 
- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/` redirect to `/docs`
- `http://127.0.0.1:8000/redoc`

### Docker

You can run the api with docker. The dockerfile can be downloaded from releases or build by yourself. More instructions
coming soon.

↪ [ImageDatasetAPI Releases](https://github.com/Artif3xx/ImageDatasetAPI/releases)

## Collection Images

To be able to classify images we save as much incoming metadata as possible. Location 
information and other useless stuff will be ignored. We focus on the camera settings and
other information about how the image was taken.

### Apple Shortcuts

The simples way is to use a shortcut for this. You simply need to select an image 
and send it to the api. The Metadata will be extracted on the server. You can find some example
shortcuts in the `shortcuts` folder.

↪ [Apple Shortcuts for ImageDatasetAPI](https://github.com/Artif3xx/ImageDatasetAPI/tree/master/shortcuts) 

## Getting Images

To request an image, you simply need to send a get request to the api. You can choose 
between two different endpoints.

### Get `/random`

returns a random image from the dataset

#### Query Params

- `label` - (optional) the label of the image as string in a list. If no label is given, a random image
will be returned. You can select as many labels as you want, the minimum is one. 

```
Example without labels:
http://127.0.0.1:8000/random

Example with labels:
http://127.0.0.1:8000/random?labels=['yellow']
```

## Labels

The images are labels if possible. The labels are extracted from the metadata. If no label is 
available, the image will be labeled as "unknown" and saved in a different folder. The server 
maintainer needs to take care of the images.

To get the available labels, you can choose between the following endpoints:

### Get `/labels`

returns all labels from the image

#### Query Params

- `imageID` - the id of the image as integer

```
Example:
http://127.0.0.1:8000/labels?imageID=42
```

### Post `/updateLabels`

updates the labels for the given image id. This method can be used to add or remove labels from an image. According 
to this, there is no delete method implemented. There must at least a empty array be sent to remove all labels.

#### Query Params

- `imageID` - the id of the image as integer
- `labels` - the labels as string array in a list. In this case the minium is an empty list.
Example: `["label1", "label2"]`

```
Example: 
http://127.0.0.1:8000/updateLabels?imageID=42?labels=["label1", "label2"]

Remove Labels Example:
http://127.0.0.1:8000/updateLabels?imageID=42?labels=[]
```
