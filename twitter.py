import tweepy

# Enter API tokens below
consumer_key = 'O5LwpCA9D4GzTumNXn4Vc9B70'
consumer_secret = 'eu6vOsqjPIBFJCHcXLlhrE0jKn8vmuI6Bg6QO8w4xdQ8rHw5Im'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAI1DuwEAAAAAmQNwDJ%2BA6FVfqtRNh6mslwtOCzc%3DGS5u5mpraGbnEwSy5O0q1E2JDmAqtzoD2P0aTuHVOxq66zuu4p'
access_token = '1811860120529154048-HXJ7AicXlFmnvEnp80b79GlbXeALJc'
access_token_secret = 'jjT0Ejtot4pqkQv88pV0GRQA4Pn1FGTaTkA9kwTEpWqDN'

# V1 Twitter API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# V2 Twitter API Authentication
client = tweepy.Client(
    bearer_token,
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret,
    wait_on_rate_limit=True,
)

# Upload image to Twitter. Replace 'filename' your image filename.
def postToTwitter(gameImage):
    media_id = api.media_upload(filename=gameImage).media_id_string
    # Text to be Tweeted
    text = "Hello Twitter!"

    # Send Tweet with Text and media ID
    client.create_tweet(text=text, media_ids=[media_id])
    print("Tweeted!")