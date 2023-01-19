import requests
import json
import os

class MvieSession:

    _token_file_path = None
    _logger = None

    def __init__(self):
        print('Class init')

    def __init__(self, app):
        self._token_file_path = os.path.join(app.config['BASE_DIR'], 'token.json')
        self._logger = app.logger

    def login(self, app):
        self._logger.info('Logging to MVIE')

        login_url = app.config['MVIE_BASE_URL'] + '/api/v1/users/sessions'
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        data = {
            "grant_type": "password",
            "password": app.config['MVIE_PASSWORD'],
            "username": app.config['MVIE_USERNAME']
        }

        response = requests.post(login_url, headers=headers, verify=True, json=data)

        if response.status_code == 200:
            response_data = response.json()
            app.logger.debug('Login response %s : ' + str(response_data))
            if response_data['token']:
                self.update_token(response_data['token'])
        else:
            app.logger.error('Can not login')


    def load_token_file(self):
        data = {}
        if os.path.exists(self._token_file_path):
            self._logger.info('Reading token file')
            token_file = open(self._token_file_path, 'r')
            data = json.load(token_file)
            token_file.close()
            return data
        return data


    def update_token(self, token):
        data = self.load_token_file()

        self._logger.info('Updating Token')
        data['token'] = token
        token_file = open(self._token_file_path, 'w')
        json.dump(data, token_file)
        token_file.close()
        self._logger.info('Token Updated')

    def get_token(self):
        data = self.load_token_file()
        return data['token'] if data['token'] else None

    def update_max_image_id(self, image_id):
        data = self.load_token_file()

        self._logger.info('Updating last fetched image id')
        data['maxImageId'] = image_id
        token_file = open(self._token_file_path, 'w')
        json.dump(data, token_file)
        token_file.close()
        self._logger.info('Image Id updated')

    def get_max_image_id(self):
        data = self.load_token_file()
        if 'maxImageId' in data:
            return data['maxImageId']
        return None
