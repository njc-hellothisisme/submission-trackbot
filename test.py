import os
import discord
from dotenv import load_dotenv
from discord.ext import tasks
import codeforces_api

cf_api = codeforces_api.CodeforcesApi()
print(type(cf_api.user_status("hellothisisme",-1,1)[0].verdict))