##################################################################################################
## Check Screens to make sure we do not overwrite developers original                           ##
## screens                                                                                      ##
## Modify the following:                                                                        ##
##    'gui.jg_mod_version'                                                                      ##
##    'gui.dev_mod_page'                                                                        ##
##    'gui.mod_update_date'                                                                     ##
##    'gui.developer_name'                                                                      ##
##    'gui.developer_support'                                                                   ##
##################################################################################################
init 1:#Mod Defaults
    define gui.mod_dev = "JiGSaW Games Studios"
    define gui.jg_mod_version = '0.7'
    define gui.mod_update_version = 1
    define gui.dev_mod_page = "abnormal_mod"
    define gui.mod_update_date = "12/10/2024"
    define gui.mod_update_url = "https://github.com/JiGSaWKilla89/{}/releases".format(gui.dev_mod_page)
    define gui.mod_check_url = 'https://raw.githubusercontent.com/JiGSaWKilla89/{}/main/version'.format(gui.dev_mod_page)
    define gui.donate_mod = "https://buymeacoffee.com/jigsawgames"
    define gui.mod_issues = "https://github.com/JiGSaWKilla89/{}/issues/new/choose".format(gui.dev_mod_page)
    define gui.developer_name = "Emerald Deceivers"
    define gui.developer_support = "http://patreon.com/EmeraldDeceivers"
    default mod_changelog = read_changelog()
    default mod_updated = "None", gui.jg_mod_version

    define gui.mod_info_size = gui.title_text_size-20
    define gui.mod_savename_input_size = gui.text_size-10
    define gui.mod_savename_input_ypos = 10
    define gui.mod_savename_input_xpos = -30
    define gui.mod_save_page_input_ypos = -30
    define gui.mod_save_goto_page_xsize = 750
    define gui.mod_save_goto_page_ysize = 50

    define gui.use_custom_caret = False

    define gui.textbox_location = "mod/images/textbox.png"

default persistent._support_mod_display = True

style donate_mod_text:
    text_align 0.5
    align (0.5,0.5)
    outlines [(2, "#fff9", 1, 1)]

style donate_mod_vbox:
    align (0.5,0.5)
    spacing 10

style donate_mod_hbox:
    align (0.5,0.5)
    spacing 20

style donate_mod_button:
    align (0.5,0.5)

style donate_mod_button_text:
    text_align 0.5
    align (0.5,0.5)

screen support_mod_developer():
    style_prefix "donate_mod"
    default closing = 30

    button:
        action Return()
    if closing > 0:
        timer 1 action SetLocalVariable("closing", closing-1) repeat True
    if closing == 0:
        timer .1 action Return()
    text "Window Will Close in: %s"%closing align (0.01, 0.01)
    vbox:
        spacing 200
        vbox:
            text "{b}{u}[jg_1]JiG[jg_3][jg_2]SaW[jg_3] Multi-Mod{/u}{/b}" size gui.name_text_size
            text "for [config.name] Version: [gui.jg_mod_version]"
            text "Current Game Version: [config.version]" size gui.text_size-10 color "#FF0"
            text "If you enjoy using my mod please consider buying me a beer."
        hbox:
            textbutton "Buy Me a Beer" action OpenURL(gui.donate_mod)
            text " | "
            textbutton "Return to Game" action Return()
    
    key "dismiss" action Hide(),Return()
    key "toggle_skip" action Hide(),Return()
    key "skip" action Hide(),Return()

label before_main_menu:
    if persistent._support_mod_display:
        show screen support_mod_developer
        $ renpy.pause(hard=True)
    return

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

#Music Definitions

default persistent._main_menu_track = True #New

init python:
    config.default_music_volume = 0.5

init 999 python: #New
    config.has_music = True #New
    

init python:#New
    if persistent._main_menu_track is True:#New
        config.main_menu_music = PunchDeckAliveInstrumental#New
    else:#New
        config.main_menu_music = None#New
        renpy.music.stop(channel=u'music', fadeout=None)#New

