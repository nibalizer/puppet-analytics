
from datetime import datetime

from elasticsearch import Elasticsearch
from flask import Flask

es = Elasticsearch()
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello and welcome to Puppet analytics!"

if __name__ == "__main__":
    app.run()
