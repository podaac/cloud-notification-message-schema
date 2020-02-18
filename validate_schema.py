import json

myfile = open("cumulus_sns_schema.json",'r')
data = myfile.read()

json.loads(data)
