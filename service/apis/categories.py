import logging
from itertools import chain

import requests
from flask import Blueprint, jsonify
from google_trans_new import google_translator

all_locations_info_link = "https://yourtrip.qbank.pro/public/data.php?type=all_objects"
categories = Blueprint("categories", __name__)
logging.basicConfig(filename='std.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level="INFO")


def get_categories_info() -> list:
    info = requests.get(all_locations_info_link)
    return info.json()


@categories.route("/all", methods=["GET"])
def get_all_categories():
    locations_mock = get_categories_info()
    all_categories = [location["categories"] for location in locations_mock]
    unique_categories_en = list(set(chain(*all_categories)))

    translator = google_translator()
    result = [
        {"label": str(translator.translate(category, lang_src='en', lang_tgt='ru')).strip().capitalize(),
         "alias": category}
        for category in unique_categories_en
    ]
    return jsonify(result)


@categories.route("/<path:category>/tags", methods=["GET"])
def get_all_tags_by_category(category):
    locations_mock = get_categories_info()
    related_tags = [location["tags"] for location in locations_mock if category in location["categories"]]
    if related_tags:
        tags = related_tags[0]
    else:
        tags = []
    return jsonify(tags)
