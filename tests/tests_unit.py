import unittest
import requests
from flask import json
from task_6.app import Main


class TestOutputType(unittest.TestCase):
    global data, link
    link = "http://127.0.0.1:5000/api/v1/report/json"
    data = requests.get(link)

    def test_output_json(self):
        try:
            json.loads(data.text)
        except ValueError as err:
            print("Your output in xml format")
            return False
        print("Your output in json format")
        return True

def test_client():

    test_json = Main.get(format='json')
    test_xml = Main.get(format='xml')

    with test_json.test_client() as test_client:
        response = test_client.get('/api/v1/report/<format>')
        assert response.status_code == 200

    with test_xml.test_client() as test_client:
        response = test_client.get('/api/v1/report/<format>')
        assert response.status_code == 200


if __name__ == '__main__':
    unittest.main()
