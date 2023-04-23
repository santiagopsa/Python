import requests
import keys

# Replace these with your own access token and secret


def twitter_look(subject):

    # Build the URL for the search endpoint
    base_url = 'https://api.twitter.com/2/tweets/search/recent'
    params = {
        'query': subject,
        'max_results': 100,
        'expansions': 'author_id',
        'user.fields': 'username',
        'tweet.fields': 'public_metrics',
        'media.fields': 'preview_image_url',
    }
    headers = {
        'Authorization': f'Bearer {keys.twitter_access_token}',
    }

    # Make the request to the search endpoint
    response = requests.get(base_url, params=params, headers=headers)

    # Print the text of each tweet
    cadena_texto=[]
    if response.status_code == 200:
        data = response.json()
        for tweet in data['data']:
            cadena_texto.append(tweet['text'])
        return cadena_texto

    else:
        return cadena_texto
