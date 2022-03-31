import gevent.monkey
gevent.monkey.patch_all()

import discord
from discord import Embed
import os
import requests
import random
from datetime import datetime
from discord.ext import *
from replit import db
from keep_alive import keep_alive
from discord_components import *
from tabulate import tabulate
import csv
import pandas as pd
import time
import threading 
import math
import json

#######################################################################################
#LONG LIVE ARADENA
#######################################################################################

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

DiscordComponents(client)
data = [['name','health','stamina','move','mythical','cooldown','time','main','id','stringtext']]
#eventRanges
b1,b2 = 150, 165 #god charge
e1,e2 = 1,9 #boost
f1,f2 = 20,29 #spatial
g1,g2 = 50,57 #morath
h1,h2 = 60,72 #stun
i1,i2 = 72,76 #bribes
j1,j2 = 80,87 #forest
o1,o2 = 90,95 #ravine
k1,k2 = 96,100 #desert
l1,l2 = 105,112 #gravity
n1,n2 = 120,127 #meta

global godChargeDuration
godChargeDuration = 0
global godChargeName 
godChargeName = ""

df = pd.DataFrame(data)
df.to_csv("healthStamina.csv",index = False, header=False)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  channel = client.get_channel(933312223982542919)
  await channel.send("News 📯:")
  print("I have returned to Aradena!")
        
