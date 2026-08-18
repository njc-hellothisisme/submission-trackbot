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
last_submission: codeforces_api.Submission = None

possible_verdict ={
    "OK": "AC",
    "PARTIAL": "PC",
    "COMPILATION_ERROR": "CE",
    "RUNTIME_ERROR": "RTE",
    "TIME_LIMIT_EXCEEDED": "TLE",
    "MEMORY_LIMIT_EXCEEDED": "MLE",
    "IDLENESS_LIMIT_EXCEEDED": "Interactive TLE",
    "WRONG_ANSWER": "WA"
}

@tasks.loop(seconds = 10.0)
async def fetch_submission(message):
    global last_submission
    # fetch a submission and broadcasts it if it is a new submission
    fetched_submission = cf_api.user_status("hellothisisme",-1,1)[0]
    if fetched_submission.id == last_submission.id:
        return
    if fetched_submission.verdict in ["","TESTING", "SUBMITTED"]:
        return
    print("New submission registered!")
    await message.channel.send(
        f"""New submission recorded with ID {fetched_submission.id}
Problem is {fetched_submission.problem.contest_id}{fetched_submission.problem.index}
Verdict is {possible_verdict.get(fetched_submission.verdict,"FAILED")}
Submission can be viewed at codeforces.com/contest/{fetched_submission.problem.contest_id}/submission/{fetched_submission.id}.
"""
    )
    last_submission = fetched_submission

@client.event
async def on_ready():
    print(f'Bot is ready!')
    global last_submission 
    last_submission = cf_api.user_status("hellothisisme",-1,1)[0]

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    if message.content.startswith('$init'):
        await message.channel.send('Bot initialised, listening for new submissions...')
        fetch_submission.start(message)
client.run(token)
