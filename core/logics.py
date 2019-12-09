import requests
from config import Config
from datetime import datetime


def uber_estimate(latitude='77.627600', longitude='12.927880'):
    # returns estimation time of uberGO
    uber_url = (
        "https://rr1iky5f5f.execute-api.us-east-1.amazonaws.com/api/estimate/time?start_longitude={}&start_latitude={}".format(longitude, latitude))
    response = requests.get(uber_url)
    estimate = 0
    data = response.json()
    for time in data.get('times'):
        if time.get('display_name') == 'uberGO':
            estimate = int(time.get('estimate')) / 60
    return int(estimate)


def here_maps_estimate(source, destination):
    # Alternative for google maps, returns the estimation time of travel from source to destination
    url = ("https://route.api.here.com/routing/7.2/calculateroute.json?app_id={}&app_code={}&waypoint0=geo!{}&waypoint1=geo!{}&mode=fastest;car;traffic:disabled".format(
        Config.HERE_MAPS_API_ID, Config.HERE_MAPS_APP_KEY, source, destination))
    response = requests.get(url)
    data = response.json()
    travel_time_estimation = int(data.get('response').get("route")[0].get("summary").get('baseTime') / 60)
    return travel_time_estimation


def schedule_email(timestamp, email):
    """
    Input
        timestamp: Exact time to send the notification email
        email: User email
    """

    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail
    response = {}

    message = Mail(
        from_email='noreply@almabase.com',
        to_emails=email,
        subject='Book Uber',
        html_content='<strong>Time to book an Uber</strong>')
    if datetime.now().timestamp() > timestamp:
        raise KeyboardInterrupt
    message.send_at = int(timestamp)
    try:
        sg = SendGridAPIClient(Config.SENDGRID_API_KEY)
        sg.send(message)
        response['status'] = True
        response['data'] = 'Email will be triggered at {}'.format(datetime.fromtimestamp(timestamp))
        response['error'] = None
    except Exception:
        response['status'] = False
        response['error'] = 'Error in sending email'
        response['data'] = None
    return response
