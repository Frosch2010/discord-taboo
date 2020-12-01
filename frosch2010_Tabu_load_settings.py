import os
import json

import frosch2010_Console_Utils as fCU

def load_settings(tabuSettings, file_path=None):

    fCU.log_In_Console("Try to load settings...", "LOAD-SETTINGS", "inf")

    if not file_path:

        file_path = "tabu-settings.txt"

    
    if os.path.isfile(file_path):

        with open(file_path) as json_file:

            data = json.load(json_file)

            try:

                tabuSettings.tabu_channelID_join = int(data["Channel-Settings"]["Join Channel-ID"])
                tabuSettings.tabu_channelID_team_1 = int(data["Channel-Settings"]["Team-1 Channel-ID"])
                tabuSettings.tabu_channelID_team_2 = int(data["Channel-Settings"]["Team-2 Channel-ID"])
                tabuSettings.tabu_channelID_add_terms = int(data["Channel-Settings"]["Add-Terms Channel-ID"])
                tabuSettings.tabu_channelID_bot_admin = int(data["Channel-Settings"]["Bot-Admin Channel-ID"])
                
                tabuSettings.tabu_bot_token = str(data["General-Settings"]["Bot-Token"])
                tabuSettings.tabu_default_save_terms = bool(data["General-Settings"]["Default-Save-Terms"])

                tabuSettings.tabu_default_points_to_win = int(data["Game-Settings"]["Default-Points-To-Win"])
                tabuSettings.tabu_round_lenght = int(data["Game-Settings"]["Round-Lenght"])
                tabuSettings.tabu_switching_lenght = int(data["Game-Settings"]["Switching-Lenght"])
                tabuSettings.tabu_min_players = int(data["Game-Settings"]["Min-Players"])

            except:

                fCU.log_In_Console("Failed to load settings!", "LOAD-SETTINGS", "err")
                fCU.log_In_Console("Shutdown bot. Please check the settings-file for errors.", "LOAD-SETTINGS", "inf")

                exit()

            fCU.log_In_Console("Settings successfully loaded.", "LOAD-SETTINGS", "inf")
    else:

        fCU.log_In_Console("No settings-file found...", "LOAD-SETTINGS", "err")
        fCU.log_In_Console("Shutdown bot. Please configure the bot.", "LOAD-SETTINGS", "inf")

        exit()