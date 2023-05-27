from random import randrange
import requests
import openai
import json

# Load your API key from an environment variable or secret management service
openai.api_key = "{OPENAI API KEY HERE}"
browser_cookie = "{COOKIE HERE}"

def auth_headers():
    return {
        'authority': 'discord.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': 'OTE2Nzc4MDk2MTk4Mjk1NTUy.GMkh-0.TL-9jOdLseX-nj70x3YDNyk0z5JoEtyD5yqbhs',
        'cookie': browser_cookie,
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"'
    }

# Send a message originating from your Discord account to a channel
def send(message, channel_id):
    payload = {
        'content': message,
        'flags': 0,
        'nonce': randrange(1000000000000000000, 10000000000000000000),
        'tts': False
    }

    res = requests.post(f'https://discord.com/api/v9/channels/{channel_id}/messages', headers=auth_headers(), data=payload)
    return json.loads(res.text)

# Prompt user to input a channel ID
def channel():
    return input('Channel ID: ')

# Retrieve the last N messages from a channel
def previous_messages(count, channel_id):
    res = requests.get(f'https://discord.com/api/v9/channels/{channel_id}/messages?limit={count}', headers=auth_headers())
    return json.loads(res.text)

# Format a user ID into a mention
def mention(user_id):
    return f'<@{user_id}>'

# Generate original text from a prompt using the GPT-3.5 engine
def generate_text(prompt, max_tokens=2000):
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = [
            {'role': 'user', 'content': prompt},
        ],
        max_tokens = max_tokens
    )

    return response.choices[0]['message']['content']
