init -1500 python early:
    import os
    import zipfile
    zip_path = os.path.join(config.gamedir, "mod", "mutagen.zip")
    zip_directory = os.path.join(config.gamedir, "python-packages")
    zip_final = os.path.join(zip_directory, "mutagen")

    def extract_packages(zip_path, directory, zip_final):

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(directory)

        if os.path.exists(zip_final):
            os.unlink(zip_path)

    if os.path.exists(zip_path):
        extract_packages(zip_path, zip_directory, zip_final)

init python:
    shortcuts = """
{size=75}{color=FB4301}JiG{/color}{color=#000}SaW{/color} Mod Shortcuts{/size}

Toggle Textbox Shortcut: {color=FB4301}T{/color}
Toggle Choice Hotkeys: {color=FB4301}C{/color}
Toggle Custom Savenames: {color=FB4301}Shift+S{/color}
Toggle Fancy Text: {color=FB4301}Shift+F{/color}
Toggle Fancy Text Effect: {color=FB4301}E{/color}
Toggle Fancy Text Always Effect: {color=FB4301}R{/color}
Toggle Walkthrough: {color=FB4301}W{/color}
Toggle Walkthrough Choice Tooltips: {color=FB4301}Shift+T{/color}
Toggle Cheat Mod: {color=FB4301}END{/color}
Toggle Music Room: {color=FB4301}M{/color}
Toggle Notifications Stack/Standard: {color=FB4301}N{/color}
Adjust Textbox Visibility Keypad {color=FB4301}+/-{/color}
"""

    wt_choice_tooltip = """Each Choice marked with either Good Choice/Bad Choice is
just a recommendation from me.
You play the game the way you want."""

