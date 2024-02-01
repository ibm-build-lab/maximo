import inspect
import logging
import datetime as dt
import math
import requests
import json
from sqlalchemy.sql.sqltypes import TIMESTAMP, VARCHAR
import numpy as np
import pandas as pd

from iotfunctions.base import BaseTransformer
from iotfunctions import ui
import ast
from tabulate import tabulate

logger = logging.getLogger(__name__)

# Specify the URL to your package here.
# This URL must be accessible via pip install.
# Example assumes the repository is private.
# Replace XXXXXX with your personal access token.
# Replace github_username with name of your github username
# Replace gihub_repo_name with name of github repo
# After @ you must specify a branch.
# EXAMPLE: git+https://XXXXXv@github.ibm.com/jatindra-suthar/rtw@main

PACKAGE_URL = 'git+https://XXXXXv@github.ibm.com/github_username/gihub_repo_name@branch_name'


class SendNotificationOnThresholds(BaseTransformer):
    '''
    This function make REST calls to external system when low or high threshold value matches to the input item
    Ensure that only one threshold is configured, either high or low. If a value is configured for high, leave the value for low blank, and vice versa.
    '''


    def __init__(self, input_items, high, low, url, owner, headers, output_items):

        self.input_items = input_items
        self.output_items = output_items
        self.high = high
        self.low = low
        self.url = url
        self.owner = owner
        self.headers = headers
        super().__init__()

    def execute(self, df):
        payload_dict = {
            "_entityType": self._entity_type.name,
            "owner": self.owner,
            "parameter": self.input_items
        }

        print("==========json_payload========")
        print(payload_dict)
        print("==================")

        df_copy = df.copy()
        df_thresholds = pd.DataFrame()
        alert_prefix = "LOW_"

        if self.high is not None:
            df_thresholds = df_copy[df_copy[self.input_items] > float(self.high)]
            alert_prefix = "HIGH_"
        elif self.low is not None:
            df_thresholds = df_copy[df_copy[self.input_items] < float(self.low)]

        df_thresholds[self.output_items] = ''

        print("==========df_thresholds========")
        print(df_thresholds.head(10))

        for index, row in df_thresholds.iterrows():

            try:
                print(self.__dict__.keys())
                payload_dict['alertValue'] = row[self.input_items]
                payload_dict['alertName'] = alert_prefix + self._entity_type.name
                payload_dict['alertTime'] = str(row['EVT_TIMESTAMP'])

                print("Calling http ==================", self.url)
                print("Payload ========", payload_dict)
                print("headers ========", self.headers)
                post_response = requests.post(self.url, json=json.dumps(payload_dict), headers=ast.literal_eval(self.headers))

                print("Response code == ", post_response.status_code)

                if post_response.status_code == 200:
                    df_thresholds.at[index, 'Notification'] = alert_prefix + 'OK'
                else:
                    df_thresholds.at[index, 'Notification'] = alert_prefix + 'NOK'
                print("Calling http Finished==================")

            except Exception as e:
                print(f"An exception occurred: {str(e)}")
                df_thresholds.at[index, self.output_items] = alert_prefix + 'NOK'

        return df_thresholds

    @classmethod
    def build_ui(cls):
        # define arguments that behave as function inputs
        inputs = []
        inputs.append(ui.UISingleItem(
            name='input_items',
            datatype=float,
            description="Data items adjust")
        )
        inputs.append(ui.UISingle(
            name='high',
            description="High Threshold value",
            datatype=float)
        )
        inputs.append(ui.UISingle(
            name='low',
            description="Low Threshold value",
            datatype=float)
        )
        inputs.append(ui.UISingle(
            name='owner',
            description="Username of owner to whom alert should be assigned ",
            datatype=str)
        )
        inputs.append(ui.UISingle(
            name='url',
            description="End point to send notification",
            datatype=str)
        )
        inputs.append(ui.UIParameters(
            name='headers',
            description="Key value pair for headers")
        )

        outputs = [
            ui.UIFunctionOutSingle(name='output_items', datatype=str, description='Notification status')]
        return (inputs, outputs)
