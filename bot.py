from datetime import datetime
import asyncio
from asyncio.events import get_event_loop
import discord
import os
import random
import dotenv
from discord.ext import commands, tasks
import discord.utils
from datetime import datetime
from discord.utils import get
import queue
import time
from collections import deque
import threading
import random

intents = discord.Intents.default()
intents.members = True
melusine = discord.Client(intents=intents)

owner=342596794716258305
supreme=580712675168747541
general= [580712675168747541,448847892631912448,496329386140631041,834837462047260722,543017354062462977,342596794716258305,455227937759821824,595630237761404939,625695398207422504,498516043577163807,593439697800396840,294616663922573312,239685136868835328,334270005384577026]

pesan_semangat = [
    "You probably will lose anyway",
    "This person has no idea what is chess anyway",
    "We don't expect anything from you",
    "Get rekt lmao",
    "You have something better to do than this",
    "Don't embarass yourself",
    "Don't even think to cheat, you will still lose",
    "Have you ever wondered how this kind of confidence is actually dangerous?"
]
listGulag = {}
listExGulag = []

femboiDetector = [
    "femboi",
    "f3mbo1",
    "cowok cantik",
    "cowok sexy",
    "femboy",
    "feminime boy",
    "cowo cantik",
    "cowo seksi",
    "looks female enough"
    "digenjot cwk"
]
antiFemboi = [
    "Disgusting. Period.",
    "Please shut the F up!",
    "https://cdn.discordapp.com/attachments/973278400577937472/973283840443424768/unknown.png",
    "https://cdn.discordapp.com/attachments/973278400577937472/973285395410329661/unknown.png",
    "https://cdn.discordapp.com/attachments/973278400577937472/973287789573578812/unknown.png",
    "I don't know you have such shit taste. Considering blocking."
]

unsent = deque()

@melusine.event
async def on_ready():
    print('We have logged in as {0.user}'.format(melusine))

@melusine.event
async def on_message(message):
    if message.author == melusine.user:
        return
    if (message.content.lower().startswith('daftar chess')):
        role_chess = message.guild.get_role(973202911200964638)
        print('Chess procedure has been initiated')
        await message.author.add_roles(role_chess)
        msg = "Registration Ticket for Chess competition \n Registrant: {} \n Time of Registration {} \n Number of Ticket {} \n Motivational: {}"
        timestamp = datetime.now()
        emb=discord.Embed(title="Chess Participant", description=msg.format(message.author.mention, timestamp.strftime("%m/%d/%Y, %H:%M:%S"), len(role_chess.members), random.choice(pesan_semangat)))
        return await message.channel.send(embed=emb)
    if (message.content.lower().startswith('show chess participant')):
        print("Indexing Chess Participant")
        role_chess = message.guild.get_role(973202911200964638)
        print(len(role_chess.members))
        msg = ""
        i = 0
        for member in role_chess.members:
            i+=1
            msg += str(i) + ". " + member.display_name + "\n"
        if(i == 0):
            msg = "There are no any participant as to date"
        emb=discord.Embed(title="Chess Participant", description=msg)
        return await message.channel.send(embed=emb)

    roleGulag = message.guild.get_role((int(os.getenv('GULAG'))))
    roleGeneral = message.guild.get_role(int(os.getenv('GENERAL')))
    roleSoldier = message.guild.get_role((int(os.getenv('SOLDIER'))))
    roleTahanan = message.guild.get_role((int(os.getenv('TAHANAN'))))

    if (message.author.id == owner) or (message.author.id == supreme):
        if(len(message.mentions)>0 and message.content.lower().startswith('grant ')):
          user = message.mentions[-1]
          channel = melusine.get_channel(806884409004785674)

          if(roleGulag in user.roles):
            await user.remove_roles(roleGulag)
          
          await user.add_roles(roleGeneral)

          msg = "General access has been granted into " + user.mention + ". \nDon't missuse your gifts <:gas:913641013627736094>"
          return await channel.send(msg)
          
    if((message.content.lower().startswith('forcegulag ')) and (roleGeneral in message.author.roles)):
        if(len(message.mentions) > 0):
          user = message.mentions[-1]
          channel = melusine.get_channel(831810540602523648)

          await user.add_roles(roleGulag)
          await user.remove_roles(roleSoldier)
          if (roleGeneral in user.roles):
            await user.remove_roles(roleGeneral)

          msg = "Judgement has been handed down to " + user.mention
          await channel.send(msg)

          await asyncio.sleep(86400)
          msg = "Judgement has been relieved from " + user.mention + "\nNow please behave as you should"
          return await channel.send(msg)

    if((message.content.lower().startswith('forcefree ')) and (roleGeneral in message.author.roles)):
        if(len(message.mentions) > 0):
          user = message.mentions[-1]
          channel = melusine.get_channel(831810540602523648)

          await user.remove_roles(roleGulag)
          if (user.id in general):
            await user.add_roles(roleGeneral)

          msg = "Judgement has been relieved from " + user.mention + "\nBe grateful for the enlightenment"
          return await channel.send(msg)


    if (message.content.lower().startswith('petition ') and (roleSoldier in message.author.roles)):
        print('Gulag petition procedure has been initiated')
        
        if(len(message.mentions) > 0):
          if(message.author in listExGulag):
              msg = "Detention vote to the convicted is rejected because you are still in cooldown period after being expunged to Gulag. Please wait until your session is over."
              await message.reply(msg)
          user = message.mentions[-1]
          if user == melusine.user:
            return
          channel = message.channel
          msg = "Detention vote to the convicted: {}"
          desc = "Suspect: " + user.name + "\nReact <:gas:913641013627736094> to sentence the suspect detention into Gulag"
          emb=discord.Embed(title="Gulag Petition", description=desc)

          await message.delete()
          msg = await channel.send(embed=emb)
          listGulag[msg.id] = user.id
          emoji = discord.utils.get(melusine.emojis, name='gas')
          await msg.add_reaction(emoji)

    if(any(femboiWord in message.content.lower() for femboiWord in femboiDetector)):
        if (random.random() < 20):
            msg = random.choice(antiFemboi)
            return await message.reply(msg, mention_author=False)
        return
    
    if ((message.content.lower().startswith('~reveal')) and (roleGeneral in message.author.roles)):
        channel = message.channel
        if unsent:
          msg = unsent.pop()
          emb=discord.Embed(title="Deleted message by " + msg.author.name, description=msg.content)
        else:
          msg = "There are no unsent message"
          emb=discord.Embed(title="Nothing", description=msg)
        await channel.send(embed=emb)

