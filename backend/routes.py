from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################

@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture["id"] == id:
            return picture
    return {"message": "picture not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.get_json()
    picture_id = picture.get("id", None)  # Use get method to avoid KeyError
    if picture_id is not None:
        for existing_picture in data:
            if existing_picture["id"] == picture_id:
                return jsonify({"Message": f"picture with id {picture_id} already present", "id": picture_id}), 302
        data.append(picture)
        return jsonify({"Message": "Picture created successfully", "id": picture_id}), 201
    else:
        return jsonify({"Message": "No id provided", "id": None}), 400

######################################################################
# UPDATE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture = request.get_json()
    for existing_picture in data:
        if existing_picture["id"] == id:
            existing_picture.update(picture)
            return jsonify({"Message": "Picture updated successfully"}), 200
    return jsonify({"message": "picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    picture_index = next((index for index, picture in enumerate(data) if picture["id"] == id), None)
    if picture_index is not None:
        data.pop(picture_index)
        return "", 204
    return jsonify({"message": "picture not found"}), 404
