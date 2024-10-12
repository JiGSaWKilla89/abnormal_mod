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
Toggle Notifications Stack/Standard: {color=FB4301}N{/color}
Adjust Textbox Visibility Keypad {color=FB4301}+/-{/color}
"""

    wt_choice_tooltip = """Each Choice marked with either Good Choice/Bad Choice is
just a recommendation from me.
You play the game the way you want."""

init -5 python:
    import time
    import operator
    config.developer = True
    config.console = True
    config.autoreload = True
    config.rollback_length = 100
    config.hard_rollback_limit = 150

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
        "ADVCharacter", "ADVSpeaker", "Action", "AddToSet", "Alpha", "AlphaBlend", "AlphaDissolve", "AlphaMask", 
        "AnimatedValue", "Animation", "At", "Attribute", "AudioData", "AudioPositionValue", "Bar", "BarValue", 
        "Borders", "BrightnessMatrix", "Button", "Call", "Camera", "CaptureFocus", "Character", "ClearFocus", "Color", 
        "ColorMatrix", "ColorizeMatrix", "ComposeTransition", "Composite", "Condition", "ConditionGroup", "ConditionSwitch", 
        "Confirm", "Continue", "ContrastMatrix", "CopyToClipboard", "Crop", "CropMove", "CurrentScreenName", "CycleDict", 
        "CycleField", "CycleLocalVariable", "CycleScreenVariable", "CycleVariable", "DictEquality", "DictInputValue", 
        "DictValue", "DisableAllInputValues", "Dissolve", "DownloadSync", "Drag", "DragGroup", "DynamicCharacter", 
        "DynamicDisplayable", "DynamicImage", "EditFile", "EndReplay", "ExecJS", "FactorZoom", "Fade", "FieldEquality", 
        "FieldInputValue", "FieldValue", "FileAction", "FileCurrentPage", "FileCurrentScreenshot", "FileDelete", "FileJson", 
        "FileLoad", "FileLoadable", "FileNewest", "FilePage", "FilePageName", "FilePageNameInputValue", "FilePageNext", 
        "FilePagePrevious", "FileSave", "FileSaveName", "FileScreenshot", "FileSlotName", "FileTakeScreenshot", "FileTime", 
        "FileUsedSlots", "Fixed", "Flatten", "FontGroup", "Frame", "Function", "Gallery", "GamepadCalibrate", "GamepadExists", 
        "GetCharacterVolume", "GetFocusRect", "GetMixer", "GetTooltip", "Grid", "HBox", "Help", "Hide", "HideInterface", 
        "HueMatrix", "IdentityMatrix", "If", "Image", "ImageButton", "ImageDissolve", "ImageReference", "IncrementDict", 
        "IncrementField", "IncrementLocalVariable", "IncrementScreenVariable", "IncrementVariable", "Input", "InputValue", 
        "InvertMatrix", "InvertSelected", "JSONDB", "Jump", "Language", "Layer", "LayeredImage", "LayeredImageProxy", 
        "Live2D", "LiveComposite", "LiveCrop", "LiveTile", "LocalVariableInputValue", "LocalVariableValue", "MainMenu", 
        "Matrix", "Max", "MixerValue", "Model", "Motion", "MouseDisplayable", "MouseMove", "Move", "MoveFactory", "MoveIn", 
        "MoveOut", "MoveTransition", "Movie", "MultiPersistent", "MultiRevertable", "MultipleTransition", "MusicRoom", 
        "NVLCharacter", "NVLSpeaker", "NoRollback", "Notify", "Null", "NullAction", "OffsetMatrix", "OldMoveTransition", 
        "OpacityMatrix", "OpenDirectory", "OpenURL", "PY2", "Pan", "ParameterizedText", "Particles", "Pause", "PauseAudio", 
        "Pixellate", "Placeholder", "Play", "PlayCharacterVoice", "Position", "Preference", "PushMove", "Queue", "QueueEvent", 
        "QuickLoad", "QuickSave", "Quit", "RemoveFromSet", "Replay", "RestartStatement", "Return", "Revolve", "RevolveInOut", 
        "RollForward", "Rollback", "RollbackToIdentifier", "RotateMatrix", "RotoZoom", "RoundRect", "SaturationMatrix", 
        "ScaleMatrix", "ScreenVariableInputValue", "ScreenVariableValue", "Screenshot", "Scroll", "SelectedIf", "SensitiveIf", 
        "SepiaMatrix", "Set", "SetCharacterVolume", "SetDict", "SetField", "SetLocalVariable", "SetMixer", "SetMute", 
        "SetScreenVariable", "SetVariable", "SetVoiceMute", "Show", "ShowMenu", "ShowTransient", "ShowingSwitch", "SideImage", 
        "SizeZoom", "Skip", "SlottedNoRollback", "SnowBlossom", "Solid", "Speaker", "SplineMatrix", "SplineMotion", "Sprite", 
        "SpriteManager", "Start", "StaticValue", "Stop", "Style", "StylePreference", "SubTransition", "Swing", "Text", 
        "TextButton", "Tile", "TintMatrix", "ToggleDict", "ToggleField", "ToggleFocus", "ToggleLocalVariable", "ToggleMute", 
        "ToggleScreen", "ToggleScreenVariable", "ToggleSetMembership", "ToggleVariable", "ToggleVoiceMute", "Tooltip", 
        "Transform", "TransformMatrix", "UploadSync", "VBox", "VariableInputValue", "VariableValue", "Viewport", "VoiceInfo", 
        "VoiceReplay", "Window", "With", "XScrollValue", "YScrollValue", "Zoom", "ZoomInOut", 'absolute', 'color', 'defaultdict', 
        'dict', 'list', 'object', 'position', 'pystr', 'python_dict', 'python_list', 'python_object', 'python_set', 'set', 
        'str', 'unicode', 'xrange', 'alt', 'bchr', 'bord', 'eval', 'hyperlink_function', 'hyperlink_sensitive', 
        'hyperlink_styler', 'input', 'menu', 'nvl_clear', 'nvl_clear_next', 'nvl_erase', 'nvl_hide', 'nvl_menu', 'nvl_show', 
        'nvl_show_core', 'nvl_window', 'predict_menu', 'predict_say', 'print', 'range', 'raw_input', 'say', 'set_reload', 
        'sorted', 'sv', 'time_check', 'tobytes', 'toggle_skipping', 'var_search', 'voice', 'voice_can_replay', 'voice_replay', 
        'voice_sustain', "achievement", "audio", "bubble", "build", "director", "gui", "iap", "icon", "layeredimage", 
        "store", "textshader", "updater", "alicefade", "blinds", "buffbertfade", "dissolve", "downrightfade", "ease", 
        "easeinbottom", "easeinleft", "easeinright", "easeintop", "easeoutbottom", "easeoutleft", "easeoutright", 
        "easeouttop", "fade", "fadeslash", "fastfade", "fastredfade", "firefade", "flash", "hallofade", "healfade", 
        "holyfade", "hpunch", "in_03", "in_08", "in_09", "in_18", "in_24", "irisin", "irisout", "lightfade", 
        "longfade", "lucyfade", "lucyquickfade", "move", "moveinbottom", "moveinleft", "moveinright", "moveintop", 
        "moveoutbottom", "moveoutleft", "moveoutright", "moveouttop", "out_03", "out_08", "out_09", "out_18", "out_24", 
        "pinkfade", "pinkflash", "pixellate", "portalfade", "pushdown", "pushleft", "pushright", "pushup", "redfade", 
        "slideawaydown", "slideawayleft", "slideawayright", "slideawayup", "slidedown", "slideleft", "slideright", "slideup", 
        "slowyellowfade", "squares", "upleftfade", "virginfade", "vpunch", "wipedown", "wipeleft", "wiperight", "wipeup", 
        "yorikofade", "zoomin", "zoominout", "zoomout", "bypass_list", "center", "default", "delayed_blink", "left", 
        "notify_appear", "offscreenleft", "offscreenright", "reset", "right", "swing", "top", "topleft", "topright", 
        "truecenter", "config", "anim ", "basestring ", "chr", "default_transition", "define", "division", "extend", 
        "im", "inspect", "layout", "library", "nvl_list", "nvl_variant", "open", "os", "persistent", "preferences", 
        "print_function", "pygame_sdl2", "quick_menu", "random", "renpy", "round", "style", "suppress_overlay", "sys", 
        "theme", "ui", "unicode_literals", "vldf_timer", "with_statement", "mouse_visible", "absolute_import", "main_menu", 
        "small", "touch", "AlwaysEffectChange", "AutoForwardTime", "EffectDelayDisplay", "FancyCheck", "FancyText", "SlowEffectChange", 
        "TextSpeed", "ToggleFancyText", "VolumeDisplay", "always_pulse", "always_shake", "save_name", "slow_fade", 
        "slow_nonsense", "slow_rotate", "slow_shake", "slow_shaking_slide", "slow_slide_down", "slow_slide_left", 
        "slow_slide_right", "slow_slide_up", "slow_typewriter",
        ]
    
    bypass_list = [i.strip() for i in bypass_list]

    def adjust_brightness(hex_color, levels):
        def clamp(value):
            return max(0, min(255, value))

        # Convert hex to RGB(A)
        hex_color = hex_color.lstrip('#')

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
        for i in dir(default):
            if not i.startswith(("_","__")):
                if name:
                    if name in i:
                        print("VAR:{} | VALUE:{}".format(i, eval(i)))
                else:
                    if isinstance(eval(i),renpy.character.ADVCharacter):
                        pass
                    elif i in bypass_list:
                        pass
                    else:
                        print("VAR:{} | VALUE:{}".format(i, eval(i)))

    def set_reload():
        print(config.reload)
        if config.autoreload:
            config.autoreload = False
        else:
            config.autoreload = True

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
            if main_menu and not self.bypass:
                return
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
            if main_menu and not self.bypass:
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
            if main_menu and not self.bypass:
                return
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
            if main_menu and not self.bypass:
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

init 1:
    image splashText = Text(shortcuts.strip(), style="splash")
    default preferences.text_cps = 120
    default persistent._unlocked_gallery = False
    default persistent._show_empty_gallery = False
    default persistent._sharing_content = False

    default _go_to_page = ""
    default jg_s = "{size=40}"
    default jg_1 = "{color=#FB4301}"
    default jg_2 = "{color=#000000}"
    default jg_3 = "{/color}"

    default notify_messages = []
    default notify_duration = 4.0
    default notify_history_length = 5

init python:
    def read_rpy_file(file):
        with renpy.open_file(file, encoding="utf-8") as readfile:
            return readfile.readlines()

