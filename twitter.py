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

nba_team_hashtags = {
    'ATL': '#TrueToAtlanta', 
    'BOS': '#BleedGreen', 
    'BKN': '#BrooklynGrit', 
    'CHA': '#AllFly', 
    'CHI': '#BullsNation', 
    'CLE': '#BeTheFight', 
    'DAL': '#MFFL',  # Mavs Fans For Life
    'DEN': '#MileHighBasketball', 
    'DET': '#DetroitBasketball', 
    'GSW': '#DubNation', 
    'HOU': '#Rockets', 
    'IND': '#Pacers', 
    'LAC': '#ClipperNation', 
    'LAL': '#LakeShow', 
    'MEM': '#GrindCity', 
    'MIA': '#HeatCulture', 
    'MIL': '#FearTheDeer', 
    'MIN': '#RaisedByWolves', 
    'NOP': '#WBD',  # Won't Bow Down
    'NYK': '#NewYorkForever', 
    'OKC': '#ThunderUp', 
    'ORL': '#MagicTogether', 
    'PHI': '#HereTheyCome', 
    'PHX': '#WeAreTheValley', 
    'POR': '#RipCity', 
    'SAC': '#SacramentoProud', 
    'SAS': '#GoSpursGo', 
    'TOR': '#WeTheNorth', 
    'UTA': '#TakeNote', 
    'WAS': '#DCAboveAll'
}

# Upload image to Twitter. Replace 'filename' your image filename.
def postToTwitter(gameImage, caption):
    media_id = api.media_upload(filename=gameImage).media_id_string
    # Text to be Tweeted
    text_parts = [
        f'Final: {caption["Teams"][0]} {caption["Score"][0]}, {caption["Teams"][1]} {caption["Score"][1]}',
        f'{caption['Date']}',
        f'{nba_team_hashtags[caption["Teams"][0]]} // {nba_team_hashtags[caption["Teams"][1]]}',
        f'#{caption["Teams"][0]}vs{caption["Teams"][1]} // #{caption["Teams"][1]}vs{caption["Teams"][0]}',
        '#NBA #NBATwitter'
    ]

    text = '\n'.join(text_parts)
    # Send Tweet with Text and media ID
    client.create_tweet(text=text, media_ids=[media_id])
    tweeted = f'Tweeted! {caption["Teams"][0]} vs {caption["Teams"][1]}'
    print(tweeted)