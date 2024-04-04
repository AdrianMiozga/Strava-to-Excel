import calendar
import json
import webbrowser
from datetime import datetime

from requests_oauthlib import OAuth2Session

PERSISTENCE_FILE = "python/persistence.json"


def main():
    with open("python/config.json", "r", encoding="UTF-8") as file:
        contents = json.load(file)

        client_id = contents.get("client_id")
        client_secret = contents.get("client_secret")

    token = None

    try:
        with open(PERSISTENCE_FILE, "r", encoding="UTF-8") as file:
            contents = json.load(file)

            token = {
                "access_token": contents.get("access_token"),
                "refresh_token": contents.get("refresh_token"),
                "token_type": "Bearer",
                "expires_in": contents.get("expires_at") - datetime.now().timestamp(),
            }
    except FileNotFoundError:
        pass

    extra = {
        "client_id": client_id,
        "client_secret": client_secret,
    }

    oauth = OAuth2Session(
        client_id,
        token=token,
        redirect_uri="https://localhost/exchange_token",
        auto_refresh_url="https://www.strava.com/api/v3/oauth/token",
        auto_refresh_kwargs=extra,
        scope=["read,activity:read_all"],
        token_updater=token_saver,
    )

    if not token or not token.get("access_token"):
        authorization_url, _ = oauth.authorization_url(
            "https://www.strava.com/oauth/authorize"
        )

        webbrowser.open(authorization_url)

        authorization_response = input("Enter the full callback URL: ")

        token = oauth.fetch_token(
            "https://www.strava.com/api/v3/oauth/token",
            authorization_response=authorization_response,
            client_secret=client_secret,
            include_client_id=True,
        )

        token_saver(token)

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


def token_saver(token):
    with open(PERSISTENCE_FILE, "w", encoding="UTF-8") as file:
        data = {
            "access_token": token.get("access_token"),
            "refresh_token": token.get("refresh_token"),
            "expires_at": token.get("expires_at"),
        }

        json.dump(data, file, indent=2)
        file.write("\n")


if __name__ == "__main__":
    main()
