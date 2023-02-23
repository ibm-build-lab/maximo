# MVI-OCR

Utilizing Maximo Visual Inspection with an Optical Character Recognition Solution.

## Overview

When using Maximo Visual Inspection (MVI) for object detection, there are sometimes additional categorization that is dependent on specific text on the object.  This article details one solution to this particular use case by tying in MVI with an Optical Character Recognition (OCR) solution to help in the categorization.

While working with a customer on a product recognition play, we realized that MVI was great at recognizing the specific product but wasn’t always right when picking up on additional nuances like if that product was a sub brand.  While we could always get MVI to recognize the product’s logo consistently, it may not pick up if that product was mini, original, or chewy as an example.

One solution to this, was to use MVI to recognize the brand and attempt to recognize the sub brand but send it to an Optical Character Recognition (OCR) solution if the confidence scores are low to act as a tie breaker.

Although this solution was specific to product recognition, it can be used for any project where we are using MVI for object recognition where there can be text on the object that may provide a second categorization.

<img width="801" alt="flow" src="https://user-images.githubusercontent.com/7766512/216315617-731ee6d6-7297-4bd4-a495-e66c3a6c3faf.png">

Since this solution is meant for handling thousands of files per hour, we proposed separating the logic into a separate VM with an additional GPU that the OCR solution can utilize for faster processing.  This also allows the customer to tie in some of their customized logic on that VM.

## Configuration
Refer to the MVI-OCR documentation for installation and configuration details:
https://developer.ibm.com/tutorials/sending-images-mviedge-ocr/


## Project structure

<img width="157" alt="structure" src="https://user-images.githubusercontent.com/7766512/216315974-5293611b-b616-4611-842e-3c5b8699bdd0.png">


### requirements.txt

`requirements.txt` file lists all the dependencies for this project. When any new dependency is required, it should be added to this file. Before running an application make sure to download listed dependencies in this file using below command from root directory of project.

`pip3 install -r requirements.txt`

This step is required only when we run project first time, or any new dependency is added to this file.

### app/config.py
It consists configurations for server base URL, secret tokens, username/passwords directories name etc.

### app/main/route.py
All endpoints are declared in this file. It maps URL to specific function that will handle the logic of that URL.

### app/service/add_device_image.py
Logic to add images to input source of MVI Edge is written in this file. It calls MVI Edge’s endpoint to add image in input source. Input source id is should be declared in config.py file. Once file is uploaded it move file from input folder to folder name specified for variable `UPLOADED_DIR_NAME` in `config.py` file.

### app/service/fetch_inference.py
This file contains logic to fetch inferences from MVI Edge. While fetching inferences it creates directories from labels detected in inference and downloads images to respective directories.
Confidence score is calculated by averaging confidence of all labels detected on images. 
After fetching inferences two .csv files are created under `BASE_DIR` as below:
1.	`inferences.csv`: To collect all inferences fetched till date. 
2.	`ocr_inferences.csv`: Inferences that needs to pass to OCR solutions.  Once OCR process is done, content from this file will be removed.

### app/service/ocr.py
It processes images and extract text from images. It takes ocr_inferences.py as input to get location of images that needs to pass to OCR. 
It matches text from OCR with labels configured for `OCR_LABELS_TO_MATCH` config variable. For the text match fuzzywuzzy library is used.
After process and based on the match images are moved to OCR processed and OCR uncategorized directories.

### app/templates
This directory contains html files for UI. `base.html` is master template file contains declaration for css and js as well as navigations. Other html files contain html for specific view only extends `base.html`

## MVIE useful APIs

### Login to MVI Edge

`POST https://<MVIE_URL>/api/v1/users/sessions`

```sh
Request Body:
{  
  "grant_type": "password",
  "password": "",
  "username": ""
}
```

### Fetch Inferences

`GET https://<MVIE_URL>/inspections/images/inferences?uuid=<inspection_uuid>&image_id=<image_id>`

```sh
Header:  
mvie-controller : <session_token>
```

### Get list of input sources

`GET https://<MVIE_URL>/devices`

```sh
Header:
mvie-controller : <session_token>
```

## Prerequisites
- [Maximo Visual Inspection](https://www.ibm.com/products/maximo/visual-inspection)
- Maximo Visual Inspection Edge
- Python (3.9/3.10)
