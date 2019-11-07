"""
General function definitions.
"""

import requests
from wordcount.settings import WORDCOUNT_API


def check_spelling(content):
    """
    Given a string of text, return a list of misspelled words checked via Bing Spell Check API.
    The check is case-insensitive.
    Lowercase words that the SC API suggests should be capitalized will not be included in the result.
    List contains single error message when API key is not set or API request was not successful.
    """
    if not WORDCOUNT_API['SPELLCHECK_API_KEY']:
        return ['No API key set for spell checking (SPELLCHECK_API_KEY).']

    words = []

    endpoint = 'https://api.cognitive.microsoft.com/bing/v7.0/SpellCheck'
    data = {
        'text': content
    }
    params = {
        'mkt': 'en-us',
        'mode': 'proof'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Ocp-Apim-Subscription-Key': WORDCOUNT_API['SPELLCHECK_API_KEY'],
    }
    resp = requests.post(endpoint, headers=headers, params=params, data=data)

    if resp.status_code != 200:
        return ['Could not check spelling. Bing Spell Check API returned code %d.' % resp.status_code]

    data = resp.json()

    if 'flaggedTokens' in data:
        for item in data['flaggedTokens']:
            if 'suggestions' in item and item['suggestions'][0]['suggestion'].lower() == item['token']:
                # Ignore capitalization corrections
                continue
            words.append(item['token'])

    return words
