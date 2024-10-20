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
    