@client.event
async def on_message(message):

  msg = message.content
  args = message.content.split()
  action_victory = ActionRow(Button(label="Now go forth and adventure!🐲", custom_id="victory",disabled=True))
  descriptionTavern = "The battle is upon us, may the crowd be entertained!" #variables placed here for testing declaration
  finalPhrase = "The crowd is overjoyed 📯! Look at this bloodbath!"

  if ((msg == 'killcommand') and (message.author.name == 'cyanark43') and (message.author.discriminator == '9761')):
    print(message.author.name,'#',message.author.discriminator)
    print(message.author.id)
    await message.channel.send('`Uploading data to metaverse: Activiating Pyranus Protocol Delta 6`')
    os.system("kill 1") # Are you sure this process is always process 1

  if (msg == "testingcyanark"):
    shufflelist()
    sortRaceLeaderboard()
    await message.reply("Shuffled")

  if ((msg.count(" ") > 1) and (message.channel.id == 898770246662488164)):
    await message.delete()

  if (((msg.startswith('horse booster')) or (msg.startswith('Horse booster'))) and (message.channel.id == 898770246662488164)): 
    channel = client.get_channel(898770246662488164)
    server = client.get_guild(864511755504713789)
    role = server.get_role(867868403082330162)
    await channel.set_permissions(role, send_messages = False)
    await message.reply("You have guessed wisely - the King tells you of a shortcut in the next race, you can already smell victory!")

  if ((message.channel.id == 883377238114963506)):
    emoji = '🔥'
    await message.add_reaction(emoji)
    if (msg[41] != 0):
      emoji = '<:crown1:892258939805241385>'
      await message.add_reaction(emoji)

  if ((msg == '$allocateOG') and (message.author.name == 'cyanark43') and (message.author.discriminator == '9761')): 
    server = client.get_guild(864511755504713789)
    memberlist = await server.fetch_members(limit=50).flatten()
    for x in memberlist: 
      print(x.name,":",x.id)

  if ((msg == '$join')):
    author = message.author.name
    if (joinrace(author)):
      await message.reply("You have joined the race {}!".format(author))
    else:
      await message.reply("You are already entered in the race **{}**!".format(author))
    #sortrace()

  if ((msg == '$rleaderboard') and (message.author.name == 'cyanark43') and (message.author.discriminator == '9761')) or ((msg == '$rleaderboard') and (message.author.name == 'Marcius of Irium') and (message.author.discriminator == '6735')):
    embedL = discord.Embed(color=0x993723)
    embedL.set_thumbnail(url="https://i.imgur.com/FScjpsR.jpg") #"https://i.imgur.com/Qtmmvio.png" 
    output = "```" + tabulate(getTopTenMRL(), headers="keys", stralign="left", numalign = "center", showindex=True, tablefmt='github') + "```"
    embedL.add_field(name="The Aradenean Race: Top Racers 🏆", value = output, inline = False) 
    await message.channel.send(embed=embedL, components=[])

  if ((msg == '$compete') and (message.author.name == 'cyanark43') and (message.author.discriminator == '9761')) or ((msg == '$compete') and (message.author.name == 'Marcius of Irium') and (message.author.discriminator == '6735')):
    shufflelist()
    df = pd.read_csv("race.csv")
    datastorer = pd.read_csv("race.csv")
    players,i,line,caseValue = len(df),0,0,0

    if (players > 25):
      timelength = 45
    else: 
      timelength = round(float(players))*2

    lineR,lineL,racerName,racerPosition = "","","",racepositions()

    embedCompete = discord.Embed(color=0xeab99a, title="The Great Aradenean Race 🏛️")
    embedCompete.set_thumbnail(url="https://i.imgur.com/WyZlDHF.png")
    embedCompete.add_field(name="Racer Name: ", value="TBD",inline=True)
    embedCompete.set_footer(text="A race every day brought to you by the Royal Council! \n 📯|🏇{}|🏁".format(lineR))
    embedEdited = await message.channel.send(embed=embedCompete, components=[])

    while (i < timelength):
      lineR += "-"
      i += 1

    textValue = ("`" + str(players) + ' knights on valiant steeds will race for the glory of Aradena!' + "`")
    await message.channel.send(textValue)
    time.sleep(0.3)

    for timer in range(1, (timelength + 1)):
      lineL += "-"
      if lineR.startswith("-"):
        lineR = lineR.replace("-", '', 1)

      while timer <= timelength: #while loop to break print for final loop
        new_embed = embedCompete
        caseValue = random.randint(1,265)

        if ((timer >= timelength-1) or (timer <= 2)):
          caseValue = 420

        print("Case value:",caseValue)
        group = randomGroup(caseValue)
        eventString = incrementracevalue(caseValue,group)
        datastorer = getTopTenMR(timer,timelength)
        
        racerName = ("```" + tabulate(datastorer, headers="keys", stralign="left", numalign = "center", showindex=True, tablefmt='github') + "```") 
        new_embed.set_field_at(0, name="♞-Race Standings-♞", value=racerName, inline=True)
        new_embed.set_footer(text="A race every day brought to you by the Royal Council! \n {} \n 📯|{}🏇{}|🏁".format(eventString, lineL, lineR))

        await embedEdited.edit(embed=new_embed)
        if (len(eventString) > 2):
          if "spatial" in eventString:
            time.sleep(1.6)
          time.sleep(2)

        if (timer<timelength):
          time.sleep(1.4)

        eventExecute(caseValue,group)
        line += 1
        break

    applyScores(datastorer)
    df = pd.read_csv("race.csv")
    await message.channel.send('Congratulations! The fastest knight in the realm is from the great guild of **{}** 🏇🏆'.format(df.at[0,'name']))
    resetrace()
            
  # if ((msg != '$leaderboard') and (msg != ('$mleaderboard')) and (msg.startswith('$battle') == False) and ((msg !=('$completelb')))):
  #   if ((message.author != client.user)):
  #     time.sleep(0.25)
  #     print ("Improper Message Deleted")
  #     await message.delete()
  #   return

  if (msg.startswith('$leaderboard')):
    embedL = discord.Embed(color=0x993723)
    embedL.set_thumbnail(url="https://i.imgur.com/86ixKlt.png") #"https://i.imgur.com/Qtmmvio.png" 
    output = "```" + tabulate(getTopTen(message.author.name), headers="keys", stralign="left", numalign = "center", showindex=False, tablefmt='github') + "```"
    embedL.add_field(name="The Colosseum: Top 10 🏆", value = output, inline = False) 
    await message.channel.send(embed=embedL, components=[])
    print(getTopTen(message.author.name))

  if (msg.startswith('$m')):
    searchString = msg.replace('$m','') #clear leading 0s - 0080 = 80 
    searchString = searchString.lstrip('0')
    if(searchString == ('')):
      searchString = '0'
    intSearchString = int(searchString)
    if ((intSearchString > 7999) or (intSearchString < 0)):
      await message.reply("Invalid Warrior ID requested!")
    else: 
      urlString = 'https://images.aradena.io/tokens/1/large/{}.png'.format(searchString)
      dataString = 'https://api.aradena.io/tokens/{}'.format(searchString)
      tempString = requests.get(dataString)
      res = json.loads(tempString.text)
      totalStat,colorE = 0,0x87CEFA
      stat_list = [0]*5

      classString = (str((res['attributes'][7]['value']))).lower() 
      if (classString == "heroic"):
        colorE = 0x8A2BE2
      elif (classString == "legendary"):
        colorE = 0xF0E68C

      for i in range(8,13):
        totalStat += int((res['attributes'][i]['value']))
        stat_list[i-8] = int((res['attributes'][i]['value']))
        print(res['attributes'][i]['value'])
      print("Total Stats:", totalStat)  

      embedS = discord.Embed(color=colorE, title = ("Warrior #{}".format(searchString)), url="https://opensea.io/assets/0xef9c21e3ba31a74910fc7e7cb3fc814ad842ad6e/{}".format(searchString))
      embedS.add_field(name="Stats of this {} warrior:".format(classString), value = "```" +"ATT: "+str(stat_list[0])+" | DEF: "+ str(stat_list[1])+" | MAG: " + str(stat_list[2]) + "\nAGI: " + str(stat_list[3]) + " | INT: "+str(stat_list[4])+ " | TOTAL: "+str(totalStat)+"🍻```",inline=False)
      embedS.set_image(url=urlString) 
      await message.channel.send(embed=embedS)

  if (msg.startswith('$f')):
    searchString = msg.replace('$f','') #clear leading 0s - 0080 = 80 
    searchString = searchString.lstrip('0')
    if(searchString == ('')):
      searchString = '0'
    intSearchString = int(searchString)
    if ((intSearchString > 5199) or (intSearchString < 0)):
      await message.reply("Invalid Warrior ID requested!")
    else: 
      urlString = 'https://images.aradena.io/tokens/2/large/{}.png'.format(searchString)
      dataString = 'https://api.aradena.io/tokens/2/{}'.format(searchString)
      tempString = requests.get(dataString)
      res = json.loads(tempString.text)
      totalStat,colorE = 0,0x87CEFA
      stat_list = [0]*5

      classString = (str((res['attributes'][7]['value']))).lower() 
      if (classString == "heroic"):
        colorE = 0x8A2BE2
      elif (classString == "legendary"):
        colorE = 0xF0E68C

      for i in range(8,13):
        totalStat += int((res['attributes'][i]['value']))
        stat_list[i-8] = int((res['attributes'][i]['value']))
        print(res['attributes'][i]['value'])
      print("Total Stats:", totalStat)  

      embedS = discord.Embed(color=colorE, title = ("Warrior #{}".format(searchString)), url="https://opensea.io/assets/0x3d74450d135f16b6fa20c1211c6faef93ee73d7c/{}".format(searchString))
      embedS.add_field(name="Stats of this {} warrior:".format(classString), value = "```" +"ATT: "+str(stat_list[0])+" | DEF: "+ str(stat_list[1])+" | MAG: " + str(stat_list[2]) + "\nAGI: " + str(stat_list[3]) + " | INT: "+str(stat_list[4])+ " | TOTAL: "+str(totalStat)+"🍻```",inline=False)
      embedS.set_image(url=urlString) 
      await message.channel.send(embed=embedS)

  if (msg.startswith('$mleaderboard')):
    embedL = discord.Embed(color=0x993723)
    embedL.set_thumbnail(url="https://i.imgur.com/86ixKlt.png") #"https://i.imgur.com/Qtmmvio.png" 
    output = "```" + tabulate(getTopTenM(message.author.name), headers="keys", stralign="left", numalign = "center", showindex=False, tablefmt='github') + "```"
    embedL.add_field(name="The Colosseum: Top 10 🏆", value = output, inline = False) 
    await message.channel.send(embed=embedL, components=[])
    print(getTopTen(message.author.name))

  if (msg == '!moon'):
    embedL = discord.Embed(color=0x993723, title="A wizard descends from the skies")
    embedL.set_author(name="Warriors of Aradena",icon_url="https://imgur.com/PPzYRXX.png")
    embedL.add_field(name="and he proclaims...", value = "soon young warrior, soon🌙", inline = False) 
    await message.channel.send(embed=embedL, components=[])
    print("moon")

  if (msg == '!lambo'):
    embedL = discord.Embed(color=0x993723, title="You call the name of a rare stallion")
    embedL.set_author(name="Warriors of Aradena",icon_url="https://imgur.com/PPzYRXX.png")
    embedL.add_field(name="Only the wealthiest merchants can afford one,", value = "However, a prophecy says you will have many one day!🏆", inline = False) 
    await message.channel.send(embed=embedL, components=[])
    print("lambo")

  # if (msg == '!wen'):
  #   await message.reply(content = "One scroll has been unveiled yells the wizard, word of free steaks (*wizard might have had some of Tom's tankard*)! He prophesizes the next two scrolls could be are coming soon! Tom, as drunk as ever, says it must be on <t:{}>!".format(random.randint(-20*round(time.time()), 20*round(time.time()))))
    #"**Soon** says a wise Wizard. However, Tom the Drunk, after his thirtieth tankard, proclaims the date will be when the dragons arrive, around <t:{}>!".format(random.randint(-20*round(time.time()), 20*round(time.time()))))
    #print("wen")

  if (msg.startswith('$completelb')):
    embedL = discord.Embed(color=0x993723)
    output = "```" + tabulate(getFullList(0, 9), headers="keys", stralign="left", numalign = "center", showindex=False, tablefmt='github') + "```"
    embedL.add_field(name="The Colosseum: Top 10 🏆", value = output, inline = False) 

    output2 = "```" + tabulate(getFullList(9,19), headers="keys", stralign="left", numalign = "center", showindex=False, tablefmt='github') + "```"
    embedL.add_field(name="Competing for Glory", value = output2, inline = False) 

    output3 = "```" + tabulate(getFullList(19,29), headers="keys", stralign="left", numalign = "center", showindex=False, tablefmt='github') + "```"
    embedL.add_field(name="Not Forgotten", value = output3, inline = False)

    await message.channel.send(embed=embedL, components=[])
    
  if (msg.startswith('$battle')):
    #if(not onlyOne()):
    #  await message.reply("⚠️Temporary: Only one fight allowed in the tavern!")
    #  return
    if(len(message.mentions) == 0):
      await message.reply("You have to fight someone, otherwise what's the point of a battle?")
      return

    elif(len(args) != 2):
      await message.reply('No group fights, only tag one brave lad! Sir {}'.format(message.author.name))
      return
    
    elif(message.mentions[0].bot == True):
      await message.reply("Stop fighting the Colosseum workers!")
      return
      
    playerMain = message.author.name
    playerOpp = message.mentions[0].name

    if((findHealth(playerMain) is not None) and (findHealth(playerOpp) is not None)):
      await message.reply(content = "Stop trying to join someone else's battle {}!".format(message.author.mention))
      endFight = True
      print("test1")
      return

    if(findHealth(playerMain) is not None):
      await message.reply(content = "Stop trying to fight the whole arena {}!".format(message.author.mention))
      endfight = True 
      print("test2")
      return

    if(findHealth(playerOpp) is not None):
      await message.reply(content = "Stop trying to join someone else's battle {}!".format(message.author.mention))
      endFight = True
      print("test3")
      return

    if(message.mentions[0].id == client.user.id):
      await message.reply("The Colosseum always wins!")
      return
    
    if(message.mentions[0].id == message.author.id):
      await message.reply("Quit punching yourself!")
      return

    gamesTotal()
    createPlayer(playerMain)
    createPlayer(playerOpp)
    createPlayerLeaderboard(playerMain)
    createPlayerLeaderboard(playerOpp)
    ###########
    
    updateRole(playerMain, 1)
    updateRole(playerOpp, 0)
    updateString(playerMain, descriptionTavern)
    ###########

    resetPlayer(playerMain)
    resetPlayer(playerOpp)
    battleId = (findbattleId())
    ###########

    action_row = ActionRow([
    Button(label="Grab", custom_id= "grab"+str(battleId)), 
    Button(label="Punch",style=ButtonStyle.blue, custom_id="punch"+str(battleId)),
    Button(label="Kick",style=ButtonStyle.red, custom_id="kick"+str(battleId)),
    Button(label="Block",style=ButtonStyle.green, custom_id="block"+str(battleId)),
    Button(label="Flee Colosseum?", custom_id="Flee Colosseum?"+str(battleId))], [Button(label="<Mythical Powerup🔥>", custom_id= "mythical"+str(battleId))] )

    #action_row2 = ActionRow([Button(label="Mythical Powerup", custom_id= "mythical"+str(battleId))])

    moveMain = "📜"
    moveOpp = "📜"
  
    (globals()[(playerMain+"Battle")]) = discord.Embed(color=0xeab99a, title="The Colosseum 🏛️")
    (globals()[(playerMain+"Battle")]).set_thumbnail(url="https://i.imgur.com/OYnHQiy.jpg") #https://i.imgur.com/0f0nAHt.png #https://i.imgur.com/BhScmnc.png https://imgur.com/6sZJy3R.png
    (globals()[(playerMain+"Battle")]).add_field(name=playerMain+moveMain, value="Health: {}  ❤️\n Stamina: {}  ⚡".format(findHealth(playerMain), findStamina(playerMain)), inline=True)
    (globals()[(playerMain+"Battle")]).add_field(name="vs.", value="⚔️", inline=True)
    (globals()[(playerMain+"Battle")]).add_field(name=playerOpp+moveOpp, value="Health: {}  ❤️\n Stamina: {}  ⚡".format(findHealth(playerOpp), findStamina(playerOpp)), inline=True)
    (globals()[(playerMain+"Battle")]).set_footer(text = descriptionTavern)

    #print(cyanark43Battle)
    print(globals()[(playerMain+"Battle")])

    await message.channel.send(embed=(globals()[(playerMain+"Battle")]), components=(action_row))

    embedVictory = discord.Embed(color=0x993723)
    embedVictory.set_author(name="Warriors of Aradena",icon_url="https://imgur.com/PPzYRXX.png") #"https://imgur.com/PPzYRXX.png"
    embedVictory.set_thumbnail(url="https://i.imgur.com/6tnpdBU.png") #"https://imgur.com/6sZJy3R.png")
    embedVictory.add_field(name="-", value="-", inline=True) 

    print("Battle between: ",playerMain," and ", playerOpp)

