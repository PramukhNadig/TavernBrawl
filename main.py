import discord
import os
import requests
import json
import random
import PycordUtils
from discord.ext import *
from replit import db
from keep_alive import keep_alive
from discord_components import *
from tabulate import tabulate
import csv
import pandas as pd
import time

#######################################################################################
# v1.0 complete
#######################################################################################

battleId = 0
client = discord.Client()
DiscordComponents(client)
data = [['name','health','stamina','move','time','main','id','stringtext']]
df = pd.DataFrame(data)
df.to_csv("healthStamina.csv",index = False, header=False)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
      
@client.event
async def on_message(message):
  msg = message.content
  args = message.content.split()
  
  action_victory = ActionRow(Button(label="Now go forth and adventure!🐲", custom_id="victory",disabled=True))

  descriptionTavern = "The battle is upon us!" #variables placed here for testing declaration
  finalPhrase = "The bards will write songs of this battle 📯"
  
  if (msg.startswith('$leaderboard')):
    
    embedL = discord.Embed(color=0x993723)
    embedL.set_thumbnail(url="https://i.imgur.com/Qtmmvio.png")
    #embedVar.add_field(name="Leaders", value = getTopTen(), inline = True) 
    output = "```" + tabulate(getTopTen(), headers="keys", stralign="left", numalign = "center", showindex=False, tablefmt='github') + "```"
    embedL.add_field(name="Top 10 to ever do it 🏆", value = output, inline = False) 

    await message.channel.send(embed=embedL, components=[])
 
    print(getTopTen())
    
  if (msg.startswith('$battle')):
    
    #if(not onlyOne()):
    #  await message.reply("⚠️Temporary: Only one fight allowed in the tavern!")
    # return

    if(len(message.mentions) == 0):
      await message.reply("You have to fight someone, otherwise what's the point of a brawl?")
      return

    elif(len(args) != 2):
      await message.reply('No gang fights, only tag one lad! Sir {}'.format(message.author.name))
      return
    
    elif(message.mentions[0].bot == True):
      await message.reply("Stop fighting the alehouse workers!")
      return
      
    tempMain = message.author.name
    tempOpp = message.mentions[0].name
    endFight = False

    if((findHealth(tempMain) is not None) and (findHealth(tempOpp) is not None)):
      await message.reply(content = "Stop trying to join someone else's brawl {}!".format(message.author.mention))
      endFight = True
      print("test3")
      return

    if(findHealth(tempMain) is not None):
      await message.reply(content = "Stop trying to fight the whole tavern {}!".format(message.author.mention))
      endfight = True 
      print("test1")
      return

    if(findHealth(tempOpp) is not None):
      await message.reply(content = "Stop trying to join someone else's brawl {}!".format(message.author.mention))
      endFight = True
      print("test2")
      return

    if (endFight == False):
      playerMain = message.author.name
      playerOpp = message.mentions[0].name

    if(message.mentions[0].id == client.user.id):
      await message.reply("The tavern always wins!")
      return
    
    if(message.mentions[0].id == message.author.id):
      await message.reply("Quit punching yourself!")
      return

    if (endFight == False):
      gamesTotal()

      createPlayer(playerMain)
      createPlayer(playerOpp)
      createPlayerLeaderboard(playerMain)
      createPlayerLeaderboard(playerOpp)

      updateRole(playerMain, 1)
      updateRole(playerOpp, 0)

      updateString(playerMain, descriptionTavern)
      
      resetPlayer(playerMain)
      resetPlayer(playerOpp)

      battleId = (findbattleId())

      ###########
      action_row = ActionRow([
      Button(label="Grab", custom_id= "grab"+str(battleId)), 
      Button(label="Punch",style=ButtonStyle.blue, custom_id="punch"+str(battleId)),
      Button(label="Kick",style=ButtonStyle.red, custom_id="kick"+str(battleId)),
      Button(label="Block",style=ButtonStyle.green, custom_id="block"+str(battleId)),
      Button(label="Flee Tavern?", custom_id="Flee Tavern?"+str(battleId))])

    moveMain = "📜"
    moveOpp = "📜"
  
    embedVar = discord.Embed(color=0x993723, title="The Tavern Brawl 🍺")
    embedVar.set_thumbnail(url="https://i.imgur.com/0f0nAHt.png") #https://i.imgur.com/BhScmnc.png https://imgur.com/6sZJy3R.png
    embedVar.add_field(name=playerMain+moveMain, value="Health: {}  ❤️\n Stamina: {}  ⚡".format(findHealth(playerMain), findStamina(playerMain)), inline=True)
    embedVar.add_field(name="vs.", value="⚔️", inline=True)
    embedVar.add_field(name=playerOpp+moveOpp, value="Health: {}  ❤️\n Stamina: {}  ⚡".format(findHealth(playerOpp), findStamina(playerOpp)), inline=True)
    embedVar.set_footer(text = descriptionTavern)

    await message.channel.send(embed=embedVar, components=action_row)

    embedVictory = discord.Embed(color=0x993723)
    embedVictory.set_author(name="Warriors of Aradena",icon_url="https://imgur.com/PPzYRXX.png")
    embedVictory.set_thumbnail(url="https://imgur.com/6sZJy3R.png")
    embedVictory.add_field(name="-", value="-", inline=True) 

    print("Battle between: ",playerMain," and ", playerOpp)

