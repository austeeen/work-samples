"""
    Badger Vision Service
    Copyright (C) 2020 Badger Technologies
"""
import json
import logging
from flask import Flask
from flask import request
from flask_cors import CORS

from storage.s3_storage import S3Storage
from fmcg_blur import FMCGBlur

app = Flask(__name__)
cors = CORS(app)


def run_blur(request_data):
    logging.debug(request_data)

    image_storage = S3Storage(request_data["storage"][0])
    image_filter = FMCGBlur(request_data["filter_graph"]["properties"])

    image_storage.save_image(image_filter.blur(image_storage.get_image()))

    return {}


@app.route("/badger-vision/api/v1/filter_graphs",  methods=['POST'])
def filter_graphs():
    request_data = json.loads(request.data)
    filter_graph_name = request_data["filter_graph"]["name"]
    if filter_graph_name == "fmcg_blur":
        return run_blur(request_data)
    else:
        message = f"Unsupported filter_graph[{filter_graph_name}]"
        logging.error(message)
        return message, 501


@app.route("/health-check")
def health_check():
    return "GOOD", 200


def setup_logging():
    logging.basicConfig(format="%(asctime)s %(levelname)s [%(module)s::%(funcName)s] %(message)s", level=logging.DEBUG)


if __name__ == "__main__":
    setup_logging()
    logging.info("bv-service start")
    app.run(host="PRIVATE", port=PRIVATE, debug=True)
    logging.info("bv-service exit")