init -5 python:
    # Initialize your musicroom
    mr = MusicRoom(fadeout=.5, fadein=0.5, loop=True, shuffle=True, single_track=False, channel="music")
    mrenergetic = MusicRoom(fadeout=.5, fadein=0.5, loop=True, shuffle=True, single_track=False, channel="music")
    mrchill = MusicRoom(fadeout=.5, fadein=0.5, loop=True, shuffle=True, single_track=False, channel="music")
    mrrelaxed = MusicRoom(fadeout=.5, fadein=0.5, loop=True, shuffle=True, single_track=False, channel="music")
    mrhappy = MusicRoom(fadeout=.5, fadein=0.5, loop=True, shuffle=True, single_track=False, channel="music")
    mrsad = MusicRoom(fadeout=.5, fadein=0.5, loop=True, shuffle=True, single_track=False, channel="music")

    playlist_data = [
        ("sorted_tracks_all", mr, 1, "All"), 
        ("sorted_tracks_energetic", mrenergetic, 2, "Energetic"),
        ("sorted_tracks_chill", mrchill, 3, "Chill"), 
        ("sorted_tracks_relaxed", mrrelaxed, 4, "Relaxed"),
        ("sorted_tracks_sad", mrsad, 5, "Sad"),
        ("sorted_tracks_happy", mrhappy, 6, "Happy"),
    ]

init 10 python:
    music_list = find_music()

    generate_track_list(music_list)

    add_to_playlist(mr)

    sorted_tracks_all = sorted_music_tracks(music_tracks, "All")#Edit Here
    sorted_tracks_energetic = sorted_music_tracks(music_tracks, "Energetic")#Edit Here
    sorted_tracks_chill = sorted_music_tracks(music_tracks, "Chill")#Edit Here
    sorted_tracks_relaxed = sorted_music_tracks(music_tracks, "Relaxed")#Edit Here
    sorted_tracks_happy = sorted_music_tracks(music_tracks, "Happy")#Edit Here
    sorted_tracks_sad = sorted_music_tracks(music_tracks, "Sad")#Edit Here

