from frosch2010_Tabu_settings import tabu_settings
from random import shuffle
from random import randrange
import asyncio
import copy
import discord

import frosch2010_Tabu_variables as fTV
import frosch2010_Console_Utils as fCU
import frosch2010_Discord_Utils as fDU
import frosch2010_Tabu_other_funtions as fTOF
import frosch2010_Class_Utils as fCLU
import frosch2010_Tabu_manage_timer as fMT

#-----------------------------------------------------

async def on_Start_Game(isRevengeStart, msg, tabuVars, tabuSettings, tabuLanguage, client):

    tabuVars.tabu_is_running = True

    #Start-Ausgabe
    fCU.log_In_Console("{} started game...".format(msg.author.name), "ON-START", "inf")

    if not isRevengeStart:
        await fDU.send_Message_To_Channel(tabuLanguage.tabu_user_started_game.replace("[USER_NAME]", str(msg.author.name)), [msg.channel])



    if isRevengeStart:
        tabuVars.tabu_points_to_win = tabuVars.tabu_last_points_to_win

    else:
        tabuVars.tabu_points_to_win = tabu_settings.tabu_default_points_to_win



    #Abfrage, ob Points-To-WIN veraendert werden soll
    args = msg.content.split(" ")

    if len(args) >= 3:

        try:

            tabuVars.tabu_points_to_win = int(args[2])

            fCU.log_In_Console("{} set points to win to: {}".format(msg.author.name, str(tabuVars.tabu_points_to_win)), "ON-START", "inf")

        except:
            
            fCU.log_In_Console("{} cant set points to win. Cant parse point-count from arguments.".format(msg.author.name), "ON-START", "err")


    tabuVars.tabu_last_points_to_win = tabuVars.tabu_points_to_win


    #Loesche Nachrichten in Team-Channels
    fCU.log_In_Console("Delete messages for team 1 and 2...", "ON-START", "inf")

    await fDU.delete_Messages_From_Channel([client.get_channel(tabuSettings.tabu_channelID_team_1), client.get_channel(tabuSettings.tabu_channelID_team_2)])


    #Loesche Nachrichten in allen Privat-Channels der Spieler mit dem Bot
    fCU.log_In_Console("Delete messages for all players...", "ON-START", "inf")

    channels = []

    for player in tabuVars.tabu_player_list_all:

        await player.create_dm()

        channels.append(client.get_channel(player.dm_channel.id))

    await fDU.delete_Messages_From_Channel(channels, 4)


    #Spieler in Teams aufteilen
    fCU.log_In_Console("Shuffel playerlist and split them in teams...", "ON-START", "inf")

    shuffle(tabuVars.tabu_player_list_all)

    team_size = (len(tabuVars.tabu_player_list_all) / 2)

    tabuVars.tabu_player_list_team_1 = tabuVars.tabu_player_list_all[:int(team_size)]
    tabuVars.tabu_player_list_team_2 = tabuVars.tabu_player_list_all[int(team_size):]

    if not isRevengeStart:
        await fTOF.print_Who_Which_Team(tabuVars, msg.channel)

    #Start Team bestimmen
    fCU.log_In_Console("Set start team...", "ON-START", "inf")

    tabuVars.tabu_guessing_team_num = randrange(0,1)
    tabuVars.tabu_start_team_num = tabuVars.tabu_guessing_team_num


    #Zeit pro Runde setzen + Timer starten
    fCU.log_In_Console("Starting timer...", "ON-START", "inf")

    tabuVars.tabu_current_time = copy.deepcopy(tabuSettings.tabu_round_lenght)
    fCLU.Timer(1, fMT.manage_timer, [tabuVars, tabuSettings, tabuLanguage, client])


    #Timer-Nachrichten an alle senden
    fCU.log_In_Console("Sending countdown-messages...", "ON-START", "inf")

    await fTOF.send_Team_Countdowns(tabuVars, tabuSettings, tabuLanguage, client)
    await fTOF.send_Explainer_Countdown(tabuVars, tabuLanguage)


    #Fertig
    fCU.log_In_Console("Started successfully...", "ON-START", "inf")

    await fTOF.send_New_Word_Card(tabuVars, tabuSettings, tabuLanguage, client)