###################################################

    @client.event
    async def on_button_click(interaction):
      random.seed(datetime.now())

      if (("mythical"+str(findID(interaction.user.name))) == (interaction.custom_id)):
        if (findCooldown(interaction.user.name) >= 3) and (findMythical(interaction.user.name) == 0):
          updateMythical((interaction.user.name),1)
          await interaction.respond(content = "Mythical attack enabled😤", ephemeral=True)

        elif (findCooldown(interaction.user.name) >= 3) and (findMythical(interaction.user.name) == 1):
          updateMythical((interaction.user.name),0)
          await interaction.respond(content = "Mythical attack disabled, but remains ready!", ephemeral=True)
          
        else:
          turnsPending = 0
          if (findCooldown(interaction.user.name) < 3):
            turnsPending = (3 - findCooldown(interaction.user.name))
          await interaction.respond(content = "Mythical attack charging up. Turns remaining: {}".format(turnsPending), ephemeral=True)


      if ( ("grab"+str(findID(interaction.user.name))) == (interaction.custom_id) or ("punch"+str(findID(interaction.user.name))) == (interaction.custom_id) or ("kick"+str(findID(interaction.user.name))) == (interaction.custom_id) or ("block"+str(findID(interaction.user.name))) == (interaction.custom_id)or ("Flee Colosseum?"+str(findID(interaction.user.name))) == (interaction.custom_id)): 

        if ((findRole(interaction.user.name))==1):
          playerMain = interaction.user.name
          playerOpp = findOpposingPlayer(playerMain, findID(playerMain))
        else:
          playerOpp = interaction.user.name 
          playerMain = findOpposingPlayer(playerOpp, findID(playerOpp)) 

        dmg1, dmg2, stam1, stam2 = 0,0,0,0
        moveMain, moveOpp = "🛡️","🛡️" 
        crit1, crit2 = "",""
        actMain, actOpp = "Spilled a beer and fell", "Slipped on said beer"

        if (interaction.user.name == playerMain):

          if interaction.component.label.startswith("Grab"):
            #print(interaction.custom_id)
            updateMove(playerMain,1) 
            
          elif interaction.component.label.startswith("Punch"):
            updateMove(playerMain,2)

          elif interaction.component.label.startswith("Kick"):
            updateMove(playerMain,3)
      
          elif interaction.component.label.startswith("Block"):
            updateMove(playerMain,4)

          elif interaction.component.label.startswith("Flee Colosseum?"):
            updateMove(playerMain,5)
          
          moveMain = "🏹"
          if ((findHealth(playerMain) > 0) and (findHealth(playerOpp) > 0)):
            embedUpdate((globals()[(playerMain+"Battle")]),playerOpp,playerMain,moveMain,moveOpp)
          #print(globals()[(playerMain+"Battle")])

        if (interaction.user.name == playerOpp):

          if interaction.component.label.startswith("Grab"):
            updateMove(playerOpp,1)
            
          elif interaction.component.label.startswith("Punch"):
            updateMove(playerOpp,2)

          elif interaction.component.label.startswith("Kick"):
            updateMove(playerOpp,3)

          elif interaction.component.label.startswith("Block"):
            updateMove(playerOpp,4)

          elif interaction.component.label.startswith("Flee Colosseum?"):
            updateMove(playerOpp,5)

          moveOpp = "🏹"
          if ((findHealth(playerMain) > 0) and (findHealth(playerOpp) > 0)):
            embedUpdate((globals()[(playerMain+"Battle")]),playerOpp,playerMain,moveMain,moveOpp)
          #print(globals()[(playerMain+"Battle")])

        if((((interaction.user.name == playerOpp) or (interaction.user.name == playerMain)) and ((findMove(playerOpp)>0) and (findMove(playerMain)>0))) or findMove(playerMain) == 5 or findMove(playerOpp) == 5):

          usageMyth, damageMyth = 0.62, 22
          #P1 GRAB
          if ((findMove(playerMain) == 1) and (findMove(playerOpp) == 1)): #GRAB / GRAB 
            dmg1, dmg2 = random.randint(0, 5), random.randint(0, 5)
            stam1, stam2 = random.randint(12, 12), random.randint(12, 12) 
            actMain, actOpp = "Grab", "Grab"

          elif ((findMove(playerMain) == 1) and (findMove(playerOpp) == 2)): #GRAB / PUNCH 
            dmg1, dmg2 = random.randint(1, 5), random.randint(12, 15)
            stam1, stam2 = random.randint(12, 12), random.randint(6, 10) 
            actMain, actOpp = "Grab", "Punch"

          elif ((findMove(playerMain) == 1) and (findMove(playerOpp) == 3)): #GRAB / KICK 
            dmg1, dmg2 = random.randint(1, 3), random.randint(4, 10)
            stam1, stam2 = random.randint(12, 12), random.randint(22, 25) 
            actMain, actOpp = "Grab", "Kick"

          elif ((findMove(playerMain) == 1) and (findMove(playerOpp) == 4)): #GRAB / BLOCK 
            dmg1, dmg2 = random.randint(8, 12), random.randint(0, 0)
            stam1, stam2 = random.randint(12, 12), random.randint(-12, -8)
            actMain, actOpp = "Grab", "Block"

          #P2 PUNCH
          elif ((findMove(playerMain) == 2) and (findMove(playerOpp) == 1)): #PUNCH / GRAB 
            dmg1, dmg2 = random.randint(12, 15), random.randint(1, 5)
            stam1, stam2 = random.randint(6, 10), random.randint(12, 12) 
            actMain, actOpp = "Punch", "Grab"

          elif ((findMove(playerMain) == 2) and (findMove(playerOpp) == 2)): #PUNCH / PUNCH  
            dmg1, dmg2 = random.randint(5, 12), random.randint(5, 12)
            stam1, stam2 = random.randint(10, 15), random.randint(10, 15) 
            actMain, actOpp = "Punch", "Punch"

          elif ((findMove(playerMain) == 2) and (findMove(playerOpp) == 3)): #PUNCH / KICK 
            dmg1, dmg2 = random.randint(5, 10), random.randint(16, 35)
            stam1, stam2 = random.randint(10, 15), random.randint(15, 25) 
            actMain, actOpp = "Punch", "Kick"

          elif ((findMove(playerMain) == 2) and (findMove(playerOpp) == 4)): #PUNCH / BLOCK 
            dmg1, dmg2 = random.randint(3,8), random.randint(0, 3)
            stam1, stam2 = random.randint(10, 15), random.randint(-12, -8)
            actMain, actOpp = "Punch", "Block"

          #P3 KICK
          elif ((findMove(playerMain) == 3) and (findMove(playerOpp) == 1)): #KICK / GRAB 
            dmg1, dmg2 = random.randint(4, 10), random.randint(1, 3)
            stam1, stam2 = random.randint(22, 25), random.randint(12, 12) 
            actMain, actOpp = "Kick", "Grab" 

          elif ((findMove(playerMain) == 3) and (findMove(playerOpp) == 2)): #KICK / PUNCH 
            dmg1, dmg2 = random.randint(16, 35), random.randint(5, 10)
            stam1, stam2 = random.randint(15, 25), random.randint(10, 15) 
            actMain, actOpp = "Kick", "Punch" 

          elif ((findMove(playerMain) == 3) and (findMove(playerOpp) == 3)): #KICK / KICK 
            dmg1, dmg2 = random.randint(15, 20), random.randint(15, 20)
            stam1, stam2 = random.randint(15, 25), random.randint(15, 25) 
            actMain, actOpp = "Kick", "Kick" 

          elif ((findMove(playerMain) == 3) and (findMove(playerOpp) == 4)): #KICK / BLOCK 
            dmg1, dmg2 = random.randint(-3, 4), random.randint(8, 15)
            stam1, stam2 = random.randint(15, 25), random.randint(-12, -8) 
            actMain, actOpp = "Kick", "Block" 

          #P4 BLOCK
          elif ((findMove(playerMain) == 4) and (findMove(playerOpp) == 1)): #BLOCK / GRAB 
            dmg1, dmg2 = random.randint(0, 0), random.randint(8, 12)
            stam1, stam2 = random.randint(-12, -8), random.randint(12, 12) 
            actMain, actOpp = "Block", "Grab" 

          elif ((findMove(playerMain) == 4) and (findMove(playerOpp) == 2)): #BLOCK / PUNCH
            dmg1, dmg2 = random.randint(0, 3), random.randint(3, 8)
            stam1, stam2 = random.randint(-12, -8), random.randint(10, 15) 
            actMain, actOpp = "Block", "Punch" 

          elif ((findMove(playerMain) == 4) and (findMove(playerOpp) == 3)): #BLOCK / KICK
            dmg1, dmg2 = random.randint(8, 15), random.randint(-3, 4)
            stam1, stam2 = random.randint(-12, -8), random.randint(15, 25) 
            actMain, actOpp = "Block", "Kick" 

          elif ((findMove(playerMain) == 4) and (findMove(playerOpp) == 4)): #BLOCK / BLOCK
            dmg1, dmg2 = 0,0
            stam1, stam2 = random.randint(-15, -10), random.randint(-15, -10)
            actMain, actOpp = "Block", "Block" 
            
          #definedUpdateAll function // handles inputing move that requires too much stamina
          if((random.randint(1, 15)) == 1):
            if (actMain == "Block"):
              dmg2 = round(random.randint(-8,-5) * random.uniform(2.1, 3.1))
            else:
              dmg1 = round((dmg1+2) * random.uniform(1.4, 1.6))
            crit1 = "Enchanted🔮 "
            print("crit")

          elif((random.randint(1, 15)) == 10):
            if (actOpp == "Block"):
              dmg1 = round((random.randint(-8,-5)) * random.uniform(2.1, 3.1))
            else:  
              dmg2 = round((dmg2+2) * random.uniform(1.4, 1.6))
            crit2 = "Enchanted🔮 "
            print("crit")
          
          if ((random.randint(1, 40)) == 20):
            if (actMain == "Block"):
              dmg2 = round((random.randint(-11,-9)) * random.uniform(2.1, 3.1))
              dmg1 += (random.randint(5,8))
            else: 
              dmg1 = round((abs(dmg1)+8) * random.uniform(1.6, 1.8))
            crit1 = crit1 + "Dark Magic🌒 "
            print("Demon crit")

          elif ((random.randint(1, 40)) == 2):
            if (actOpp == "Block"):
              dmg1 = round((random.randint(-11,-9)) * random.uniform(2.1, 3.1))
              dmg2 += (random.randint(5,8))
            else:  
              dmg2 = round((abs(dmg2)+8) * random.uniform(1.6, 1.8))
            crit2 = crit2 + "Dark Magic🌒 "
            print("Demon crit")        

          if ((random.randint(1, 200)) == 30):
            if (actMain == "Block"):
              dmg2 = round((random.randint(-30,-5)) * random.uniform(1.1, 3.1))
              dmg1 += (random.randint(5,20))
            else: 
              dmg1 = round((abs(dmg1)+20) * random.uniform(1.4, 1.8))
            crit1 = crit1 + "Morath's Magic⚕️ "
            print("Max crit")

          elif ((random.randint(1, 200)) == 3):
            if (actOpp == "Block"):
              dmg1 = round((random.randint(-30,-5)) * random.uniform(1.1, 3.1))
              dmg2 += (random.randint(5,20))
            else:  
              dmg2 = round((abs(dmg2)+20) * random.uniform(1.4, 1.8))
            crit2 = crit2 + "Morath's Magic⚕️ "
            print("Max crit")

          if((findMythical(playerMain))==1):
              crit1 = crit1 + "Mythical🔥 "
              if (dmg1 < 0):
                dmg1 = random.randint(8,15)
              else:
                print(dmg1)
                print(abs((((findStamina(playerMain) - stam1)*usageMyth)/damageMyth)+1),"x")
                dmg1 = abs ( round( (dmg1+2) *((((findStamina(playerMain) - stam1)*usageMyth)/damageMyth)+1)) )
                print(dmg1)
              #print (dmg1)
              #print((((findStamina(playerMain) - stam1)*usageMyth)/damageMyth)+1)

          if((findMythical(playerOpp))==1):
              crit2 = crit2 + "Mythical🔥 "
              if (dmg2 < 0):
                dmg2 = random.randint(8,15)
              else:
                print(dmg2)
                print(abs((((findStamina(playerOpp) - stam2)*usageMyth)/damageMyth)+1),"x") 
                dmg2 = abs ( round( (dmg2+2) *((((findStamina(playerOpp) - stam2)*usageMyth)/damageMyth)+1)) )
                print(dmg2)
              #print(dmg2)
              #print((((findStamina(playerOpp) - stam1)*usageMyth)/damageMyth)+1)

          if ((actMain == "Block") and (actOpp == "Block")):
            stam1 -= random.randint(5,8)
            stam2 -= random.randint(5,8)

          if ((actMain == "Block") and ((findStamina(playerOpp) - stam2) < 0)): 
            updateHealth(playerMain, int(findHealth(playerMain)))  #opponent inflicted
            updateHealth(playerOpp, int(findHealth(playerOpp)))
            updateStamina(playerMain, int(findStamina(playerMain)) - (-10)) #self-inflicted
            updateStamina(playerOpp, int(findStamina(playerOpp)) - (-10))
            actOpp = "Tired😴"
            dmg1, dmg2 = 0,0 

          elif ((actOpp == "Block") and ((findStamina(playerMain) - stam1) < 0)):
            updateHealth(playerMain, int(findHealth(playerMain)))  #opponent inflicted
            updateHealth(playerOpp, int(findHealth(playerOpp)))
            updateStamina(playerMain, int(findStamina(playerMain)) - (-10)) #self-inflicted
            updateStamina(playerOpp, int(findStamina(playerOpp)) - (-10))
            actMain = "Tired😴"
            dmg1, dmg2 = 0,0 

          elif (((findStamina(playerOpp) - stam2) < 0) and ((findStamina(playerMain) - stam1) < 0)):
            updateHealth(playerMain, int(findHealth(playerMain)))  #opponent inflicted
            updateHealth(playerOpp, int(findHealth(playerOpp)))
            updateStamina(playerMain, int(findStamina(playerMain)) - (-10)) #self-inflicted
            updateStamina(playerOpp, int(findStamina(playerOpp)) - (-10))
            dmg1, dmg2 = 0,0 
            actMain, actOpp = "Tired😴", "Tired😴"

          elif ((findStamina(playerMain) - stam1) < 0):
            updateHealth(playerMain, int(findHealth(playerMain)) - round((dmg2+4)*2.5))  #opponent inflicted
            updateHealth(playerOpp, int(findHealth(playerOpp)))
            updateStamina(playerMain, int(findStamina(playerMain)) - (-10)) #self-inflicted
            updateStamina(playerOpp, int(findStamina(playerOpp)) - stam2)
            dmg1, dmg2 = 0, round((dmg2+4)*2.5)
            actMain = "Tired😴"

          elif ((findStamina(playerOpp) - stam2) < 0):
            updateHealth(playerMain, int(findHealth(playerMain)))  #opponent inflicted
            updateHealth(playerOpp, int(findHealth(playerOpp)) - round((dmg1+4)*2.5))
            updateStamina(playerMain, int(findStamina(playerMain)) - stam1) #self-inflicted
            updateStamina(playerOpp, int(findStamina(playerOpp)) - (-10))
            dmg1, dmg2 = round((dmg1+4)*2.5), 0
            actOpp = "Tired😴"

          else: 
            if((findMythical(playerMain))==1):
              print("P.main/Mythical stamina used:", stam1, "//", (findStamina(playerMain)), "/", (findStamina(playerMain) - stam1),"/", round((findStamina(playerMain) - stam1)*usageMyth))
              stam1 += round((findStamina(playerMain) - stam1)*usageMyth)
              print("Stam used post increase: ",stam1)
              updateCooldown(playerMain,0)
              updateMythical(playerMain,0)

            if((findMythical(playerOpp))==1):
              print("P.opp/Mythical stamina used: ", stam2, "//", (findStamina(playerOpp)), "/", (findStamina(playerOpp) - stam2),"/", round((findStamina(playerOpp) - stam2)*usageMyth))
              stam2 += round((findStamina(playerOpp) - stam2)*usageMyth)
              print("Stam used post increase: ",stam2)
              updateCooldown(playerOpp,0)
              updateMythical(playerOpp,0)

            updateHealth(playerMain, int(findHealth(playerMain)) - dmg2)  #opponent inflicted
            updateHealth(playerOpp, int(findHealth(playerOpp)) - dmg1)

            updateStamina(playerMain, int(findStamina(playerMain)) - stam1) #self-inflicted
            updateStamina(playerOpp, int(findStamina(playerOpp)) - stam2)

          #Handling for sub-zero/sur-100 Stamina/health and "Give Up" input
          if (findHealth(playerMain)>105):
            updateHealth(playerMain, 105)
          if (findHealth(playerOpp)>105):
            updateHealth(playerOpp, 105)
          if (findHealth(playerMain)<0):
            updateHealth(playerMain, 0)
          if (findHealth(playerOpp)<0):
            updateHealth(playerOpp, 0)

          if(findStamina(playerMain) > 100):
            updateStamina(playerMain, 100) 
          if(findStamina(playerOpp) > 100):
            updateStamina(playerOpp, 100)
          if(findStamina(playerMain) < 0):
            updateStamina(playerMain, 0) 
          if(findStamina(playerOpp) < 0):
            updateStamina(playerOpp, 0)

          if ((findMove(playerMain) == 5)):
            updateHealth(playerMain, -5)
          if ((findMove(playerOpp) == 5)):
            updateHealth(playerOpp, -5)

          updateMove(playerOpp,0)
          updateMove(playerMain,0)
          updateCooldown(playerMain,(findCooldown(playerMain)+1))
          updateCooldown(playerOpp,(findCooldown(playerOpp)+1))
          moveMain, moveOpp = "📜", "📜"
        
        victoryString = "The crowd is overjoyed! Your victory will echo throughout the kingdom for centuries 📯"

        if ((findHealth(playerMain) < 1) and (findHealth(playerOpp) < 1)):
          embedVictory.set_field_at(0,name="You two warriors both bled out! Look at this mess on the battleground ⚔️", value=finalPhrase, inline=True)
          embedDescription(embedVictory,playerOpp, playerMain, actMain, actOpp, dmg1, dmg2, crit1, crit2) 
          await interaction.edit_origin(embed=embedVictory,components=action_victory)
          print("| No Winner #TIED: ", playerOpp, "[vs. ", playerMain, "] Game:", str(findID(playerMain)))
          resetMechanic(playerMain, playerOpp)
          return

        elif (findHealth(playerMain)< (-1)):
          embedVictory.set_field_at(0,name="What a battle, yet only " + playerOpp + " stands victorious! ⚔️", value=victoryString, inline=True)
          if (findHealth(playerOpp) != 100):
            incrementLeaderboard(playerMain, 'l')
            incrementLeaderboard(playerOpp, 'w')
            embedVictory.set_footer(text = playerMain + " fled the Colosseum, what a shame! The King will have his head!")
            print("!/", playerMain, " fled vs. ", playerOpp)
          else: 
            embedVictory.set_footer(text = playerMain + " cancelled the match, no win or loss recorded!")
          await interaction.edit_origin(embed=embedVictory,components=action_victory)
          print("| Winner: ", playerOpp, "[vs. ", playerMain, "] Cancelled Game:", str(findID(playerMain)))
          resetMechanic(playerMain, playerOpp)
          time.sleep(0.085)
          return
          
        elif (findHealth(playerOpp) < (-1)):
          embedVictory.set_field_at(0,name="What a battle, yet only " + playerMain + " stands victorious! ⚔️",value=victoryString, inline=True) 
          if (findHealth(playerMain) != 100):
            incrementLeaderboard(playerMain, 'w')
            incrementLeaderboard(playerOpp, 'l')
            embedVictory.set_footer(text = playerOpp + " fled the Colosseum, what a shame! The King will have his head!")
            print("!/", playerOpp, " fled vs. ", playerMain)
          else:
            embedVictory.set_footer(text = playerOpp + " cancelled the match, no win or loss recorded!")
          await interaction.edit_origin(embed=embedVictory,components=action_victory)
          print("| Winner: ", playerMain, "[vs. ", playerOpp, "] Cancelled Game:", str(findID(playerMain)))
          resetMechanic(playerMain, playerOpp)
          time.sleep(0.085)
          return
          
        elif (findHealth(playerMain) <= 0):
          (globals()[(playerMain+"Battle")]) = discord.Embed(color=0x993723)
          (globals()[(playerMain+"Battle")]).set_author(name="Warriors of Aradena",icon_url="https://imgur.com/PPzYRXX.png")
          (globals()[(playerMain+"Battle")]).set_thumbnail(url="https://i.imgur.com/6tnpdBU.png")
          (globals()[(playerMain+"Battle")]).add_field(name="What a brawl, yet only " + playerOpp + " stands victorious! ⚔️",value=victoryString, inline=True) 
          embedDescription((globals()[(playerMain+"Battle")]),playerOpp, playerMain, actMain, actOpp, dmg1, dmg2, crit1, crit2)
          #####
          await interaction.edit_origin(embed=(globals()[(playerMain+"Battle")]),components=action_victory)
          incrementLeaderboard(playerMain, 'l')
          incrementLeaderboard(playerOpp, 'w')
          resetMechanic(playerMain, playerOpp)
          time.sleep(0.085)
          print("| Winner: ", playerOpp, "[vs. ", playerMain, "]")
          return

        elif (findHealth(playerOpp) <= 0):
          (globals()[(playerMain+"Battle")]) = discord.Embed(color=0x993723)
          (globals()[(playerMain+"Battle")]).set_author(name="Warriors of Aradena",icon_url="https://imgur.com/PPzYRXX.png")
          (globals()[(playerMain+"Battle")]).set_thumbnail(url="https://i.imgur.com/6tnpdBU.png") 
          (globals()[(playerMain+"Battle")]).add_field(name="What a brawl, yet only " + playerMain + " stands victorious! ⚔️",value=victoryString, inline=True) 
          embedDescription((globals()[(playerMain+"Battle")]),playerOpp, playerMain, actMain, actOpp, dmg1, dmg2, crit1, crit2)
          await interaction.edit_origin(embed=(globals()[(playerMain+"Battle")]),components=action_victory)
          incrementLeaderboard(playerMain, 'w')
          incrementLeaderboard(playerOpp, 'l')
          resetMechanic(playerMain, playerOpp)
          time.sleep(0.085)
          print("| Winner: ", playerMain, "[vs. ", playerOpp, "]")
          return 

        else:
          if ((moveMain  == "📜") and (moveOpp == "📜")):
            embedDescription((globals()[(playerMain+"Battle")]), playerOpp, playerMain, actMain, actOpp, dmg1, dmg2, crit1,crit2)
            print(playerMain," dealt = ", dmg1, "|", playerOpp, "dealt = ", dmg2, "|| Main stam = ", stam1, "| Opp stam = ", stam2)
          embedUpdate((globals()[(playerMain+"Battle")]),playerOpp,playerMain,moveMain,moveOpp)
          await interaction.edit_origin(embed=(globals()[(playerMain+"Battle")]))  

      else: 
        await interaction.respond(content = "This is not your fight warrior!", ephemeral=True)
      
