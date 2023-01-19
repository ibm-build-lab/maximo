import easyocr
import cv2
from flask import Blueprint
import os
import shutil
import csv
from fuzzywuzzy import fuzz

cron = Blueprint("cron", __name__)
_ocr_output_file = 'ocr_output.csv'

def easy_ocr(app):
    ocr_input_dir = os.path.join(app.config["BASE_DIR"], app.config["DIR_NAME_FOR_NXT_INF"])

    app.logger.info('Reading files from ' + ocr_input_dir)
    response_data = []

    for root,d_names,fnames in os.walk(ocr_input_dir):
        for dir in d_names:

            files_to_add = [fn for fn in os.listdir(os.path.join(root, dir))
                        if any(fn.endswith(ext) for ext in app.config["ALLOWED_FILE_EXTENSIONS"])]

            try:
                for fl in files_to_add:
                    img = cv2.imread(os.path.join(root, dir, fl))
                    reader = easyocr.Reader(['en'], gpu=True)
                    result = reader.readtext(img)
                    matched_label, op_directory, labels = process_result(result, root, dir, fl, app)
                    response_data.append({'imageId': fl,
                        'mviLabel': dir,
                        'ocrMatchedLabel': matched_label,
                        'outputDir' : op_directory,
                        'labels': labels })
            except Exception as e:
                app.logger.error('Error while processing %s in %s dir', fl, dir)
                app.logger.error(e)

    return response_data


def process_result(result, root, dir, file, app):
    predefined_labels = app.config['OCR_LABELS_TO_MATCH']
    match_found = False
    matched_label = ''
    op_directory = app.config['OCR_UNCTZD_DIR']
    labels = ''

    if result is None or len(result) == 0:
        move_file(os.path.join(root, dir), os.path.join(app.config['BASE_DIR'], op_directory), file)
        write_csv(file, dir, matched_label, os.path.join(app.config['BASE_DIR'], op_directory), labels, app, _ocr_output_file)
        return matched_label, op_directory, labels

    labels = ','.join(i[1] for i in result)

    for item in result:
        match_found, matched_label = match_closest(item[1], predefined_labels)
        if match_found:
            match_found = True
            break

    if match_found:
        op_directory = os.path.join(app.config['OCR_PCSD_DIR'], matched_label)
        
    move_file(os.path.join(root, dir), os.path.join(app.config['BASE_DIR'], op_directory), file)
    write_csv(file, dir, matched_label, os.path.join(app.config['BASE_DIR'], op_directory), labels, app, _ocr_output_file)
    return matched_label, op_directory, labels

def move_file(source, destination, file):
    if not os.path.exists(destination):
        os.makedirs(destination)
    shutil.move(os.path.join(source, file), os.path.join(destination, file))


def write_csv(image_id, label, matched_label, op_dir,labels, current_app, csv_file_name):
    columns = [image_id, label, matched_label, op_dir, labels]
    with open(os.path.join(current_app.config["BASE_DIR"], csv_file_name), 'a') as f:
        csv_writer = csv.writer(f, quotechar="'")
        csv_writer.writerow(columns)


def read_ocr_processed_csv(file, fieldnames):
    json_array = []
    if os.path.exists(file):
        with open(file, encoding='utf-8') as csvf:
            reader = csv.DictReader( csvf, fieldnames, skipinitialspace=True, quotechar="'")
            for row in reader:
                if os.path.exists(os.path.join(row['dirPath'], row['imageId'])):
                    if not row['ocrMatchedLabel'] or row['ocrMatchedLabel'] == "":
                        row['outputDir'] = 'ocr_uncategorized/'
                    else:
                        row['outputDir'] = 'ocr_processed/' + row['mviLabel']
                    json_array.append(row)    
        csvf.close()
    return json_array


def match_closest(str, labels):
    for label in labels:
        if fuzz.ratio(str.lower().replace(' ',''), label.lower().replace(' ','')) >= 50:
            return True, label
    return False, ''

