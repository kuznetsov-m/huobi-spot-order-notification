<img src="https://upload.wikimedia.org/wikipedia/commons/d/d8/Huobi-logo.png" height="100" />

# huobi-spot-order-notification
![printscreen](https://user-images.githubusercontent.com/61391551/171191088-60e3fc7b-1197-48f4-a360-799f3f1829c8.png)

The simplest spot order notifications telegram bot

# Configuration
Set next env variables:
- `ACCESS_KEY` and `SECRET_KEY` from your Huobi account
- `TELEGRAM_API_TOKEN` - telegram bot API token
- `TELEGRAM_USER_ID` - telegram notifications reciver user id
optional env variables:
- `SYMBOLS` - list of tracked symbols. Example: `btcusdt,ethusdt`.

# Heroku deployment
Create app and add next buildpacks:
- [Python Poetry Buildpack](https://github.com/moneymeets/python-poetry-buildpack)
- Heroku Python Buildpack