################################

def embedUpdate(embedTemp,playerOpp,playerMain, moveMain, moveOpp): 
  embedTemp.set_field_at(0, name=playerMain+moveMain, value="Health: {}  ❤️\n Stamina: {}  ⚡".format(findHealth(playerMain),findStamina(playerMain)), inline=True)
  embedTemp.set_field_at(2, name=playerOpp+moveOpp, value="Health: {}  ❤️\n Stamina: {}  ⚡".format(findHealth(playerOpp),findStamina(playerOpp)), inline=True) 
  embedTemp.set_footer(text=(str(findString(playerMain)) + "\n" + str(findString(playerOpp))))

def embedDescription (embedTemp, playerOpp, playerMain, actMain, actOpp, dmg1, dmg2, crit1, crit2): 
  errorfeed = ""
  if (dmg1<0):
    updateString(playerMain, ("Somehow " + playerOpp + " heals " + str(abs(dmg1)) + " point(s)"))
    updateString(playerOpp, ("and " + playerOpp + " deals " + str(dmg2) + " damage to " + playerMain + " [Mysterious " + crit2 + actOpp + "]⚗️!" ))
  elif (dmg2<0):
    updateString(playerMain, ("Somehow " + playerMain + " heals " + str(abs(dmg2)) + " point(s)"))
    updateString(playerOpp, ("and " + playerMain + " deals " + str(dmg1) + " damage to " + playerOpp +" [Mysterious " + crit1 + actMain + "]!⚗️" ))
  else:
    if ((actMain == "Tired😴") or (actOpp == ("Tired😴"))):
      updateString(playerMain, (playerMain + " deals " + str(dmg1) + " damage [" + crit1 + actMain + "]"))
      updateString(playerOpp, ("and " + playerOpp + " deals " + str(dmg2) + " damage [" + crit2 + actOpp + "]!")) 

    elif (((findHealth(playerMain) < 1) or (findHealth(playerOpp) < 1)) and ((dmg1 == 0) and (dmg2 == 0))):
      updateString(playerMain, (playerMain + " deals around " + str(dmg1) + " damage [" + crit1 + actMain + "]"))
      updateString(playerOpp, ("and " + playerOpp + " deals around " + str(dmg2) + " damage [" + crit2 + actOpp + "]"))
      errorfeed = "\n (Note: Discord input error, but battle results are accurate)"

    elif ((findHealth(playerMain) < 1) or (findHealth(playerOpp) < 1)):
      updateString(playerMain, (playerMain + " deals " + str(dmg1) + " damage [" + crit1 + actMain + "]"))
      updateString(playerOpp, ("and " + playerOpp + " deals " + str(dmg2) + " damage [" + crit2 + actOpp + "]"))

    else: 
      updateString(playerMain, playerMain + " deals " + str(dmg1) + " damage [" + crit1 + actMain + "]")
      updateString(playerOpp, "and " + playerOpp + " deals " + str(dmg2) + " damage [" + crit2 + actOpp + "]!")

  embedTemp.set_footer( text=(str(findString(playerMain)) + "\n" + str(findString(playerOpp)) + str(errorfeed)))

