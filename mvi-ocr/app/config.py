
class Config:

    #DIR
    BASE_DIR = ""

    #GENERAL
    ALLOWED_FILE_EXTENSIONS = ['jpg','jpeg', 'png']
    FILE_IP_DIR_NAME = "input/"
    PROCESSED_OP_DIR_NAME = "processed/"
    INF_UNCTZD_DIR = "unindentified/"
    UPLOADED_DIR_NAME = "uploaded/"
    DIR_NAME_FOR_NXT_INF = "ocr/"
    LOG_FILE_DIR = BASE_DIR + "logs/"
    OCR_PCSD_DIR = "ocr_processed/"
    OCR_UNCTZD_DIR = "ocr_uncategorized/"

    #It is recommaned to set this True. If it is set to False, it will expose application to security risk
    SSL_VALIDATION = True

    # List of labels to match with OCR
    OCR_LABELS_TO_MATCH = []

    #MVI Edge
    MVIE_BASE_URL = ''
    MVIE_USERNAME = ''
    MVIE_PASSWORD =  ''
    MVIE_INPUT_SRC_UUID = ''
    MVIE_INSPTN_UUID = ''
    MVIE_ADD_IMG_DVC_URL = MVIE_BASE_URL + '/api/v1/devices/images?uuid='+MVIE_INPUT_SRC_UUID
    MVIE_GET_INF_IMG_URL = MVIE_BASE_URL + '/api/v1/inspections/images/inferences?uuid='+MVIE_INSPTN_UUID
