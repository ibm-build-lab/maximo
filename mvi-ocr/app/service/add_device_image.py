from flask import Blueprint
import time
import os
import requests

cron = Blueprint("cron", __name__)
logger = None

def add_image_to_device(app, mvie_session, file_util):
    logger = app.logger
    logger.info("Adding image to input source %s", time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

    base_dir = app.config["BASE_DIR"]
    input_directory = base_dir + app.config['FILE_IP_DIR_NAME']
    upload_directory = base_dir + app.config['UPLOADED_DIR_NAME']

    token = mvie_session.get_token()
    logger.debug('Token found: %s', str(token))

    if not token:
        mvie_session.login(app)
        token = mvie_session.get_token()

    headers = {'mvie-controller': token}
    files_to_add = [fn for fn in os.listdir(input_directory)
              if any(fn.endswith(ext) for ext in app.config["ALLOWED_FILE_EXTENSIONS"])]

    logger.debug(files_to_add)

    upload_count = 0
    for fl in files_to_add:
        try:
            files = {'file': open(input_directory + fl, 'rb')}
            response = requests.post(app.config['MVIE_ADD_IMG_DVC_URL'], files=files , headers=headers, verify=app.config['SSL_VALIDATION'])
            response_data = response.json()
            logger.debug('Response received %s', str(response_data))
            if response.status_code == 200:
                file_util.copy_file(input_directory, upload_directory, fl, is_copy=False)
                upload_count += 1
            elif response.status_code == 401:
                mvie_session.login(app)
                break
        except Exception as e:
            logger.error('Error occurred while adding files to input source %s', str(e))

    return upload_count