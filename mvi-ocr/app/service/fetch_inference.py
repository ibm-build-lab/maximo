from flask import Blueprint
import time
import requests
import shutil
import os
from csv import writer
import statistics

cron = Blueprint("cron", __name__)
logger = None

def get_inference_images(app, mvie_session):
    logger = app.logger
    logger.info("Fetching inference images " + time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

    token = mvie_session.get_token()
    logger.debug('Token : %s', str(token))

    if not token:
        mvie_session.login(app)
        return

    headers = {'mvie-controller': str(token)}

    last_fetched_image_id = mvie_session.get_max_image_id()
    inference_image_url = app.config['MVIE_GET_INF_IMG_URL']
    logger.debug('Last fetched image id: %s', str(last_fetched_image_id))

    if last_fetched_image_id:
        inference_image_url = inference_image_url + '&image_id=' + last_fetched_image_id

    try:
        response = requests.get(inference_image_url, headers=headers, verify=app.config['SSL_VALIDATION'])
        response_data = response.json()
        logger.debug('Image inference response received')

        if response.status_code == 401:
            mvie_session.login(app)

        if response.status_code == 200 and len(response_data) > 0:
            return check_result(response_data, app, mvie_session)
        else:
            return []  
        
    except Exception as e:
        logger.error('Exception while fetchig images: %s', str(e))
        return []


def check_result(response_data, current_app, mvie_session):
    base_dir = current_app.config["BASE_DIR"]
    processed_files_dir = base_dir + current_app.config["PROCESSED_OP_DIR_NAME"]
    unidentified_files_dir = base_dir + current_app.config["INF_UNCTZD_DIR"]
    ocr_files_dir = base_dir + current_app.config["DIR_NAME_FOR_NXT_INF"]
    image_id = None
    result = []
    
    current_app.logger.debug('Images count %d', len(response_data))

    for image in response_data:
        image_id = image['image_id']
        image_url = current_app.config['MVIE_BASE_URL'] + image['imageUrl']
        
        try:
            if 'inferences' in image.keys() and len(image['inferences']) > 0:
                _labels = []
                _confidence = []
                for inference in image['inferences']:
                    _labels.append(inference['label'])
                    _confidence.append(inference['score'])

                label = ' '.join(_labels)
                confidence = statistics.mean(_confidence)
                result.append({'imageId': image_id, 'imageUrl': image_url,'label': label, 'confidence': confidence})
                write_to_file(image_id, confidence, label, ocr_files_dir + label, current_app, 'ocr_inferences.csv')
                write_to_file(image_id, confidence, label, ocr_files_dir + label, current_app, 'inferences.csv')
                download_image(ocr_files_dir + label, image_url, image_id, current_app)
                download_image(processed_files_dir + label, image_url, image_id, current_app)
            else:
                download_image(unidentified_files_dir, image_url, image_id, current_app)

        except Exception as e:
            mvie_session.update_max_image_id(image_id)
            raise e 

    mvie_session.update_max_image_id(image_id)
    return result

def download_image(directory, image_url, image_id, current_app):
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    res = requests.get(image_url, stream = True, verify=current_app.config['SSL_VALIDATION'])

    if res.status_code == 200:
        with open(os.path.join(directory, image_id),'wb') as img:
            shutil.copyfileobj(res.raw, img)
    else:
        logger.debug('Image Couldn\'t be retrieved: %s', str(image_url))


def write_to_file(image_id, confidence, label, file_path, current_app, file_name):
    columns = [image_id, confidence, label, file_path]
    with open(os.path.join(current_app.config["BASE_DIR"], file_name), 'a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(columns)
        f_object.close()
