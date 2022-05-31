# huobi-spot-order-notification
The simplest spot order notifications telegram bot

# Configuration
Set next env variables:
- `ACCESS_KEY` and `SECRET_KEY` from your Huobi account
- `TELEGRAM_API_TOKEN` - telegram bot API token
- `TELEGRAM_USER_ID` - telegram notifications reciver user id

# Heroku deployment
Create app and add next buildpacks:
- [Python Poetry Buildpack](https://github.com/moneymeets/python-poetry-buildpack)
- Heroku Python Buildpack