###################################################

    @client.event
    async def on_button_click(interaction):
      
      if ( ("grab"+str(findID(interaction.user.name))) == (interaction.custom_id) or ("punch"+str(findID(interaction.user.name))) == (interaction.custom_id) or ("kick"+str(findID(interaction.user.name))) == (interaction.custom_id) or ("block"+str(findID(interaction.user.name))) == (interaction.custom_id)or ("Flee Tavern?"+str(findID(interaction.user.name))) == (interaction.custom_id)): 
        print ("Huge W")

        if ((findRole(interaction.user.name))==1):
          playerMain = interaction.user.name
          playerOpp = findOpposingPlayer(playerMain, findID(playerMain))
        else:
          playerOpp = interaction.user.name 
          playerMain = findOpposingPlayer(playerOpp, findID(playerOpp)) 

        dmg1, dmg2, stam1, stam2 = 0,0,0,0
        moveMain, moveOpp = "🛡️","🛡️" 
        crit1, crit2 = "",""
        actMain, actOpp = "", ""

        if (interaction.user.name == playerMain):

          if interaction.component.label.startswith("Grab"):
            print(interaction.custom_id)
            updateMove(playerMain,1) 
            
          elif interaction.component.label.startswith("Punch"):
            updateMove(playerMain,2)

          elif interaction.component.label.startswith("Kick"):
            updateMove(playerMain,3)
      
          elif interaction.component.label.startswith("Block"):
            updateMove(playerMain,4)

          elif interaction.component.label.startswith("Flee Tavern?"):
            updateMove(playerMain,5)
          
          moveMain = "🏹"
          embedUpdate(embedVar,playerOpp,playerMain,moveMain,moveOpp)


        if (interaction.user.name == playerOpp):

          if interaction.component.label.startswith("Grab"):
            updateMove(playerOpp,1)
            
          elif interaction.component.label.startswith("Punch"):
            updateMove(playerOpp,2)

          elif interaction.component.label.startswith("Kick"):
            updateMove(playerOpp,3)

          elif interaction.component.label.startswith("Block"):
            updateMove(playerOpp,4)

          elif interaction.component.label.startswith("Flee Tavern?"):
            updateMove(playerOpp,5)

          moveOpp = "🏹"
          embedUpdate(embedVar,playerOpp,playerMain,moveMain,moveOpp)

        if((((interaction.user.name == playerOpp) or (interaction.user.name == playerMain)) and ((findMove(playerOpp)>0) and (findMove(playerMain)>0))) or findMove(playerMain) == 5 or findMove(playerOpp) == 5):

          #P1 GRAB
          if ((findMove(playerMain) == 1) and (findMove(playerOpp) == 1)): #GRAB / GRAB 
            dmg1, dmg2 = random.randint(0, 5), random.randint(0, 5)
            stam1, stam2 = random.randint(12, 12), random.randint(12, 12) 
            actMain, actOpp = "Grab", "Grab"

          elif ((findMove(playerMain) == 1) and (findMove(playerOpp) == 2)): #GRAB / PUNCH 
            dmg1, dmg2 = random.randint(1, 5), random.randint(8, 12)
            stam1, stam2 = random.randint(12, 12), random.randint(8, 12) 
            actMain, actOpp = "Grab", "Punch"

          elif ((findMove(playerMain) == 1) and (findMove(playerOpp) == 3)): #GRAB / KICK 
            dmg1, dmg2 = random.randint(1, 3), random.randint(4, 8)
            stam1, stam2 = random.randint(12, 12), random.randint(15, 25) 
            actMain, actOpp = "Grab", "Kick"

          elif ((findMove(playerMain) == 1) and (findMove(playerOpp) == 4)): #GRAB / BLOCK 
            dmg1, dmg2 = random.randint(8, 12), random.randint(0, 0)
            stam1, stam2 = random.randint(12, 12), random.randint(-12, -8)
            actMain, actOpp = "Grab", "Block"

          #P2 PUNCH
          elif ((findMove(playerMain) == 2) and (findMove(playerOpp) == 1)): #PUNCH / GRAB 
            dmg1, dmg2 = random.randint(8, 12), random.randint(1, 5)
            stam1, stam2 = random.randint(8, 12), random.randint(12, 12) 
            actMain, actOpp = "Punch", "Grab"

          elif ((findMove(playerMain) == 2) and (findMove(playerOpp) == 2)): #PUNCH / PUNCH  
            dmg1, dmg2 = random.randint(5, 12), random.randint(5, 12)
            stam1, stam2 = random.randint(8, 12), random.randint(8, 12) 
            actMain, actOpp = "Punch", "Punch"

          elif ((findMove(playerMain) == 2) and (findMove(playerOpp) == 3)): #PUNCH / KICK 
            dmg1, dmg2 = random.randint(5, 10), random.randint(16, 35)
            stam1, stam2 = random.randint(8, 12), random.randint(15, 25) 
            actMain, actOpp = "Punch", "Kick"

          elif ((findMove(playerMain) == 2) and (findMove(playerOpp) == 4)): #PUNCH / BLOCK 
            dmg1, dmg2 = random.randint(3,8), random.randint(0, 3)
            stam1, stam2 = random.randint(8, 12), random.randint(-12, -8)
            actMain, actOpp = "Punch", "Block"

          #P3 KICK
          elif ((findMove(playerMain) == 3) and (findMove(playerOpp) == 1)): #KICK / GRAB 
            dmg1, dmg2 = random.randint(4, 8), random.randint(1, 3)
            stam1, stam2 = random.randint(15, 25), random.randint(12, 12) 
            actMain, actOpp = "Kick", "Grab" 

          elif ((findMove(playerMain) == 3) and (findMove(playerOpp) == 2)): #KICK / PUNCH 
            dmg1, dmg2 = random.randint(16, 35), random.randint(5, 10)
            stam1, stam2 = random.randint(15, 25), random.randint(8, 12) 
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
            stam1, stam2 = random.randint(-12, -8), random.randint(8, 12) 
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
          if(random.randint(1, 20) == 1):
            if (actMain == "Block"):
              dmg2 = round(random.randint(-8,-5) * random.uniform(2.1, 3.1))
            else:
              dmg1 = round((dmg1+2) * random.uniform(1.4, 1.6))
            crit1 = " Enchanted🔮"
            print("crit")

          elif(random.randint(1, 20) == 10):
            if (actOpp == "Block"):
              dmg1 = round((random.randint(-8,-5)) * random.uniform(2.1, 3.1))
            else:  
              dmg2 = round((dmg2+2) * random.uniform(1.4, 1.6))
            crit2 = " Enchanted🔮"
            print("crit")
          
          if (random.randint(1, 40) == 20):
            if (actMain == "Block"):
              dmg2 = round((random.randint(-10,-8)) * random.uniform(2.1, 3.1))
            else: 
              dmg1 = round((abs(dmg1)+8) * random.uniform(1.6, 1.8))
            crit1 = crit1 + " Dark Magic🌒"
            print("Demon crit")

          elif (random.randint(1,40) == 2):
            if (actOpp == "Block"):
              dmg1 = round((random.randint(-10,-8)) * random.uniform(2.1, 3.1))
            else:  
              dmg2 = round((abs(dmg2)+8) * random.uniform(1.6, 1.8))
            crit2 = crit2 + " Dark Magic🌒"
            print("Demon crit")

          if ((actMain == "Block") and ((findStamina(playerOpp) - stam2) < 0)): 
            updateHealth(playerMain, int(findHealth(playerMain)))  #opponent inflicted
            updateHealth(playerOpp, int(findHealth(playerOpp)))
            updateStamina(playerMain, int(findStamina(playerMain)) - (-10)) #self-inflicted
            updateStamina(playerOpp, int(findStamina(playerOpp)) - (-10))
            actOpp = "Tired😴 Block"
            dmg1, dmg2 = 0,0 

          elif ((actOpp == "Block") and ((findStamina(playerMain) - stam1) < 0)):
            updateHealth(playerMain, int(findHealth(playerMain)))  #opponent inflicted
            updateHealth(playerOpp, int(findHealth(playerOpp)))
            updateStamina(playerMain, int(findStamina(playerMain)) - (-10)) #self-inflicted
            updateStamina(playerOpp, int(findStamina(playerOpp)) - (-10))
            actMain = "Tired😴 Block"
            dmg1, dmg2 = 0,0 

          elif ((findStamina(playerMain) - stam1) < 0):
            updateHealth(playerMain, int(findHealth(playerMain)) - round((dmg2+4)*2.5))  #opponent inflicted
            updateHealth(playerOpp, int(findHealth(playerOpp)))
            updateStamina(playerMain, int(findStamina(playerMain)) - (-10)) #self-inflicted
            updateStamina(playerOpp, int(findStamina(playerOpp)) - stam2)
            dmg1, dmg2 = 0, round((dmg2+4)*2.5)
            actMain = "Tired😴 Block"

          elif ((findStamina(playerOpp) - stam2) < 0):
            updateHealth(playerMain, int(findHealth(playerMain)))  #opponent inflicted
            updateHealth(playerOpp, int(findHealth(playerOpp)) - round((dmg1+4)*2.5))
            updateStamina(playerMain, int(findStamina(playerMain)) - stam1) #self-inflicted
            updateStamina(playerOpp, int(findStamina(playerOpp)) - (-10))
            dmg1, dmg2 = round((dmg1+4)*2.5), 0
            actOpp = "Tired😴 Block"

          elif (((findStamina(playerOpp) - stam2) < 0) and ((findStamina(playerMain) - stam1) < 0)):
            updateHealth(playerMain, int(findHealth(playerMain)))  #opponent inflicted
            updateHealth(playerOpp, int(findHealth(playerOpp)))
            updateStamina(playerMain, int(findStamina(playerMain)) - (-10)) #self-inflicted
            updateStamina(playerOpp, int(findStamina(playerOpp)) - (-10))
            dmg1, dmg2 = 0,0 
            actMain, actOpp = "Tired😴 Block", "Tired😴 Block"

          else: 
            updateHealth(playerMain, int(findHealth(playerMain)) - dmg2)  #opponent inflicted
            updateHealth(playerOpp, int(findHealth(playerOpp)) - dmg1)

            updateStamina(playerMain, int(findStamina(playerMain)) - stam1) #self-inflicted
            updateStamina(playerOpp, int(findStamina(playerOpp)) - stam2)

          #Handling for sub-zero/sur-100 Stamina/health and "Give Up" input

          if (findHealth(playerMain)>100):
            updateHealth(playerMain, 100)
          if (findHealth(playerOpp)>100):
            updateHealth(playerOpp, 100)
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
            updateHealth(playerMain, -1)
          if ((findMove(playerOpp) == 5)):
            updateHealth(playerOpp, -1)

          updateMove(playerOpp,0)
          updateMove(playerMain,0)
          moveMain, moveOpp = "📜", "📜"
          
        if ((findHealth(playerMain) < 1) and (findHealth(playerOpp) < 1)):
          embedVictory.set_field_at(0,name="You two drunkards knocked each other out! Look at this mess in the tavern ⚔️", value=finalPhrase, inline=True)
          embedDescription(embedVictory,playerOpp, playerMain, actMain, actOpp, dmg1, dmg2, crit1, crit2) 
          await interaction.edit_origin(embed=embedVictory,components=action_victory)
          resetMechanic(playerMain, playerOpp)

        elif (findHealth(playerMain)<0):
          embedVictory.set_field_at(0,name="What a brawl, yet only " + playerOpp + " stands victorious! ⚔️", value="The bards will write songs of this battle 📯", inline=True) 
          embedVictory.set_footer(text = playerMain + " fled the tavern, what a shame!")
          await interaction.edit_origin(embed=embedVictory,components=action_victory)
          incrementLeaderboard(playerMain, 'l')
          incrementLeaderboard(playerOpp, 'w')
          resetMechanic(playerMain, playerOpp)

        elif (findHealth(playerOpp)<0):
          embedVictory.set_field_at(0,name="What a brawl, yet only " + playerMain + " stands victorious! ⚔️",value="The bards will write songs of this battle 📯", inline=True) 
          embedVictory.set_footer(text = playerOpp + " fled the tavern, what a shame!")
          await interaction.edit_origin(embed=embedVictory,components=action_victory)
          incrementLeaderboard(playerMain, 'w')
          incrementLeaderboard(playerOpp, 'l')
          resetMechanic(playerMain, playerOpp)

        elif (findHealth(playerMain)<1):
          embedVictory.set_field_at(0,name="What a brawl, yet only " + playerOpp + " stands victorious! ⚔️", value="The bards will write songs of this battle 📯", inline=True) 
          embedDescription(embedVictory,playerOpp, playerMain, actMain, actOpp, dmg1, dmg2, crit1, crit2)
          incrementLeaderboard(playerMain, 'l')
          incrementLeaderboard(playerOpp, 'w')
          await interaction.edit_origin(embed=embedVictory,components=action_victory)
          resetMechanic(playerMain, playerOpp)

        elif (findHealth(playerOpp)<1):
          embedVictory.set_field_at(0,name="What a brawl, yet only " + playerMain + " stands victorious! ⚔️",value="The bards will write songs of this battle 📯", inline=True) 
          embedDescription(embedVictory,playerOpp, playerMain, actMain, actOpp, dmg1, dmg2, crit1, crit2)
          incrementLeaderboard(playerMain, 'w')
          incrementLeaderboard(playerOpp, 'l')
          await interaction.edit_origin(embed=embedVictory,components=action_victory)
          resetMechanic(playerMain, playerOpp)

        else:
          if ((moveMain  == "📜") and (moveOpp == "📜")):
            embedDescription(embedVar, playerOpp, playerMain, actMain, actOpp, dmg1, dmg2, crit1,crit2) 
          
          embedUpdate(embedVar,playerOpp,playerMain,moveMain,moveOpp)

          await interaction.edit_origin(embed=embedVar) #is   
      else: 
        await interaction.respond(content = "This is not your fight warrior!", ephemeral=True)
      
