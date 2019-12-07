import requests
from datetime import datetime, timedelta


class TestClass:
    def test_001_estimation(self):
        now = datetime.now()
        lapse = now + timedelta(hours=2, minutes=30)
        params = {
            "source": "12.927880,77.627600",
            "destination": "13.035542,77.597100",
            "time_to_reach": "{}.{}".format(lapse.hour, lapse.minute),
            "email": "praveenbalaji04@gmail.com"
        }

        data = requests.get('http://localhost:5000/estimate', params=params)
        response = data.json()
        assert response.get('status') is True
        assert 'Email will be triggered at ' in response.get('data')

    def test_002_low_estimation(self):
        now = datetime.now()
        params = {
            "source": "12.927880,77.627600",
            "destination": "13.035542,77.597100",
            "time_to_reach": "{}.{}".format(now.hour, now.minute + 5),
            "email": "praveenbalaji04@gmail.com"
        }

        data = requests.get('http://localhost:5000/estimate', params=params)
        response = data.json()
        assert response.get('status') is False
        assert response.get('error') == 'Its already late, please increase the time_to_reach hours'
