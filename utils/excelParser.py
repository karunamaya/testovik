import openpyxl
import requests

def parser():
    wb = openpyxl.load_workbook('excel.xlsx')
    sheet = wb['Sheet1']
    data = []
    url = 'http://127.0.0.1:8000/materials/'
    token = ''
    headers = {'Content-Type': 'application/json'}
    # Iterate over the rows in the sheet
    for row in sheet.iter_rows(values_only=True):
        # Create a dictionary to store the row data

        row_data = {}

        row_data['title'] = row[0]
        row_data['slug'] = row[1]
        row_data['category'] = row[2]
        row_data['cost'] = row[3]
        response = requests.post(url, json=row_data, headers=headers)
        data.append(row_data)
        if token:
            headers['Authorization'] = f'Bearer {token}'
        request_data = {'data': row_data}

        # Make the POST request
    # response = requests.post(url, json=data, headers=headers)

        # Check the response status code
    if response.status_code == 201:
        print('Data written to database successfully!')
    else:
        print('Error writing data to database:', response.text)

