# Import proprietary Discord module
import discord_bot_client as disc

# Get desired channel to message (via user input)
channel_id = disc.channel()

# Get previous message data (maximum count = 50)
previous_message = disc.previous_messages(count=1, channel_id=channel_id)[0]
previous_message_author_id = previous_message['author']['id']
previous_message_author_name = previous_message['author']['username']
previous_message_content = previous_message['content']

# Mention a user, mentions are formatted using the user's ID
mention = disc.mention(previous_message_author_id)

# Generate some text using a proprietary AI text generation model
joke = disc.generate_text(prompt='tell a joke', max_tokens=100)

# Send message "hi" to a user in the specified channel
disc.send(message=f'hi {mention}, {joke}', channel_id=channel_id)