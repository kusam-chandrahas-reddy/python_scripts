import sys
from colorama import init # type: ignore
from termcolor import colored # type: ignore

text = colored('Hello, World!', on_color='on_yellow')
#text=colored(str(text),'green')
print(text)

import pandas
excelFile="testsoapexcel.xlsx"
data=pandas.read_excel(excelFile)

#print(data.columns)
#print(data.head(1))
#print(data.loc[0,'Service Name'])
#print(data.iloc[1,0]) # row 1 and column 0
x=data.iloc[1]
print(x.iloc[2])

#sys.exit(0)

import json

collection_data = {
    "info": {
        "name": "My Collection",
        "description": "A sample Postman collection created with Python",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    },
    "item": []
}

getrequest = {
    "name": "GET Request Name",
    "request": {
        "method": "GET",
        "url": "https://example.com/data",
        "description": "Fetch data from the server",
    },
    "response": []
}

postrequest = {
    "name": "POST Request Name",
    "request": {
        "method": "POST",
        "url": "https://example.com/data",
        "header": [{"key": "Content-Type", "value": "application/json"}],
        "body": {
            "mode": "raw",
            "raw": json.dumps({"key": "value"})
        },
        "description": "Send data to the server"
    },
    "response": []
}

for i,row in data.iterrows():
    name=str(row.iloc[0])
    headers=str(row.iloc[1])
    url=str(row.iloc[2])
    post_data=str(row.iloc[3])
    postrequest = {
		"name": 'name',
		"request": {
			"method": "POST",
			"url": "https://example.com/data",
			"header": [{"key": "Content-Type", "value": "application/json"}],
			"body": {
				"mode": "raw",
				"raw": json.dumps({"key": "value"})
			},
			"description": "Send data to the server"
		},
		"response": []
	}
    print(row.iloc[0])
    pass
collection_data["item"].append(getrequest)
collection_data["item"].append(postrequest)

json_data = json.dumps(collection_data, indent=2)

#print(json_data)
sys.exit(0)
with open("my_collection.json", "w") as f:
    f.write(json_data)