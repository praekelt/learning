import twitter


api = twitter.Api(
    consumer_key="YD0vDi8LB7t5qkRJzyTVBWcMy",
    consumer_secret="EO1xpfWnsuGs4lSDbQZuzMtg04lfXiuyfVq0BsoO4jhw9SwvuX",
    access_token_key="33611922-VmfZWt0JnxBLEbJFXnQq7UWjOBmly3N8TVvGWmXYs",
    access_token_secret="BNWg7t51I3JZN3C0l7tOIwrsGwcsRLHmiA93tGRXMcCbN"
)
statuses = api.GetUserTimeline(screen_name="hedleyroos")
print(statuses[1].text)
