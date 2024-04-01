import calendar
import json
import webbrowser
from datetime import datetime

from requests_oauthlib import OAuth2Session


def main():
    with open("python/config.json", "r", encoding="UTF-8") as file:
        contents = json.load(file)

        client_id = contents.get("client_id")
        client_secret = contents.get("client_secret")

    # TODO: Implement refreshing token
    oauth = OAuth2Session(
        client_id,
        redirect_uri="https://localhost/exchange_token",
        scope=["read,activity:read_all"],
    )

    authorization_url, _ = oauth.authorization_url(
        "https://www.strava.com/oauth/authorize"
    )

    webbrowser.open(authorization_url)
    authorization_response = input("Enter the full callback URL: ")

    oauth.fetch_token(
        "https://www.strava.com/api/v3/oauth/token",
        authorization_response=authorization_response,
        client_secret=client_secret,
        include_client_id=True,
    )

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

        response = oauth.get(
            "https://www.strava.com/api/v3/athlete/activities",
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
        file.write("Distance\n")
        file.write(str(round(meters / 1000)))

    print(f"Data updated. New distance {round(meters / 1000)} km")


if __name__ == "__main__":
    main()
