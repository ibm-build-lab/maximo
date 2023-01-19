# MVI-OCR

Utilizing Maximo Visual Inspection with an Optical Character Recognition Solution.

## Feature Enablement

When using Maximo Visual Inspection (MVI) for object detection, there are sometimes additional categorization that is dependent on specific text on the object.
This project is solution to this particular use case by tying in MVI with an Optical Character Recognition (OCR) solution to help in the categorization.

<img width="801" alt="image" src="https://user-images.githubusercontent.com/7766512/213415229-1f2072b0-f86d-421e-ab9e-84ccce03fd43.png">

This solution was specific to product recognition, it can be used for any project where we are using MVI for object recognition where there can be text on the object that may provide a second categorization.

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

Make sure that path for BASE_DIR exist. Checkout [APIs section](#mvie-useful-apis) to retrieve input source id.

## Run Application

To run an application navigate to root directory of project and execute below command.

```sh
flask --app app run --port 5000
```

Make sure that you have run `pip3 install -r requirements.txt` before running this project first time.


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
- Python
