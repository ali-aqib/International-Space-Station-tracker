import requests
import datetime
import smtplib
import time

MY_EMAIL = ""  # your gmail id
MY_PASSWORD = ""  # your gmail id app password
MY_LAT = 128.704060  # Your latitude
MY_LONG = 177.102493  # Your longitude


def iss_overhead():
    """Return True if ISS is overhead, False otherwise."""
    # Getting ISS position through API
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    # ISS co-ordinates
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True
    else:
        return False


def is_night():
    """Return True if it is night, False otherwise."""
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    
    # Getting sunrise and sunset time of the given co-ordinates through API.
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    # Getting today's time in UTC (only HH)
    time_now = datetime.datetime.now(datetime.UTC).hour

    if sunset <= time_now <= sunrise:
        return True
    else:
        return False


# Send an e-mail when ISS is above the given co-ordinates (MY_LAT, MY_LONG) in night.
while True:
    # Code run with a delay of 60 seconds
    time.sleep(60)
    if iss_overhead() and is_night():
        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=MY_EMAIL,
                                msg="Subject:Look UP\n\nInternational Space Station is up above your head")
