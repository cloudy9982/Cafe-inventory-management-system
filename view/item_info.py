from flask import jsonify, render_template, request, redirect, url_for, Blueprint
import sqlalchemy as db
from sqlalchemy import func
from datetime import datetime
import math
import pandas as pd
from sqlalchemy.engine import Engine
from sqlalchemy import event
import traceback
import sys


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# sql setting
path_to_db = "./db/back_demo.db"
engine = db.create_engine(f'sqlite:///{path_to_db}')
metadata = db.MetaData()
table_item = db.Table('item', metadata, autoload_with=engine)


item_app = Blueprint('item_app', __name__, url_prefix="/item")


@item_app.route('/', methods=['GET'])
def home():
    if request.method == "GET":
        connection = engine.connect()
        query = db.select(table_item)
        proxy = connection.execute(query)
        results = proxy.fetchall()
        connection.close()
        return jsonify({'item': [dict(row) for row in results]})


@item_app.route('/add', methods=['POST', 'GET'])
def add_item():
    if request.method == "POST":
        try:
            connection = engine.connect()  # connection 要放在view function中，否則會出現thread error
            if request.form['item_name'] and request.form['item_price']:  # 有寫品項名稱和價格
                query = db.insert(table_item).values(
                    name=request.form['item_name'], price=request.form['item_price'])
                connection.execute(query)
                connection.commit()
            else:
                raise Exception
        except Exception as e:
            error_class = e.__class__.__name__  # 取得錯誤類型
            detail = e.args[0] if len(e.args) >= 1 else ""  # 取得詳細內容
            cl, exc, tb = sys.exc_info()  # 取得Call Stack
            lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
            fileName = lastCallStack[0]  # 取得發生的檔案名稱
            lineNum = lastCallStack[1]  # 取得發生的行號
            funcName = lastCallStack[2]  # 取得發生的函數名稱
            errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(
                fileName, lineNum, funcName, error_class, detail)
            print(errMsg)
        finally:
            connection.close()
            return "success"

    if request.method == "GET":
        connection = engine.connect()
        query = db.select(table_item)
        proxy = connection.execute(query)
        results = proxy.fetchall()
        connection.close()
        return jsonify({'item': [dict(row) for row in results]})


@item_app.route('/update', methods=['POST', 'GET'])
def update_item():
    if request.method == "POST":
        try:
            connection = engine.connect()  # connection 要放在view function中，否則會出現thread error
            if request.form['id']:
                query = db.update(table_item).where(table_item.c.id == request.form['id']).values(
                    name=request.form['item_name'], price=request.form['item_price'])  # 寫入品項ＩＤ，即可更改品項名稱、價格
                connection.execute(query)
                connection.commit()
            else:
                raise Exception
        except Exception as e:
            error_class = e.__class__.__name__  # 取得錯誤類型
            detail = e.args[0] if len(e.args) >= 1 else ""  # 取得詳細內容
            cl, exc, tb = sys.exc_info()  # 取得Call Stack
            lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
            fileName = lastCallStack[0]  # 取得發生的檔案名稱
            lineNum = lastCallStack[1]  # 取得發生的行號
            funcName = lastCallStack[2]  # 取得發生的函數名稱
            errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(
                fileName, lineNum, funcName, error_class, detail)
            print(errMsg)
        finally:
            connection.close()
            return "success"

    if request.method == "GET":
        connection = engine.connect()
        query = db.select(table_item)
        proxy = connection.execute(query)
        results = proxy.fetchall()
        connection.close()
        return jsonify({'item': [dict(row) for row in results]})


@item_app.route('/delete', methods=['POST', 'GET'])
def delete_item():
    if request.method == "POST":
        try:
            connection = engine.connect()  # connection 要放在view function中，否則會出現thread error
            if request.form['id']:
                query = db.delete(table_item).where(
                    table_item.c.id == request.form['id'])  # 寫品項ＩＤ，即可delete
                connection.execute(query)
                connection.commit()
            else:
                raise Exception
        except Exception as e:
            error_class = e.__class__.__name__  # 取得錯誤類型
            detail = e.args[0] if len(e.args) >= 1 else ""  # 取得詳細內容
            cl, exc, tb = sys.exc_info()  # 取得Call Stack
            lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
            fileName = lastCallStack[0]  # 取得發生的檔案名稱
            lineNum = lastCallStack[1]  # 取得發生的行號
            funcName = lastCallStack[2]  # 取得發生的函數名稱
            errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(
                fileName, lineNum, funcName, error_class, detail)
            print(errMsg)
        finally:
            connection.close()
            return "delete already"

    if request.method == "GET":
        connection = engine.connect()
        query = db.select(table_item)
        proxy = connection.execute(query)
        results = proxy.fetchall()
        connection.close()
        return jsonify({'item': [dict(row) for row in results]})
