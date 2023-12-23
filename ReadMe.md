# ImageDatasetAPI

[![CodeQL](https://github.com/Artif3xx/ImageDatasetAPI/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/Artif3xx/ImageDatasetAPI/actions/workflows/github-code-scanning/codeql)
[![GitHub](https://img.shields.io/github/license/Artif3xx/ImageDatasetAPI?style=flat)](https://github.com/Artif3xx/ImageDatasetAPI/blob/master/LICENSE.rst)

| **[AMD64](https://hub.docker.com/r/castox/image-dataset-api_amd64)**                                                                                                                                                | **[ARM64](https://hub.docker.com/r/castox/image-dataset-api_arm64)**                                                                                                                                                |
|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ![Docker Image Version (latest semver)](https://img.shields.io/docker/v/castox/image-dataset-api_amd64)                                                                                                             | ![Docker Image Version (latest semver)](https://img.shields.io/docker/v/castox/image-dataset-api_arm64)                                                                                                             |
| [![Docker](https://img.shields.io/docker/image-size/castox/image-dataset-api_arm64/latest?label=Docker%20Image%20Size&style=flat)](https://hub.docker.com/repository/docker/castox/image-dataset-api_arm64/general) | [![Docker](https://img.shields.io/docker/image-size/castox/image-dataset-api_amd64/latest?label=Docker%20Image%20Size&style=flat)](https://hub.docker.com/repository/docker/castox/image-dataset-api_amd64/general) |

---

A simple docker based application to store and label images. Metadata of images will automatically be extracted and
stored as well. The api is build with FastAPI and uses a sqlite database to store the data. Images will be saved in the 
filesystem. The purpose of the project is to collect and label images for a machine learning model. To train the model,
you can simply request an image from the api. You can see the available endpoints below. 

There is also a custom frontend to manage the dataset, update labels and metadata. More information coming soon!

![ImageDatasetAPI](https://github.com/Artif3xx/ImageDatasetAPI/blob/api-development/.assets/readme/SeachPage.gif)

## Docker

This application is designed to run in a docker environment. In order to use the image you can easily pull the latest 
image from docker hub. You can find the images for [AMD](https://hub.docker.com/r/castox/image-dataset-api_amd64) and 
for [ARM](https://hub.docker.com/r/castox/image-dataset-api_arm64) here. Use the following command to pull the 
docker on your local machine:

``` bash
docker pull castox/image-dataset-api_amd64:latest
```

```bash
docker pull castox/image-dataset-api_arm64:latest
```

---

### Labels

You can add labels to an image. The labels are saved as a list of strings. You can add as many labels as you want. 
Those can be used to search for images. You can also update the labels of an image.

### Metadata

You can save and request metadata from an image. If an image is sent to the api, all available metadata will be 
extracted and saved. You can also update the metadata of an image. The metadata is saved as a dict and can be parsed 
into a json object.