def findMove(username):
  df = pd.read_csv("healthStamina.csv")
  df = df.loc[df['name'] == username]
  if(len(df) == 0):
    return None
  return df.iloc[0]['move']  

def findHealth(username):
  df = pd.read_csv("healthStamina.csv")
  df = df.loc[df['name'] == username]
  if(len(df) == 0):
    return None
  return df.iloc[0]['health']
  
def findStamina(username):
  df = pd.read_csv("healthStamina.csv")
  df = df.loc[df['name'] == username]
  if(len(df) == 0):
    createPlayer(username)
  return df.iloc[0]['stamina']  

def findTime(username):
  df = pd.read_csv("healthStamina.csv")
  df = df.loc[df['name'] == username]
  if(len(df) == 0):
    createPlayer(username)
  return df.iloc[0]['time']  

def findRole(username):
  df = pd.read_csv("healthStamina.csv")
  df = df.loc[df['name'] == username]
  if(len(df) == 0):
    return None
  return df.iloc[0]['main']

def findMythical(username):
  df = pd.read_csv("healthStamina.csv")
  df = df.loc[df['name'] == username]
  if(len(df) == 0):
    return None
  return df.iloc[0]['mythical']

def findCooldown(username):
  df = pd.read_csv("healthStamina.csv")
  df = df.loc[df['name'] == username]
  if(len(df) == 0):
    return None
  return df.iloc[0]['cooldown']

