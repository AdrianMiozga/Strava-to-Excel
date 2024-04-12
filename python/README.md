## Usage

1. Go to https://www.strava.com/settings/api and create an app. In depth instructions can be found at https://developers.strava.com/docs/getting-started/#account.

2. Create `config.json` with the following template.

```json
{
  "client_id": "<client_id>",
  "client_secret": "<client_secret>"
}
```

3. Run `main.py`.

4. Load data in Excel using `Data` > `From File/CSV`. Example M code can be found in [`query.pq`](query.pq).
