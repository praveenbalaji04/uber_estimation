from flask import Blueprint, request, jsonify
from core.logics import uber_estimate, here_maps_estimate, schedule_email
from datetime import datetime, timedelta


uber = Blueprint('uber', __name__)


@uber.route('/ping')
def ping():
    return jsonify({})


@uber.route('/estimate')
def estimate():
    response = {}
    source = request.args.get('source')
    destination = request.args.get('destination')
    time_to_reach_destination = request.args.get('time_to_reach')  # input_format: HH:MM 24hrs format
    email = request.args.get('email')
    if source is None or destination is None or time_to_reach_destination is None or email is None:
        response['status'] = False
        response['error'] = 'Please add all the parameters'
        response['data'] = None
    else:
        longitude, latitude = source.split(',')
        uber_estimation_time = uber_estimate(latitude, longitude)

        if uber_estimation_time == -1:
            response['status'] = False
            response['data'] = {}
            response['error'] = "No cab nearby to book"
        else:
            travel_estimation_time = here_maps_estimate(source, destination)
            total_travelling_minutes = travel_estimation_time + uber_estimation_time
            hours, minutes = time_to_reach_destination.split('.')
            now = datetime.now()
            start_time = datetime(
                year=now.year, month=now.month, day=now.day, hour=int(hours), minute=int(minutes))\
                - timedelta(minutes=total_travelling_minutes)
            if start_time < now:
                response = {
                    'status': False, 'data': None, 'error': 'Its already late, please increase the time_to_reach hours'}
            else:
                response = schedule_email(start_time.timestamp(), email)
    return jsonify(response)