def findID(username):
  df = pd.read_csv("healthStamina.csv")
  df = df.loc[df['name'] == username]
  if(len(df) == 0):
    return None
  return df.iloc[0]['id']

def findString(username):
  df = pd.read_csv("healthStamina.csv")
  df = df.loc[df['name'] == username]
  if(len(df) == 0):
    return None
  return df.iloc[0]['stringtext']

def findOpposingPlayer(username,battle):
  df = pd.read_csv("healthStamina.csv")
  df = df.loc[df['id'] == battle]
  if(len(df) == 0):
    return 
  df = df.loc[df['name'] != username]
  return df.iloc[0]['name']

def updateHealth(username, newHealth): 
  df = pd.read_csv("healthStamina.csv")
  idx = df.index[df['name']==username]
  df.at[idx, 'health'] = newHealth
  df.to_csv("healthStamina.csv",index = False)
  
def updateStamina(username, newHealth):
   df = pd.read_csv("healthStamina.csv")
   idx = df.index[df['name']==username]
   df.at[idx, 'stamina'] = newHealth
   df.to_csv("healthStamina.csv",index = False)
  
def updateString(username, string):
   df = pd.read_csv("healthStamina.csv")
   idx = df.index[df['name']==username]
   df.at[idx, 'stringtext'] = string
   df.to_csv("healthStamina.csv",index = False)

def updateMove(username, move):
  df = pd.read_csv("healthStamina.csv")
  idx = df.index[df['name']==username]
  df.at[idx, 'move'] = move
  if(findStamina(username) <= 0):
    df.at[idx, 'move'] = 4
  updateTime(username)
  df.to_csv("healthStamina.csv",index = False)

def updateTime(username):
   df = pd.read_csv("healthStamina.csv")
   idx = df.index[df['name']==username]
   df.at[idx, 'time'] = int(time.time())
   df.to_csv("healthStamina.csv",index = False)

def resetPlayer(username):
  updateHealth(username, 100)
  updateStamina(username, 100)
  updateMove(username, 0)
  updateTime(username)
  
def joinrace(name):
  df = pd.read_csv("race.csv")
  df = df.loc[df['name'] == name]
  if(not (len(df) == 0)):
    return False
  data = [[name, 0,0.0]]
  df = pd.DataFrame(data)
  df.to_csv('race.csv',mode='a',header=False,index=False)
  print("User joined")
  return True

#########################################################

