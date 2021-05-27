from django.test import TestCase
from django.conf import settings
import requests
import json

# Create your tests here.

def ReqData(self, query):
        DADATA_KEY = "d95e7606e5ded1dd1095eb2dc642f7734ce3f55e"
        r = requests.get('https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party?query=' + query,
                         headers={"Content-Type": "application/json; charset=utf-8",
                                  "Accept": "application/json",
                                  "Authorization": "Token " +DADATA_KEY}
                         ).text
        outjson = json.loads(r)
        # print(outjson['suggestions'][0])
        print(outjson['suggestions'][0])
        print(outjson['suggestions'][0]['value'])
        print(outjson['suggestions'][0]['data']['kpp'])
        print(outjson['suggestions'][0]['data']['okpo'])
        print(outjson['suggestions'][0]['data']['ogrn'])
        print("===============================")
        return outjson


    # print(outjson['suggestions'][0]['data']['address']['value'])
    # print(outjson['suggestions'][0]['kpp'])
    # print(outjson['suggestions'][0]['address']['value'])
ReqData("7820300501")
