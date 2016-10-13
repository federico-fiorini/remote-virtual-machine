from app import app, auth
from time import sleep
from external import GoogleComputeEngine
from logic import order_by_location
from flask_restful import reqparse
from flask import make_response, jsonify, request


TO_AVOID_INSTANCES = ['front-end', 'back-end']


@app.route("/list", methods=['POST'])
@auth.login_required
def get_list():

    # Get location name from request
    parser = reqparse.RequestParser()
    parser.add_argument('location', type=str, required=True, help='No location provided', location='json')

    json_data = request.get_json(force=True)
    location = json_data['location']

    # Get list of instances
    google = GoogleComputeEngine()
    instances = google.list_instances()

    # Filter and remove instances to avoid (back-end and front-end)
    instances = [x for x in instances if x['name'] not in TO_AVOID_INSTANCES]

    # Return only name, id and status
    instances = map(lambda x: {'id': x['id'], 'name': x['name'], 'status': x['status']}, instances)

    # Sort by location
    instances = order_by_location(instances, location)

    return make_response(jsonify({'status': 'SUCCESS', 'instances': instances}))


@app.route("/get/<string:instance_name>", methods=['GET'])
@auth.login_required
def get(instance_name):

    # Get instance
    google = GoogleComputeEngine()
    try:
        instance = google.get_instance(instance_name)
    except:
        return make_response(jsonify({'status': 'NOT FOUND'}), 404)

    # Get IP address
    ip_address = instance['networkInterfaces'][0]['accessConfigs'][0]['natIP']\
        if instance['status'] == 'RUNNING'\
        else None

    response_content = {
        "status": instance['status'],
        "IP-address": ip_address
    }

    return make_response(jsonify(response_content))


@app.route("/start", methods=['POST'])
@auth.login_required
def start():

    # Get instance name from request
    parser = reqparse.RequestParser()
    parser.add_argument('instanceName', type=str, required=True, help='No VM instance name provided', location='json')
    args = parser.parse_args()
    instance_name = args['instanceName']

    # Get instance
    google = GoogleComputeEngine()
    try:
        instance = google.get_instance(instance_name)
    except:
        return make_response(jsonify({'status': 'NOT FOUND'}), 404)

    # If RUNNING already, return IP address
    if instance['status'] == 'RUNNING':
        response_content = {
            "status": "SUCCESS",
            "IP-address": instance['networkInterfaces'][0]['accessConfigs'][0]['natIP']
        }

        return make_response(jsonify(response_content))

    # Otherwise start
    response = google.start_instance(instance_name)

    # Check status until it's running
    while response['status'] != 'RUNNING':
        sleep(2)
        response = google.get_instance(instance_name)

    response_content = {
        "status": "SUCCESS",
        "IP-address": response['networkInterfaces'][0]['accessConfigs'][0]['natIP']
    }

    return make_response(jsonify(response_content))


@app.route("/stop", methods=['POST'])
@auth.login_required
def stop():

    # Get instance name from request
    parser = reqparse.RequestParser()
    parser.add_argument('instanceName', type=str, required=True, help='No VM instance name provided', location='json')
    args = parser.parse_args()
    instance_name = args['instanceName']

    # Get instance
    google = GoogleComputeEngine()
    try:
        instance = google.get_instance(instance_name)
    except:
        return make_response(jsonify({'status': 'NOT FOUND'}), 404)

    # If TERMINATED already, return success
    if instance['status'] == 'TERMINATED':
        return make_response(jsonify({"status": "SUCCESS"}))

    # Otherwise stop
    response = google.stop_instance(instance_name)

    # Check status until it's running
    while response['status'] != 'TERMINATED':
        sleep(2)
        response = google.get_instance(instance_name)

    return make_response(jsonify({"status": "SUCCESS"}))