init -5 python:
    
    import operator
    import time
    config.developer = True
    config.console = True
    config.autoreload = True
    config.rollback_length = 100
    config.hard_rollback_limit = 150

    if not persistent._default_replays:
        persistent._default_replays = False

    if not persistent._always_effect_title:
        persistent._always_effect_title = "None"

    if not persistent._slow_effect_title:
        persistent._slow_effect_title = "Fade"

    if not persistent._effect_delay:
        persistent._effect_delay = 0.2

    if persistent._fancy_text == None:
        persistent._fancy_text = True

    if persistent._quick_menu_state == None:
        persistent._quick_menu_state = "visible"

    if persistent._quick_menu_layout == None:
        persistent._quick_menu_layout = "bottom_center"

    if persistent._choice_hotkeys == None:
        persistent._choice_hotkeys = True
    
    if persistent._walkthrough == None:
        persistent._walkthrough = True

    if persistent._choice_tooltips == None:
        persistent._choice_tooltips = True

    if persistent._textbox_visible == None:
        persistent._textbox_visible = True

    if persistent._textbox_alpha == None:
        persistent._textbox_alpha = 0.5

    if persistent._custom_savename == None:
        persistent._custom_savename = True

    bypass_list = [
        "ADVCharacter", "ADVSpeaker", "Action", "AddToSet", "Alpha", "AlphaBlend", "AlphaDissolve", 
        "AlphaMask", "AlwaysEffectChange", "AnimatedValue", "Animation", "At", "Attribute", "AudioData", 
        "AudioPositionValue", "AutoForwardTime", "Bar", "BarValue", "Borders", "BrightnessMatrix", "Button", 
        "Call", "Camera", "CaptureFocus", "Character", "ClearFocus", "Color", "ColorMatrix", "ColorizeMatrix", 
        "ComposeTransition", "Composite", "Condition", "ConditionGroup", "ConditionSwitch", "Confirm", 
        "ContrastMatrix", "Crop", "CropMove", "CurrentScreenName", "CycleQuickMenu", "CycleQuickStates", 
        "DictEquality", "DictInputValue", "DictValue", "DisableAllInputValues", "Dissolve", "DownloadSync", 
        "Drag", "DragGroup", "DynamicCharacter", "DynamicDisplayable", "DynamicImage", "EffectDelayDisplay", 
        "EndReplay", "ExecJS", "FactorZoom", "Fade", "FancyCheck", "FancyText", "FieldEquality", "FieldInputValue", 
        "FieldValue", "FileAction", "FileCurrentPage", "FileCurrentScreenshot", "FileDelete", "FileJson", 
        "FileLoad", "FileLoadable", "FileNewest", "FilePage", "FilePageName", "FilePageNameInputValue", 
        "FilePageNext", "FilePagePrevious", "FileSave", "FileSaveName", "FileScreenshot", "FileSlotName", 
        "FileTakeScreenshot", "FileTime", "FileUsedSlots", "Fixed", "Flatten", "FontGroup", "Frame", "Function", 
        "Gallery", "GamepadCalibrate", "GamepadExists", "GetCharacterVolume", "GetFocusRect", "GetMixer", 
        "GetText", "GetTooltip", "Grid", "HBox", "Help", "Hide", "HideInterface", "HueMatrix", "IdentityMatrix", 
        "If", "Image", "ImageButton", "ImageDissolve", "ImageReference", "Input", "InputValue", "InvertMatrix", 
        "InvertSelected", "JSONDB", "Jump", "Language", "Layer", "LayeredImage", "LayeredImageProxy", "Live2D", 
        "LiveComposite", "LiveCrop", "LiveTile", "MainMenu", "Matrix", "MixerValue", "Model", "Motion", 
        "MouseDisplayable", "MouseMove", "Move", "MoveFactory", "MoveIn", "MoveOut", "MoveTransition", "Movie", 
        "MultiPersistent", "MultipleTransition", "MusicRoom", "NVLCharacter", "NVLSpeaker", "NoRollback", "Notify", 
        "Null", "NullAction", "OffsetMatrix", "OldMoveTransition", "OpacityMatrix", "OpenDirectory", "OpenURL", 
        "PY2", "Pan", "ParameterizedText", "Particles", "Pause", "PauseAudio", "Pixellate", "Placeholder", "Play", 
        "PlayCharacterVoice", "Position", "Preference", "PushMove", "Queue", "QueueEvent", "QuickLoad", 
        "QuickPositions", "QuickSave", "Quit", "RemoveFromSet", "Replay", "RestartStatement", "Return", "Revolve", 
        "RevolveInOut", "RollForward", "Rollback", "RollbackToIdentifier", "RotateMatrix", "RotoZoom", "RoundRect", 
        "SaturationMatrix", "ScaleMatrix", "ScreenVariableInputValue", "ScreenVariableValue", "Screenshot", 
        "Scroll", "SelectedIf", "SensitiveIf", "SepiaMatrix", "Set", "SetCharacterVolume", "SetDict", "SetField", 
        "SetLocalVariable", "SetMixer", "SetMute", "SetScreenVariable", "SetVariable", "SetVoiceMute", "Show", 
        "ShowMenu", "ShowTransient", "ShowingSwitch", "SideImage", "SizeZoom", "Skip", "SlottedNoRollback", 
        "SlowEffectChange", "SnowBlossom", "Solid", "Speaker", "SplineMotion", "Sprite", "SpriteManager", "Start", 
        "StaticValue", "Stop", "Style", "StylePreference", "SubTransition", "Swing", "Text", "TextBoxAlpha", 
        "TextButton", "TextSpeed", "Tile", "TintMatrix", "ToggleChoiceHotkeys", "ToggleDict", "ToggleFancyText", 
        "ToggleField", "ToggleFocus", "ToggleLocalVariable", "ToggleMute", "ToggleScreen", "ToggleScreenVariable", 
        "ToggleSetMembership", "ToggleVariable", "ToggleVoiceMute", "Tooltip", "Transform", "TransformMatrix", 
        "Unlock_Replays", "UploadSync", "VBox", "VariableInputValue", "VariableValue", "Viewport", "VoiceInfo", 
        "VoiceReplay", "VolumeDisplay", "WalkthroughData", "Window", "With", "XScrollValue", "YScrollValue", 
        "Zoom", "ZoomInOut", "absolute", "absolute_import", "achievement", "alt", "anim", "audio", "basestring", 
        "bchr", "blinds", "bord", "bubble", "build", "bypass_list", "center", "chr", "collections", "color", 
        "config", "default", "default_transition", "define", "delayed_blink", "dict", "director", "dissolve", 
        "division", "ease", "easeinbottom", "easeinleft", "easeinright", "easeintop", "easeoutbottom", 
        "easeoutleft", "easeoutright", "easeouttop", "eval", "extend", "fade", "flash", "gui", "hpunch", 
        "hyperlink_function", "hyperlink_sensitive", "hyperlink_styler", "iap", "icon", "im", "input", "inspect", 
        "irisin", "irisout", "layeredimage", "layout", "left", "library", "list", "main_menu", "menu", 
        "mouse_visible", "move", "moveinbottom", "moveinleft", "moveinright", "moveintop", "moveoutbottom", 
        "moveoutleft", "moveoutright", "moveouttop", "custom_notify_appear", "nvl_clear", "nvl_clear_next", "nvl_erase", 
        "nvl_hide", "nvl_list", "nvl_menu", "nvl_show", "nvl_show_core", "nvl_variant", "nvl_window", "object", 
        "offscreenleft", "offscreenright", "open", "os", "persistent", "pixellate", "predict_menu", "predict_say", 
        "preferences", "print", "print_function", "pushdown", "pushleft", "pushright", "pushup", "pygame_sdl2", 
        "pystr", "python_dict", "python_list", "python_object", "python_set", "quick_menu", "range", "raw_input", 
        "renpy", "reset", "right", "round", "say", "set", "set_reload", "slideawaydown", "slideawayleft", 
        "slideawayright", "slideawayup", "slidedown", "slideleft", "slideright", "slideup", "small", "sorted", 
        "squares", "store", "str", "style", "suppress_overlay", "sv", "swing", "sys", "theme", "tobytes", 
        "toggle_callstack", "toggle_skipping", "top", "topleft", "topright", "touch", "truecenter", "ui", 
        "unicode", "unicode_literals", "updater", "var_search", "voice", "voice_can_replay", "voice_replay", 
        "voice_sustain", "vpunch", "walkthrough_dict", "wipedown", "wipeleft", "wiperight", "wipeup", 
        "with_statement", "xrange", "zoomin", "zoominout", "zoomout", "always_pulse", "always_shake", "slow_fade", 
        "slow_nonsense", "slow_rotate", "slow_shake", "slow_shaking_slide", "slow_slide_down", "slow_slide_left", 
        "slow_slide_right", "slow_slide_up", "slow_typewriter", "check_dic", "find_closest_menu_before_name",
        "jg_1", "jg_2", "jg_3", "jg_s", "shortcuts", "valid_dic_items", "read_rpy_file", "wt_choice_tooltip",
        "ToggleWalkthrough", "ToggleSavename", "ToggleChoiceToolTips", "ToggleTextbox", "WideRatio", "custom_join",
        ]

    bypass_list.extend(['Academic_Stats', 'Actor', 'Alex_grohl__Flip_phone', 'Alex_productions__Vlog_2_0', 
        'AudioCredits', 'Ayumi_Replay_List', 'Bensound__Badass', 'Bensound__Funky_suspense', 'Bensound__Sexy', 
        'BlocktoCall', 'Calendar', 'CalendarMonth', 'CalendarMonths', 'CalendarWeekstart', 'Count', 
        'Emiko_Replay_List', 'Envy__Tears', 'Foxxy_mulderr__Good_things_ahead', 'Fsm_team_escp__Acceleration', 
        'Fsm_team_escp__Rhythm_boulevard', 'Fsm_team_escp__Small_town_girl', 'Fsm_team_escp__kinetics', 
        'GameEvents', 'GetEmptyReplays', 'H_', 'Haruka_Replay_List', 'Julexar', 'Kane0ne', 'KazutoSensei', 
        'Kevin_macleod__Acid_trumpet', 'Kevin_macleod__Bossa_antigua', 'Kevin_macleod__Chill_wave', 
        'Kevin_macleod__Hard_boiled', 'Kevin_macleod__Hit_list', 'Kevin_macleod__Martini_sunset', 
        'Kevin_macleod__Master_disorder', 'Kevin_macleod__On_the_ground', 'Kevin_macleod__Slow_Jam', 
        'Kevin_macleod__Thief_in_the_night', 'Location_Events', 'Main_Academy', 'Main_Events', 
        'Main_Target_Events', 'Maiya_Replay_List', 'Maxkomusic__Urban_hip_hop', 'Minor_Events', 
        'Others_Replay_List', 'Priority_Events', 'Random_Events', 'Replay_List', 'Replays', 'Screen_Saver_List', 
        'Secondary_Events', 'SpecialThanks', 'Stat_Change', 'Student', 'Teacher', 'Weekend_Date_Dictionary', 
        'Weekend_Date_Events', 'Weekend_Dates_Function', 'Weekend_Event_Checker', 'Weekend_Main_Events', 
        'Weekend_Priority_Events', 'Zantengetsu', 'academy', 'academy_programs', 'academy_stats_dict', 
        'academy_stats_list', 'academybookzoom', 'acceleration', 'add_tolist', 'arrowupbookstudents', 'ayumi', 
        'ayumi_bathroom_0', 'ayumi_bathroom_01', 'ayumi_masturbating_0', 'ayumi_mc_fing_0', 'ayumi_office_0', 
        'ayumi_soushi_00_e', 'ayumi_soushi_00_ev', 'ayumi_soushi_01_e', 'ayumi_soushi_01_ev', 'ayumi_soushi_bj_0', 
        'ayumi_teaching_0', 'ayumi_teaching_01', 'b', 'bad_ass', 'badguy_vibe', 'bensound_sexy', 'blowjob', 
        'boardreq', 'bounties', 'bounties_to_add', 'bounty_check', 'calendar_view', 'calendarshown', 
        'calledstudent', 'calledstudent_list', 'callstudent_fix', 'cdict', 'char_dict', 'char_dict_female', 
        'char_dict_male', 'character_list', 'choice_appear', 'completed_requests', 'completed_tasks', 
        'confiscated_items', 'creampie', 'currentdate', 'currentmonth_output', 'currentperiod_output', 
        'currentweekday_output', 'd', 'd1', 'd2', 'dailyacademic', 'dailyacademics', 'dailyaction', 'dailyevent', 
        'dbug', 'dd', 'ddi', 'di', 'dice_rolled', 'displaytime', 'dscreen', 'emiko', 'emiko_gym_0', 'emiko_gym_00', 
        'emiko_prologue_0', 'emiko_virgin', 'emiko_virgin_shared', 'emiko_volley_0', 'even', 'event_preference', 
        'f', 'f1', 'f2', 'f_in', 'f_out', 'f_scene', 'fingering', 'first_kaori_even', 'first_kaori_event', 
        'fixingnamestuff', 'flipit', 'flipphone', 'fsm_team_escp_kinetics', 'funkysuspense', 'fzoom', 'genpachi', 
        'girl', 'good_things_ahead', 'halfzoom', 'haruka', 'haruka_date0', 'haruka_date01', 'haruka_late_0', 
        'haruka_main_0', 'haruka_main_01', 'haruka_office_0', 'haruka_weekend_0', 'hidetoshi', 'hiroshige', 
        'hit_list', 'humanize', 'initialapl', 'initialboard', 'input_appear', 'izo', 'jazz_ambient', 
        'jazz_loop_office', 'jazzy_discussion', 'key', 'kiyomi', 'koji', 'lower_music', 'lp', 'main', 'main_girl', 
        'maiya', 'maiya_bunny_0', 'maiya_bunny_00', 'maiya_hiro_0', 'maiya_hiro_01', 'maiya_panties', 
        'maiya_panties_0', 'maiya_panties_01', 'mako', 'marcus', 'martini_sunset', 'masaru', 
        'mc_late_main_01_loopintr', 'mc_late_main_01_loopintro', 'mccrpt', 'miyako', 'mrstd', 'nanako', 
        'new_bounties', 'newdayoffice', 'numeric_value', 'officeloop', 'officesprite', 'officesprite_left', 
        'officesprite_right', 'open_url', 'operator', 'perk', 'perkexample', 'photographer_dictionary', 'president', 
        'president_talk_0', 'president_talk_01', 'random_student', 'remove_fromlist', 'report_character_stats', 
        'report_file_chara_stats', 'report_file_stats', 'report_menu_stats', 'req', 'resume_music', 
        'rhythm_boulevard', 'rina', 'rina_blowjob_0', 'rstd', 'rtc', 'ryoichi', 'satoe', 'satsuki', 'sayoko', 
        'scooby', 'script_folder_path', 'sex', 'sex_anal', 'sex_mc', 'sexy_chillwave', 'skippingtime', 'slanted', 
        'slightly_slanted', 'slow_jam', 'small_town_girl', 'smallvpunch', 'sotaro', 'soushi', 'st', 'stat', 
        'story_progression', 'student', 'students_book_page', 'studentszoom', 'sus_dayloopjam', 'sus_jam', 'suzu', 
        'suzu_ba', 'suzu_bat', 'suzu_bat_Kawaguchi_0', 'suzu_bat_MC_0', 'suzu_spanking_0', 'temp_unavailable', 
        'temporary_bounties', 'temporary_list', 'temporary_unavailable_actors', 'threestrikes', 'toggle_cheats', 
        'type_event', 'types_of_event', 'urban_hiphop', 'vlog2', 'weekend_main_event', 'weekendloop', 
        'weekly_exam_e', 'weekly_exam_ev', 'weeklyreport', 'wordcounter', 'wordcounter_character_files', 
        'wordcounter_characters', 'wordcounter_files', 'wordcounter_hidden', 'wordcounter_menu_choices', 
        'wordcounter_same', 'xpr_tag', 'yoko', 'yoko_changing_room_0', 'yoko_dild', 'yoko_dildo', 'yoko_onahole_0', 
        'yoko_prologue_0', 'yuna', "non_finished_tasks", "event", "e", "completed_req", "s", "exam_list", "actor", 
        ])

    bypass_list.extend(['Academic_Program', 'Alex_productions__Breakfast_in_paris', 'Alex_productions__Chill_vibes', 
        'Donovan', 'Dylan_sitts__Mirror_moving', 'Fsm_team_escp__Small_town_boy', 'Gallery_Unlocker', 'NoneHandler', 
        'Sell_Panties', 'SlowVolDown', 'SlowVolUp', 'Strikes_Program', 'Students_Representative', 'Students_Representative_Dict', 
        'Study_Group', 'Study_Group_Dict', 'Study_Group_Intelligence_Increase', 'add_notify_message', 'adj_bri', 
        'ayumi_date01', 'ayumi_servicing_0', 'ayumi_thugs_tits', 'breakfast_in_paris', 'change_affection_cheat', 
        'change_apl_cheat', 'change_corruption_cheat', 'change_strikes_cheat', 'change_testresult_cheat', 'cheat_confirm', 
        'cheat_input_text', 'chill_vibes', 'collected_panties', 'convincing', 'cum_chest', 'cum_face', 'daily_reminder', 
        'diquick', 'emiko_servicing_0', 'entire_book_page_left', 'entire_book_page_right', 'extract_packages', 'f_flash_master', 
        'failed_tasks', 'finish_notify', 'flashcum', 'float_range', 'get_menu_lines', 'haruka_servicing_0', 'header_line_top_left', 
        'header_line_top_right', 'header_title_left', 'header_title_right', 'kiyomi_anal_plug_0', 'kiyomi_anal_punishment_0', 
        'kiyomi_plug', 'kiyomi_punished_01_ev', 'lawsuit_start', 'natsuha', 'natsuha_sex_0', 'notify_appear', 'notify_duration', 
        'notify_history_length', 'notify_messages', 'mirror_moving', 'moveright_atl_custom', 'pantie_collection', 'random_slanted', 
        'replace_fromlist', 'right_to_left', 'rina_servicing_0', 'rotated', 'satsuki_first', 'setRepeatRatedown', 'setRepeatRateup', 
        'spanked', 'time', 'toggle_notify_type', 'zip_directory', 'zip_final', 'zip_path', 'zipfile'])

    bypass_list = sorted(list(set([i.strip() for i in bypass_list])))

    def adjust_brightness(hex_color, levels):
        def clamp(value):
            return max(0, min(255, value))

        # Convert hex to RGB(A)
        try:
            hex_color = hex_color.lstrip('#')
        except:
            hex_color = hex_color.hexcode.lstrip('#')

        # Handle different hex lengths
        if len(hex_color) == 3:  # #RGB
            r, g, b = [int(c*2, 16) for c in hex_color]
            a = None
        elif len(hex_color) == 4:  # #RGBA
            r, g, b, a = [int(c*2, 16) for c in hex_color]
        elif len(hex_color) == 6:  # #RRGGBB
            r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
            a = None
        elif len(hex_color) == 8:  # #RRGGBBAA
            r, g, b, a = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16), int(hex_color[6:8], 16)
        else:
            raise ValueError("Invalid hex color format")

        # Adjust brightness
        r = clamp(r + levels)
        g = clamp(g + levels)
        b = clamp(b + levels)

        # Convert RGB(A) back to hex
        if a is None:
            return '#{:02X}{:02X}{:02X}'.format(r, g, b)
        else:
            return '#{:02X}{:02X}{:02X}{:02X}'.format(r, g, b, a)

    def var_search(name="", default=store):
        if default == persistent:
            ev = "persistent."
        elif default == gui:
            ev = "gui."
        elif default == config:
            ev = "config."
        else:
            ev = ""
        for i in dir(default):
            if not i.startswith(("_","__")):
                if name:
                    if name in i:
                        print("VAR:{} | VALUE:{}".format(i, eval(ev+i)))
                else:
                    if isinstance(eval(ev+i),renpy.character.ADVCharacter):
                        pass
                    elif i in bypass_list:
                        pass
                    else:
                        try:
                            print("VAR:{} | VALUE:{}".format(i, eval(ev+i)))
                        except Exception as e:
                            print("VAR:{}\n{}".format(i,e))

    def set_reload():
        print(config.reload)
        if config.autoreload:
            config.autoreload = False
        else:
            config.autoreload = True

    #Text Returns
    def TextSpeed():
        _cps_value = int(round(preferences.text_cps))
        _cps_value = '200' if _cps_value == 0 else _cps_value
        return _cps_value

    def AutoForwardTime():
        _auto_forward_time = int(round(preferences.afm_time))
        _auto_forward_time = '1' if _auto_forward_time == 0 else _auto_forward_time
        return _auto_forward_time

    def TextBoxAlpha():
        _alpha = float(round(persistent._textbox_alpha,2))
        _alpha = _alpha*100
        _alpha = round(_alpha,0)
        _alpha_out = str(_alpha)
        _alpha_out = _alpha_out.replace(".0"," %")
        return _alpha_out

    def VolumeDisplay(value):
        '''
        Returns the Value Volume Level to Ren'Py.
        '''
        try:
            _volume = float(round(preferences.get_mixer(value),2))
        except:
            _volume = float(round(preferences.get_volume(value),2))
        _volume = _volume*100
        _volume = round(_volume,0)
        _volume_out = str(_volume)
        _volume_out = _volume_out.replace(".0"," %")
        return _volume_out

    def FancyCheck():
        if getattr(persistent, "_fancy_text"):
            if preferences.text_cps == 200 or preferences.text_cps == 0:
                preferences.text_cps = 120
        else:
            preferences.text_cps = 0

    config.after_load_callbacks.append(FancyCheck)

    def WideRatio(width):
        # Take the width of your screen or any size for that matter
        # and you will get an output of width x height
        height = width * 9.0 / 16.0
        return int(width), int(height)

    class SlowEffectChange(Action):
        def __init__(self, bypass=False):
            self.bypass = bypass
            self.effects = {
                "Fade" : slow_fade,
                "Slide Up" : slow_slide_up(20),
                "Slide Down" : slow_slide_down(20),
                "Slide Left" : slow_slide_left(20),
                "Slide Right" : slow_slide_right(20),
                "Shake Slide" : slow_shaking_slide(10,10,20,20),
                "Shake" : slow_shake(10, 10),
                "Typewriter" : slow_typewriter,
                "Rotate" : slow_rotate,
                "Nonsense" : slow_nonsense
            }

            # Convert the dictionary keys to a list for cycling through effects
            self.effect_names = list(self.effects.keys())

            # Initialize the current effect index
            initial_effect_name = persistent._slow_effect_title if hasattr(persistent, '_slow_effect_title') else self.effect_names[0]
            self.current_index = self.effect_names.index(initial_effect_name)

        def __call__(self):
            #if main_menu and not self.bypass:
            #    return
            # Move to the next effect
            self.current_index = (self.current_index + 1) % len(self.effect_names)

            # Get the current effect name
            current_effect_name = self.effect_names[self.current_index]

            # Get the current effect function
            current_effect = self.effects[current_effect_name]

            # Apply the current effect
            persistent._slow_effect = current_effect
            persistent._slow_effect_title = current_effect_name

            # Restart interaction if needed
            renpy.restart_interaction()
            if not main_menu and not self.bypass:
                renpy.notify("Changed Effect to: %s"%persistent._slow_effect_title)

            #return persistent._slow_effect_title

    class AlwaysEffectChange(Action):
        def __init__(self, bypass=False):
            self.bypass = bypass
            self.effects = {
                "None" : None,
                "Fade" : slow_fade,
                "Always Shake" : always_shake(1, 1),
                "Always Pulse" : always_pulse
            }

            # Convert the dictionary keys to a list for cycling through effects
            self.effect_names = list(self.effects.keys())

            # Initialize the current effect index
            initial_effect_name = persistent._always_effect_title if hasattr(persistent, '_always_effect_title') else self.effect_names[0]
            self.current_index = self.effect_names.index(initial_effect_name)

        def __call__(self):
            #if main_menu and not self.bypass:
            #    return
            # Move to the next effect
            self.current_index = (self.current_index + 1) % len(self.effect_names)

            # Get the current effect name
            current_effect_name = self.effect_names[self.current_index]

            # Get the current effect function
            current_effect = self.effects[current_effect_name]

            # Apply the current effect
            persistent._always_effect = current_effect
            persistent._always_effect_title = current_effect_name

            # Restart interaction if needed
            renpy.restart_interaction()
            if not main_menu and not self.bypass:
                renpy.notify("Changed Always Effect to: %s"%persistent._always_effect_title)

            #return persistent._always_effect_title

    def ToggleFancyText():
        if main_menu:
            return
        if persistent._fancy_text:
            if preferences.text_cps == 200 or preferences.text_cps == 0:
                preferences.text_cps = 120
        else:
            preferences.text_cps = 0
        persistent._fancy_text = not persistent._fancy_text
        renpy.run(With(dissolve))
        renpy.notify(_("Fancy Text: %s")%(_("On") if persistent._fancy_text else _("Off")))
        renpy.restart_interaction()

    def EffectDelayDisplay():
        _alpha = float(round(persistent._effect_delay,2))
        _alpha = _alpha*100
        _alpha = round(_alpha,0)
        _alpha_out = str(_alpha)
        _alpha_out = _alpha_out.replace(".0","")
        if _alpha_out == "0":
            _alpha_out = "Off"
        if _alpha_out != "100":
            _alpha_out = _alpha_out.replace("0","")
        else:
            _alpha_out = _alpha_out.replace("00","0")
        return _alpha_out

    def QuickPositions():
        buttons = {
            "bottom_center"  : "Bottom Center",
            "top_center"     : "Top Center"
            }
        return buttons.get(persistent._quick_menu_layout)

    class CycleQuickStates(Action):
        def __init__(self, bypass=False):
            self.bypass = bypass

        def __call__(self):
            #if main_menu and not self.bypass:
            #    return
            if not getattr(store, "quick_menu"):
                setattr(store, "quick_menu", True)
            if persistent._quick_menu_state == "visible":
                persistent._quick_menu_state = "hover"
            elif persistent._quick_menu_state == "hover":
                persistent._quick_menu_state = "hidden"
            elif persistent._quick_menu_state == "hidden":
                persistent._quick_menu_state = "visible"
            renpy.run(With(dissolve))
            if not main_menu and not self.bypass:
                renpy.notify(_("Quick Menu is: %s")%(persistent._quick_menu_state.title()))
            renpy.restart_interaction()

    class CycleQuickMenu(Action):
        def __init__(self, bypass=False):
            self.bypass = bypass
            self.buttons = ["bottom_center", "top_center"]

            self.current_position = self.buttons.index(persistent._quick_menu_layout)

        def __call__(self):
            #if main_menu and not self.bypass:
            #    return
            current_index = self.buttons.index(persistent._quick_menu_layout)
            next_index = (current_index + 1) % len(self.buttons)
            self.current_position = self.buttons[next_index]
            persistent._quick_menu_layout = self.current_position
            renpy.run(With(dissolve))
            if not main_menu and not self.bypass:
                renpy.notify(_("Quick Menu Position: %s")%(QuickPositions()))
            renpy.restart_interaction()

    def ToggleChoiceHotkeys():
        persistent._choice_hotkeys = not persistent._choice_hotkeys
        renpy.run(With(dissolve))
        renpy.notify(_("%sHotkeys: %s")%(_("Choice ") if not main_menu else "",_("On") if persistent._choice_hotkeys else _("Off")))
        renpy.restart_interaction()

    def WalkthroughData(line, caption):
        choices = walkthrough_dict().get(line, None)
        if choices:
            valid = choices.get(caption, None)
            if valid:
                _choice_wt    = valid.get("wt"  , "")
                _choice_hint  = valid.get("hint", "")
                _choice_color = valid.get("color", None)
                _choice_size  = valid.get("size", None)

                if _choice_color in [None, "None", "none"]:
                    _choice_color = gui.text_color

                if _choice_size in [None, "None", "none"]:
                    _choice_size = gui.text_size

                if _choice_hint in [None, "None", "none"]:
                    _choice_hint = ""

                return _choice_wt, _choice_hint, _choice_color, _choice_size
        return None, None, None, None

    class GetText(Action):
        def __init__(self,screen_name,input_id):
            self.screen_name=screen_name
            self.input_id=input_id
        def __call__(self):
            if renpy.get_widget(self.screen_name,self.input_id):
                return str(renpy.get_widget(self.screen_name,self.input_id).content)

    class Unlock_Replays(Action):

        reps = [
            ##Name                 #Partner              #Notification             #Variable
            ("ayumi.name",         "",                   "Fingering",              "ayumi_MC_fing_0"), 
            ("ayumi.name",         "",                   "Masturbating",           "ayumi_masturbating_H"), 
            ("ayumi.name",         "",                   "Office",                 "ayumi_office_H"), 
            ("ayumi.name",         "soushi.name",        "BJ",                     "ayumi_soushi_bj_0"), 
            ("emiko.name",         "",                   "Gym",                    "emiko_gym_H_0"), 
            ("emiko.name",         "",                   "Prologue",               "emiko_prologue_H"),
            ("haruka.name",        "",                   "Late",                   "haruka_first_late_H"), 
            ("haruka.name",        "",                   "Office",                 "haruka_first_office_H"), 
            ("haruka.name",        "",                   "First Weekend",          "haruka_first_weekend"), 
            ("rina.name",          "",                   "First Blowjob",          "rina_first_blowjob_H"), 
            ("suzu.name",          "",                   "Suzu Shared",            "suzu_bat_01_Kawaguchi"), 
            ("suzu.name",          "",                   "Suzu Bat",               "suzu_bat_01_MC"),
            ("suzu.name",          "",                   "Spanking",               "suzu_spanking_0"), 
            ("yoko.name",          "",                   "Change Room Sex",        "yoko_changing_room_H"), 
            ("yoko.name",          "",                   "Dildo Quest",            "yoko_onahole_replay"), 
            ("yoko.name",          "",                   "Prologue",               "yoko_prologue_H")
            ]

        def __call__(self):

            for name, partner, notif, var in self.reps:
                if partner:
                    notification = "{} and {} - {} replay Unlocked".format(eval(name), eval(partner), notif)
                    if not getattr(persistent, var):
                        print(notification)
                        #setattr(persistent, var, True)
                        #renpy.notify(notification)
                else:
                    notification = "{} - {} replay Unlocked".format(eval(name), notif)
                    if not getattr(persistent, var):
                        print(notification)
                        #setattr(persistent, var, True)
                        #renpy.notify(notification)

        def get_selected(self):
            return all(getattr(persistent, i[3]) for i in self.reps)

    def GetEmptyReplays(name):
        try:
            return eval("{}_Replay_List".format(name))
        except:
            return []

    def toggle_callstack():
        if main_menu:
            return
        renpy.run(ToggleScreen("callstack", transition=dissolve))

    def ToggleWalkthrough():
        persistent._walkthrough = not persistent._walkthrough
        renpy.run(With(dissolve))
        renpy.notify(_("Walkthrough: %s")%(("On") if persistent._walkthrough else _("Off")))
        renpy.restart_interaction()

    def ToggleSavename():
        persistent._custom_savename = not persistent._custom_savename
        renpy.run(With(dissolve))
        renpy.notify(_("Custom Savenames: %s")%(("On") if persistent._custom_savename else _("Off")))
        renpy.restart_interaction()

    def ToggleChoiceToolTips():
        persistent._choice_tooltips = not persistent._choice_tooltips
        renpy.run(With(dissolve))
        renpy.notify(_("Choice Tooltips: %s")%(("On") if persistent._choice_tooltips else _("Off")))
        renpy.restart_interaction()

    def ToggleTextbox():
        persistent._textbox_visible = not persistent._textbox_visible
        renpy.run(With(dissolve))
        renpy.notify(_("Textbox: %s")%(("On") if persistent._textbox_visible else _("Off")))
        renpy.restart_interaction()

    def _fix_main_name():
        if main.name != mcname:
            main.name = mcname

    def custom_join(items, join_param="\n"):
        fix = []
        for i in items:
            if i:
                fix.append(i)

        return f"{join_param}".join(fix)

    def _adjust_dialogue(direction="+"):
        txt = "Textbox Visibility"
        if direction == "+":
            if persistent._textbox_alpha <= 0.99 :
                persistent._textbox_alpha += 0.01
            else:
                persistent._textbox_alpha = 1.0
                txt = "Textbox Is Completely Visible"
        elif direction == "-":
            if persistent._textbox_alpha > 0.01:
                persistent._textbox_alpha -= 0.01
            else:
                persistent._textbox_alpha = 0.0
                txt = "Textbox Is Completely Invisible"
        renpy.notify("%s: %s"%(txt, TextBoxAlpha()))
    
    def add_notify_message(msg=None):

        if not msg:
            return

        global notify_messages

        add_time = time.time()

        # Just in case multiple notifications are added really really 
        # fast, this gives them minorly different time values so they 
        # do not steal displayables meant for other notifications
        if notify_messages and notify_messages[-1][1] >= add_time:

            add_time = notify_messages[-1][1] + 0.01

        notify_messages.append((msg, add_time))

        # just keep notify_history_length number of messages
        notify_messages = notify_messages[-notify_history_length:]

        renpy.show_screen("notify_container")
        renpy.restart_interaction()

    def finish_notify(trans, st, at):

        max_start = time.time() - notify_duration

        if not [k for k in notify_messages if k[1] > max_start]:

            # If the notification list is now empty, hide the screen
            renpy.hide_screen("notify_container")
            renpy.restart_interaction()

        return None

    def toggle_notify_type():
        if persistent._notify_custom:
            persistent._notify_custom = False
            config.notify = renpy.display_notify
            renpy.notify("Custom Notifications Off")
        else:
            persistent._notify_custom = True
            config.notify = add_notify_message
            renpy.notify("Custom Notifications On")
        
        renpy.restart_interaction()

    #config.python_callbacks.append(_fix_main_name)
    config.after_load_callbacks.append(_fix_main_name)
    config.interact_callbacks.append(_fix_main_name)

    config.keymap[ 'quick_save_button' ] = [ 'K_F5' ]
    config.underlay.append(renpy.Keymap(quick_save_button = QuickSave()))

    config.keymap[ 'quick_load_button' ] = [ 'K_F6' ]
    config.underlay.append(renpy.Keymap(quick_load_button = QuickLoad()))

    config.keymap[ 'toggle_quick_menu_state' ] = [ 'noshift_K_q' ]
    config.underlay.append(renpy.Keymap(toggle_quick_menu_state = CycleQuickStates()))

    config.keymap[ 'toggle_quick_menu_position' ] = [ 'shift_K_q' ]
    config.underlay.append(renpy.Keymap(toggle_quick_menu_position = CycleQuickMenu()))

    config.keymap[ 'toggle_always_effect' ] = [ 'noshift_K_r' ]
    config.underlay.append(renpy.Keymap(toggle_always_effect = AlwaysEffectChange()))

    config.keymap[ 'toggle_slow_effect' ] = [ 'noshift_K_e' ]
    config.underlay.append(renpy.Keymap(toggle_slow_effect = SlowEffectChange()))

    config.keymap[ 'toggle_fancy_text' ] = [ 'shift_K_f' ]
    config.underlay.append(renpy.Keymap(toggle_fancy_text = Function(ToggleFancyText)))

    config.keymap[ 'toggle_choice_hotkeys' ] = [ 'noshift_K_c' ]
    config.underlay.append(renpy.Keymap(toggle_choice_hotkeys = Function(ToggleChoiceHotkeys)))

    config.keymap[ 'toggle_walkthrough' ] = [ 'noshift_K_w' ]
    config.underlay.append(renpy.Keymap(toggle_walkthrough = Function(ToggleWalkthrough)))

    config.keymap[ 'toggle_savename' ] = [ 'shift_K_s' ]
    config.underlay.append(renpy.Keymap(toggle_savename = Function(ToggleSavename)))

    config.keymap[ 'toggle_choice_tooltips' ] = [ 'shift_K_t' ]
    config.underlay.append(renpy.Keymap(toggle_choice_tooltips = Function(ToggleChoiceToolTips)))

    config.keymap[ 'toggle_textbox' ] = [ 'noshift_K_t' ]
    config.underlay.append(renpy.Keymap(toggle_textbox = Function(ToggleTextbox)))

    config.keymap[ 'toggle_callstack' ] = [ 'K_HOME' ]
    config.underlay.append(renpy.Keymap(toggle_callstack = Function(toggle_callstack)))

    config.keymap[ 'toggle_visibility_up' ] = [ 'K_KP_PLUS', 'repeat_K_KP_PLUS' ]
    config.underlay.append(renpy.Keymap(toggle_visibility_up = Function(_adjust_dialogue, "+")))

    config.keymap[ 'toggle_visibility_down' ] = [ 'K_KP_MINUS', 'repeat_K_KP_MINUS' ]
    config.underlay.append(renpy.Keymap(toggle_visibility_down = Function(_adjust_dialogue, "-")))

    config.keymap[ 'toggle_notifications' ] = [ 'K_n' ]
    config.underlay.append(renpy.Keymap(toggle_notifications = Function(toggle_notify_type)))

    config.overlay_screens.append("shortcuts")

    if persistent._notify_custom == None:
        persistent._notify_custom = True

    if persistent._notify_custom:
        config.notify = add_notify_message
    else:
        config.notify = renpy.display_notify

    def NoneHandler(value: str) -> None:
        renpy.run(NullAction())

    config.hyperlink_handlers["#"] = NoneHandler

