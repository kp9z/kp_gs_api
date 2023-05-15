# Google Sheets API Package

This package provides a simple interface for interacting with Google Sheets using the Google Sheets API. It allows you to retrieve data from a Google Sheet, update data in a Google Sheet, and append data to a Google Sheet.

## Installation

To install this package, simply run:

```bash
pip install git+https://github.com/kp9z/kp_gs_api
```

## Usage

To use this package, you will need to have a Google Cloud Platform project set up and have created a service account with the appropriate credentials. 

Download 'client_secret.json' from Google API Console and rename them as **'gs_secret.json'**

You will also need to have a Google Sheet that you want to interact with.

```python
from gs_api import GoogleSheetsAPI

# Initialize the GoogleSheetsAPI object with the link to your Google Sheet
sheet_services = GoogleSheetsAPI('https://docs.google.com/spreadsheets/d/your_sheet_id/edit#gid=0')

# Retrieve data from a range in the Google Sheet
input_sheet = 'Sheet1!A1:B10'
data = sheet_services.get_data(input_sheet)

# Update data in a range in the Google Sheet
new_data = [['John', 'Doe'], ['Jane', 'Doe']]
sheet_services.update_data(new_data, 'Sheet1!A11:B12')

# Append data to a range in the Google Sheet
new_data = [['John', 'Doe'], ['Jane', 'Doe']]
sheet_services.append_data(new_data, 'Sheet1!A11:B12')
```
