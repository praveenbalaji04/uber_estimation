from flask import Blueprint, request, jsonify
from core.logics import uber_estimate, here_maps_estimate, schedule_email
from datetime import datetime, timedelta
import pytz


uber = Blueprint('uber', __name__)


@uber.route('/ping')
def ping():
    return jsonify({"status": True})


@uber.route('/estimate')
def estimate():
    '''
    Input:
        source: latitude and longitude Eg- 12.974304,77.653350
        destination: latitude and longitude Eg - 12.970081,77.653693
        time_to_reach: should be in 24 hrs format and hour and minute seperator should be only dot(.), Eg - 16.00
        email: email of the user, who has to receive the notification
    Reseponse:
        success response:
            {
                data: {
                    Email notification time: "15:13:00",
                    Request created time (current time): "14:53:30",
                    Time to reach the destination: "15.30",
                    Total time to reach the place: 17,
                    },
                error: null,
                status: true,
            }
        failure response:
            {
                data: null,
                status: false,
                error: "Its already late, please increase the time_to_reach hours or minutes"
            }
            or 
            {
                data: null,
                status: false,
                error: "No cab nearby to book"
            }
            or incase of missing params
            {
                data: null,
                status: false,
                error: "Please add all the parameters"
            }
    '''

    response = {}
    source = request.args.get('source')
    destination = request.args.get('destination')
    time_to_reach_destination = request.args.get('time_to_reach')  # input_format: HH.MM 24hrs format
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
            response['data'] = None
            response['error'] = "No cab nearby to book"
        else:
            travel_estimation_time = here_maps_estimate(source, destination)
            total_travelling_minutes = travel_estimation_time + uber_estimation_time
            hours, minutes = time_to_reach_destination.split('.')
            now = datetime.now(tz=pytz.timezone("Asia/Kolkata"))
            start_time = datetime(
                year=now.year, month=now.month, day=now.day, hour=int(hours), minute=int(minutes))\
                - timedelta(minutes=total_travelling_minutes)
            if start_time < now:
                response = {
                    'status': False, 'data': None, 'error': 'Its already late, please increase the time_to_reach hours or minutes'}
            else:
                sendgrid_response = schedule_email(start_time.timestamp(), email)
                response_data = {
                    "Request created time (current time)": now.strftime("%X"),
                    "Email notification time": start_time.strftime("%X"),
                    "Total time to reach the place": total_travelling_minutes,
                    "Time to reach the destination": time_to_reach_destination
                }
                response['status'] = sendgrid_response.get('status')
                response['data'] = response_data
                response['error'] = sendgrid_response.get('error')

    return jsonify(response)
