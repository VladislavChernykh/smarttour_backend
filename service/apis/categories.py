import logging
from itertools import chain

from flask import Blueprint, jsonify
from google_trans_new import google_translator

from service.apis.locations import get_locations_info

categories = Blueprint("categories", __name__)
logging.basicConfig(filename='std.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level="INFO")


@categories.route("/all", methods=["GET"])
def get_all_categories():
    locations_mock = get_locations_info()
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
    locations_mock = get_locations_info()
    related_tags = [location["tags"] for location in locations_mock if category in location["categories"]]
    tags = related_tags[0] if related_tags else []
    translator = google_translator()
    result = [
        {"label": str(translator.translate(tag.replace("_", " "), lang_src='en', lang_tgt='ru')).strip().capitalize(),
         "alias": tag} for tag in tags
    ]
    return jsonify(result)
