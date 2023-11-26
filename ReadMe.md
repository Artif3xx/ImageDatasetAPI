# ImageDatasetAPI

A simple docker based application to store and label images. Metadata of images will automatically be extracted and
stored as well. The api is build with FastAPI and uses a sqlite database to store the data. Images will be saved in the 
filesystem. The purpose of the project is to collect and label images for a machine learning model. To train the model,
you can simply request an image from the api. You can see the available endpoints below. 

There is also a custom frontend to manage the dataset, update labels and metadata. More information coming soon!

![ImageDatasetAPI](https://github.com/Artif3xx/ImageDatasetAPI/blob/f44a42d9b1d3437e42ef8ba04f5e862166636bd4/.assets/readme/SeachPage.gif)

## Docker

You can run the api with docker. The dockerfile can be downloaded from releases or build by yourself. More instructions
coming soon.

↪ [ImageDatasetAPI Releases](https://github.com/Artif3xx/ImageDatasetAPI/releases)

---

### Labels

You can add labels to an image. The labels are saved as a list of strings. You can add as many labels as you want. 
Those can be used to search for images. You can also update the labels of an image.

### Metadata

You can save and request metadata from an image. If an image is sent to the api, all available metadata will be 
extracted and saved. You can also update the metadata of an image. The metadata is saved as a dict and can be parsed 
into a json object.
