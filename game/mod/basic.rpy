init 1:#Mod Defaults
    define gui.mod_dev = "JiGSaW Games Studios"
    define gui.jg_mod_version = '0.7'
    define gui.mod_update_version = 1
    define gui.mod_update_date = "12/10/2024"
    define gui.mod_update_url = "https://github.com/JiGSaWKilla89/abnormal_mod/releases"
    define gui.mod_check_url = 'https://raw.githubusercontent.com/JiGSaWKilla89/abnormal_mod/main/version'
    default mod_changelog = read_changelog()
    default mod_updated = "None", gui.jg_mod_version


init 1:#Defines
    define gui.slot_delete_text_idle_color = "#F00"
    define gui.slot_delete_text_outlines = [(2, "#0009", 1, 1)]
    define gui.input_prompt_text_outlines = [ (2, "#00000080", 0, 0) ]
    define gui.input_button_text_outlines = [ (2, "#00000080", 0, 0) ]
    define gui.quick_button_text_outlines = [(2, "#0009", 1, 1)]
    
    define config.end_game_transition = dissolve
    define config.end_splash_transition = dissolve
    define config.enter_replay_transition = dissolve
    define config.exit_replay_transition = dissolve
    define config.after_load_transition = dissolve
    define config.end_game_transition = dissolve
    define config.game_main_transition = dissolve
    define config.main_game_transition = dissolve

init -5 python:
    import requests
    import json
    from datetime import datetime

    def read_changelog():
        path = os.path.join(config.gamedir, "mod", "MODCHANGELOG")

        try:
            with open(path, "r") as f:
                return f.readlines()
        except:
            return []

    def write_changelog(line):
        path = os.path.join(config.gamedir, "mod", "MODCHANGELOG")

        data = read_changelog()

        with open(path, "a") as f:
            if not f"{line}\n" in data:
                f.write(f"{line}\n")

    def get_latest_mod():
        global mod_changelog
        # URL of the file containing the dictionary
        
        response = None  # Initialize response to None

        # Fetch the file from the URL
        try:
            response = requests.get(gui.mod_check_url)

            # Check if the request was successful
            if response.status_code == 200:
                try:
                    # Load the JSON data into a Python dictionary
                    data = json.loads(response.text)

                    web_date = data["date_update"]
                    web_version_game = data["version_game"]
                    web_version = data["version_update"]

                    for i in data["changelog"]:
                        write_changelog(i)

                    mod_changelog = read_changelog()

                    if gui.jg_mod_version != web_version_game:
                        return "Mod game version changed"
                    elif gui.mod_update_version != web_version:
                        return "Mod version changed", web_version_game
                    elif gui.mod_update_date != web_date:
                        return "Update date has changed", web_version_game
                    elif config.version > web_version_game:
                        return "Game Version Newer Than Mod", config.version
                    else:
                        return "Mod up-to-date", gui.jg_mod_version
                except json.JSONDecodeError as e:
                    return "JSON Error", gui.jg_mod_version
            else:
                return "Could Not Connect to Host"
        except requests.ConnectionError as ce:
            if response is not None:
                renpy.write_log(f"HTTP Error: Received status code {response.status_code}: {ce}")
            else:
                renpy.write_log(f"Connection Error: {ce}")
            return "HTTP Error", gui.jg_mod_version

        except requests.Timeout as rto:
            renpy.write_log(f"Timeout: The request timed out {rto}")
            return "Timeout", gui.jg_mod_version

        except requests.RequestException as e:
            renpy.write_log(f"Request Error: {e}")
            return "Request Error", gui.jg_mod_version
