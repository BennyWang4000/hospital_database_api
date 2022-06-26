
import sys
from email import charset
from flask import Flask, request, jsonify
# import pymssql
import json
import pyodbc
import pandas as pd

# server = '192.168.14.109,1433'
server = '127.0.0.1,1433'
server = 'localhost'
database = 'hospital'
username = 'app'
password = 'nutcadmin'
print("connecting.......")
connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                            server+';DATABASE='+database+';UID='+username+';PWD=' + password + ';Trusted_Connection=no;')
cursor = connection.cursor()

print("connected!")

app = Flask(__name__)


@app.route('/select', methods=['POST'])
def select():
    request_data = request.get_json()
    sql = request_data['query']
    cursor.execute(sql)

    df = pd.DataFrame.from_records(cursor.fetchall(), columns=[
                                   col[0] for col in cursor.description])

    return df.to_json(orient='records')


@app.route('/insert', methods=['POST'])
def insert():
    request_data = request.get_json()
    sql = request_data['query']
    cursor.execute(sql)
    connection.commit()

    return jsonify({'code': 200})


if __name__ == "__main__":
    app.run()
