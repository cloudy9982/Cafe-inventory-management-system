from flask import Flask, render_template, request, redirect, url_for, Blueprint
from flask_moment import Moment
from datetime import datetime
import sqlalchemy as db
from sqlalchemy import func
import math
from view.item_info import item_app

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

moment = Moment(app)
app.register_blueprint(item_app)


@app.route('/')
def index():
    return render_template('index.html',
                           page_header="index",
                           current_time=datetime.utcnow())


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
