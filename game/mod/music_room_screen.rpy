default persistent._current_music_room = 1
default persistent._music_icon_idle_color = "#FB4301"
default persistent._music_icon_hover_color = "#000"
default persistent._music_icon_idle_color_default = "#FB4301"
default persistent._music_icon_hover_color_default = "#000"
default persistent._music_overlay = True

screen musicroom():
    modal True
    style_prefix "musicroom"
    tag menu
    default barvalue = AdjustableAudioPositionValue()
    default barvalue_active = AudioPositionValue()
    default timer_active = False
    default show_locked = False
    default prog_tt = ""
    default mouse_active = False
    default current_room = get_rooms(persistent._current_music_room)
    default mood = "All"
    default previoustrack = ""
    default currentTrack = GetMusicPlaying(current_room).filename
    default nexttrack = ""

    $ tooltip = GetTooltip()
    default current_loop = False
    default current_track = None
    #if not main_menu:
    #    on "replace" action [SetLocalVariable("current_track", current_room.get_track()),
    #        SetLocalVariable("current_loop", renpy.music.get_loop())]
    #    if current_track:
    #        if not current_room.get_track() == current_track:
    #            key ("K_m", "game_menu") action Play("music", current_track, loop=current_loop), Function(preferences.set_mixer, "music", 0.5), Return()
    #        else:
    #            key ("K_m", "game_menu") action Queue("music", current_track, loop=current_loop), Function(preferences.set_mixer, "music", 0.5), Return()
    #    else:
    #        key ("K_m", "game_menu") action current_room.Stop(), Return()
    # Start the music playing on entry to the music room.
    if not renpy.music.is_playing() and persistent._start_music_on_enter:
        on "replace" action current_room.Play()

    #if not custom_keep_music_playing:
    #    # Restore the main menu music upon leaving.
    #    if config.main_menu_music:
    #        if not current_room.get_track() == config.main_menu_music:
    #            on "replaced" action Play("music", config.main_menu_music, loop=True), Function(preferences.set_mixer, "music", 0.5)
    #        else:
    #            on "replaced" action Queue("music", config.main_menu_music, loop=True), Function(preferences.set_mixer, "music", 0.5)
    #    else:
    #        on "replaced" action current_room.Stop()

    timer .5 action GetMusicPlaying(current_room), SetLocalVariable('currentTrack', GetMusicPlaying(current_room).filename) repeat True

    use game_menu(_("Music"), scroll=None):
        vbox:
            hbox:
                spacing 10
                xfill True
                imagebutton:
                    style "imagebutton_sounds"
                    idle Transform(
                        'mod/images/back_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/back_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_idle_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    hover Transform(
                        'mod/images/back_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/back_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_hover_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    selected "back_button_selected"
                    insensitive "back_button_insensitive"
                    action current_room.Previous(),SetLocalVariable("timer_active", True)
                    tooltip "Previous Track\n[current_room.previous_track]"
                imagebutton:
                    style "imagebutton_sounds"
                    idle Transform(
                        'mod/images/rewind_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/rewind_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_idle_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    hover Transform(
                        'mod/images/rewind_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/rewind_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_hover_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    selected "rewind_button_selected"
                    insensitive "rewind_button_insensitive"
                    action current_room.Rewind()
                    tooltip "Rewind\n[current_room.current_track]"
                if renpy.music.is_playing(channel='music'):
                    imagebutton:
                        style "imagebutton_sounds"
                        idle Transform(
                            ('mod/images/play_outline.png' if current_room.get_pause() else 'mod/images/pause_outline.png') if not persistent._use_outline_music_buttons else ('mod/images/play_solid.png' if current_room.get_pause() else 'mod/images/pause_solid.png'),
                            matrixcolor=ColorSingle(persistent._music_icon_idle_color),
                            xysize=(gui.button_size,gui.button_size),
                            align=(0.5,0.5))
                        hover Transform(
                            ('mod/images/play_outline.png' if current_room.get_pause() else 'mod/images/pause_outline.png') if not persistent._use_outline_music_buttons else ('mod/images/play_solid.png' if current_room.get_pause() else 'mod/images/pause_solid.png'),
                            matrixcolor=ColorSingle(persistent._music_icon_hover_color),
                            xysize=(gui.button_size,gui.button_size),
                            align=(0.5,0.5))
                        selected ("play_button_selected" if current_room.get_pause() else "pause_button_selected")
                        insensitive ("play_button_insensitive" if current_room.get_pause() else "pause_button_insensitive")
                        action current_room.TogglePause()
                        tooltip "Pause/Play\n[current_room.current_track]"
                else:
                    imagebutton:
                        style "imagebutton_sounds"
                        idle Transform(
                            'mod/images/play_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/play_solid.png',
                            matrixcolor=ColorSingle(persistent._music_icon_idle_color),
                            xysize=(gui.button_size,gui.button_size),
                            align=(0.5,0.5))
                        hover Transform(
                            'mod/images/play_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/play_solid.png',
                            matrixcolor=ColorSingle(persistent._music_icon_hover_color),
                            xysize=(gui.button_size,gui.button_size),
                            align=(0.5,0.5))
                        selected "play_button_selected"
                        insensitive "play_button_insensitive"
                        action current_room.Play()
                        tooltip "Play\n[current_room.current_track]"
                imagebutton:
                    style "imagebutton_sounds"
                    idle Transform(
                        'mod/images/stop_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/stop_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_idle_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    hover Transform(
                        'mod/images/stop_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/stop_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_hover_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    selected "stop_button_selected"
                    insensitive "stop_button_insensitive"
                    action current_room.Stop()
                    tooltip "Stop\n[current_room.current_track]"
                imagebutton:
                    style "imagebutton_sounds"
                    idle Transform(
                        'mod/images/fast_forward_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/fast_forward_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_idle_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    hover Transform(
                        'mod/images/fast_forward_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/fast_forward_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_hover_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    selected "fast_forward_button_selected"
                    insensitive "fast_forward_button_insensitive"
                    action current_room.Forward()
                    tooltip "Fast Forward\n[current_room.current_track]"
                imagebutton:
                    style "imagebutton_sounds"
                    idle Transform(
                        'mod/images/next_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/next_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_idle_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    hover Transform(
                        'mod/images/next_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/next_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_hover_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    selected "next_button_selected"
                    insensitive "next_button_insensitive"
                    action current_room.Next(),SetLocalVariable("timer_active", True)
                    tooltip "Next Track\n[current_room.next_track]"
                imagebutton:
                    style "imagebutton_sounds"
                    idle Transform(
                        ('mod/images/repeat_once_outline.png' if current_room.single_track else 'mod/images/repeat_outline.png') if not persistent._use_outline_music_buttons else ('mod/images/repeat_once_solid.png' if current_room.single_track else 'mod/images/repeat_solid.png'),
                        matrixcolor=ColorSingle(persistent._music_icon_idle_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    hover Transform(
                        ('mod/images/repeat_once_outline.png' if current_room.single_track else 'mod/images/repeat_outline.png') if not persistent._use_outline_music_buttons else ('mod/images/repeat_once_solid.png' if current_room.single_track else 'mod/images/repeat_solid.png'),
                        matrixcolor=ColorSingle(persistent._music_icon_hover_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    selected ("repeat_once_button_selected" if current_room.single_track else "repeat_button_selected")
                    insensitive ("repeat_once_button_insensitive" if current_room.single_track else "repeat_button_insensitive")
                    action current_room.ToggleSingleTrack()
                    tooltip "Repeat\n[current_room.current_track]"
                imagebutton:
                    style "imagebutton_sounds"
                    idle Transform(
                        ('mod/images/shuffle_outline.png' if current_room.shuffle else 'mod/images/shuffle_off_outline.png') if not persistent._use_outline_music_buttons else ('mod/images/shuffle_solid.png' if current_room.shuffle else 'mod/images/shuffle_off_solid.png') ,
                        matrixcolor=ColorSingle(persistent._music_icon_idle_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    hover Transform(
                        ('mod/images/shuffle_outline.png' if current_room.shuffle else 'mod/images/shuffle_off_outline.png') if not persistent._use_outline_music_buttons else ('mod/images/shuffle_solid.png' if current_room.shuffle else 'mod/images/shuffle_off_solid.png') ,
                        matrixcolor=ColorSingle(persistent._music_icon_hover_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    selected ("shuffle_button_selected" if current_room.shuffle else "shuffle_off_button_selected")
                    insensitive ("shuffle_button_insensitive" if current_room.shuffle else "shuffle_off_button_insensitive")
                    action current_room.ToggleShuffle()
                    tooltip "Shuffle Playlist"
                imagebutton:
                    style "imagebutton_sounds"
                    idle Transform(
                        'mod/images/settings_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/settings_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_idle_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    hover Transform(
                        'mod/images/settings_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/settings_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_hover_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    selected "settings_button_selected"
                    insensitive "settings_button_insensitive"
                    action Show("color_picker_mr", transition=dissolve)
                    tooltip "Settings"
                imagebutton:
                    style "imagebutton_sounds"
                    idle Transform(
                        ('mod/images/silent_outline.png' if get_mute(channel="music") == 0.0\
                        else 'mod/images/volume_half_outline.png' if get_mute(channel="music")\
                        > 0.0 and get_mute(channel="music") < 0.6 or get_mute(channel="music")\
                        == 0.6 else 'mod/images/volume_outline.png') if not persistent._use_outline_music_buttons\
                        else ('mod/images/silent_solid.png' if get_mute(channel="music") == 0.0\
                            else 'mod/images/volume_half_solid.png' if get_mute(channel="music")\
                            > 0.0 and get_mute(channel="music") < 0.6 or get_mute(channel="music")\
                            == 0.6 else 'mod/images/volume_solid.png'),
                        matrixcolor=ColorSingle(persistent._music_icon_idle_color),
                        xysize=gui.button_size_mute,
                        align=(0.5,0.5))
                    hover Transform(
                        ('mod/images/silent_outline.png' if get_mute(channel="music") == 0.0\
                        else 'mod/images/volume_half_outline.png' if get_mute(channel="music")\
                        > 0.0 and get_mute(channel="music") < 0.6 or get_mute(channel="music")\
                        == 0.6 else 'mod/images/volume_outline.png') if not persistent._use_outline_music_buttons\
                        else ('mod/images/silent_solid.png' if get_mute(channel="music") == 0.0\
                            else 'mod/images/volume_half_solid.png' if get_mute(channel="music")\
                            > 0.0 and get_mute(channel="music") < 0.6 or get_mute(channel="music")\
                            == 0.6 else 'mod/images/volume_solid.png'),
                        matrixcolor=ColorSingle(persistent._music_icon_hover_color),
                        xysize=gui.button_size_mute,
                        align=(0.5,0.5))
                    selected "mute_player_selected"
                    insensitive "mute_player_insensitive"
                    action MutePlayer()
                    tooltip "Mute Music"
                hbox:
                    spacing 5
                    xalign 1.0
                    add "readablePos" yalign 0.0 yoffset -5
                    bar value (barvalue if not timer_active and renpy.music.is_playing(channel='music') else barvalue_active):
                        if not timer_active:
                            hovered barvalue.hovered
                            unhovered barvalue.unhovered
                            tooltip "Progress\n[current_room.current_track]"
                        base_bar Frame(Solid(persistent._music_icon_idle_color), gui.slider_borders, tile=gui.slider_tile)
                        hover_base_bar Frame(Solid(persistent._music_icon_hover_color), gui.slider_borders, tile=gui.slider_tile)
                        thumb Transform(Solid(persistent._music_icon_hover_color),ysize=gui.slider_size, xsize=30)
                        hover_thumb Transform(Solid(persistent._music_icon_idle_color),ysize=gui.slider_size, xsize=30)
                        
                    add "readableDur" yalign 0.0 yoffset -5
            hbox:
                xfill True            
                vbox:
                    xalign 0.0
                    label _("Music Volume: %s"%VolumeDisplay('music')) xalign 0.0 text_color persistent._music_icon_idle_color
                vbox:
                    xalign 1.0
                    bar value Preference("music volume") xalign 1.0 tooltip "Volume\n{}".format(VolumeDisplay('music')):
                        hovered SetLocalVariable("mouse_active", True)
                        unhovered SetLocalVariable("mouse_active", False)
                        base_bar Frame(Solid(persistent._music_icon_idle_color), gui.slider_borders, tile=gui.slider_tile)
                        hover_base_bar Frame(Solid(persistent._music_icon_hover_color), gui.slider_borders, tile=gui.slider_tile)
                        thumb Transform(Solid(persistent._music_icon_hover_color),ysize=gui.slider_size, xsize=30)
                        hover_thumb Transform(Solid(persistent._music_icon_idle_color),ysize=gui.slider_size, xsize=30)
            hbox:
                xfill True
                text "Moods"
                for i in playlist_data:
                    if getattr(store, i[0]):
                        textbutton i[3]:
                            if i[3] != "All":
                                action [
                                    If(GetMusicPlaying(current_room).filename != i[1].playlist[0], i[1].Play(i[1].playlist[0])),
                                    SetLocalVariable("mood", i[3]), 
                                    SetField(persistent, "_current_music_room", i[2]), 
                                    SetLocalVariable("current_room", i[1])]
                            else:
                                action [
                                    If(GetMusicPlaying(current_room).filename != currentTrack, mr.Play(currentTrack)), 
                                    SetLocalVariable("mood", "All"), 
                                    SetField(persistent, "_current_music_room", 1), 
                                    SetLocalVariable("current_room", mr)]
                            selected persistent._current_music_room == i[2]
                            text_color persistent._music_icon_idle_color
                            text_hover_color persistent._music_icon_hover_color
                            text_selected_color gui.selected_color
            vpgrid:
                id "music"
                scrollbars "vertical"
                xsize config.screen_width - gui.game_menu_navigation_frame_xsize
                mousewheel True
                draggable True
                pagekeys True
                cols 1
                side_yfill True
                side_xfill True
                spacing 5
                xfill True
                vbox:
                    spacing 5
                    for artist in get_playlist(persistent._current_music_room).keys():
                        frame:
                            has vbox
                            text artist
                            for title in get_playlist(persistent._current_music_room)[artist].keys():
                                $ track_info = get_playlist(persistent._current_music_room)[artist][title]

                                $ track = track_info["musicroom_path"]
                                $ length = track_info.get("length", "0:00")
                                $ get_locked = track_info.get("unlocked")
                                $ locked = _("- locked") if not track_info.get("unlocked") else ""
                                $ custom = _(" (User Music)") if track_info.get("custom") else ""
                                if seen_track(track):
                                    $ track_info["unlocked"] = True
                                if mood == "All" or mood == track_info["mood"]:
                                    if show_locked:
                                        hbox:
                                            xfill True
                                            textbutton "{}{}({}){}".format(title," {}".format(locked), length, custom):
                                                if GetMusicPlaying(current_room).filename == track:
                                                    at music_playing_trans
                                                action current_room.Play(track),SelectedIf(current_room.Play(track)), SetLocalVariable("currentTrack", track)
                                                text_color persistent._music_icon_idle_color
                                                text_hover_color persistent._music_icon_hover_color
                                                text_selected_color gui.selected_color
                                            hbox:
                                                xalign 1.0
                                                textbutton "|" text_color persistent._music_icon_idle_color xalign 1.0
                                                textbutton track_info.get("credits_license_name", "None"):
                                                    action OpenURL(track_info.get("credits_license", "None"))
                                                    tooltip "%s License"%title
                                                    text_color persistent._music_icon_idle_color
                                                    text_hover_color persistent._music_icon_hover_color
                                                    text_selected_color gui.selected_color
                                                    xalign 1.0
                                                textbutton "|" text_color persistent._music_icon_idle_color xalign 1.0
                                                textbutton track_info.get("credits_link_name", "None"):
                                                    action OpenURL(track_info.get("credits_link", "None"))
                                                    tooltip "%s Link"%title
                                                    text_color persistent._music_icon_idle_color
                                                    text_hover_color persistent._music_icon_hover_color
                                                    text_selected_color gui.selected_color
                                                    xalign 1.0
                                    else:
                                        if get_locked:
                                            hbox:
                                                xfill True
                                                textbutton "{}{}({}){}".format(title," {}".format(locked), length, custom):
                                                    if GetMusicPlaying(current_room).filename == track:
                                                        at music_playing_trans
                                                    action current_room.Play(track),SelectedIf(current_room.Play(track)), SetLocalVariable("currentTrack", track)
                                                    text_color persistent._music_icon_idle_color
                                                    text_hover_color persistent._music_icon_hover_color
                                                    text_selected_color gui.selected_color
                                                hbox:
                                                    xalign 1.0
                                                    textbutton "|" text_color persistent._music_icon_idle_color xalign 1.0
                                                    textbutton track_info.get("credits_license_name", "None"):
                                                        action OpenURL(track_info.get("credits_license", "None"))
                                                        tooltip "%s License"%title
                                                        text_color persistent._music_icon_idle_color
                                                        text_hover_color persistent._music_icon_hover_color
                                                        text_selected_color gui.selected_color
                                                        xalign 1.0
                                                    textbutton "|" text_color persistent._music_icon_idle_color xalign 1.0
                                                    textbutton track_info.get("credits_link_name", "None"):
                                                        action OpenURL(track_info.get("credits_link", "None"))
                                                        tooltip "%s Link"%title
                                                        text_color persistent._music_icon_idle_color
                                                        text_hover_color persistent._music_icon_hover_color
                                                        text_selected_color gui.selected_color
                                                        xalign 1.0
                                        else:
                                            textbutton _("Locked")

    if timer_active:
        timer 3 action SetLocalVariable("timer_active", False)

    if tooltip:
        nearrect:
            focus "tooltip"
            prefer_top True
            frame:
                at choice_appear(.5)
                style_prefix "tooltip"
                if "Progress" in tooltip:
                    vbox:
                        text tooltip
                        add "readablePosTT" xalign 0.5
                else:
                    hbox:
                        text tooltip

    if mouse_active:
        key "mousedown_4" action SlowVolUp("music","_fast_vol_music","music")
        key "mousedown_5" action SlowVolDown("music","_fast_vol_music","music")

    text "Now Playing: [current_room.current_track]" align (0.99, 0.05)

screen color_picker_mr():
    modal True
    default activate = False
    default option = ""
    default field = ""
    use game_menu("Music Player Settings"):
        vbox:
            spacing 20
            vbox:
                style_prefix "check"
                label _("Music Volume\n[jg_s]{}".format("Fast" if persistent._fast_vol_music else "Slow"))
                textbutton _("Fast"):
                    action SetField(persistent, "_fast_vol_music", True)
                textbutton _("Slow"):
                    action SetField(persistent, "_fast_vol_music", False)
            vbox:
                style_prefix "check"
                label _("Music Buttons\n[jg_s]{}".format("Solid" if persistent._use_outline_music_buttons else "Outline"))
                textbutton _("Solid"):
                    action SetField(persistent, "_use_outline_music_buttons", True)
                textbutton _("Outline"):
                    action SetField(persistent, "_use_outline_music_buttons", False)

            hbox:
                spacing 10
                imagebutton:
                    idle Transform(
                        'mod/images/back_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/back_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_idle_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                
                    action NullAction()
                imagebutton:
                    idle Transform(
                        'mod/images/rewind_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/rewind_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_idle_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    action NullAction()
                imagebutton:
                    idle Transform(
                        'mod/images/play_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/play_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_idle_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    action NullAction()
                imagebutton:
                    idle Transform(
                        'mod/images/pause_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/pause_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_idle_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    action NullAction()
                imagebutton:
                    idle Transform(
                        'mod/images/stop_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/stop_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_idle_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    action NullAction()
                imagebutton:
                    idle Transform(
                        'mod/images/fast_forward_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/fast_forward_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_idle_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    action NullAction()
                imagebutton:
                    idle Transform(
                        'mod/images/next_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/next_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_idle_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    action NullAction()
                imagebutton:
                    idle Transform(
                        'mod/images/repeat_once_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/repeat_once_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_idle_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    action NullAction()
                imagebutton:
                    idle Transform(
                        'mod/images/repeat_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/repeat_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_idle_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    action NullAction()
                imagebutton:
                    idle Transform(
                        'mod/images/shuffle_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/shuffle_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_idle_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    action NullAction()
                imagebutton:
                    idle Transform(
                        'mod/images/shuffle_off_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/shuffle_off_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_idle_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    action NullAction()
                imagebutton:
                    idle Transform(
                        'mod/images/silent_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/silent_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_idle_color),
                        xysize=gui.button_size_mute,
                        align=(0.5,0.5))
                    action NullAction()
                imagebutton:
                    idle Transform(
                        'mod/images/volume_half_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/volume_half_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_idle_color),
                        xysize=gui.button_size_mute,
                        align=(0.5,0.5))
                    action NullAction()
                imagebutton:
                    idle Transform(
                        'mod/images/volume_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/volume_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_idle_color),
                        xysize=gui.button_size_mute,
                        align=(0.5,0.5))
                    action NullAction()
            hbox:#Good Choice
                spacing 15
                vbox:
                    textbutton "Set Idle Color Buttons":
                        
                        action If(option == "_music_icon_idle_color", 
                            true=[SetScreenVariable("activate", False), SetScreenVariable("option", ""), SetScreenVariable("field", "")], 
                            false=[SetScreenVariable("activate", True), SetScreenVariable("option", "_music_icon_idle_color"), SetScreenVariable("field", "_music_icon_idle_color")])
                        text_color persistent._music_icon_idle_color
                        text_hover_color adjust_brightness(persistent._music_icon_idle_color, -50)
                vbox:
                    textbutton "Reset":
                        action SetField(persistent, "_music_icon_idle_color", persistent._music_icon_idle_color_default) 
                        sensitive persistent._music_icon_idle_color != persistent._music_icon_idle_color_default
            hbox:
                spacing 10
                imagebutton:
                    idle Transform(
                        'mod/images/back_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/back_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_hover_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    action NullAction()
                imagebutton:
                    idle Transform(
                        'mod/images/rewind_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/rewind_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_hover_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    action NullAction()
                imagebutton:
                    idle Transform(
                        'mod/images/play_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/play_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_hover_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    action NullAction()
                imagebutton:
                    idle Transform(
                        'mod/images/pause_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/pause_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_hover_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    action NullAction()
                imagebutton:
                    idle Transform(
                        'mod/images/stop_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/stop_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_hover_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    action NullAction()
                imagebutton:
                    idle Transform(
                        'mod/images/fast_forward_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/fast_forward_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_hover_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    action NullAction()
                imagebutton:
                    idle Transform(
                        'mod/images/next_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/next_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_hover_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    action NullAction()
                imagebutton:
                    idle Transform(
                        'mod/images/repeat_once_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/repeat_once_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_hover_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    action NullAction()
                imagebutton:
                    idle Transform(
                        'mod/images/repeat_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/repeat_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_hover_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    action NullAction()
                imagebutton:
                    idle Transform(
                        'mod/images/shuffle_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/shuffle_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_hover_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    action NullAction()
                imagebutton:
                    idle Transform(
                        'mod/images/shuffle_off_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/shuffle_off_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_hover_color),
                        xysize=(gui.button_size,gui.button_size),
                        align=(0.5,0.5))
                    action NullAction()
                imagebutton:
                    idle Transform(
                        'mod/images/silent_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/silent_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_hover_color),
                        xysize=gui.button_size_mute,
                        align=(0.5,0.5))
                    action NullAction()
                imagebutton:
                    idle Transform(
                        'mod/images/volume_half_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/volume_half_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_hover_color),
                        xysize=gui.button_size_mute,
                        align=(0.5,0.5))
                    action NullAction()
                imagebutton:
                    idle Transform(
                        'mod/images/volume_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/volume_solid.png',
                        matrixcolor=ColorSingle(persistent._music_icon_hover_color),
                        xysize=gui.button_size_mute,
                        align=(0.5,0.5))
                    action NullAction()
            hbox:#Good Choice
                spacing 15
                vbox:
                    textbutton "Set Hover Color Buttons":
                        
                        action If(option == "_music_icon_hover_color", 
                            true=[SetScreenVariable("activate", False), SetScreenVariable("option", ""), SetScreenVariable("field", "")], 
                            false=[SetScreenVariable("activate", True), SetScreenVariable("option", "_music_icon_hover_color"), SetScreenVariable("field", "_music_icon_hover_color")])
                        text_color persistent._music_icon_hover_color
                        text_hover_color adjust_brightness(persistent._music_icon_hover_color, -50)
                vbox:
                    textbutton "Reset":
                        action SetField(persistent, "_music_icon_hover_color", persistent._music_icon_hover_color_default) 
                        sensitive persistent._music_icon_hover_color != persistent._music_icon_hover_color_default
            
        if activate:
            use color_picker(FieldSimpleValue(persistent,option), field)

transform music_playing_trans:
    alpha 1.0
    easein .5 alpha 0.5
    pause .5
    easein .5 alpha 1.0
    repeat

screen music_overlay():
    $ tooltip = GetTooltip()
    default current_room = get_rooms(persistent._current_music_room)
    default mood = "All"
    default currentTrack = GetMusicPlaying(current_room).filename
    default lock = False
    #timer .5 action [
    #    GetMusicPlaying(current_room), 
    #    SetLocalVariable("current_room", get_rooms(persistent._current_music_room)),
    #    SetLocalVariable('currentTrack', GetMusicPlaying(current_room).filename)] repeat True
    default shown = False

    mousearea:
        xysize (1000,600)
        align (1.0,0.12)
        hovered SetLocalVariable("shown", True), With(dissolve)
        unhovered SetLocalVariable("shown", False), With(dissolve)
    if shown and persistent._music_overlay or lock:
        frame:
            background Transform(Solid("#000"), alpha=.7)
            align (1.0,0.12)
            padding (20,10,20,10)
            xsize 1000
            ysize 600
            vbox:
                yfill True
                vbox:
                    spacing 5
                    yalign 0.0
                    text "Now Playing" size gui.bar_size+10
                    text "[current_room.current_track]" size gui.bar_size-5 xmaximum 1000
                hbox:
                    yalign 0.5
                    spacing 30
                    text "Progress" size gui.text_size-10
                    hbox:
                        xalign 1.0
                        yoffset -2
                        add "readablePosTT"
                        text "/" size gui.text_size-10
                        add "readableDurTT"
                vbox:
                    spacing 10
                    yalign 1.0
                    hbox:
                        spacing 10
                        xsize 1000
                        xfill True
                        text "Moods" yalign .5
                        for i in playlist_data:
                            if getattr(store, i[0]):
                                textbutton i[3][0]:
                                    if i[3] != "All":
                                        action [
                                            If(GetMusicPlaying(current_room).filename != i[1].playlist[0], i[1].Play(i[1].playlist[0])),
                                            SetVariable("mood", i[3]), 
                                            SetField(persistent, "_current_music_room", i[2]), 
                                            SetVariable("current_room", i[1])]
                                    else:
                                        action [
                                            If(GetMusicPlaying(current_room).filename != currentTrack, mr.Play(currentTrack)), 
                                            SetVariable("mood", "All"), 
                                            SetField(persistent, "_current_music_room", 1), 
                                            SetVariable("current_room", mr)]
                                    selected persistent._current_music_room == i[2]
                                    text_color persistent._music_icon_idle_color
                                    text_hover_color persistent._music_icon_hover_color
                                    text_selected_color gui.selected_color
                                    tooltip i[3]
                    hbox:
                        spacing 50
                        xalign 0.5
                        xsize 1000
                        xfill True
                        imagebutton:
                            style "imagebutton_sounds"
                            idle Transform(
                                'mod/images/back_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/back_solid.png',
                                matrixcolor=ColorSingle(persistent._music_icon_idle_color),
                                xysize=(gui.button_size,gui.button_size),
                                align=(0.5,0.5))
                            hover Transform(
                                'mod/images/back_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/back_solid.png',
                                matrixcolor=ColorSingle(persistent._music_icon_hover_color),
                                xysize=(gui.button_size,gui.button_size),
                                align=(0.5,0.5))
                            selected "back_button_selected"
                            insensitive "back_button_insensitive"
                            action current_room.Previous(),SetLocalVariable("timer_active", True)
                            tooltip "Previous Track\n[current_room.previous_track]"
                        if renpy.music.is_playing(channel='music'):
                            imagebutton:
                                style "imagebutton_sounds"
                                idle Transform(
                                    ('mod/images/play_outline.png' if current_room.get_pause() else 'mod/images/pause_outline.png') if not persistent._use_outline_music_buttons else ('mod/images/play_solid.png' if current_room.get_pause() else 'mod/images/pause_solid.png'),
                                    matrixcolor=ColorSingle(persistent._music_icon_idle_color),
                                    xysize=(gui.button_size,gui.button_size),
                                    align=(0.5,0.5))
                                hover Transform(
                                    ('mod/images/play_outline.png' if current_room.get_pause() else 'mod/images/pause_outline.png') if not persistent._use_outline_music_buttons else ('mod/images/play_solid.png' if current_room.get_pause() else 'mod/images/pause_solid.png'),
                                    matrixcolor=ColorSingle(persistent._music_icon_hover_color),
                                    xysize=(gui.button_size,gui.button_size),
                                    align=(0.5,0.5))
                                selected ("play_button_selected" if current_room.get_pause() else "pause_button_selected")
                                insensitive ("play_button_insensitive" if current_room.get_pause() else "pause_button_insensitive")
                                action current_room.TogglePause()
                                tooltip "Pause/Play\n[current_room.current_track]"
                        else:
                            imagebutton:
                                style "imagebutton_sounds"
                                idle Transform(
                                    'mod/images/play_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/play_solid.png',
                                    matrixcolor=ColorSingle(persistent._music_icon_idle_color),
                                    xysize=(gui.button_size,gui.button_size),
                                    align=(0.5,0.5))
                                hover Transform(
                                    'mod/images/play_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/play_solid.png',
                                    matrixcolor=ColorSingle(persistent._music_icon_hover_color),
                                    xysize=(gui.button_size,gui.button_size),
                                    align=(0.5,0.5))
                                selected "play_button_selected"
                                insensitive "play_button_insensitive"
                                action current_room.Play()
                                tooltip "Play\n[current_room.current_track]"
                        imagebutton:
                            style "imagebutton_sounds"
                            idle Transform(
                                'mod/images/stop_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/stop_solid.png',
                                matrixcolor=ColorSingle(persistent._music_icon_idle_color),
                                xysize=(gui.button_size,gui.button_size),
                                align=(0.5,0.5))
                            hover Transform(
                                'mod/images/stop_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/stop_solid.png',
                                matrixcolor=ColorSingle(persistent._music_icon_hover_color),
                                xysize=(gui.button_size,gui.button_size),
                                align=(0.5,0.5))
                            selected "stop_button_selected"
                            insensitive "stop_button_insensitive"
                            action current_room.Stop()
                            tooltip "Stop\n[current_room.current_track]"
                        imagebutton:
                            style "imagebutton_sounds"
                            idle Transform(
                                'mod/images/next_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/next_solid.png',
                                matrixcolor=ColorSingle(persistent._music_icon_idle_color),
                                xysize=(gui.button_size,gui.button_size),
                                align=(0.5,0.5))
                            hover Transform(
                                'mod/images/next_outline.png' if not persistent._use_outline_music_buttons else 'mod/images/next_solid.png',
                                matrixcolor=ColorSingle(persistent._music_icon_hover_color),
                                xysize=(gui.button_size,gui.button_size),
                                align=(0.5,0.5))
                            selected "next_button_selected"
                            insensitive "next_button_insensitive"
                            action current_room.Next(),SetLocalVariable("timer_active", True)
                            tooltip "Next Track\n[current_room.next_track]"
                        imagebutton:
                            style "imagebutton_sounds"
                            idle Transform(
                                ('mod/images/locked_outline.png' if lock else 'mod/images/unlocked_outline.png') if not persistent._use_outline_music_buttons else ('mod/images/locked_solid.png' if lock else 'mod/images/unlocked_solid.png'),
                                matrixcolor=ColorSingle(persistent._music_icon_idle_color),
                                xysize=(gui.button_size,gui.button_size),
                                align=(0.5,0.5))
                            hover Transform(
                                ('mod/images/locked_outline.png' if lock else 'mod/images/unlocked_outline.png') if not persistent._use_outline_music_buttons else ('mod/images/locked_solid.png' if lock else 'mod/images/unlocked_solid.png'),
                                matrixcolor=ColorSingle(persistent._music_icon_hover_color),
                                xysize=(gui.button_size,gui.button_size),
                                align=(0.5,0.5))
                            selected ("locked_button_selected" if lock else "unlocked_button_selected")
                            insensitive ("locked_button_insensitive" if lock else "unlocked_button_insensitive")
                            action ToggleLocalVariable("lock")
                            tooltip "Keep Screen Active"

    if tooltip:
        nearrect:
            focus "tooltip"
            prefer_top True
            frame:
                at choice_appear(.5)
                style_prefix "tooltip"
                if "Progress" in tooltip:
                    vbox:
                        text tooltip
                        add "readablePosTT" xalign 0.5
                else:
                    hbox:
                        text tooltip
    
init python:
    config.overlay_screens.append("music_overlay")

style musicroom_label_text is gui_label_text:
    color gui.bar_left_color
    outlines gui.musicroom_time_text_outlines

style imagebutton_sounds:
    hover_sound "mod/sfx/button_h.mp3"
    activate_sound "mod/sfx/button_a.mp3"

style musicroom_imagebutton:
    align (0.5, 0.5)

style musicroom_vscrollbar is gui_vscrollbar:
    unscrollable "hide"
    #base_bar Frame(Solid(gui.bar_left_color), gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    #thumb Frame(Solid(gui.bar_right_color), gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    #hover_base_bar Frame(Solid(gui.bar_right_color), gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    #hover_thumb Frame(Solid(gui.bar_left_color), gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style musicroom_text:
    properties gui.text_properties("musicroom")

style music_room_time:
    font gui.musicroom_time_text_font
    size gui.musicroom_time_size
    outlines gui.musicroom_time_text_outlines

style musicroom_hbox:
    ysize gui.bar_size*2

style musicroom_button:
    properties gui.button_properties("musicroom_button")
    xfill False
    hover_sound "mod/sfx/button_h.mp3"
    activate_sound "mod/sfx/button_a.mp3"

style musicroom_button_text:
    properties gui.text_properties("musicroom_button")

style musicroom_frame:
    background gui.musicroom_frame_background
    padding gui.musicroom_frame_padding
    xsize gui.musicroom_frame_xsize

style musicroom_bar is gui_bar:
    hover_sound "mod/sfx/button_h.mp3"
    activate_sound "mod/sfx/button_a.mp3"
    xsize 1000
    idle_left_bar Transform(
        Frame(
            "mod/images/%s_%s/left.png"%aspect_ratio,
            gui.bar_borders, tile=gui.bar_tile),
        matrixcolor=ColorSingle(gui.musicroom_bar_left_idle_color))
    idle_right_bar Transform(
        Frame(
            "mod/images/%s_%s/right.png"%aspect_ratio,
            gui.bar_borders, tile=gui.bar_tile),
        matrixcolor=ColorSingle(gui.musicroom_bar_right_idle_color))

    hover_left_bar Transform(
        Frame(
            "mod/images/%s_%s/left.png"%aspect_ratio,
            gui.bar_borders, tile=gui.bar_tile),
        matrixcolor=ColorSingle(gui.musicroom_bar_left_hover_color))
    hover_right_bar Transform(
        Frame(
            "mod/images/%s_%s/right.png"%aspect_ratio,
            gui.bar_borders, tile=gui.bar_tile),
        matrixcolor=ColorSingle(gui.musicroom_bar_right_hover_color))

style musicroom_slider is gui_slider:
    base_bar Frame(Solid(gui.bar_left_color), gui.slider_borders, tile=gui.slider_tile)
    hover_base_bar Frame(Solid(gui.bar_right_color), gui.slider_borders, tile=gui.slider_tile)
    thumb Transform(Solid(gui.bar_right_color),ysize=gui.slider_size, xsize=30)
    hover_thumb Transform(Solid(gui.bar_left_color),ysize=gui.slider_size, xsize=30)
    xsize 1000
    xalign 1.0