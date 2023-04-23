from google.oauth2 import service_account
from googleapiclient import discovery
import pandas as pd
import numpy as np
import re

class GoogleSheetsAPI:
    def __init__(self, spreadsheet_link) -> None:
        self.service = self._get_service()
        self.sheet_services = self.service.spreadsheets()
        self.spreadsheet_id = self._get_google_sheet_id(spreadsheet_link)
    

    def _get_google_sheet_id(url):
        # regex to get id from google sheet link python
        regex = r"spreadsheets\/d\/(.*?)\/"
        match = re.search(regex, url)
        if match:
            return match.group(1)
        return None


    def _get_service(self):
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        credentials = service_account.Credentials.from_service_account_file('gs_keys.json', scopes=SCOPES)
        service = discovery.build('sheets', 'v4', credentials=credentials)
        return service

    def get_data(self, range, to_dataframe=True):
        """
        Retrieves data from a Google Sheet.

        Parameters:
        range (str): The range of cells to retrieve, e.g. 'Sheet1!A1:B10'.
        to_dataframe (bool): Whether to return the data as a Pandas DataFrame.

        Returns:
        list or pandas.DataFrame: The retrieved data.
        """
        request = self.sheet_services.values().get(spreadsheetId=self.spreadsheet_id, range=range)
        response = request.execute()
        response = response.get('values', [])
        if to_dataframe:
            return self._convert_data_to_df(response)
        return response

    def _convert_data_to_df(self, data, convert_empty_to_nan=True):
        """
        Converts a list of data to a Pandas DataFrame.

        Parameters:
        data (list): The data to convert.
        convert_empty_to_nan (bool): Whether to convert empty cells to NaN.

        Returns:
        pandas.DataFrame: The converted data.
        """
        df = pd.DataFrame(data)
        if convert_empty_to_nan:
            # convert all empty data as NaN 
            df = df.replace(r'^\s*$', np.nan, regex=True)
        header_row = df.iloc[0]
        return pd.DataFrame(df.values[1:], columns=header_row)

    def update_data(self, data, range, from_dataframe=True):
        """
        Updates data in a Google Sheet.

        Parameters:
        data (list or pandas.DataFrame): The data to update.
        range (str): The range of cells to update, e.g. 'Sheet1!A1:B10'.
        from_dataframe (bool): Whether the data is a Pandas DataFrame.

        Returns:
        dict: The response from the API.
        """
        value_input_option = 'USER_ENTERED'
        if from_dataframe:
            data = data.where(pd.notnull(data), None)
            data_list = [data.columns.values.tolist()]
            data = data_list + data.values.tolist()
        value_range_body = {
            'values': data,
        }
        request = self.sheet_services.values().update(spreadsheetId=self.spreadsheet_id, range=range, valueInputOption=value_input_option, body=value_range_body)
        response = request.execute()
        return response

    def append_data(self, data, range):
        """
        Appends data to a Google Sheet.

        Parameters:
        data (list): The data to append.
        range (str): The range of cells to append to, e.g. 'Sheet1!A1:B10'.

        Returns:
        None
        """
        resource = {
            "majorDimension": "ROWS",
            "values": data
        }
        spreadsheetId = self.spreadsheet_id
        self.sheet_services.values().append(
            spreadsheetId=spreadsheetId,
            range=range,
            body=resource,
            valueInputOption="USER_ENTERED"
        ).execute()
