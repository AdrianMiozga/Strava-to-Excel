import calendar
import json
from datetime import datetime

import requests


def main():
    with open("python/config.json", "r", encoding="UTF-8") as file:
        token = json.load(file).get("token")

    headers = {
        "Authorization": f"Bearer {token}",
    }

    time = datetime(int(datetime.now().strftime("%Y")), 1, 1, 0, 0, 0)
    timestamp = calendar.timegm(time.timetuple())

    page = 1
    meters = 0

    while True:
        params = {
            "after": timestamp,
            "page": page,
            "per_page": 200,
        }

        response = requests.get(
            "https://www.strava.com/api/v3/athlete/activities",
            headers=headers,
            params=params,
            timeout=5,
        )

        if response.status_code != 200:
            print(f"ERROR: HTTP {response.status_code}")
            break

        json_response = response.json()

        if len(json_response) == 0:
            break

        for summary_activity in json_response:
            if summary_activity["type"] == "Ride":
                meters += summary_activity["distance"]

        page += 1

    with open("data.csv", "w", encoding="UTF-8") as file:
        file.write("Przejechane\n")
        file.write(str(round(meters / 1000)))


if __name__ == "__main__":
    main()
