"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")




# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_get_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/members/<member_id>', methods=['GET'])
def handle_individual_member(member_id):
    try:
        member_find = jackson_family.get_member(int(member_id))
        if not member_find or member_find == {}:
            return jsonify({"error": "Member not found"}), 404
        return jsonify(member_find), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/members/<member_id>', methods=['DELETE'])
def handle_delete_individual_member(member_id):
    try:
        deleted = jackson_family.delete_member(int(member_id))
        if not deleted or deleted == {}:
            return jsonify({"error": "Member not found"}), 404
        return jsonify({"done": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/members', methods=['POST'])
def handle_adding_individual_member():
    try:
        body = request.get_json()
        if not body or "first_name" not in body or "age" not in body or "lucky_numbers" not in body:
            return jsonify({"error": "Missing required fields"}), 400
        body["id"] = jackson_family._generate_id()
        body["last_name"] = jackson_family.last_name
        member = jackson_family.add_member(body)
        return jsonify(member), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500






# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
