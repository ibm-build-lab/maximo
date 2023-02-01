# MVI-OCR

Utilizing Maximo Visual Inspection with an Optical Character Recognition Solution.

## Feature Enablement

When using Maximo Visual Inspection (MVI) for object detection, there are sometimes additional categorization that is dependent on specific text on the object.  This article details one solution to this particular use case by tying in MVI with an Optical Character Recognition (OCR) solution to help in the categorization.

`By Jatindra Suthar, Jeremy Alcanzare, Zeel Patel, and Hans J. Klose`

While working with a customer on a product recognition play, we realized that MVI was great at recognizing the specific product but wasn’t always right when picking up on additional nuances like if that product was a sub brand.  While we could always get MVI to recognize the product’s logo consistently, it may not pick up if that product was mini, original, or chewy as an example.

One solution to this, was to use MVI to recognize the brand and attempt to recognize the sub brand but send it to an Optical Character Recognition (OCR) solution if the confidence scores are low to act as a tie breaker.

Although this solution was specific to product recognition, it can be used for any project where we are using MVI for object recognition where there can be text on the object that may provide a second categorization.

<img width="801" alt="image" src="https://raw.githubusercontent.com/ibm-build-lab/maximo/main/mvi-ocr/images/flow.png">

Since this solution is meant for handling thousands of files per hour, we proposed separating the logic into a separate VM with an additional GPU that the OCR solution can utilize for faster processing.  This also allows the customer to tie in some of their customized logic on that VM.

## Download Solution

Solution can be downloaded and customized for your particular use case as needed.  Below is the use and configuration of the Python automation script that uses the APIs exposed by MVI Edge to upload images to MVI Edge for inspections and to fetch the inferences.  Python webapp is built using Python Flask framework.  For web UI, Jinja – Web template engine is used.

Clone the solution `git clone https://github.com/ibm-build-lab/maximo.git`

## Login to VM

If you are using VM to run this solution login to VM
`ssh <user>@<host> -i <p_key>`

## Deploy Source Code

Create a directory such as /home/mvi-ocr on the server then deploy by cloning from git or by copying the source code to that VM. 
If you have downloaded zip file, then you can copy zip file to VM using below command.

`scp -i <p_key> <file>.zip <user>@<ip>:/home/mvi-ocr/`

Then unzip the file:

```sh
cd /home/mvi-ocr/
unzip <file>.zip
```

## Configurations

Update the [config.py](app/config.py) file in [/app/](app) folder to update the configuration accordingly. Most of the configuration remain. Only few configuration may change when new inspection or input source is created on MVI Edge.

| Configuration | Description |
| ------ | ------ |
| BASE_DIR | Base directory where all inference related data will be store. E.g. Input, processed directories and other csv files that stores the inferences results. |
| MVIE_BASE_URL | MVI Edge URL |
| MVIE_USERNAME | MVI Edge user name |
| MVIE_PASSWORD | MVI Edge Password |
| MVIE_INPUT_SRC_UUID | MVI Edge input source id |
| MVIE_INSPTN_UUID | MVI Edge inspection id |
| OCR_LABELS_TO_MATCH | List of labels to match with OCR |

Make sure that path for BASE_DIR exist. Checkout [APIs section](#mvie-useful-apis) to retrieve input source id.
MVIE_INSPTN_UUID can be retrieved by; Go to MVIE instance, from dashboard click on inspection to open inspection configuration page. From browser address bar inspection id can be copied.

E.g `https://{host}/#/stations/{station_id}/inspections/{inspection_id}`

Please note that it is advisable to set value of SSL_VALIDATION=True in config.py otherwise it will expose the application to security risk. 

## Install Dependencies

This project uses dependencies that needs to be installed before running an application. Navigate to location of requirements.txt file and run below command to install dependencies.

`pip3 install -r requirements.txt`

## Run Application

To run an application navigate to root directory of project and execute below command.

```sh
flask --app app run --port 5000
```

If you are running an application on virtual instance make sure to add `–host 0.0.0.0` in run command to access the app using server IP address at specified port.  
 
After running above command, application will be available at `http://<host>:5000/`

With default configuration some directories and csv files will be automatically created under directory name configured for `BASE_DIR` config. The directories’ name can configured in [config.py](app/config.py) file. 

<img width="801" alt="image" src="https://raw.githubusercontent.com/ibm-build-lab/maximo/main/mvi-ocr/images/directories.png">

Put files in input directory that you wish to upload to input source of MVI Edge for inference.

<img width="801" alt="image" src="https://raw.githubusercontent.com/ibm-build-lab/maximo/main/mvi-ocr/images/home.png">

Click on `Upload Image` button on home page to send files to MVI Edge. Once files are uploaded, files from input directory will be moved to `uploaded` directory for backup. 

Click on `Fetch Inferences` to fetch the inferences of recently uploaded images. After fetching the inferences, images with detected object will be downloaded to `processed` folder by creating sub-directories. For example, `ABC` is object which is detected on image then new directory named `ABC` will be created and that images will be downloaded to `processed/ABC` folder.

`Inferences` page displays the list of fetched inferences till date with Label detected on image, Confidence score and other metadata.

<img width="801" alt="image" src="https://raw.githubusercontent.com/ibm-build-lab/maximo/main/mvi-ocr/images/inference.png">

If additional categorization is need on fetched inferences, click on `OCR/Process` OCR to pass images to OCR solution. This will display only those images for which object is detected and is under `processed` folder.

OCR solution will use labels configured for `OCR_LABELS_TO_MATCH` config to match the text. If match found, images will be copied to `ocr_processed/<MATCHED_TEXT>` directory otherwise images will be moved to `ocr_uncategorized` directory.

`Ouput` page displays list of all processed OCR.

## Session management

To send API request to MVI Edge, it is required to login and get the token from MVI Edge by passing username/password. This username/password can be change by updating the `config.py` file as mentioned above in configuration section. 

Whenever we run application script will login to MVIE and will update the token in `token.json` file and that token will be used to communicate with MVI Edge. TTL for token is 30 mins and TTL get refreshed when new API call is made to Edge. 
 
 
Moreover, `token.json` also stores the max ImageId retrieved from MVI Edge. As MVIE returns all inferences till date, we need to pass the max ImageId in order to fetch inferences occurred only after particular id. Python script automatically update this ID in json file as we fetch inferences and next time it will fetch only those inferences which has id greater than stored inference id. 

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

## Project structure

<img alt="image" src="https://raw.githubusercontent.com/ibm-build-lab/maximo/main/mvi-ocr/images/structure.png">

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


## Prerequisites
- [Maximo Visual Inspection](https://www.ibm.com/products/maximo/visual-inspection)
- Maximo Visual Inspection Edge
- Python (3.9/3.10)