label splashscreen:
    scene black
    with Pause(1)

    show splashText with dissolve
    with Pause(15)

    hide text with dissolve
    with Pause(1)

    $ mod_updated = get_latest_mod()

    return

init 1:# Defaults
    image splashText = Text(shortcuts.strip(), style="splash")
    default preferences.text_cps = 120
    default persistent._unlocked_gallery = False
    default persistent._show_empty_gallery = False
    default persistent._sharing_content = False

    default _go_to_page = ""
    default jg_s = "{size=24}"
    default jg_1 = "{color=#FB4301}"
    default jg_2 = "{color=#000000}"
    default jg_3 = "{/color}"

    default notify_messages = []
    default notify_duration = 4.0
    default notify_history_length = 5
    
    default char_dict_female = {}
    default char_dict_male = {}

## Cheats ######################################################################################################################
init python:# Init Cheats
    def toggle_cheats():
        if main_menu:
            return
        renpy.run(ToggleScreen("cheats", transition=dissolve))

    config.keymap[ 'toggle_cheats' ] = [ 'K_END' ]
    config.underlay.append(renpy.Keymap(toggle_cheats = Function(toggle_cheats)))

    def _cheat_chars_data():
        return [ayumi, emiko, haruka, maiya, genpachi, hiroshige, izo, miyako, nanako, rina, ryoichi, sayoko, satsuki, soushi, sotaro, suzu, yoko, yuna]

    def Generate_Char_Dict(lst):
        char_dic_female = {}
        char_dic_male = {}
        for i in lst:
            if i.gender == 0:
                if not i.nametag in char_dic_female:
                    char_dic_female[i.nametag] = {
                        "name" : i.name,
                        "surname" : i.surname,
                        "class" : i,
                        "outfit" : i.outfit,
                        "available" : i.available,
                        "met" : i.met,
                        "virgin" : i.virgin,
                        "personality" : i.personality,
                        "intelligence" : i.intelligence,
                        "testResult" : i.testResult,
                        "strikes" : i.strikes,
                        "affection" : i.affection,
                        "perversion" : i.perversion,
                        "lewd" : i.lewd
                    }
            elif i.gender == 1:
                if not i.nametag in char_dic_male:
                    char_dic_male[i.nametag] = {
                        "name" : i.name,
                        "surname" : i.surname,
                        "class" : i,
                        "outfit" : i.outfit,
                        "available" : i.available,
                        "met" : i.met,
                        "virgin" : i.virgin,
                        "personality" : i.personality,
                        "intelligence" : i.intelligence,
                        "testResult" : i.testResult,
                        "strikes" : i.strikes,
                        "affection" : i.affection,
                        "perversion" : i.perversion,
                        "lewd" : i.lewd
                    }
        return char_dic_female, char_dic_male

    #renpy.run(CyclePersonalities("Pure"))
    class CyclePersonalities(Action):
        def __init__(self, personality, char):
            self.buttons = ["Pure", "Outgoing", "Shy", "Charming", "Cold", "Delinquent", "Nerd"]

            self.char = char
            self.personality = personality

            self.current_position = self.buttons.index(personality)

        def __call__(self):
            current_index = self.buttons.index(self.personality)
            next_index = (current_index + 1) % len(self.buttons)
            self.current_position = self.buttons[next_index]
            self.char.personality = self.current_position
            renpy.restart_interaction()

    class CycleOutfits(Action):
        def __init__(self, outfit, char):
            self.buttons = ["School", "Swim", "Gym", "Casual", "Naked"]

            self.char = char
            self.outfit = outfit

            self.current_position = self.buttons.index(outfit)

        def __call__(self):
            current_index = self.buttons.index(self.outfit)
            next_index = (current_index + 1) % len(self.buttons)
            self.current_position = self.buttons[next_index]
            image = "images/characters/%s/%s.png"%(self.char.nametag,self.current_position)
            if renpy.loadable(image):
                self.char.outfit = self.current_position
            else:
                self.char.outfit = "School"
            renpy.restart_interaction()
    #Generate_Char_Dict([ayumi, emiko, haruka, maiya, genpachi, hiroshige, izo, miyako, nanako, rina, ryoichi, sayoko, satsuki, soushi, sotaro, suzu, yoko, yuna])
    #Personalities : "Pure", "Outgoing", "Shy", "Charming", "Cold", "Delinquent"
    #print_stats([ayumi, emiko, haruka, maiya, genpachi, hiroshige, izo, miyako, nanako, rina, ryoichi, sayoko, satsuki, soushi, sotaro, suzu, yoko, yuna])
    def print_stats(lst):
        print()
        for i in lst:
            if i.gender == 0:
                print("'{}' : {{".format(i.name.lower()))
                print("    'class' : {},".format(i.nametag))
                print("    'outfit' : '{}',".format(i.outfit))
                print("    'available' : {},".format(i.available))
                print("    'met' : {},".format(i.met))
                print("    'virgin' : {},".format(i.virgin))
                print("    'personality' : '{}',".format(i.personality))
                print("    'intelligence' : {},".format(i.intelligence))
                print("    'testResult' : {},".format(i.testResult))
                print("    'strikes' : {},".format(i.strikes))
                print("    'affection' : {},".format(i.affection))
                print("    'perversion' : {},".format(i.perversion))
                print("    'lewd' : {}".format(i.lewd))
                print("    },")

    def _sex_symbol_status(value):
        if value >= 95:
            return "{size=22}{color=#ff002e}Corrupted!"
        elif value >= 75:
            return "{size=22}{color=#ff0049}Perverted"
        elif value >= 55:
            return "{size=22}{color=#ff008f}Lustful"
        elif value >= 30:
            return "{size=22}{color=#ff9300}Slutty"
        elif value >= 10:
            return "{size=22}{color=#ffe000}Curious"
        elif value < 10:
            return "{size=22}{color=#7cffe1}Pure"
        else:
            return "{size=22}{color=#FFFFFF}None"

    def _viewership_status(value):
        if value >= 100000:
            return "{size=22}Very High!"
        elif value >= 50000:
            return "{size=22}High"
        elif value >= 15000:
            return "{size=22}Normal"
        elif value >= 5000:
            return "{size=22}Low"
        elif value < 5000:
            return "{size=22}Very Low"
        else:
            return "{size=22}No Data!!"

    def _board_status(value):
        if value >= 90:
            return "{size=20}The Board is Delighted with your performance!"
        elif value >= 75:
            return "{size=20}The Board is Happy with the way you run the Academy."
        elif value >= 60:
            return "{size=20}The Board is Satisfied with the way the Academy is functioning."
        elif value >= 40:
            return "{size=20}The Board is Dissatisfied with your directing of the Academy."
        elif value >= 11:
            return "{size=20}The Board is Incredibly Frustrated with your performance!"
        elif value < 11:
            return "{size=20}The Board is considering removing you from your position. Do something fast!"

    def _grades_status(value):
        if value >= 96:
            return "{size=25}{b}A{/b}+"               
        elif value >= 90:
            return "{size=25}{b}A{/b}"               
        elif value >= 85:
            return "{size=25}{b}A{/b}-"                   
        elif value >= 80:
            return "{size=25}{b}B{/b}+"                   
        elif value >= 75:
            return "{size=25}{b}B{/b}"                   
        elif value >= 70:
            return "{size=25}{b}B{/b}-"                   
        elif value >= 65:
            return "{size=25}{b}C{/b}+"                  
        elif value >= 60:
            return "{size=25}{b}C"                  
        elif value >= 55:
            return "{size=25}{b}C{/b}-"                  
        elif value >= 50:
            return "{size=25}{b}D{/b}+"                 
        elif value >= 45:
            return "{size=25}{b}D"                
        elif value >= 40:
            return "{size=25}{b}D{/b}-"                  
        elif value < 40:
            return "{size=25}{b}F{/b}"

    def _student_trust_status(value):
        if value >= 90:
            return "veryhappysymbol"
        elif value >= 63:# and sttrust >= 63:
            return "happysymbol"
        elif value >= 38:# and sttrust >= 38:
            return "neutralsymbol"
        elif value >= 15:# and sttrust >= 15:
            return "sadsymbol"
        elif value < 15:
            return "verysadsymbol"

    def _student_grade_status(rstd):
        if "Cheated_Exam" in rstd.topics and rstd.testResult == 0:
            return "{size=40}{color=#c30000}{font=gui/fonts/CrimsonText-SemiBold.ttf}{i}0"
        elif rstd.testResult >= 96:
            return "{=cheats_inline_40}A+"
        elif rstd.testResult >= 90:
            return "{=cheats_inline_40}A"
        elif rstd.testResult >= 85:
            return "{=cheats_inline_40}A-" 
        elif rstd.testResult >= 80:
            return "{=cheats_inline_40}B+"
        elif rstd.testResult >= 75:
            return "{=cheats_inline_40}B"
        elif rstd.testResult >= 70:
            return "{=cheats_inline_40}B-"
        elif rstd.testResult >= 65:
            return "{=cheats_inline_40}C+"
        elif rstd.testResult >= 60:
            return "{=cheats_inline_40}C"
        elif rstd.testResult >= 55:
            return "{=cheats_inline_40}C-"
        elif rstd.testResult >= 50:
            return "{=cheats_inline_40}D+"
        elif rstd.testResult >= 45:
            return "{=cheats_inline_40}D"
        elif rstd.testResult >= 40:
            return "{=cheats_inline_40}D-"
        elif rstd.testResult < 40:
            return "{=cheats_inline_40}F"

    def _student_strike_status(rstd):
        if rstd.strikes >= 3:
            return "{color=#000000} /  /  /", 0, 0
        elif rstd.strikes == 2:
            return "{color=#000000} /  /", 1.5, 0
        elif rstd.strikes == 1:
            return "{color=#000000} /", 0, 0
        else:
            return "{color=#000000}{size=20}{i}(clean record){/i}",0 , 0.55

    def _student_report_status(rstd):
        if rstd.personality == "Pure":
            if rstd.gender == 0:
                return "{size=18}{color=#000000}{i}  [rstd.surname] [rstd.name] is a student that possesses a genuinely friendly and warm personality. Her inviting and authentic nature naturally attracts others to be around. As a result, forming social connections comes easily to her.", 550
            elif rstd.gender == 0:
                return "{size=18}{color=#000000}{i}  [rstd.surname] [rstd.name] is a student that possesses a genuinely friendly and warm personality. His inviting and authentic nature naturally attracts others to be around. As a result, forming social connections comes easily to Him.", 550
            else:
                return "{size=18}{color=#000000}{i}  [rstd.surname] [rstd.name] is a student that possesses a genuinely friendly and warm personality. Their inviting and authentic nature naturally attracts others to be around. As a result, forming social connections comes easily to this student.", 550                                                        
        elif rstd.personality == "Outgoing":
            if rstd.gender == 0:
                return "{size=18}{color=#000000}{i}  [rstd.surname] [rstd.name] is a student that embodies a lively and authentic personality, naturally engaging in social situations, often speaking with enthusiasm and a noticeable volume. Her unreserved approach might have a polarizing effect, prompting swift judgements from others regarding whether they enjoy her company or not.", 550
            elif rstd.gender == 1:
                return "{size=18}{color=#000000}{i}  [rstd.surname] [rstd.name] is a student that embodies a lively and authentic personality, naturally engaging in social situations, often speaking with enthusiasm and a noticeable volume. His unreserved approach might have a polarizing effect, prompting swift judgements from others regarding whether they enjoy his company or not.", 550
            else:
                return "{size=18}{color=#000000}{i}  [rstd.surname] [rstd.name] is a student that embodies a lively and authentic personality, naturally engaging in social situations, often speaking with enthusiasm and a noticeable volume. Their unreserved approach might have a polarizing effect, prompting swift judgements from others regarding whether they enjoy their company or not.", 550                
        elif rstd.personality == "Shy":
            if rstd.gender == 0:
                return "{size=18}{color=#000000}{i}  [rstd.surname] [rstd.name] is a student that often displays an introverted and reserved nature. She tends to exhibit reticence in social interactions and may feel uncomfortable or apprehensive in group settings.", 550
            elif rstd.gender == 1:
                return "{size=18}{color=#000000}{i}  [rstd.surname] [rstd.name] is a student that often displays an introverted and reserved nature. He tends to exhibit reticence in social interactions and may feel uncomfortable or apprehensive in group settings.", 550
            else:
                return "{size=18}{color=#000000}{i}  [rstd.surname] [rstd.name] is a student that often displays an introverted and reserved nature. They tend to exhibit reticence in social interactions and may feel uncomfortable or apprehensive in group settings.", 550
        elif rstd.personality == "Charming":
            if rstd.gender == 0:
                return "{size=18}{color=#000000}{i}  [rstd.surname] [rstd.name] possesses a charismatic magnetism that captivates others. Her ability to effortlessly appear persuasive allows her to influence and win favors from peers, making her stand out in the student community. As a result, she is often seen surrounded by admirers and occupies an elevated social standing among the students", 550
            elif rstd.gender == 1:
                return "{size=18}{color=#000000}{i}  [rstd.surname] [rstd.name] possesses a charismatic magnetism that captivates others. His ability to effortlessly appear persuasive allows him to influence and win favors from peers, making him stand out in the student community. As a result, he is often seen surrounded by admirers and occupies an elevated social standing among the students", 550
            else:
                return "{size=18}{color=#000000}{i}  [rstd.surname] [rstd.name] possesses a charismatic magnetism that captivates others. Their ability to effortlessly appear persuasive allows them to influence and win favors from peers, making them stand out in the student community. As a result, they are often seen surrounded by admirers and occupies an elevated social standing among the students", 550                                                               
        elif rstd.personality == "Cold":
            if rstd.gender == 0:
                return "{size=18}{color=#000000}{i}  [rstd.surname] [rstd.name] displays a cautions and cynical personality. She carefully navigates through social situations with sharp wit and a guarded mindset. It is unusual for her to open up about herself or to provide more information that was required for most interactions", 500
            elif rstd.gender == 1:
                return "{size=18}{color=#000000}{i}  [rstd.surname] [rstd.name] displays a cautions and cynical personality. He carefully navigates through social situations with sharp wit and a guarded mindset. It is unusual for him to open up about herself or to provide more information that was required for most interactions", 500
            else:
                return "{size=18}{color=#000000}{i}  [rstd.surname] [rstd.name] is a student that displays a cautions and cynical personality. They carefully navigate through social situations with sharp wit and a guarded mindset. It is unusual for them to open up about themselves or to provide more information that was required for most interactions", 500
        elif rstd.personality == "Nerd":
            if rstd.gender == 0:
                return "{size=18}{color=#000000}{i}  [rstd.surname] [rstd.name] is a student who often displays social awkwardness and introversion. She is almost always immersed in her own peculiar hobbies and subjects. Although these diverse interests might lead to increased curiosity about these niche subjects, it might also renders the student potentially vulnerable in certain social situations.", 500
            elif rstd.gender == 1:
                return "{size=18}{color=#000000}{i}  [rstd.surname] [rstd.name] is a student who often displays social awkwardness and introversion. He is almost always immersed in his own peculiar hobbies and subjects. Although these diverse interests might lead to increased curiosity about these niche subjects, it might also renders the student potentially vulnerable in certain social situations.", 500
            else:
                return "{size=18}{color=#000000}{i}  [rstd.surname] [rstd.name] is a student who often displays social awkwardness and introversion. They are almost always immersed in their own peculiar hobbies and subjects. Although these diverse interests might lead to increased curiosity about these niche subjects, it might also renders the student potentially vulnerable in certain social situations.", 500
        elif rstd.personality == "Delinquent":
            if rstd.gender == 0:
                return "{size=18}{color=#000000}{i}  [rstd.surname] [rstd.name] is a student who presents a rebellious and nonconforming nature, frequently clashing with others due to her defiance towards rules and authorities. Her confrontational behavior may lead to increased disciplinary issues, and she is viewed as a typical 'troublemaker' based on our earlier observations.", 500
            elif rstd.gender == 1:
                return "{size=18}{color=#000000}{i}  [rstd.surname] [rstd.name] is a student who presents a rebellious and nonconforming nature, frequently clashing with others due to his defiance towards rules and authorities. His confrontational behavior may lead to increased disciplinary issues, and he is viewed as a typical 'troublemaker' based on our earlier observations.", 500
            else:
                return "{size=18}{color=#000000}{i}  [rstd.surname] [rstd.name] is a student who presents a rebellious and nonconforming nature, frequently clashing with others due to their defiance towards rules and authorities. Their confrontational behavior may lead to increased disciplinary issues, and they are viewed as a typical 'troublemaker' based on our earlier observations.", 500
        else:
            return "{=cheats_inline_itallic}  [rstd.surname] [rstd.name] is one of the students at {b}ReLive Academy{/b}.", 550

    def _student_intelligence_status(rstd,lvl=1):
        if lvl == 1:
            if rstd.gender == 0:
                return "{size=18}{color=#000000}{i}  It should be noted that Ms. [rstd.surname] is a very gifted student, having passed many of our initial examinations with flying colors. It is with no caution, that our experts consider her level of intellect to be more than spectacular. Some would even use the word \'Genius\'."
            elif rstd.gender == 1:
                return "{=cheats_inline_itallic}  It should be noted that Mr. [rstd.surname] is a very gifted student, having passed many of our initial examinations with flying colors. It is with no caution, that our experts consider his level of intellect to be more than spectacular. Some would even use the word \'Genius\'."
            else:
                return "{=cheats_inline_itallic}  It should be noted that [rstd.surname] is a very gifted student, having passed many of our initial examinations with flying colors. It is with no caution, that our experts consider their level of intellect to be more than spectacular. Some would even use the word \'Genius\'."
        if lvl == 2:
            if rstd.testResult <= academy.gradesthreshold:
                if rstd.gender == 0:
                    return"{=cheats_inline_itallic} Despite having exceeded many of our initial reports, this student has failed to achieve a significant positive result in their last weekly exam."
            else:
                if rstd.gender == 0:
                    return "{=cheats_inline_itallic} Due to such an unusually intelligent student, it should be very hard to challenge her without severly impacting our other students grades."
                elif rstd.gender == 1:
                    return "{=cheats_inline_itallic} Due to such an unusually intelligent student, it should be very hard to challenge him without severly impacting our other students grades."
                else:
                    return "{=cheats_inline_itallic} Due to such an unusually intelligent student, it should be very hard to challenge them without severly impacting our other students grades."
        if lvl == 3:
            if rstd.gender == 0:
                return "{=cheats_inline_itallic}  She has demonstrated to be a very intelligent student and, under normal circumstances, should have no problem navigating through her academics."
            elif rstd.gender == 1:
                return "{=cheats_inline_itallic}  He has demonstrated to be a very intelligent student and, under normal circumstances, should have no problem navigating through his academics."
            else:
                return "{=cheats_inline_itallic}  They have demonstrated to be a very intelligent student and, under normal circumstances, should have no problem navigating through their academics."
    
    def _student_corruption_status(rstd):
        if rstd.corruption >= 95:
            return "{=cheats_inline_random}{color=#ff002e}Corrupted!"
        elif rstd.corruption >= 75:
            return "{=cheats_inline_random}{color=#ff0049}Perverted"
        elif rstd.corruption >= 55:
            return "{=cheats_inline_random}{color=#ff008f}Lustful"
        elif rstd.corruption >= 30:
            return "{=cheats_inline_random}{color=#ff9300}Slutty"
        elif rstd.corruption >= 10:
            return "{=cheats_inline_random}{color=#ffe000}Curious"
        elif rstd.corruption < 10:
            return "{=cheats_inline_random}{color=#000000}Pure"

    def _student_affection_status(rstd):
        if rstd.affection >= 91:
            return "{=cheats_inline_random}{color=#ff4edc}Passion!"
        elif rstd.affection >= 70:
            return "{=cheats_inline_random}{color=#e04646}Love"
        elif rstd.affection >= 40:
            return "{=cheats_inline_random}{color=#ff714e}Warm"
        elif rstd.affection >= 5:
            return "{=cheats_inline_random}{color=#46e0ad}Like"
        elif rstd.affection >= 0:
            return "{=cheats_inline_random}{color=#ffe000}Indifference"
        elif rstd.affection >= -20:
            return "{=cheats_inline_random}{color=#000000}Dislike"
        elif rstd.affection < -20:
            return "{=cheats_inline_random}{color=#000000}Hate"

    def _student_intelligence_lvl(rstd):
        if rstd.intelligence >= 2.5:
            return "{=cheats_inline_20}Genius"
        elif rstd.intelligence >= 1.6:
            return "{=cheats_inline_20}Smart"
        elif rstd.intelligence >= 1.2:
            return "{=cheats_inline_20}Apt"
        elif rstd.intelligence >= 0.9:
            return "{=cheats_inline_20}Average"
        elif rstd.intelligence >= 0.7:
            return "{=cheats_inline_20}Limited"
        elif rstd.intelligence >= 0.5:
            return "{=cheats_inline_20}Slow"
        elif rstd.intelligence < 0.5:
            return "{=cheats_inline_20}Dim" 

    def read_rpy_file(file):
        with renpy.open_file(file, encoding="utf-8") as readfile:
            return readfile.readlines()

    def GenerateReplays(script):
        replacements = [
            ("Ayumi", "[ayumi.name]"), ("Haruka", "[haruka.name]"),
            ("Emiko", '[emiko.name]'), ("Yoko", '[yoko.name]'),
            ("Rina", '[rina.name]'), ("Suzu", "[suzu.name]"),
            ("Kawaguchi", "[hidetoshi.surname]"), ("Yusuke", "[main.name]")
        ]

        #Flag, Girl, Name, Block, Dict, Desc
        out = []

        data = read_rpy_file(script)

        for line in data:
            line = line.strip()
            line = line.replace('"', '').replace("\\","")
            ntr = False
            if "Replays(persistent." in line:
                start_index = line.find("Replays(persistent.") + len("Replays(persistent.")
                s = line[start_index:].replace(")", "")
                d = s.split(", ")

                if d[-1].startswith("ntr"):
                    ntr = True
                else:
                    fix = ", ".join([d[-2],d[-1]])
                    d = [i for i in d[0:5]]
                    d.append(fix)

                var = d[0]
                char = d[1]
                for og, rp in replacements:
                    d[1] = d[1].replace(og,rp)
                girl = d[1]
                for og, rp in replacements:
                    d[2] = d[2].replace(og,rp)
                name = d[2]
                label = d[3].strip()
                button_idle = label +"_idle"
                button_hover = label + "_hover"
                dic = eval(d[4])
                for og, rp in replacements:
                    d[5] = d[5].replace(og, rp)
                desc = d[5]
                #Variable, Girl, Girl_Name, Replay Name, Label, Desc
                out.append(ReplayCheat(var, char, name, label, dic, desc, ntr, button_idle, button_hover, WideRatio(384)))

        return out

    class ReplayCheat():
        def __init__(self, flag, girl, name, label, dic, desc, sharing, idle, hover, size):
            self.flag        = flag
            self.girl        = girl
            self.name        = name
            self.label       = label
            self.dic         = dic
            self.desc        = desc
            self.sharing     = sharing
            self.idle        = Transform(idle, xysize=size)
            self.hover       = Transform(hover, xysize=size)
            self.insensitive = Transform(idle, xysize=size, matrixcolor=SaturationMatrix(0.2))

    _cheats_replay = GenerateReplays("Replay System.rpy")

    bypass_list.extend(["CyclePersonalities", "CycleOutfits", "print_stats", "Generate_Char_Dict"])

    bypass_list.extend(["ReplayCheat", "GenerateReplays", "_cheats_replay", 
        "valid_dic_items", "walkthrough_dict", "wt_update", "filter_wt", 
        "update_check_walkthrough", "script_ignore_lines", 
        "event_ignore_lines"])

#######################################################################################
