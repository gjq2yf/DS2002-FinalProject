from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response, guess_rank

# Step 0: load our token from somewhere safe
load_dotenv()
Token: Final[str] = os.getenv('DISCORD_TOKEN')

# Step 1: BOT SETUP Without intents your bot won't respond
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

# track user responses
user_responses = {}


# Step 2: Message Function
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled ... probably)')
        return
    try:
        if message.author in user_responses:
            await handle_existing_response(message)
        else:
            await handle_new_response(message, user_message)
    except Exception as e:
        print(f'There has been an error: {e}')


# Step 3: Handle user response to previous prompt
async def handle_existing_response(message: Message) -> None:
    correct_answer = user_responses[message.author]['answer']
    # check if user answer matches correct answer
    user_message = message.content.strip()
    if user_message == correct_answer:
        await message.channel.send(f"Correct! It is: \n{correct_answer}")
    else:
        await message.channel.send(f"Wrong! The correct answer was: \n{correct_answer}")
    # delete user responses once session is over
    del user_responses[message.author]


# Step 4: Handle new user response
async def handle_new_response(message: Message, user_message: str) -> None:
    # get response from user
    response, answer = get_response(user_message)
    await message.channel.send(response)
    # if there exists a user response, add it to user_responses to track sessions
    if answer:
        user_responses[message.author] = {'answer': answer}


# Step 5: Handle the startup of the bot
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')


# Step 6: Let's handle the messages
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)


# Step 7: Main Starting point
def main() -> None:
    client.run(Token)


if __name__ == '__main__':
    main()

