import os
import json
import requests
import traceback
from flask import Flask, jsonify, request
from elasticsearch import Elasticsearch
from flask_basicauth import BasicAuth
from flask_compress import Compress

app = Flask(__name__)
app.config['SECRET_KEY'] = 'xxxxxxxxxxxxxxxx'

ES_URI = "xxx.xxx.xxx.xxx:9200"

ES_CONFIG = {
    "timeout": 200,
    "max_retries": 5,
    "retry_on_timeout": True,
}

client = Elasticsearch(ES_URI, **ES_CONFIG)

app.config['BASIC_AUTH_USERNAME'] = 'abc'
app.config['BASIC_AUTH_PASSWORD'] = 'xyz@123'

basic_auth = BasicAuth(app)

Compress(app)

fields_to_fetch = {
            'vehicle_missing_data': [
                'DateOfIncidence', 'PhoneNumbers', 'VehicleNumbers', 'AccusedName'
            ],
            'vehicle_data': [
                'VehicleNumber', 'VehicleType', 'VehicleModel', 'OwnerName', 'OwnerAddress', 'RTO'
            ],
            'challan_data': [
                'FullName', 'VehicleNumber', 'NoticeNumber', 'VehicleType', 'VehicleModel', 'Address'
            ],
        }

index_display_name = {'vehicle_data': 'vehicleRegistry'}

def get_display_name(index_name):
    return index_display_name.get(index_name, index_name)

@app.route("/getData/", methods=['POST'])
@basic_auth.required
def getElasticData():
    try:
        payload = request.json

        final_results = {get_display_name(index): [] for index in fields_to_fetch}

        # Common search function
        def search_index(index_name, fields, search_value):
            if not search_value:  # skip if value is empty
                return []

            # search_value_upper = search_value.upper()

            if index_name in fields_to_fetch:
                queries = []
                for field in fields:
                    if field in fields_to_fetch[index_name]:
                        if field in ['VehicleNumbers', 'VehicleNumber']:  # Fields associated with 'vehicle_registry_no'
                            queries.append({"wildcard": {field: f"*{search_value.upper()}*"}})
                            queries.append({"match": {field: search_value.upper()}})
                        else:
                            query = {"match": {field: search_value}}
                            queries.append(query)

                # queries = [{"match": {field: search_value}} for field in fields if field in fields_to_fetch[index_name]]  # this is commented because, want wildcard vehicle searches.
                if queries:
                    es_query = {"_source": fields_to_fetch[index_name], "query": {"bool": {"should": queries}}}
                    # print(json.dumps(es_query, indent=4))  # debug
                    try:
                        es_data = client.search(body=es_query, index=index_name, size=1000)
                        hits = es_data['hits']['hits']
                        return [hit['_source'] for hit in hits]
                    except Elasticsearch.exceptions.RequestError as e:
                        print(f"Error executing Elasticsearch query: {e}")
                        return []
            return []

        mappings = {
            'vehicle_registry_no': ['VehicleNumbers', 'VehicleNumber'],
            'phone_no': ['PhoneNumbers', 'MobileNumber', 'PhoneNumber'],
            'name': ['Name', 'FullName', 'OwnerName'],
            'vehicle_type': ['VehicleType'],
            'vehicle_model': ['VehicleModel'],
            'address': ['FullAddress', 'Address', 'Location']
        }

        # Iterate as per payload and search each item
        for key, value in payload.items():
            fields = mappings.get(key)
            if fields:
                for index_name in fields_to_fetch.keys():
                    results = search_index(index_name, fields, value)
                    if results:
                        display_name = get_display_name(index_name)
                        final_results[display_name] = final_results.get(display_name, []) + results

        return jsonify({'Result': final_results})

    except Exception as e:
        traceback.print_exc()
        return jsonify({'Result': "Please Check Your Query", 'Error': str(e)})


if __name__ == '__main__':
    app.run(host="xxx.xxx.xxx.xxx", port=0000, debug=True)

