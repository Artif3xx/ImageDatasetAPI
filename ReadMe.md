# DatasetAPI

A simple api to save and serve images. The purpose is to separate data
and a machine learning model. To train the model, you simply need to 
request an image from the api. The api will return a random image from
the dataset.

### Framework

The whole API is build with [FastAPI](https://fastapi.tiangolo.com/). Docs are available and can be accessed 
here: 
- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/` redirect to `/docs`
- `http://127.0.0.1:8000/redoc`

## Collection Images

To be able to classify images we save as much incoming metadata as possible. Location 
information and other useless stuff will be ignored. We focus on the camera settings and
other information about how the image was taken.

### Apple Shortcuts

The simples way is to use a shortcut for this. You simply need to select an image 
and send it to the api. The Metadata will be extracted on the server. You can find some example
shortcuts in the `shortcuts` folder.

## Getting Images

To request an image, you simply need to send a get request to the api. You can choose 
between two different endpoints.

### Get `/random`

returns a random image from the dataset

#### Query Params

- `label` - (optional) the label of the image as string. If no label is given, a random image will be returned

```
Example: 
http://127.0.0.1:8000/random

Example: 
http://127.0.0.1:8000/random?labels=yellow
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
- `labels` - the labels as string array. Example: `["label1", "label2"]`

```
Example: 
http://127.0.0.1:8000/updateLabels?imageID=42?labels=["label1", "label2"]

Remove Labels Example:
http://127.0.0.1:8000/updateLabels?imageID=42?labels=[]
```
