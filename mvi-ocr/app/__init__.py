from flask import Flask
import os
from app.config import Config
import logging
from logging.handlers import RotatingFileHandler


def create_app(config=Config):

    app = Flask(__name__)
    app.config.from_object(config)

    from app.service.add_device_image import add_image_to_device
    from app.service.fetch_inference import get_inference_images
    from app.util.mvie_session import MvieSession
    from app.util.file_util import FileUtil
    from app.main.route import main

    #Blueprints
    app.register_blueprint(main)

    #Create directories
    os.mkdir(app.config["BASE_DIR"] + app.config["FILE_IP_DIR_NAME"]) if not os.path.exists(app.config["BASE_DIR"] + app.config["FILE_IP_DIR_NAME"]) else None
    os.mkdir(app.config["BASE_DIR"] + app.config["PROCESSED_OP_DIR_NAME"]) if not os.path.exists(app.config["BASE_DIR"] + app.config["PROCESSED_OP_DIR_NAME"]) else None
    os.mkdir(app.config["BASE_DIR"] + app.config["INF_UNCTZD_DIR"]) if not os.path.exists(app.config["BASE_DIR"] + app.config["INF_UNCTZD_DIR"]) else None
    os.mkdir(app.config["BASE_DIR"] + app.config["UPLOADED_DIR_NAME"]) if not os.path.exists(app.config["BASE_DIR"] + app.config["UPLOADED_DIR_NAME"]) else None
    os.mkdir(app.config["BASE_DIR"] + app.config["DIR_NAME_FOR_NXT_INF"]) if not os.path.exists(app.config["BASE_DIR"] + app.config["DIR_NAME_FOR_NXT_INF"]) else None
    os.mkdir(app.config["BASE_DIR"] + app.config["OCR_PCSD_DIR"]) if not os.path.exists(app.config["BASE_DIR"] + app.config["OCR_PCSD_DIR"]) else None
    os.mkdir(app.config["BASE_DIR"] + app.config["OCR_UNCTZD_DIR"]) if not os.path.exists(app.config["BASE_DIR"] + app.config["OCR_UNCTZD_DIR"]) else None
    os.mkdir(app.config["LOG_FILE_DIR"]) if not os.path.exists(app.config["LOG_FILE_DIR"]) else None


    #Create CSV file to write inference responses to be processed for ocr
    if not os.path.exists(os.path.join(app.config["BASE_DIR"], 'ocr_inferences.csv')):
        ocr_inference_file = open(os.path.join(app.config["BASE_DIR"], 'ocr_inferences.csv'), 'w+')
        ocr_inference_file.close()

    #Create CSV file to write inference responses to be processed
    if not os.path.exists(os.path.join(app.config["BASE_DIR"], 'inferences.csv')):
        inference_file = open(os.path.join(app.config["BASE_DIR"], 'inferences.csv'), 'w+')
        inference_file.close()    

    init_logger(app)
    mvie_session = MvieSession(app)
    mvie_session.login(app)
    

    with app.app_context():
        app.logger.info('Application Context Startup')

    return app


def init_logger(app):
    file_handler = RotatingFileHandler(os.path.join(app.config['LOG_FILE_DIR'], 'mvi.log'), maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s :: %(levelname)s :: %(funcName)s :: %(relativeCreated)d :: %(message)s [in %(pathname)s:%(funcName)20s():%(lineno)d]'))
    file_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.DEBUG)
    logger = logging.getLogger('mvie')
    logger.setLevel(logging.ERROR)
    app.logger.info('Application Startup')