def incrementracevalue(case, group):
  df = pd.read_csv("race.csv")
  idx, c1 = 0, 0
  eventString = ""
  while idx < len(df):
    df.at[idx, 'pvalue'] += random.randint(3,8)
    if (case == 420):
      df.at[idx, 'pvalue'] += random.randint(0,3)
    idx += 1
  if ((len(df) > 20) and (case != 420)):
    idxa = 19
    while idxa < len(df):
      df.at[idxa, 'pvalue'] -= random.randint(0,1)
      idxa += 1

  if (b1<=case<=b2):
    if (godChargeDuration == 0):
      eventString = "EVENT: {} uses the forbidden agility spells for {} turns❗💨".format(group[0],(group[1]))
    else:
      eventString = ""
      
  if (e1<=case<=e2):
    eventString = "EVENT: {}, {} & {} use magic❗🔮".format(group[0],(group[1]),group[2])
  if (f1<=case<=f2):
    if ((group[0]) == (group[1])):
      eventString = "EVENT: {} uses spatial magic to swap spots with himself❗🔮 \n What an amateur mage!".format(group[0])
    else: 
      eventString = "EVENT: {} uses spatial magic to swap spots with {}❗🔮".format(group[0],(group[1]))
  if (40<=case<=45):
    eventString = "EVENT: The leading knights get bombarbded by arrows❗🏹"
  if (g1<=case<=g2):
    eventString = "EVENT: Morath attacks🧛: {} & {} disappear❗".format(group[0],(group[1]))
  if (h1<=case<=h2):
    if ((group[0]) == (group[1])):
      eventString = "EVENT: {} uses a lightning spell to stun himself❗🌩️ \n Morath laughs at this amateur mage!".format(group[0])
    else: 
      eventString = "EVENT: {} uses a lightning spell to stun {}❗🌩️".format(group[0],(group[1]))
    
  if (i1<=case<=i2):
    eventString = "EVENT: {} bribes guards to halt the racers on his tail❗🪙".format(group[0])
  if (j1<=case<=j2):
    eventString = "LOCATION: Racers enter part of the Bloodwood forest❗🌲 \n~Leading racers are attacked by werewolves!"
  if (k1<=case<=k2):
    eventString = "LOCATION: Racers enter part of the Desert of Winds❗🏜️ \n~Blinding sandstorms! Riders pair up!"
  if (o1<=case<=o2):
    eventString = "LOCATION: Racers enter part of the ravine of Ohiolo❗🏞️ \n~The worst realm in the kingdom. Some riders fall back!"
  if (l1<=case<=l2):
    eventString = "EVENT: {} uses an enchanted gravity strike❗🌒".format(group[0])

  if (n1<=case<=n2): 
    eventString = "EVENT: Racers in the far back find a secret shortcut in the mountains❗" 
 
  df.to_csv("race.csv",index = False)
  sortrace()
  return eventString

def eventExecute(case, group):
  df = pd.read_csv("race.csv")
  #print(df)

  if ((b1<=case<=b2) and ((globals()[('godChargeDuration')]) == 0)):
    v1,duration = (df[df['name']==group[0]].index.values),group[1]
    (globals()[('godChargeName')]) = group[0]
    (globals()[('godChargeDuration')]) = group[1]
    print(godChargeName,godChargeDuration,"in Execute")

  if ((globals()[('godChargeDuration')]) > 0):
    v1 = (df[df['name']== (globals()[('godChargeName')])].index.values)
    m1 = v1[0]
    print(df.at[m1,'pvalue'])
    df.at[m1,'pvalue'] += random.randint(2,6)
    print(df.at[m1,'pvalue'])
    globals()[('godChargeDuration')] -= 1
    if (globals()[('godChargeDuration')] == 0):
      globals()[('godChargeName')] = ""

    print(godChargeDuration, godChargeName)

  if (e1<=case<=e2):
    v1,v2,v3 = (df[df['name']==group[0]].index.values),(df[df['name']==group[1]].index.values),(df[df['name']==group[2]].index.values)
    m1,m2,m3 = v1[0],v2[0],v3[0]
    df.at[m1,'pvalue'] += random.randint(3,5)
    df.at[m2,'pvalue'] += random.randint(5,6)
    df.at[m3,'pvalue'] += random.randint(1,7)

  if (f1<=case<=f2):
    print("Spatial.exe")
    v1,v2 = (df[df['name']==group[0]].index.values),(df[df['name']==group[1]].index.values)
    m1,m2 = v1[0],v2[0]
    print(m1,m2)
    temp = df.at[m1,'pvalue']
    df.at[m1,'pvalue'] = df.at[m2,'pvalue']+1
    df.at[m2,'pvalue'] = temp

  if (40<=case<=45):
    c1 = 0
    print("Arrow.exe")
    while c1 < 3:
      df.at[c1,'pvalue'] -= random.randint(5,7)
      c1 += 1
  
  if (g1<=case<=g2):
    print("Morath.exe")
    v1,v2 = (df[df['name']==group[0]].index),(df[df['name']==group[1]].index)
    m1,m2 = v1[0],v2[0]
    print(m1,m2)
    df = df.drop([m1, m2])

  if (h1<=case<=h2):
    print("Stun.exe")
    v2 = (df[df['name']==group[1]].index)
    m2 = v2[0]
    df.at[m2,'pvalue'] -= random.randint(12,16)

  if (i1<=case<=i2):
    print("Bribery.exe")
    v1 = (df[df['name']==group[0]].index)
    m1 = v1[0]
    df.at[(m1+1),'pvalue'] -= random.randint(7,10)
    df.at[(m1+2),'pvalue'] -= random.randint(7,10)

  if (j1<=case<=j2):
    print("Bloodwood.exe")
    idx = 1
    temp = random.randint(2,(len(df)-1))
    df.at[0, 'pvalue'] += random.randint(-12,-5)
    while idx < temp:
      df.at[idx, 'pvalue'] += random.randint(-10,0)
      idx += 1

  if (k1<=case<=k2):
    print("Desert.exe")
    idx = 0
    temp = (len(df)-2)
    while idx < temp:
      df.at[idx+1, 'pvalue'] = df.at[idx, 'pvalue']
      idx += 2

  if (o1<=case<=o2):
    print("Ravine.exe")
    idx = 0
    temp = random.randint(2,(len(df)-1))
    samp = tuple(random.sample(range(0,(len(df)-1)),temp))
    print(samp)
    while idx < temp:
      df.at[samp[idx], 'pvalue'] -= random.randint(4,7)
      idx += 1

  if (l1<=case<=l2):
    print("Gravity.exe")
    idx = 0
    v1 = (df[df['name']==group[0]].index)
    m1 = v1[0]
    print(m1)
    while idx < (len(df)-1):
      df.at[idx, 'pvalue'] = ((df.at[idx, 'pvalue'])-round(((df.at[idx, 'pvalue'])-(df.at[m1, 'pvalue']))/2))
      idx += 1

  if (n1<=case<=n2): 
    print("THE FLANK")
    tempPval = df.at[5,'pvalue'] 
    idx = (len(df)-5) 
    print ("IDX:",idx)
    while idx <= (len(df)-1):
      df.at[idx,'pvalue'] = tempPval
      idx += 1 

  df.to_csv("race.csv",index = False)

def randomGroup(case):
  df = pd.read_csv("race.csv")

  if (b1<=case<=b2):
    group = tuple(random.sample(range(5, len(df)-4),3))
    result = (df.at[group[0],'name'],random.randint(2,4))
    print(result) 
    return result 

  if ((e1<=case<=e2)):
    group = tuple(random.sample(range(0, len(df)-1), 3))
    result = (df.at[group[0],'name'], df.at[group[1],'name'], df.at[group[2],'name'])
    print(result) 
    return result 

  if (f1<=case<=f2):
    temp = (random.randint(8,len(df)-1))
    temp2 = (random.randint(1,5))
    if (temp2 > temp):
      temp2 = random.randint(0,3)
    result = (df.at[temp,'name'], df.at[temp2,'name'])
    return result

  if (g1<=case<=g2):
    temp = (random.randint(0,len(df)-1))
    temp2 = (random.randint(0,(len(df)-1)))
    while (temp == temp2):
      temp2 = (random.randint(0,(len(df)-1)))
    result = (df.at[temp,'name'], df.at[temp2,'name'])
    return result

  if (h1<=case<=h2):
    temp = (random.randint(0,len(df)-1))
    temp2 = (random.randint(0,(12)))
    #while ((temp2 >= temp) or (temp2 > 12)):
    #  temp2 = (random.randint(0,(len(df)-1)))
    result = (df.at[temp,'name'], df.at[temp2,'name'])
    return result

  if (i1<=case<=i2):
    if ((len(df)) < 12):
      x = len(df)
    else: 
      x = 12
    temp = (random.randint(0,x))
    temp2,temp3 = (temp+1),(temp+2)
    result = (df.at[temp,'name'], df.at[temp2,'name'],df.at[temp3,'name'])
    return result

  if (l1<=case<=l2):
    temp = (random.randint(2,11))
    result = (df.at[temp,'name'],df.at[temp,'name'])
    return result
 
#############################################################33

def resetrace():
  data = [['name','pvalue','Time']]
  df = pd.DataFrame(data)
  df.to_csv("race.csv",index = False, header=False)

  # while idx < len(df):
  #   df.at[idx, 'pvalue'] = 0
  #   df.at[idx, 'Time'] = 0.00
  #   idx += 1
  #df.to_csv("race.csv",index = False) 

