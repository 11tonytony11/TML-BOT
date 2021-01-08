import json
import discord
from discord.ext import commands

message_counter = {'בניית-מפרטים-אישיים': [0, 0], 'המלצות-לציוד-הקפי': [0, 0],
                   'צאט-מחשבים-כללי': [0, 0], "📌general📌": [0, 0]}
# Messages
path = 'a.png'
video_link = ' '
tms_text = ' '

# Frequencies
tms_counter = 140
tml_counter = 225

# Bot constructor
intents = discord.Intents.default()
intents.members = False
Client = commands.Bot(command_prefix='#', intents=intents)


# --------------------------------------------------------------------------


@Client.event
async def on_ready():
    await get_counters()
    print('Bot is online')

# --------------------------------------------------------------------------


@Client.event
async def on_message(message):
    channel = message.channel.name

    """
    low_boundary = datetime.datetime.now().replace(hour=18, minute=0, second=0, microsecond=0)
    high_boundary = datetime.datetime.now().replace(hour=6, minute=0, second=0, microsecond=0)
    if "<@&626993342583930882>" in message.content and datetime.datetime.now() > low_boundary or datetime.datetime.now() 
    < high_boundary:
        await message.delete()
        return
    """

    # Get settings and counters
    await get_settings()

    # If the message is not in the relevant channel
    if channel not in message_counter.keys() or message.author.id == CENSORED:
        return

    # Update the channel counter
    inced_array = [(x + 1) % 250 for x in message_counter[channel]]
    message_counter.update({channel: inced_array})

    # Send message
    await update_and_send(message, channel)


# --------------------------------------------------------------------------


async def update_and_send(message, channel):
    global tml_counter, tms_counter, tms_text, video_link

    # TMS
    if message_counter[channel][0] == tms_counter:
        await message.channel.send(tms_text, file=discord.File(path))
        message_counter[channel][0] = 0

    # TML
    if message_counter[channel][1] == tml_counter:
        await message.channel.send(video_link)
        message_counter[channel][1] = 0

    await update_counters_in_settings()

# --------------------------------------------------------------------------


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


# --------------------------------------------------------------------------


async def get_settings():
    global tms_counter, tml_counter, tms_text, video_link
    channel = Client.get_channel(CENSORED)
    message = await channel.fetch_message(CENSORED)
    data = message.content.split("\n")

    tms_counter = int(data[0])
    tml_counter = int(data[2])

    tms_text = data[1]
    video_link = data[3]


# --------------------------------------------------------------------------


async def update_counters_in_settings():
    # Read current message
    settings_channel = Client.get_channel(CENSORED)
    message = await settings_channel.fetch_message(CENSORED)

    await message.edit(content=json.dumps(message_counter, ensure_ascii=False))


# --------------------------------------------------------------------------

async def get_counters():
    global message_counter

    settings_channel = Client.get_channel(CENSORED)
    message = await settings_channel.fetch_message(CENSORED)

    message_counter = json.loads(message.content)

# --------------------------------------------------------------------------


# Run the client with discord token
Client.run(read_token())


# Developed by Tony Malinkovich for TML