init -1:
    python:
        """
        define TrackName = AudioCredits( #Template
            "", #Title
            "", #Artist
            "mod/music/.ogg", #Path
            "", #Link
            "", #Link URL
            "", #Description
            "", #License
            "", #License URL
            "Relaxed" #Mood
        )

        define TrackName = AudioCredits(
            "",
            "",
            "mod/music/.ogg",
            "",
            "",
            "",
            "",
            "",
            "Relaxed"
        )
        """
    
    define AlexanderNakaradaEmotionalPiano = AudioCredits(
        "Emotional Piano Improvisation",
        "Alexander Nakarada",
        "mod/music/Alexander Nakarada - Emotional Piano Improvisation.ogg",
        "Film Music",
        "https://filmmusic.io/song/6199-emotional-piano-improvisation",
        "",
        "Film Music License",
        "https://filmmusic.io/standard-license",
        "Relaxed"
        )
    define BensoundADayToRemember = AudioCredits(
        "A Day To Remember",
        "Bensound",
        "mod/music/Bensound - A Day To Remember.ogg",
        "Bensound",
        "https://www.bensound.com/royalty-free-music/track/a-day-to-remember-wedding-music",
        "",
        "Bensound",
        "https://www.bensound.com",
        "Happy"
        )
    define BensoundAdventure = AudioCredits(
        "Adventure",
        "Bensound",
        "mod/music/Bensound - Adventure.ogg",
        "Bensound",
        "https://www.bensound.com/royalty-free-music/track/adventure",
        "",
        "Bensound",
        "https://www.bensound.com",
        "Happy"
        )
    define BensoundBeyondTheLine = AudioCredits(
        "Beyond The Line",
        "Bensound",
        "mod/music/Bensound - Beyond The Line.ogg",
        "Bensound",
        "https://www.bensound.com/royalty-free-music/track/beyond-the-line",
        "",
        "Bensound",
        "https://www.bensound.com",
        "Happy"
        )
    define BensoundMemories = AudioCredits(
        "Memories",
        "Bensound",
        "mod/music/Bensound - Memories.ogg",
        "Bensound",
        "https://www.bensound.com/royalty-free-music/track/memories",
        "",
        "Bensound",
        "https://www.bensound.com",
        "Happy"
        )
    define BensoundTenderness = AudioCredits(
        "Tenderness",
        "Bensound",
        "mod/music/Bensound - Tenderness.ogg",
        "Bensound",
        "https://www.bensound.com/royalty-free-music/track/tenderness",
        "",
        "Bensound",
        "https://www.bensound.com",
        "Relaxed"
        )
    define KevinMacLeodCarefree = AudioCredits(
        "Carefree",
        "Kevin Macleod", 
        "mod/music/Kevin MacLeod - Carefree.ogg", 
        "Film Music", 
        "https://incompetech.filmmusic.io/song/3476-carefree", 
        "", 
        "Film Music License", 
        "https://filmmusic.io/standard-license", 
        "Happy"
        )
    define KevinMacLeodColdFunk = AudioCredits(
        "Cold Funk",
        "Kevin Macleod", 
        "mod/music/Kevin MacLeod - Cold Funk.ogg", 
        "Film Music", 
        "https://incompetech.filmmusic.io/song/3522-cold-funk", 
        "", 
        "Film Music License", 
        "https://filmmusic.io/standard-license", 
        "Energetic"
        )
    define KevinMacLeodMidsummerSky = AudioCredits(
        "Midsummer Sky",
        "Kevin Macleod", 
        "mod/music/Kevin MacLeod - Midsummer Sky.ogg", 
        "Film Music", 
        "https://incompetech.filmmusic.io/song/4049-midsummer-sky", 
        "", 
        "Film Music License", 
        "https://filmmusic.io/standard-license", 
        "Happy"
        )
    define KevinMacLeodRavingEnergy = AudioCredits(
        "Raving Energy",
        "Kevin Macleod", 
        "mod/music/Kevin MacLeod - Raving Energy.ogg", 
        "Film Music", 
        "https://filmmusic.io/song/5029-raving-energy", 
        "", 
        "Film Music License", 
        "https://filmmusic.io/standard-license", 
        "Energetic"
        )
    define KevinMacLeodRealizer = AudioCredits(
        "Realizer",
        "Kevin Macleod", 
        "mod/music/Kevin MacLeod - Realizer.ogg", 
        "Film Music", 
        "https://filmmusic.io/song/5047-realizer", 
        "", 
        "Film Music License", 
        "https://filmmusic.io/standard-license", 
        "Energetic"
        )
    define KevinMacLeodWiththeSea = AudioCredits(
        "With the Sea",
        "Kevin Macleod", 
        "mod/music/Kevin MacLeod - With the Sea.ogg", 
        "Film Music", 
        "https://incompetech.filmmusic.io/song/4638-with-the-sea", 
        "", 
        "Film Music License", 
        "https://filmmusic.io/standard-license", 
        "Energetic"
        )
    define PunchDeck808Lotus = AudioCredits(
        "808 Lotus",
        "Punch Deck",
        "mod/music/Punch Deck - 808 Lotus.ogg",
        "Soundcloud",
        "https://soundcloud.com/punch-deck",
        "",
        "CC BY 3.0",
        "http://creativecommons.org/licenses/by/3.0/",
        "Energetic"
        )
    define PunchDeckAimless = AudioCredits(
        "Aimless",
        "Punch Deck",
        "mod/music/Punch Deck - Aimless Lyrics.ogg",
        "Soundcloud",
        "https://soundcloud.com/punch-deck",
        "",
        "CC BY 3.0",
        "http://creativecommons.org/licenses/by/3.0/",
        "Energetic"
        )
    define PunchDeckAliveInstrumental = AudioCredits(
        "Alive (Instrumental)",
        "Punch Deck",
        "mod/music/Punch Deck - Alive (Instrumental).ogg",
        "Soundcloud",
        "https://soundcloud.com/punch-deck",
        "",
        "CC BY 3.0",
        "http://creativecommons.org/licenses/by/3.0/",
        "Relaxed"
        )
    define PunchDeckClose = AudioCredits(
        "Close",
        "Punch Deck",
        "mod/music/Punch Deck - Close.ogg", 
        "Soundcloud",
        "https://soundcloud.com/punch-deck",
        "", 
        "CC BY 3.0",
        "http://creativecommons.org/licenses/by/3.0/",
        "Happy"
        )
    define PunchDeckDream13 = AudioCredits(
        "Dream 13",
        "Punch Deck",
        "mod/music/Punch Deck - Dream 13.ogg", 
        "Soundcloud",
        "https://soundcloud.com/punch-deck",
        "", 
        "CC BY 3.0",
        "http://creativecommons.org/licenses/by/3.0/",
        "Relaxed"
        )
    define PunchDeckDrive = AudioCredits(
        "Drive",
        "Punch Deck",
        "mod/music/Punch Deck - Drive.ogg", 
        "Soundcloud",
        "https://soundcloud.com/punch-deck",
        "", 
        "CC BY 3.0",
        "http://creativecommons.org/licenses/by/3.0/",
        "Energetic"
        )
    define PunchDeckFrozenShimmer = AudioCredits(
        "Frozen Shimmer",
        "Punch Deck",
        "mod/music/Punch Deck - Frozen Shimmer.ogg", 
        "Soundcloud",
        "https://soundcloud.com/punch-deck",
        "", 
        "CC BY 3.0",
        "http://creativecommons.org/licenses/by/3.0/",
        "Sad"
        )
    define PunchDeckICantStop = AudioCredits(
        "I Can't Stop",
        "Punch Deck",
        "mod/music/Punch Deck - I Cant Stop.ogg", 
        "Soundcloud",
        "https://soundcloud.com/punch-deck",
        "", 
        "CC BY 3.0",
        "http://creativecommons.org/licenses/by/3.0/",
        "Energetic"
        )
    define PunchDeckLostintheVoid = AudioCredits(
        "Lost in the Void",
        "Punch Deck",
        "mod/music/Punch Deck - Lost in the Void.ogg", 
        "Soundcloud",
        "https://soundcloud.com/punch-deck",
        "", 
        "CC BY 3.0",
        "http://creativecommons.org/licenses/by/3.0/",
        "Chill"
        )
    define PunchDeckNeonDrive = AudioCredits(
        "Neon Drive",
        "Punch Deck",
        "mod/music/Punch Deck - Neon Drive.ogg", 
        "Soundcloud",
        "https://soundcloud.com/punch-deck",
        "", 
        "CC BY 3.0",
        "http://creativecommons.org/licenses/by/3.0/",
        "Chill"
        )
    define PunchDeckNeonUnderworld = AudioCredits(
        "Neon Underworl",
        "Punch Deck",
        "mod/music/Punch Deck - Neon Underworld.ogg", 
        "Soundcloud",
        "https://soundcloud.com/punch-deck",
        "", 
        "CC BY 3.0",
        "http://creativecommons.org/licenses/by/3.0/",
        "Chill"
        )
    define PunchDeckRise = AudioCredits(
        "Rise",
        "Punch Deck",
        "mod/music/Punch Deck - Rise.ogg", 
        "Soundcloud",
        "https://soundcloud.com/punch-deck",
        "", 
        "CC BY 3.0",
        "http://creativecommons.org/licenses/by/3.0/",
        "Energetic"
        )
    define PunchDeckVHSHeroes = AudioCredits(
        "VHS Heroes",
        "Punch Deck",
        "mod/music/Punch Deck - VHS Heroes.ogg", 
        "Soundcloud",
        "https://soundcloud.com/punch-deck",
        "", 
        "CC BY 3.0",
        "http://creativecommons.org/licenses/by/3.0/",
        "Energetic"
        )
    define PunchDeckWalkWiththeFire = AudioCredits(
        "Walk With The Fire",
        "Punch Deck",
        "mod/music/Punch Deck - Walk With the Fire.ogg", 
        "Soundcloud",
        "https://soundcloud.com/punch-deck",
        "", 
        "CC BY 3.0",
        "http://creativecommons.org/licenses/by/3.0/",
        "Energetic"
        )
    define SaschaEndeAfterEarth = AudioCredits(
        "After Earth",
        "Sascha Ende",
        "mod/music/Sascha Ende - After Earth.ogg",
        "Film Music",
        "https://filmmusic.io/song/154-after-earth",
        "",
        "Film Music License",
        "https://filmmusic.io/standard-license",
        "Chill"
        )
    define SaschaEndeInTheMoment = AudioCredits(
        "In The Moment",
        "Sascha Ende",
        "mod/music/Sascha Ende - In The Moment.ogg",
        "Film Music",
        "https://filmmusic.io/song/287-in-the-moment",
        "",
        "Film Music License",
        "https://filmmusic.io/standard-license",
        "Chill"
        )
    define SaschaEndeLetMeBeFree = AudioCredits(
        "Let Me Be Free",
        "Sascha Ende",
        "mod/music/Sascha Ende - Let Me Be Free.ogg",
        "Film Music",
        "https://filmmusic.io/song/164-let-me-be-free",
        "",
        "Film Music License",
        "https://filmmusic.io/standard-license",
        "Energetic"
        )
    define SaschaEndeVibesInParadise = AudioCredits(
        "Vibes Is Paradise",
        "Sascha Ende",
        "mod/music/Sascha Ende - Vibes In Paradise.ogg",
        "Film Music",
        "https://filmmusic.io/song/434-vibes-in-paradise",
        "",
        "Film Music License",
        "https://filmmusic.io/standard-license",
        "Energetic"
        )
    define ScottBuckleyANewYear = AudioCredits(
        "A New year",
        "Scott Buckley",
        "mod/music/Scott Buckley - A New Year.ogg",
        "Soundcloud",
        "https://soundcloud.com/scottbuckley/a-new-year-cc-by",
        "",
        "CC BY 4.0",
        "https://creativecommons.org/licenses/by/4.0/",
        "Relaxed"
        )
    define ScottBuckleyAscension = AudioCredits(
        "Ascension",
        "Scott Buckley",
        "mod/music/Scott Buckley - Ascension.ogg",
        "Soundcloud",
        "https://soundcloud.com/scottbuckley/ascension-cc-by",
        "",
        "CC BY 4.0",
        "https://creativecommons.org/licenses/by/4.0/",
        "Sad"
        )
    define ScottBuckleyGrowingUp = AudioCredits(
        "Growing Up",
        "Scott Buckley",
        "mod/music/Scott Buckley - Growing Up.ogg",
        "Soundcloud",
        "https://soundcloud.com/scottbuckley/growing-up-cc-by",
        "",
        "CC BY 4.0",
        "https://creativecommons.org/licenses/by/4.0/",
        "Happy"
        )
    define ScottBuckleyIcarus = AudioCredits(
        "Icarus",
        "Scott Buckley",
        "mod/music/Scott Buckley - Icarus.ogg",
        "Soundcloud",
        "https://soundcloud.com/scottbuckley/icarus-cc-by",
        "",
        "CC BY 4.0",
        "https://creativecommons.org/licenses/by/4.0/",
        "Happy"
        )
    define ScottBuckleyNightfall = AudioCredits(
        "Nightfall",
        "Scott Buckley",
        "mod/music/Scott Buckley - Nightfall.ogg",
        "Soundcloud",
        "https://soundcloud.com/scottbuckley/nightfall-cc-by",
        "",
        "CC BY 4.0",
        "https://creativecommons.org/licenses/by/4.0/",
        "Sad"
        )
    define ScottBuckleyPassage = AudioCredits(
        "Passage",
        "Scott Buckley",
        "mod/music/Scott Buckley - Passage.ogg",
        "Soundcloud",
        "https://soundcloud.com/scottbuckley/passage",
        "",
        "CC BY 4.0",
        "https://creativecommons.org/licenses/by/4.0/",
        "Sad"
        )
    define ScottBuckleyResonance = AudioCredits(
        "Resonance",
        "Scott Buckley",
        "mod/music/Scott Buckley - Resonance.ogg",
        "Soundcloud",
        "https://soundcloud.com/scottbuckley/resonance-cc-by",
        "",
        "CC BY 4.0",
        "https://creativecommons.org/licenses/by/4.0/",
        "Energetic"
        )
    define ScottBuckleyStarsInHerSkies = AudioCredits(
        "Stars in Her Skies",
        "Scott Buckley",
        "mod/music/Scott Buckley - Stars In Her Skies.ogg",
        "Soundcloud",
        "https://soundcloud.com/scottbuckley/stars-in-her-skies",
        "",
        "CC BY 4.0",
        "https://creativecommons.org/licenses/by/4.0/",
        "Chill"
        )
    define ScottBuckleyTitan = AudioCredits(
        "Titan",
        "Scott Buckley",
        "mod/music/Scott Buckley - Titan.ogg",
        "Soundcloud",
        "https://soundcloud.com/scottbuckley/titan-cc-by",
        "",
        "CC BY 4.0",
        "https://creativecommons.org/licenses/by/4.0/",
        "Happy"
        )
    define ScottBuckleyWhereStarsFall = AudioCredits(
        "Where Stars Fall",
        "Scott Buckley",
        "mod/music/Scott Buckley - Where Stars Fall.ogg",
        "Soundcloud",
        "https://soundcloud.com/scottbuckley/where-stars-fall-cc-by",
        "",
        "CC BY 4.0",
        "https://creativecommons.org/licenses/by/4.0/",
        "Energetic"
        )
    