def sortrace():
  df = pd.read_csv("race.csv")
  df = df.sort_values(['pvalue'], ascending=(False))
  idx = 1
  while idx < len(df):
    df.at[idx, 'Time'] = round((float(((df.at[idx, 'pvalue']) - (df.at[0, 'pvalue'])))/3.75)-(random.random()/2),2)
    idx += 1
    df.to_csv("race.csv",index = False) 
  df = df.sort_values(['Time'], ascending=(False))
  df.at[0,'Time'] = 0.0
  df.to_csv("race.csv",index = False)

def racepositions():
  df = pd.read_csv("race.csv")
  if len(df) < 10:
    iterations = len(df)
  else: 
    iterations = 10
  i = 0
  tempstring = ""
  while i < iterations:
    tempstring += "{} \n".format(i+1)
    i += 1
  return tempstring

def raceleadernames():
  df = pd.read_csv("race.csv")
  if len(df) < 10:
    iterations = len(df)
  else: 
    iterations = 10
  i = 0
  tempstring = ""
  while i < iterations:
    tempstring += "{} \n".format(df.at[i,'name'])
    i += 1
  return tempstring

def createPlayer(username):
  df = pd.read_csv("healthStamina.csv")
  df = df.loc[df['name'] == username]
  if(not (len(df) == 0)):
    return False
  #data = [[username, 100, 100, 0, int(time.time()),0,findbattleId()," "]]
  data = [[username, 100, 100, 0, 0, 0, int(time.time()),0,findbattleId()," "]]
  df = pd.DataFrame(data)
  df.to_csv('healthStamina.csv', mode='a', header=False, index=False)
  return True

def updateID(username):
   df = pd.read_csv("healthStamina.csv")
   idx = df.index[df['name']==username]
   df.at[idx, 'id'] = battleId
   df.to_csv("healthStamina.csv",index = False)

def updateRole(username, playerMain):
   df = pd.read_csv("healthStamina.csv")
   idx = df.index[df['name']==username]
   if(playerMain == 1):
    df.at[idx, 'main'] = 1
   else:
    df.at[idx, 'main'] = 0
   df.to_csv("healthStamina.csv",index = False)
   
def resetMechanic(playerMain, playerOpp):
  removePlayer(playerMain)
  removePlayer(playerOpp)

def removePlayer(username):
  df = pd.read_csv("healthStamina.csv")
  df = df.loc[df['name'] != username]
  df.to_csv("healthStamina.csv",index = False)
  
def gamesTotal():
  df = pd.read_csv('gameLog.csv')
  df = df[['games']]
  df['games']+=1
  df.to_csv('gameLog.csv',index = False)
  df = pd.read_csv('gameLog.csv')
  #print((df.iloc[0]['games']))

def updateMythical(username, mythical):
   df = pd.read_csv("healthStamina.csv")
   idx = df.index[df['name']==username]
   df.at[idx, 'mythical'] = mythical
   df.to_csv("healthStamina.csv",index = False)

def updateCooldown(username, cooldown):
   df = pd.read_csv("healthStamina.csv")
   idx = df.index[df['name']==username]
   df.at[idx, 'cooldown'] = cooldown
   df.to_csv("healthStamina.csv",index = False)

######################
def battleId():
  df = pd.read_csv('gameLog.csv')
  df = df[['battleId']]
  df['battleId']+=1
  df.to_csv('gameLog.csv',index = False)

def findbattleId():
  df = pd.read_csv('gameLog.csv')
  return df.iloc[0]['games']
#######################
  
def onlyOne():
  df = pd.read_csv('healthStamina.csv')
  if(len(df) >=2):
    return False
  return True

def incrementLeaderboard(username, types):
  df = pd.read_csv("leaderboard.csv")
  idx = df.index[df['name']==username]
  if(types == 'l'):
    df.at[idx, 'losses'] = findPlayerLeaderboard(username, 'l')+1
  else:
    df.at[idx, 'wins'] = findPlayerLeaderboard(username, 'w')+1
  df.at[idx, 'wr'] = findPlayerLeaderboard(username, 'w')/((findPlayerLeaderboard(username, 'w') + findPlayerLeaderboard(username, 'l')))
  df.to_csv("leaderboard.csv",index = False)

def findPlayerLeaderboard(username, types):
  df = pd.read_csv("leaderboard.csv")
  df = df.loc[df['name'] == username]
  if(types == 'l'):
    return df.iloc[0]['losses']
  return df.iloc[0]['wins']

def createPlayerLeaderboard(username):
  df = pd.read_csv("leaderboard.csv")
  df = df.loc[df['name'] == username]
  if(not (len(df) == 0)):
    return False
  data = [[username, 0,0]]
  df = pd.DataFrame(data)
  df.to_csv('leaderboard.csv', mode='a', header=False, index=False)  

def sortLeaderboard():
  df = pd.read_csv("leaderboard.csv")
  df = df.sort_values(['wins','losses'], ascending=(False, True))
  df.to_csv("leaderboard.csv",index = False)

def sortRaceLeaderboard():
  df = pd.read_csv("raceleaderboard.csv")
  df = df.sort_values(['score'], ascending=(False))
  df.to_csv("raceleaderboard.csv",index = False)

def getTopTen(username):
  sortLeaderboard()
  df = pd.read_csv('leaderboard.csv')
  for i, row in df.iterrows():
    username = df.at[i, 'name']
    if(df.at[i, 'losses']+df.at[i, 'wins'] == 0 or df.at[i, 'wins'] == 0):
      df.at[i, 'wr'] = 0
    else:
      wr = df.at[i, 'wins']/(df.at[i, 'wins']+df.at[i, 'losses'])
      wr = wr*1000
      wr = int(round(wr,1))
      wr = wr/10
      df.at[i, 'wr'] = round(float(wr), 2)
    df.to_csv('leaderboard.csv', index = False)
  df1 = (df.head(10))
  return df1

def getTopTenM(username):
  sortLeaderboard()
  df = pd.read_csv("leaderboard.csv")
  df1 = (df.head(10))
  df1 = df1.drop(columns=['losses','wr'], axis=1)
  return df1

def getTopTenMR(a,b):
  df = pd.read_csv("race.csv")
  #print(df)
  sortrace()
  df = pd.read_csv("race.csv")
  #print(df)
  if (a<b):
    df1 = (df.head(20))
  else:
    df1 = (df.head(12))
  df1 = df1.drop(columns=['pvalue'], axis=1)
  df1.index += 1
  #print(df1)
  return df1

def shufflelist():
  df = pd.read_csv("race.csv")
  df = df.sample(frac = 1)
  df.to_csv('race.csv', index = False)

def getTopTenMRL():
  df = pd.read_csv("raceleaderboard.csv")
  df1 = (df.head(20))
  df1.index += 1
  return df1

def getFullList(base,base2):
  sortLeaderboard()
  df = pd.read_csv("leaderboard.csv")
  df1 = (df.iloc[base:base2, 0:3])
  return df1

def getWarriorName(dictionary, number):
  return dict.get(number)

def populateList(ls, n):
  for i in range(n):
    ls[i] = 0

def incrementRandomly(ls):
  for i in range(len(ls)):
    pass

def applyScores(datastorer):
  scores = [15, 12, 10, 8, 7, 6, 5, 4, 3, 2, 1,0]
  df = datastorer
  print(df)

  i = 1
  while(i < 13):
    username = df.at[i, 'name']
    score = scores[i-1]
    populateLeaderboard(username,score)
    i +=1
    print("LB:",i)
  df1 = pd.read_csv("raceleaderboard.csv")
  print(df1)
  sortRaceLeaderboard()

def populateLeaderboard(username,scorer):
  df = pd.read_csv("raceleaderboard.csv")
  df1 = df.loc[df['name'] == username]
  if((len(df1) != 0)):
    idx = df[df['name']==username].index
    temp = df.at[idx[0], 'score']
    df.at[idx[0], 'score'] = (temp + scorer)
    df.to_csv("raceleaderboard.csv",index = False)
    print(username,(df.at[idx[0], 'score']))
    return True

  else:
    data = [[username, scorer]]
    df = pd.DataFrame(data)
    df.to_csv('raceleaderboard.csv', mode='a', header=False, index=False)  
    return False

#async def racestart():
  # if (message.channel.id == 919329490881105954): 
  
#This scheduler runs late by a few ms every time I can do it in a way that involves more coding but this is what we got rn
# async def scheduler():
#   x = 1
#   #threading.Timer(x*60.0,scheduler).start() # called every x minutes
#   #while True: 
#   await asyncio.sleep(5)


keep_alive()
client.run(os.getenv('TOKEN'))

