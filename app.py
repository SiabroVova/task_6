import sqlite3
from flask import Flask, render_template, json, make_response, request
from task_6.main import print_report, build_report
from flask_restful import Api, Resource
import xml.etree.ElementTree as ET


app = Flask(__name__)
api = Api(app, default_mediatype='application/json')


class Main(Resource):

    def get(self, format):

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Drivers")

        if format == 'json':
            my_json = cursor.fetchall()
            res = json.dumps(my_json, indent=None, sort_keys=False, separators=(", ", ": ")).replace("\n", "")
            return res

        elif format == 'xml':
            data = cursor.fetchall()
            results = ET.Element("results")

            for s in range(0, 19):

                number = ET.SubElement(results, "number")
                abb = ET.SubElement(results, "abb")
                name = ET.SubElement(results, "name")
                car = ET.SubElement(results, "car")
                time = ET.SubElement(results, "time_result")

                number.text = str(s+1)
                abb.text = data[s][1]
                name.text = data[s][2]
                car.text = data[s][3]
                time.text = data[s][4]
            xml_str = ET.tostring(results, encoding='utf-8', method='xml')
            resp = make_response(xml_str)
            resp.headers["content-type"] = "text/xml"
            return resp

        conn.close()

    def post(self):
        req = request.get_json()
        print('req', req)
        return req, 201


api.add_resource(Main, "/api/v1/report/<format>")

@app.route('/')
def index():
    title = "HOME"
    content = "Hello! You are on the Monaco 2018 Race web-report!"
    return render_template("index.html", title=title, content=content)

@app.route('/report')
def gen_report():
    title = "REPORT"
    content = "You are on the page with common report for Monaco 2018 race."
    content2 = print_report(build_report())
    return render_template("index.html", title=title, content=content, content2=content2)

@app.route('/report/<order>')
def order_report(order):
    title = "REPORT with sort"
    content = "You are on the page with common report for Monaco 2018 race. You can sort report by parameter."
    content2 = print_report(build_report(param=order))

    return render_template("index.html", title=title, content=content, content2=content2)

@app.route('/report/drivers')
def driver():
    title = "DRIVERS"
    content = "List of drivers with their codes:"
    dict_for_abb = {}  # dict for names and codes from abbreviations file
    with open("docs/abbreviations.txt", 'r', encoding="utf-8") as f_abb:
        for string in f_abb:
            index_for_cut = string.find('_', 4)
            dict_for_abb.update({string[0:3]: [string[4:index_for_cut]]})
    content2 = dict_for_abb
    return render_template("index_for_drv_list.html", title=title, content=content, content2=content2)

@app.route('/report/<driver_id>')
def report(driver_id):
    title = driver_id
    content = "Here you can see details for separate driver:"
    dict_for_abb = {}  # dict for names and codes from abbreviations file
    with open("docs/abbreviations.txt", 'r', encoding="utf-8") as f_abb:
        for string in f_abb:
            index_for_cut = string.find('_', 4)
            dict_for_abb.update({string[0:3]: [string[4:index_for_cut]]})
    x = dict_for_abb[title][0]
    content2 = print_report(build_report(), name=x)
    return render_template("index.html", title=title, content=content, content2=content2)

@app.route('/report/drivers/<order>')
def order(order):
    title = "DRIVERS with sort"
    content = "List of drivers with their codes sorted accordingly:"
    dict_for_abb = {}  # dict for names and codes from abbreviations file
    with open("docs/abbreviations.txt", 'r', encoding="utf-8") as f_abb:
        for string in f_abb:
            index_for_cut = string.find('_', 4)
            dict_for_abb.update({string[0:3]: [string[4:index_for_cut]]})
    if order == "asc":
        content2 = dict(sorted(dict_for_abb.items(), key=lambda item: item[0]))
    elif order == "desc":
        content2 = dict(sorted(dict_for_abb.items(), key=lambda item: item[0], reverse=True))
    return render_template("index_for_drv_list.html", title=title, content=content, content2=content2)


if __name__ == '__main__':
    app.run(debug=True, port=5000, host="127.0.0.1")
