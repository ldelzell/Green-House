import json
import csv
import requests

# url = input("Please enter the IP address of the Flask server [localhost] : ")
# if not url:
# else: 
#     url = url + ":5000/post_data"
url = "http://localhost:5000/post_data"

with open("sendData.csv", 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        response = requests.post(url, json=row)
        if response.status_code != 200 :
            print (response.text)