import os
import discord
from dotenv import load_dotenv
from discord.ext import tasks
import codeforces_api
load_dotenv()
#get token
token = os.getenv("token")
#enable intents
intents = discord.Intents.default()
intents.message_content = True

# sets up client
client = discord.Client(intents=intents)
# sets up cf api access
cf_api = codeforces_api.CodeforcesApi()
# sets up the last submission that is registered; default to first submission registered
last_cf_submission = None
last_ac_submission = None

possible_cf_verdict ={
    "OK": "ACCEPTED",
    "PARTIAL": "PARTIAL CREDIT",
    "COMPILATION_ERROR": "COMPILE ERROR",
    "RUNTIME_ERROR": "RUNTIME ERROR",
    "TIME_LIMIT_EXCEEDED": "TIME LIMIT EXCEEDED",
    "MEMORY_LIMIT_EXCEEDED": "MEMORY LIMIT EXCEEDED",
    "IDLENESS_LIMIT_EXCEEDED": "IDLENESS LIMIT EXCEEDED",
    "WRONG_ANSWER": "WRONG ANSWER"
}
possible_ac_verdict = {
    "AC": "ACCEPTED",
    "CE": "COMPILE ERROR",
    "RE": "RUNTIME ERROR",
    "TLE": "TIME LIMIT EXCEEDED",
    "MLE": "MEMORY LIMIT EXCEEDED",
    "OLE": "OUTPUT LIMIT EXCEEDED",
    "WA": "WRONG ANSWER"
}

def return_latest_cf_submission():
    return cf_api.user_status("hellothisisme",-1,1)[0]

def prep_cf_submission():
    global last_cf_submission
    last_cf_submission = return_latest_cf_submission()

def prep_ac_submission():
    #todo: decipher json bullshit
    pass

@tasks.loop(seconds = 20.0)
async def fetch_cf_submission(message):
    global last_cf_submission
    # fetch a submission and broadcasts it if it is a new submission
    fetched_submission = return_latest_cf_submission()
    if fetched_submission.id == last_cf_submission.id:
        return
    if fetched_submission.verdict in ["","TESTING", "SUBMITTED"]:
        return
    print("New submission registered!")
    await message.channel.send(
        f"""New Codeforces submission recorded with ID {fetched_submission.id}
Problem is {fetched_submission.problem.contest_id}{fetched_submission.problem.index}
Verdict is {possible_cf_verdict.get(fetched_submission.verdict,"FAILED")}
"""
    )
    embed_link = discord.Embed(
        title="View submission here",
        color=discord.Color.blue(), # Or use a hex code like 0x3498db
        url=f"https://codeforces.com/contest/{fetched_submission.problem.contest_id}/submission/{fetched_submission.id}"  # Turns the title into a clickable hyperlink
    )
    await message.channel.send(embed=embed_link)
    last_cf_submission = fetched_submission

@tasks.loop(seconds=20.0)
async def fetch_ac_submission(message):
    #todo: actually implement this
    pass

@client.event
async def on_ready():
    print(f'Bot is ready!')
    prep_cf_submission()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    if message.content.startswith('$init'):
        await message.channel.send('Bot initialised, listening for new submissions...')
        fetch_cf_submission.start(message)
client.run(token)