@melusine.event
async def on_raw_reaction_add(payload):
  if(payload.user_id == melusine.user.id):
    return
  if((payload.message_id in listGulag) & (payload.emoji == discord.utils.get(melusine.emojis, name='gas'))):
    channel = await melusine.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    reaction = discord.utils.get(message.reactions, emoji=payload.emoji)

    server = await melusine.fetch_guild(payload.guild_id)
    roleGulag = message.guild.get_role((int(os.getenv('GULAG'))))
    roleSoldier = message.guild.get_role((int(os.getenv('SOLDIER'))))
    roleGeneral = message.guild.get_role(int(os.getenv('GENERAL')))
    
    msgTime = message.created_at
    now = datetime.utcnow()
    difference = now - msgTime
    total_seconds = difference.total_seconds()

    hour = float(3600)
    counter = 0
    userList = await reaction.users().flatten()
    if total_seconds < hour:
      for person in userList:
        member = await server.fetch_member(person.id)
        if (not roleGulag in member.roles) and (not member.id in listExGulag):
          counter += 1
      if(counter < 7):
        return
      idConvicted = listGulag[payload.message_id]
      user = await server.fetch_member(idConvicted)
      listGulag.pop(payload.message_id)
      listExGulag.add(user.id)
      await user.add_roles(roleGulag)
      if (roleGeneral in user.roles):
        await user.remove_roles(roleGeneral)
      gulagChannel = melusine.get_channel(831810540602523648)
      await message.delete()
      await gulagChannel.send("Suspect " + user.mention + " has been convicted to Gulag Detention. Enjoy your stay!")
      
      await asyncio.sleep(86400)
      msg = "Judgement has been relieved from " + user.mention + "\nNow you can enact your revenge you always wanted all this time"
      await gulagChannel.send(msg)
      await asyncio.sleep(172800)
      listExGulag.remove(user.id)
      return
    else:
      await message.delete(message)
      await channel.send("The petition is no longer in contract")

@melusine.event
async def on_raw_message_delete(payload):
  unsent.append(payload.cached_message)

@melusine.event 
async def on_member_join(member):
    channel = get(member.guild.channels, id=916671843656691722)
    role = get(member.guild.roles, id=858162980180590633)

    desc = "Welcome to the Server, Stranger by the name " + member.mention + "\nPlease wait for 12 hours at max before gaining full access to this server!"
    emb=discord.Embed(title="Welcome Notice", description=desc)
    msg = await channel.send(embed=emb)

    await asyncio.sleep(10)
    if(member.id in general):
        return
    else:
        member.remove_roles(role)

melusine.run('ODM0ODM3NDYyMDQ3MjYwNzIy.YIGs-Q.hg1LxZAHZn2Vws9GCadQJxlO2h0')