################################

def embedUpdate(embedVar,playerOpp,playerMain, moveMain, moveOpp): 
  embedVar.set_field_at(0, name=playerMain+moveMain, value="Health: {}  ❤️\n Stamina: {}  ⚡".format(findHealth(playerMain),findStamina(playerMain)), inline=True)

  embedVar.set_field_at(2, name=playerOpp+moveOpp, value="Health: {}  ❤️\n Stamina: {}  ⚡".format(findHealth(playerOpp),findStamina(playerOpp)), inline=True) 
  
  embedVar.set_footer(text=(str(findString(playerMain)) + "\n" + str(findString(playerOpp))))


def embedDescription (embedVar, playerOpp, playerMain, actMain, actOpp, dmg1, dmg2, crit1, crit2): 
  if (dmg1<0):
    updateString(playerMain, ("Somehow " + playerOpp + " heals " + str(abs(dmg1)) + " point(s)"))
    updateString(playerOpp, ("and " + playerOpp + " deals " + str(dmg2) + " damage to " + playerMain + " [ Mysterious" + crit2 + " " + actOpp + " ]⚗️!" ))

  elif (dmg2<0):
    updateString(playerMain, ("Somehow " + playerMain + " heals " + str(abs(dmg2)) + " point(s)"))
    updateString(playerOpp, ("and " + playerMain + " deals " + str(dmg1) + " damage to " + playerOpp +" [ Mysterious" + crit1 + " "+ actMain + " ]!⚗️" ))
  
  else:
    if ((actMain == "Tired😴 Block") or actOpp == ("Tired😴 Block")):
      updateString(playerMain, (playerMain + " deals " + str(dmg1) + " damage [" + crit1 +" " + actMain + " ]"))
      
      
      updateString(playerOpp, ("and " + playerOpp + " deals " + str(dmg2) + " damage [" + crit2 + " " + actOpp + " ]!🔥")) 

      #embedVar.set_footer(text=(playerMain + " deals " + str(dmg1) + " damage [" + crit1 +" " + actMain + " ] \nand " + playerOpp + " deals " + str(dmg2) + " damage [" + crit2 + " " + actOpp + " ]!🔥 \n🗡️ Tired Block😴 occured because stamina was too low!" ))
    else: 
      updateString(playerMain, playerMain + " deals " + str(dmg1) + " damage [" + crit1 +" " + actMain + " ]")
      updateString(playerOpp, "and " + playerOpp + " deals " + str(dmg2) + " damage [" + crit2 + " " + actOpp + " ]!🔥")
      
      #embedVar.set_footer(text=(playerMain + " deals " + str(dmg1) + " damage [" + crit1 +" " + actMain + " ] \nand " + playerOpp + " deals " + str(dmg2) + " damage [" + crit2 + " " + actOpp + " ]!🔥" ))
      
  embedVar.set_footer(text=(str(findString(playerMain)) + "\n" + str(findString(playerOpp))))

 
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
  
def createPlayer(username):
  df = pd.read_csv("healthStamina.csv")
  df = df.loc[df['name'] == username]
  if(not (len(df) == 0)):
    return False
  data = [[username, 100, 100, 0, int(time.time()),0,findbattleId()," "]]
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
  df = df.sort_values(['wins'], ascending=False)
  df.to_csv("leaderboard.csv",index = False)


def getTopTen():
  sortLeaderboard()
  df = pd.read_csv("leaderboard.csv")
  df = (df.head(10))  

  return df

keep_alive()

client.run(os.getenv('TOKEN'))

