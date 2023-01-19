from flask import Blueprint, request, render_template, current_app, abort, send_file
from app.service.add_device_image import add_image_to_device
from app.service.fetch_inference import get_inference_images
from app.util.mvie_session import MvieSession
from app.util.file_util import FileUtil
from app.service.ocr import easy_ocr, read_ocr_processed_csv
import os
import csv
import json

main = Blueprint("main", __name__)
INPUT_HTML = 'input.html'
FILES_HTML = 'files.html'
VISION_EDGE_IMG_PATH = '/opt/ibm/vision-edge/images/'

@main.route('/')
def home():
    action = request.args.get('action')
    file_util = FileUtil()
    mvie_session = MvieSession(current_app) 

    if action is None:
        files = fetch_files(current_app.config['FILE_IP_DIR_NAME'])
        return render_template(INPUT_HTML, 
        message='',
        action="uploadImage",
        buttonLabel="Upload Images",
        dir=current_app.config['FILE_IP_DIR_NAME'],
        files=files)
    elif action == 'uploadImage':
        current_app.logger.info('Uploading images to MVI input source')
        image_count = add_image_to_device(current_app, mvie_session, file_util)
        return render_template('home.html', message=str(image_count) + ' image(s) uploaded!', show_table=False)        
    else:
       return render_template(INPUT_HTML, message='')


@main.route('/fetchInference')
def fetch_inference():
    mvie_session = MvieSession(current_app) 
    current_app.logger.info('Fetching image inferences')
    result = get_inference_images(current_app, mvie_session)
    return render_template('home.html', message="MVI Inferences Output",data=result, show_table=True)


@main.route('/ocr')
def ocr():
    action = request.args.get('action')

    if action == 'processOcr':
        current_app.logger.info('Processing OCR')
        result = easy_ocr(current_app)
        #Removing file content after processing
        open(os.path.join(current_app.config['BASE_DIR'], 'ocr_inferences.csv'), 'w').close()
        return render_template('ocr.html',
            message='',
            dir=current_app.config['DIR_NAME_FOR_NXT_INF'],
            data=result,
            imgeUrl=current_app.config['MVIE_BASE_URL'] + VISION_EDGE_IMG_PATH + current_app.config['MVIE_INSPTN_UUID'] +'/')
    elif action == "viewOcrProcessed":
        csv = os.path.join(current_app.config['BASE_DIR'], 'ocr_output.csv')
        field_name = ("imageId","mviLabel","ocrMatchedLabel","dirPath", "labels")
        result = read_ocr_processed_csv(csv, field_name)
        return render_template('ocr.html',
            message='OCR Output',
            dir=current_app.config['DIR_NAME_FOR_NXT_INF'],
            data=result,
            imgeUrl=current_app.config['MVIE_BASE_URL'] + VISION_EDGE_IMG_PATH + current_app.config['MVIE_INSPTN_UUID'] +'/')
    else:
        csv = os.path.join(current_app.config['BASE_DIR'], 'ocr_inferences.csv')
        field_name = ("imageId","score","label","dirPath")
        result = read_csv(csv, field_name, current_app.config['DIR_NAME_FOR_NXT_INF'], False)
        return render_template(FILES_HTML, data=result,
            message="Below images will be processed for OCR",
            action="processOcr",
            buttonLabel="Process OCR",
            dir=current_app.config['DIR_NAME_FOR_NXT_INF'])


@main.route('/output')
def output():

    ocr_csv = os.path.join(current_app.config['BASE_DIR'], 'ocr_output.csv')
    field_name = ("imageId","mviLabel","ocrMatchedLabel","dirPath", "labels")
    ocr_result = read_ocr_processed_csv(ocr_csv, field_name)
    f_ocr_result = filter(lambda x: x["ocrMatchedLabel"] != '', ocr_result)

    return render_template('output.html',
        data=f_ocr_result,
        imgeUrl=current_app.config['MVIE_BASE_URL'] + VISION_EDGE_IMG_PATH + current_app.config['MVIE_INSPTN_UUID'] +'/')


@main.route('/processed')
def processed():
    csv = os.path.join(current_app.config['BASE_DIR'], 'inferences.csv')
    field_name = ("imageId","score","label","dirPath")
    result = read_csv(csv, field_name, current_app.config['PROCESSED_OP_DIR_NAME'], True)
    return render_template(FILES_HTML,
        data=result,
        dir=current_app.config['PROCESSED_OP_DIR_NAME'],
        imgeUrl=current_app.config['MVIE_BASE_URL'] + VISION_EDGE_IMG_PATH + current_app.config['MVIE_INSPTN_UUID'] +'/')


@main.route('/view/', defaults={'req_path': ''})
@main.route('/view/<path:req_path>')
def processed_file(req_path):
    file_name = req_path + '.csv'
    csv = os.path.join(current_app.config['BASE_DIR'], file_name)
    field_name = ("imageId","score","label","dirPath")
    result = read_csv(csv, field_name, current_app.config['PROCESSED_OP_DIR_NAME'], False)
    return render_template(FILES_HTML, data=result, dir=current_app.config['PROCESSED_OP_DIR_NAME'])


@main.route('/files/', defaults={'req_path': ''})
@main.route('/files/<path:req_path>')
def dir_listing(req_path):
    files, is_file = fetch_files(req_path)

    if is_file:
        return files
 
    return render_template(FILES_HTML,files=files)


def fetch_files(directory):
    abs_path = os.path.join(current_app.config['BASE_DIR'], directory)

    if not os.path.exists(abs_path):
        return abort(404)

    if os.path.isfile(abs_path):
        return send_file(abs_path), True

    files = os.listdir(abs_path)
    return files


def read_csv(file, fieldnames, dir, surpass_check):
    json_array = []
    with open(file, encoding='utf-8') as csvf:
        reader = csv.DictReader( csvf, fieldnames)
        for row in reader:
            if surpass_check or os.path.exists(os.path.join(row['dirPath'], row['imageId'])):
                row['outputDir'] =  dir + row['label']
                json_array.append(row)
    csvf.close()           
    return json_array
