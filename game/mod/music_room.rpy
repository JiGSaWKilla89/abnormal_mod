default music_last_playing = None
default stoptrack = None
default time_position = 0.0
default time_duration = 0.0
default persistent._current_music_room = 1
default persistent._music_icon_idle_color = "#FB4301"
default persistent._music_icon_hover_color = "#2a2a2a"
default persistent._music_icon_idle_color_default = "#FB4301"
default persistent._music_icon_hover_color_default = "#2a2a2a"
default persistent._music_overlay = True
default persistent._music_ff_rew = 1.0
default persistent._start_music_on_enter = True
default custom_keep_music_playing = True
default persistent._use_outline_music_buttons = False

init 10 python:
    def MP_IMG(img,state="idle", size=(gui.button_size,gui.button_size)):
        return Transform(
            'mod/images/{}_outline.png'.format(img) if not persistent._use_outline_music_buttons else 'mod/images/{}_solid.png'.format(img),
            matrixcolor=ColorSingle(getattr(persistent, "_music_icon_{}_color".format(state))),
            xysize=size,
            align=(0.5,0.5))
    
    def MP_BAR(state):
        return Frame(Solid(getattr(persistent, "_music_icon_{}_color".format(state))), gui.slider_borders, tile=gui.slider_tile)

    def MP_THUMB(state):
        return Transform(Solid(getattr(persistent,"_music_icon_{}_color".format(state))),ysize=gui.slider_size, xsize=60)

    def MP_TEXT(state):
        return getattr(persistent, "_music_icon_{}_color".format(state))

init -1000 python:
    import pygame
    import re
    from mutagen.oggvorbis import OggVorbis
    from mutagen.mp3 import MP3
    from mutagen.flac import FLAC
    from mutagen.oggopus import OggOpus
    from mutagen import File as MutagenFile

    if persistent._fast_vol_music == None:
        persistent._fast_vol_music = True

    class SlowVolUp(Action):
        def __init__(self,channel,control,check):
            self.channel = channel
            self.control = f"persistent.{control}"
            self.defaultvolumea = 0.01 if not eval(self.control) else 0.1
            self.defaultvolumeb = "0.01" if not eval(self.control) else 0.1
            self.check = f"config.has_{check}"

        def __call__(self):
            if eval(self.check):
                self.slowvolup()
                renpy.restart_interaction()

        def slowvolup(self):
            global preferences
            try:
                myvol = float(round(preferences.get_mixer(self.channel),2))
            except:
                myvol = float(round(preferences.get_volume(self.channel),2))
            vol = myvol
            vollist = list(float_range(0, 1, self.defaultvolumeb))

            if eval(self.control):
                myvol = min(vollist, key=lambda x:abs(x-myvol))
            for i in vollist:
                if myvol == i:
                    vol += self.defaultvolumea
                    try:
                        preferences.set_mixer(self.channel,max(0.0, min(1.0, vol)))
                    except:
                        preferences.set_volume(self.channel,max(0.0, min(1.0, vol)))
            return

    class SlowVolDown(Action):
        def __init__(self,channel,control,check):
            self.channel = channel
            self.control = f"persistent.{control}"
            self.defaultvolumea = 0.01 if not eval(self.control) else 0.1
            self.defaultvolumeb = "0.01" if not eval(self.control) else 0.1
            self.check = f"config.has_{check}"
        def __call__(self):
            if eval(self.check):
                self.slowvoldown()
                renpy.restart_interaction()

        def slowvoldown(self):
            global preferences
            try:
                myvol = float(round(preferences.get_mixer(self.channel),2))
            except:
                myvol = float(round(preferences.get_volume(self.channel),2))
            vol = myvol
            vollist = list(float_range(0, 1, self.defaultvolumeb))

            if eval(self.control):
                myvol = min(vollist, key=lambda x:abs(x-myvol))
            if myvol == 1.0:
                vol -= self.defaultvolumea
                preferences.set_volume(self.channel,vol)
            for i in vollist:
                if myvol == i:
                    vol -= self.defaultvolumea
                    try:
                        preferences.set_mixer(self.channel,max(0.0, min(1.0, vol)))
                    except:
                        preferences.set_volume(self.channel,max(0.0, min(1.0, vol)))
            return

    def setRepeatRateup():
        if hasattr(config,"key_repeat"):
            setattr(config,"key_repeat",(.1, .001))

    def setRepeatRatedown():
        if hasattr(config,"key_repeat"):
            setattr(config,"key_repeat",(.3, .03))

    def generate_float_list(start,end,step):
        float_list = []
        # generate floats from 1.0 to 0.5 with a step of 0.01
        for i in range(start, end, step):
            float_list.append(round(i/100, 2))
        return float_list

    def round_float(value):
        return round(float(value),2)

    def float_range(start, stop, step):
        import decimal
        while start < stop:
            yield float(start)
            start += decimal.Decimal(step)

    class MutePlayer(Action):
        custom_vol = 0.0
        def __init__(self, channel="music", custom=False):
            self.custom = custom
            self.channel = channel

        def __call__(self):
            '''
            Mutes the music player.
            '''
            global preferences
            try:
                if float(round(preferences.get_mixer(self.channel),2)) in generate_float_list(100,50,-1):
                    preferences.set_mixer(self.channel, 0.5)
                elif float(round(preferences.get_mixer(self.channel),2)) in generate_float_list(50,0,-1):
                    preferences.set_mixer(self.channel, 0.0)
                elif float(round(preferences.get_mixer(self.channel),2)) == 0.0:
                    preferences.set_mixer(self.channel, 1.0)
            except:
                if float(round(preferences.get_volume(self.channel),2)) in generate_float_list(100,50,-1):
                    preferences.set_volume(self.channel, 0.5)
                elif float(round(preferences.get_volume(self.channel),2)) in generate_float_list(50,0,-1):
                    preferences.set_volume(self.channel, 0.0)
                elif float(round(preferences.get_volume(self.channel),2)) == 0.0:
                    preferences.set_volume(self.channel, 1.0)

            renpy.restart_interaction()

        def selected(self):
            try:
                return preferences.get_mixer(self.channel) == 0.0
            except:
                return preferences.get_volume(self.channel) == 0.0

    def get_mute(channel="music"):
        try:
            return preferences.get_mixer(channel)
        except:
            return preferences.get_volume(channel)

    def convert_time(x):
        '''
        Converts track position and duration to human-readable time.
        '''

        hour = ""

        if int (x / 3600) > 0:
            hour = str(int(x / 3600))

        if hour != "":
            if int((x % 3600) / 60) < 10:
                minute = ":0" + str(int((x % 3600) / 60))
            else:
                minute = ":" + str(int((x % 3600) / 60))
        else:
            minute = "" + str(int(x / 60))

        if int(x % 60) < 10:
            second = ":0" + str(int(x % 60))
        else:
            second = ":" + str(int(x % 60))

        return hour + minute + second

    def music_pos(style_name, size, yalign, st, at):
        '''
        Returns the track position to Ren'Py.
        '''

        global time_position
        if renpy.music.is_playing(channel="music"):
            if renpy.music.get_pos(channel='music') is not None:
                time_position = renpy.music.get_pos(channel='music') or time_position
        else:
            time_position = 0.0

        readableTime = convert_time(time_position)
        d = Text(readableTime, style=style_name, size=size, xalign=0.0, yalign=yalign)
        return d, 0.20

    def music_postt(style_name, size, st, at):
        '''
        Returns the track position to Ren'Py.
        '''

        global time_position
        if renpy.music.is_playing(channel="music"):
            if renpy.music.get_pos(channel='music') is not None:
                time_position = renpy.music.get_pos(channel='music') or time_position
        else:
            time_position = 0.0

        readableTime = convert_time(time_position)
        d = Text(readableTime, style=style_name, size=size, xalign=0.0, yalign=0.5)
        return d, 0.20

    def music_dur(style_name, size, yalign, st, at):
        '''
        Returns the track duration to Ren'Py.
        '''

        global time_duration
        if renpy.music.is_playing(channel="music"):
            try:
                time_duration = get_audio_length() or time_duration
            except:
                time_duration = renpy.music.get_duration(
                    channel='music') or time_duration
        else:
            time_duration = 0.0

        readableDuration = convert_time(time_duration)
        d = Text(readableDuration, style=style_name, size=size, xalign=0.5, yalign=yalign)
        return d, 0.20

    def music_durtt(style_name, size, st, at):
        '''
        Returns the track duration to Ren'Py.
        '''

        global time_duration
        if renpy.music.is_playing(channel="music"):
            try:
                time_duration = get_audio_length() or time_duration
            except:
                time_duration = renpy.music.get_duration(
                    channel='music') or time_duration
        else:
            time_duration = 0.0

        readableDuration = convert_time(time_duration)
        d = Text(readableDuration, style=style_name, size=size, xalign=0.5, yalign=0.5)
        return d, 0.20

    @renpy.pure
    class __CustomMusicRoomPlay(Action, FieldEquality):
        """
        The action returned by MusicRoom.Play when called with a file.
        """

        identity_fields = [ "mr" ]
        equality_fields = [ "filename" ]

        def __init__(self, mr, filename, loop):
            self.mr = mr
            self.filename = filename
            self.loop = loop
            self.selected = self.get_selected()

        def __call__(self):

            renpy.restart_interaction()

            if self.mr.get_track(self.mr.channel) == self.filename:
                if renpy.music.get_pause(self.mr.channel):
                    renpy.music.set_pause(False, self.mr.channel)
                    return

            self.mr.play(self.filename, 0, loop=self.loop)
            file = self.mr.get_track(self.mr.channel)
            if self.filename != file:
                self.filename = file

        def get_sensitive(self):
            return self.mr.is_unlocked(self.filename)

        def get_selected(self):
            return self.mr.get_track(self.mr.channel) == self.filename

        def periodic(self, st):
            if self.selected != self.get_selected():
                self.selected = self.get_selected()
                renpy.restart_interaction()

            self.mr.periodic(st)

            return .1

    #renpy.loader.transfn(os.path.join(config.gamedir, "audio", "sfx", "Alexander Nakarada - Blood And Steel.ogg"))
    #get_music_len(os.path.join(config.gamedir, "audio", "sfx", "Alexander Nakarada - Blood And Steel.ogg"))
    def get_music_len(file, readable=True):
        from io import BytesIO
        audio = None

        try:
            track = renpy.open_file(file)
            track_data = track.read()

            filename = BytesIO(track_data)
            filename.seek(0)

            audio = MutagenFile(filename, easy=False)

            if audio.info.length:
                if readable:
                    length_seconds = int(audio.info.length)
                    minutes, seconds = divmod(length_seconds, 60)
                    return "{}:{:02}".format(minutes, seconds)
                else:
                    return audio.info.length
            else:
                return 0.0
        except Exception as e:
            renpy.write_log("Executing Method 2 as BytesIO Method Failed | Error: {}".format(e))
            try:
                audio = OggVorbis(file)
            except Exception:
                try:
                    audio = MP3(file)
                except Exception:
                    try:
                        audio = FLAC(file)
                    except Exception:
                        try:
                            audio = OggOpus(file)
                        except Exception as e:
                            renpy.write_log("Error: {}".format(e))
                            return None
            if audio:
                if readable:
                    length_seconds = int(audio.info.length)
                    minutes, seconds = divmod(length_seconds, 60)
                    return "{}:{:02}".format(minutes, seconds)
                else:
                    return audio.info.length
            else:
                return 0.0

    @renpy.pure
    class AdjustableAudioPositionValue(BarValue, DictEquality):

        '''
        Class that replicates a music progress bar in Ren'Py.
        '''
        def __init__(self, update_interval=0.01):
            self.mr = mr
            self.update_interval = update_interval
            self._hovered = False
            self.duration = renpy.music.get_duration(self.mr.channel)
            self.pos = renpy.music.get_pos(self.mr.channel)
            self.adjustment = None
            self.current = None
            self.length = 0.0

        def next_track(self):
            playlist = self.mr.unlocked_playlist()
            music_playing = self.mr.get_track(self.mr.channel) if renpy.music.is_playing(self.mr.channel) else playlist[0]

            try:
                current_index = playlist.index(next((i for i in playlist if i in music_playing), playlist[0]))
                previous_index = (current_index - 1) % len(playlist)
                next_index = (current_index + 1) % len(playlist)

            except (ValueError, IndexError):
                next_index = None
                current_index = None
                previous_index = None

            return playlist[previous_index],playlist[current_index],playlist[next_index]

        def get_audio_length(self):
            music_file = self.mr.get_track(self.mr.channel)
            if self.current != music_file:

                path = os.path.join(config.gamedir, music_file).replace('\\','/')
                if renpy.loadable(path):
                    file = renpy.loader.transfn(path)
                else:
                    file = music_file
                length = get_music_len(file, False)
                self.current = music_file
                self.length = length
            return self.length

        def get_pos_duration(self):
            global time_position, time_duration

            pos = time_position\
                if not renpy.music.is_playing(self.mr.channel)\
                    else renpy.music.get_pos(self.mr.channel) or self.pos\
                    if self.pos != None else 0.0
            try:
                duration = self.get_audio_length() or self.duration
            except:
                duration = time_duration\
                    if not renpy.music.is_playing(self.mr.channel)\
                    else renpy.music.get_duration(self.mr.channel) or self.duration\
                    if self.duration != 0.0 else 3.0
            return pos, duration

        def getloop_shuffle(self):
            loop = self.mr.single_track
            shuffle = self.mr.shuffle
            return loop, shuffle

        def get_adjustment(self):
            pos, duration = self.get_pos_duration()
            self.adjustment = renpy.ui.adjustment(value=pos, range=duration,
                changed=self.set_pos, adjustable=True)

            return self.adjustment

        def hovered(self):
            self._hovered = True

        def unhovered(self):
            self._hovered = False

        def set_pos(self, value=0):
            loop, shuffle = self.getloop_shuffle()
            pos, duration = self.get_pos_duration()
            if (self._hovered and pygame.mouse.get_pressed()[0]):
                self.pos = value

            if pos != self.pos:
                mr.play_from(str(self.next_track()[1]),value=value)

                renpy.music.queue(self.next_track()[2]\
                    if not loop else self.next_track()[1],
                    self.mr.channel, loop=loop)

            self.pos = value

        def periodic(self, st):
            pos, duration = self.get_pos_duration()
            loop, shuffle = self.getloop_shuffle()
            self.pos = pos

            self.set_new_track()

            if self.duration != duration:
                self.duration = duration

            if pos and pos <= self.duration:
                self.adjustment.set_range(self.duration)
                self.adjustment.change(pos)

            if pos > self.duration - 0.20:
                if (self._hovered and pygame.mouse.get_pressed()[0]):
                    if loop:
                        renpy.music.play(self.next_track()[1],
                            self.mr.channel,
                            loop=True,
                            fadein=self.mr.fadein,
                            tight=True)
                    elif shuffle:
                        renpy.music.play(self.next_track()[2],
                            self.mr.channel,
                            loop=False,
                            fadein=self.mr.fadein,
                            tight=True)
                    elif not loop and not shuffle:
                        renpy.music.play(self.next_track()[2],
                            self.mr.channel,
                            loop=False,
                            fadein=self.mr.fadein,
                            tight=True)
                elif not self._hovered:
                    if loop:
                        renpy.music.queue(self.next_track()[1],
                            self.mr.channel,
                            loop=True,
                            fadein=self.mr.fadein,
                            tight=True)
                    elif shuffle:
                        renpy.music.queue(self.next_track()[2],
                            self.mr.channel,
                            loop=False,
                            fadein=self.mr.fadein,
                            tight=True)
                    elif not loop and not shuffle:
                        renpy.music.queue(self.next_track()[2],
                            self.mr.channel,
                            loop=False,
                            fadein=self.mr.fadein,
                            tight=True)

            return self.update_interval

        def set_new_track(self):
            self.filename = self.mr.get_track()

    MusicRoom.duration = 0.0
    MusicRoom.position = 0.0

    def musicroom_match(self,val):
        # Define regular expressions to match the <from> segment and file extension
        from_regex = r"\<from (\d+\.\d+)\>"

        result = re.sub(from_regex,"",val)

        return result

    MusicRoom.match = musicroom_match

    def musicroom_get_track(self,channel="music"):
        filename = renpy.music.get_playing(channel)

        if filename != None:
            if "<from" in filename:
                filename = self.match(filename)
            else:
                filename = renpy.music.get_playing(channel=self.channel)

        #if not renpy.seen_audio(filename):
        #    renpy.seen_audio(filename)

        return filename

    MusicRoom.get_track = musicroom_get_track

    def musicroom_Play(self, filename=None, loop=None):
        global music_last_playing
        """
        :doc: music_room method

        This action causes the music room to start playing. If `filename` is given, that
        file begins playing. Otherwise, the currently playing file starts
        over (if it's unlocked), or the first file starts playing.

        If `filename` is given, buttons with this action will be insensitive
        while `filename` is locked, and will be selected when `filename`
        is playing.
        """
        if hasattr(store,"music_last_playing"):
            if music_last_playing != None:
                filename = music_last_playing
                music_last_playing = None

        if filename is None:
            return self.play

        if filename != None:
            if "<from" in filename:
                filename = self.match(filename)
                return filename

        if filename not in self.filenames:
            raise Exception("{0!r} is not a filename registered with this music room.".format(filename))

        return __CustomMusicRoomPlay(self, filename, loop)

    MusicRoom.Play = musicroom_Play

    def musicroom_play(self, filename=None, offset=0, queue=False, loop=None, shuffle=None, custom=False):
        """
        Starts the music room playing. The file we start playing with is
        selected in two steps.

        If `filename` is an unlocked file, we start by playing it.
        Otherwise, we start by playing the currently playing file, and if
        that doesn't exist or isn't unlocked, we start with the first file.

        We then apply `offset`. If `offset` is positive, we advance that many
        files, otherwise we go back that many files.

        If `queue` is true, the music is queued. Otherwise, it is played
        immediately.
        """

        playlist = self.unlocked_playlist(filename)
        if not playlist:
            return

        if filename is None:
            filename = self.get_track(self.channel) if not self.get_track(self.channel) == None\
                else self.store_current_track()\
                if not self.store_current_track == None\
                else renpy.music.get_playing(channel=self.channel)\
                if renpy.music.get_playing(channel=self.channel) != None\
                else playlist[0]

        try:
            idx = playlist.index(filename)
        except ValueError:
            idx = 0

        idx = (idx + offset) % len(playlist)

        if self.single_track:
            playlist = [ playlist[idx] ]
        elif self.loop:
            playlist = playlist[idx:] + playlist[:idx]
        else:
            playlist = playlist[idx:]

        if queue:
            renpy.music.queue(playlist, channel=self.channel, loop=self.loop)
        else:
            renpy.music.play(playlist, channel=self.channel, fadeout=self.fadeout, fadein=self.fadein, loop=self.loop)

    MusicRoom.play = musicroom_play

    def musicroom_play_from(self, filename=None,offset=0,queue=False,value=0.0, **kwargs):
        """
        Starts the music room playing. The file we start playing with is
        selected in two steps.

        If `filename` is an unlocked file, we start by playing it.
        Otherwise, we start by playing the currently playing file, and if
        that doesn't exist or isn't unlocked, we start with the first file.

        We then apply `offset`. If `offset` is positive, we advance that many
        files, otherwise we go back that many files.

        If `queue` is true, the music is queued. Otherwise, it is played
        immediately.

        This will help will the adjustable position slider
        """

        playlist = self.unlocked_playlist(filename)

        if not playlist:
            return

        if filename is None:
            filename = renpy.music.get_playing(channel=self.channel)

        try:
            idx = playlist.index(filename)
        except ValueError:
            idx = 0

        idx = (idx + offset) % len(playlist)

        if self.single_track:
            playlist = [ playlist[idx] ]
        elif self.loop:
            playlist = playlist[idx:] + playlist[:idx]
        else:
            playlist = playlist[idx:]

        if queue:
            renpy.music.queue(playlist, channel=self.channel, loop=self.loop)
        else:
            renpy.music.play("<from {}>{}".format(value,filename), channel=self.channel, loop=self.loop, **kwargs)

    MusicRoom.play_from = musicroom_play_from

    def musicroom_periodic(self, st):
        global music_last_playing

        if st == self.st:
            return
        elif st < self.st:
            self.last_playing = None

        self.st = st

        current_playing = self.get_track(self.channel)
        if current_playing is None:
            current_playing = ""

        if self.last_playing != current_playing:
            action = self.action.get(current_playing, None)
            renpy.run_action(action)

        if renpy.music.is_playing(channel=self.channel):
            self.last_playing = current_playing
            music_last_playing = current_playing
        else:
            self.last_playing = music_last_playing

        self.Previous_Current_Next()

    MusicRoom.periodic = musicroom_periodic

    def musicroom_forward(self, filename=None,offset=0,queue=False,value=0.0, **kwargs):
        """
        Starts the music room playing. The file we start playing with is
        selected in two steps.

        If `filename` is an unlocked file, we start by playing it.
        Otherwise, we start by playing the currently playing file, and if
        that doesn't exist or isn't unlocked, we start with the first file.

        We then apply `offset`. If `offset` is positive, we advance that many
        files, otherwise we go back that many files.

        If `queue` is true, the music is queued. Otherwise, it is played
        immediately.
        """

        playlist = self.unlocked_playlist(filename)

        if not playlist:
            return

        if filename is None:
            filename = self.get_track(self.channel)

        try:
            idx = playlist.index(filename)
        except ValueError:
            idx = 0

        idx = (idx + offset) % len(playlist)

        if self.single_track:
            playlist = [ playlist[idx] ]
        elif self.loop:
            playlist = playlist[idx:] + playlist[:idx]
        else:
            playlist = playlist[idx:]

        pos = self.get_position()

        dur = self.get_duration()

        value = pos+persistent._music_ff_rew

        if value >= dur:
            value = dur

        if queue:
            if renpy.music.is_playing(self.channel):
                renpy.music.queue(playlist, channel=self.channel, loop=self.loop)
        else:
            if renpy.music.is_playing(self.channel):
                renpy.music.play("<from {}>{}".format(value, filename), channel=self.channel, loop=self.loop, **kwargs)

    MusicRoom.forward = musicroom_forward

    def musicroom_rewind(self, filename=None,offset=0,queue=False,value=0.0, **kwargs):
        """
        Starts the music room playing. The file we start playing with is
        selected in two steps.

        If `filename` is an unlocked file, we start by playing it.
        Otherwise, we start by playing the currently playing file, and if
        that doesn't exist or isn't unlocked, we start with the first file.

        We then apply `offset`. If `offset` is positive, we advance that many
        files, otherwise we go back that many files.

        If `queue` is true, the music is queued. Otherwise, it is played
        immediately.
        """

        playlist = self.unlocked_playlist(filename)

        if not playlist:
            return

        if filename is None:
            filename = self.get_track(self.channel)

        try:
            idx = playlist.index(filename)
        except ValueError:
            idx = 0

        idx = (idx + offset) % len(playlist)

        if self.single_track:
            playlist = [ playlist[idx] ]
        elif self.loop:
            playlist = playlist[idx:] + playlist[:idx]
        else:
            playlist = playlist[idx:]

        pos = self.get_position()
        dur = self.get_duration()

        value = pos-persistent._music_ff_rew

        if value < 0.0:
            value = 0.0

        if queue:
            if renpy.music.is_playing(self.channel):
                renpy.music.queue(playlist, channel=self.channel, loop=self.loop)
        else:
            if renpy.music.is_playing(self.channel):
                renpy.music.play("<from {}>{}".format(value, filename), channel=self.channel, loop=self.loop, **kwargs)

    MusicRoom.rewind = musicroom_rewind

    def musicroom_get_position(self):
        if not renpy.music.is_playing(self.channel):
            pos = self.position
        else:
            pos = renpy.music.get_pos(self.channel) or 0.0
        return pos

    MusicRoom.get_position = musicroom_get_position

    def musicroom_get_duration(self):
        if renpy.music.is_playing(channel="music"):
            try:
                time_duration = get_music_len(mr.get_track(), False) or self.duration
            except:
                time_duration = renpy.music.get_duration(
                    channel='music') or time_duration
        else:
            time_duration = self.duration
        return time_duration

    MusicRoom.get_duration = musicroom_get_duration

    def musicroom_Forward(self):
        return self.forward

    MusicRoom.Forward = musicroom_Forward

    def musicroom_Rewind(self):
        return self.rewind

    MusicRoom.Rewind = musicroom_Rewind

    def musicroom_getpause(self):
        return renpy.music.get_pause(self.channel)

    MusicRoom.get_pause = musicroom_getpause

    def musicroom_playing(self):
        return renpy.music.is_playing(self.channel)

    MusicRoom.is_playing = musicroom_playing

    def musicroom_store_current_track(self):
        global stoptrack
        filename = self.get_track(channel=self.channel)
        stoptrack = filename
        return stoptrack

    MusicRoom.store_current_track = musicroom_store_current_track

    MusicRoom._previous_track = None
    MusicRoom._current_track = None
    MusicRoom._next_track = None

    MusicRoom._previous_track_text = None
    MusicRoom._current_track_text = None
    MusicRoom._next_track_text = None
    MusicRoom._track_length = None

    def get_track_data(self, name):
        for key, value in music_tracks.items():
            for subkey, subvalue in value.items():
                length = subvalue.get("length")
                if name == subvalue.get("musicroom_path"):
                    return key, subkey, length

    MusicRoom.GetTrackData = get_track_data

    def prevcurnext(self):
        global music_tracks
        if self._current_track == self.get_track(self.channel):
            return
        playlist = self.unlocked_playlist()
        music_playing = self.get_track(self.channel) if renpy.music.is_playing("music") else playlist[0]

        try:
            index = playlist.index(next((i for i in playlist if i in music_playing), playlist[0]))
            previous_index = (index - 1) % len(playlist)
            next_index = (index + 1) % len(playlist)

            previous_track_data = self.GetTrackData(playlist[previous_index])
            current_track_data = self.GetTrackData(playlist[index])
            next_track_data = self.GetTrackData(playlist[next_index])

            self._previous_track_text = f"{previous_track_data[0]} - {previous_track_data[1]}"
            self._current_track_text = f"{current_track_data[0]} - {current_track_data[1]}"
            self._next_track_text = f"{next_track_data[0]} - {next_track_data[1]}"

            self._track_length = current_track_data[2]

            self._previous_track = playlist[previous_index]
            self._current_track = playlist[index]
            self._next_track = playlist[next_index]

        except (ValueError, IndexError, KeyError) as exception:
            #print(exception, "Music Tracks")
            self._previous_track = None
            self._current_track = None
            self._next_track = None

            self._previous_track_text = ""
            self._current_track_text = _("No Track Playing")
            self._next_track_text = ""

            self._track_length = "0.00"

        return (self._previous_track_text, self._current_track_text, self._next_track_text)

    MusicRoom.Previous_Current_Next = prevcurnext

    class GetMusicPlaying(Action):
        def __init__(self, mr):
            self.mr       = mr
            self.filename = self.mr.get_track(self.mr.channel)
            self.previous = self.mr.previous_track
            self.next     = self.mr.next_track

        def __call__(self):
            self.mr.Previous_Current_Next()
            filename = self.mr.get_track(self.mr.channel)

            if self.filename != filename:
                self.filename = self.mr.get_track(self.mr.channel)
                renpy.restart_interaction()

            previous = self.mr.previous_track
            next = self.mr.next_track

            if self.previous != previous:
                self.previous = self.mr.previous_track
                renpy.restart_interaction()

            if self.next != next:
                self.next = self.mr.next_track
                renpy.restart_interaction()
        
    @property
    def previous_track(self):
        return self._previous_track_text
    MusicRoom.previous_track = previous_track
    @property
    def current_track(self):
        return self._current_track_text
    MusicRoom.current_track = current_track
    @property
    def next_track(self):
        return self._next_track_text
    MusicRoom.next_track = next_track
    @property
    def track_length(self):
        return self._track_length
    MusicRoom.track_length = track_length
    
init -1500 python:
    import datetime
    __current_year__ = datetime.datetime.now().year

    import math as _math
    class ColorSingle(ColorMatrix, DictEquality):
        """
        :doc: colormatrix

        A ColorMatrix that can be used with :tpref:`matrixcolor` to colorize
        black and white displayables. It uses the color of each pixel
        in the black and white to interpolate between the black color
        and the white color.

        The alpha channel is not touched.

        This is inteded for use with a black and white image (or one that
        has been desaturated with :func:`SaturationMatrix`), and will yield
        strange results when used with images that are not black and white.

        `black_color`, `white_color`
            The colors used in the interpolation.
        """

        def __init__(self, color):
            self.color = Color(color)

        def __call__(self, other, done):
            nbr, nbg, nbb = self.color.rgb

            if type(other) is not type(self):
                #other = self
                red, green, blue = self.color.rgb
                alpha = self.color.alpha

            else:
                oldred,oldgreen,oldblue = other.color.rgb
                oldalpha = other.color.alpha
                red, green, blue = self.color.rgb
                alpha = self.color.alpha

                r = oldred + (red - oldred) * done
                g = oldgreen + (green - oldgreen) * done
                b = oldblue + (blue - oldblue) * done
                a = oldalpha + (alpha - oldalpha) * done

            red *= alpha
            green *= alpha
            blue *= alpha

            # Return the matrix.
            return Matrix([ red, 0, 0, 0,
                            0, green, 0, 0,
                            0, 0, blue, 0,
                            0, 0, 0, alpha,])

init python:
    bypass_list.extend([
        "custom_keep_music_playing", "aspect_ratio", "mr", "music_tracks", "find_music", 
        "sorted_music_tracks", "generate_track_list", "music_list", "generate_track_list", 
        "add_to_playlist", "seen_track", "add_to_music_tracks", "add_to_playlist", "pygame", 
        "re", "mutagen", "generate_float_list", "MutePlayer", "get_mute", "convert_time", 
        "music_pos", "music_dur", "__CustomMusicRoomPlay", "get_music_len", "AdjustableAudioPositionValue", 
        "musicroom_match", "musicroom_get_track", "musicroom_Play", "musicroom_play", "musicroom_play_from", 
        "musicroom_periodic", "musicroom_forward", "musicroom_rewind", "musicroom_get_position", 
        "musicroom_get_duration", "musicroom_Forward", "musicroom_Rewind", "musicroom_getpause", 
        "musicroom_playing", "musicroom_store_current_track", "MusicRoom.duration", "MusicRoom.position", 
        "MusicRoom.match", "MusicRoom.get_track", "MusicRoom.Play", "MusicRoom.play", "MusicRoom.play_from", 
        "MusicRoom.periodic", "MusicRoom.forward", "MusicRoom.rewind", "MusicRoom.get_position", 
        "MusicRoom.get_duration", "MusicRoom.Forward", "MusicRoom.Rewind", "MusicRoom.get_pause", 
        "MusicRoom.is_playing", "MusicRoom.store_current_track", 
        "datetime", "__current_year__", "_math", "ColorSingle", "music_durtt",
        "music_last_playing", "stoptrack", "time_position", "time_duration",
        "OrderedDict", "OggVorbis", "MP3", "FLAC", "OggOpus", "MutagenFile", "MusicRoom._previous_track",  
        "MusicRoom._current_track",  "MusicRoom._next_track",  "MusicRoom._previous_track_text",  "MusicRoom._current_track_text",  
        "MusicRoom._next_track_text",  "get_track_data",  "prevcurnext",  "previous_track",  "current_track",  "next_track",  
        "MusicRoom.GetTrackData",  "MusicRoom.Previous_Current_Next",  "MusicRoom.previous_track",  "MusicRoom.current_track",  
        "MusicRoom.next_track", "music_postt", "GetMusicPlaying", "MusicRoom._track_length", "track_length", "MusicRoom.track_length",
        ])
    aspect_ratio = (config.screen_width, config.screen_height)

init -5 python:
    class AudioCredits:
        TrackInfo = []
        def __init__(self, title, artist, filename, link_name, link, description, license, lic_link, mood):
            self.title = title
            self.artist = artist
            self.filename = filename
            self.link_name = link_name
            self.link = link
            self.description = description
            self.license = license
            self.license_link = lic_link
            self.mood = mood
            AudioCredits.TrackInfo.append(self)

        def __repr__(self):
            return str(self.filename)

        # This makes the class iterable
        def __iter__(self):
            # This returns an iterator that yields the filename as a single-item list
            return iter([self.filename])

init python:
    import os
    music_tracks = {}

    def find_music():
        data = []
        tracks = []

        for i in renpy.list_files():
            if i.endswith((".mp3", ".ogg", ".flac", ".opus", ".wav")):
                stripname = os.path.dirname(i)+"/"
                tracks.append((i, i.replace(stripname,"")))

        for audio in AudioCredits.TrackInfo:
            correction = audio.filename.replace(stripname,"")
            for track in tracks:
                if track[1] == correction:
                    if track[0] != audio.filename:
                        audio.filename = track[0]
    
            data.append([audio.title, audio.artist, audio.filename, audio.link_name, audio.link, audio.license, audio.license_link, audio.mood])

        return sorted(data)
        #title, artist, filename, link, adddescription

    from collections import OrderedDict
    def sorted_music_tracks(music_dict, mood="All"):
        sorted_music = OrderedDict()

        # Iterate over the artist names in sorted order
        for artist in sorted(music_dict.keys()):
            # Filter tracks by mood if a specific mood is set
            if mood != "All":
                # Filter tracks that match the mood
                filtered_tracks = {title: info for title, info in music_dict[artist].items() if info['mood'] == mood}
            else:
                # If no specific mood is set, include all tracks
                filtered_tracks = music_dict[artist]

            # Sort the filtered or all tracks by title
            sorted_tracks = OrderedDict(sorted(filtered_tracks.items()))
            
            # Only add artists that have matching tracks
            if sorted_tracks:
                sorted_music[artist] = sorted_tracks

        return sorted_music

    def get_playlist(d):
        for i in playlist_data:
            if d == i[2]:
                return getattr(store, i[0])

    def get_rooms(d):
        for i in playlist_data:
            if d == i[2]:
                return i[1]
       
    def generate_track_list(lst):
        for title, artist, path, credit_name, credit_link, license, license_link, mood in lst:
            add_to_music_tracks(music_tracks, artist, title, path, True, credits={'link_name': credit_name, 'link' : credit_link, "license" : license, "license_link" : license_link}, mood=mood)

init -5 python:

    def seen_track(filename):
        if renpy.seen_audio(filename):
            return True
        return False

    def add_to_music_tracks(dictionary, artist, title, path, unlocked=False, full_path=None, length=None, credits={}, custom=False, mood=None):
        global get_music_len, config
        full_path = os.path.join(config.gamedir, path).replace("\\","/")
        track_length = length if length else get_music_len(path)

        credits_link = credits.get("link", '')
        credits_link_name = credits.get("link_name", '')
        credits_license_name = credits.get("license", '')
        credits_license = credits.get("license_link", '')

        if not renpy.loadable(path):
            return

        if not artist in dictionary:
            dictionary[artist] = {}

        if not title in dictionary[artist]:
            dictionary[artist][title] = {}

        locked = dictionary[artist][title].get("unlocked")

        dictionary[artist][title]["path"] = full_path
        dictionary[artist][title]["musicroom_path"] = path
        dictionary[artist][title]["length"] = track_length
        if locked == False or locked == None:
            dictionary[artist][title]["unlocked"] = unlocked
        else:
            dictionary[artist][title]["unlocked"] = locked
        dictionary[artist][title]["credits_link"] = credits_link
        dictionary[artist][title]["credits_license"] = credits_license
        dictionary[artist][title]["credits_link_name"] = credits_link_name
        dictionary[artist][title]["credits_license_name"] = credits_license_name
        dictionary[artist][title]["custom"] = custom
        dictionary[artist][title]["mood"] = mood

    def add_to_playlist(musicroom):
        for artist, data in music_tracks.items():
            for track_title, track_data in data.items():
                path = track_data.get("musicroom_path")
                unlocked = track_data.get("unlocked", False)
                if path and renpy.loadable(path):
                    musicroom.add(path, always_unlocked=unlocked)
                    for playlist, room, current, mood in playlist_data:
                        if mood != "All":
                            if track_data["mood"].lower() == mood.lower():
                                room.add(path, always_unlocked=unlocked)

init python:

    config.keymap[ 'ToggleMusic' ] = [ 'noshift_K_m' ]
    config.underlay.append(renpy.Keymap(ToggleMusic = ShowMenu("musicroom", _transition=dissolve)))

image play_outline_idle = Transform(
    'mod/images/play_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_idle_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image play_outline_hover = Transform(
    'mod/images/play_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_hover_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image play_outline_selected = Transform(
    'mod/images/play_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_selected_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image play_outline_insensitive = Transform(
    'mod/images/play_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_insensitive_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)

image play_solid_idle = Transform(
    'mod/images/play_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_idle_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image play_solid_hover = Transform(
    'mod/images/play_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_hover_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image play_solid_selected = Transform(
    'mod/images/play_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_selected_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image play_solid_insensitive = Transform(
    'mod/images/play_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_insensitive_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)

image play_button_idle = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " play_outline_idle",
    "persistent._use_outline_music_buttons", " play_solid_idle",
)

image play_button_hover = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " play_outline_hover",
    "persistent._use_outline_music_buttons", " play_solid_hover",
)

image play_button_selected = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " play_outline_selected",
    "persistent._use_outline_music_buttons", " play_solid_selected",
)

image play_button_insensitive = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " play_outline_insensitive",
    "persistent._use_outline_music_buttons", " play_solid_insensitive",
)

image stop_outline_idle = Transform(
    'mod/images/stop_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_idle_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image stop_outline_hover = Transform(
    'mod/images/stop_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_hover_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image stop_outline_selected = Transform(
    'mod/images/stop_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_selected_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image stop_outline_insensitive = Transform(
    'mod/images/stop_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_insensitive_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)

image stop_solid_idle = Transform(
    'mod/images/stop_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_idle_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image stop_solid_hover = Transform(
    'mod/images/stop_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_hover_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image stop_solid_selected = Transform(
    'mod/images/stop_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_selected_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image stop_solid_insensitive = Transform(
    'mod/images/stop_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_insensitive_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)

image stop_button_idle = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " stop_outline_idle",
    "persistent._use_outline_music_buttons", " stop_solid_idle",
)

image stop_button_hover = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " stop_outline_hover",
    "persistent._use_outline_music_buttons", " stop_solid_hover",
)

image stop_button_selected = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " stop_outline_selected",
    "persistent._use_outline_music_buttons", " stop_solid_selected",
)

image stop_button_insensitive = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " stop_outline_insensitive",
    "persistent._use_outline_music_buttons", " stop_solid_insensitive",
)

image back_outline_idle = Transform(
    'mod/images/back_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_idle_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image back_outline_hover = Transform(
    'mod/images/back_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_hover_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image back_outline_selected = Transform(
    'mod/images/back_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_selected_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image back_outline_insensitive = Transform(
    'mod/images/back_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_insensitive_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)

image back_solid_idle = Transform(
    'mod/images/back_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_idle_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image back_solid_hover = Transform(
    'mod/images/back_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_hover_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image back_solid_selected = Transform(
    'mod/images/back_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_selected_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image back_solid_insensitive = Transform(
    'mod/images/back_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_insensitive_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)

image back_button_idle = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " back_outline_idle",
    "persistent._use_outline_music_buttons", " back_solid_idle",
)

image back_button_hover = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " back_outline_hover",
    "persistent._use_outline_music_buttons", " back_solid_hover",
)

image back_button_selected = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " back_outline_selected",
    "persistent._use_outline_music_buttons", " back_solid_selected",
)

image back_button_insensitive = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " back_outline_insensitive",
    "persistent._use_outline_music_buttons", " back_solid_insensitive",
)


image next_outline_idle = Transform(
    'mod/images/next_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_idle_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image next_outline_hover = Transform(
    'mod/images/next_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_hover_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image next_outline_selected = Transform(
    'mod/images/next_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_selected_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image next_outline_insensitive = Transform(
    'mod/images/next_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_insensitive_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)

image next_solid_idle = Transform(
    'mod/images/next_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_idle_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image next_solid_hover = Transform(
    'mod/images/next_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_hover_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image next_solid_selected = Transform(
    'mod/images/next_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_selected_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image next_solid_insensitive = Transform(
    'mod/images/next_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_insensitive_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)

image next_button_idle = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " next_outline_idle",
    "persistent._use_outline_music_buttons", " next_solid_idle",
)

image next_button_hover = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " next_outline_hover",
    "persistent._use_outline_music_buttons", " next_solid_hover",
)

image next_button_selected = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " next_outline_selected",
    "persistent._use_outline_music_buttons", " next_solid_selected",
)

image next_button_insensitive = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " next_outline_insensitive",
    "persistent._use_outline_music_buttons", " next_solid_insensitive",
)

image fast_forward_outline_idle = Transform(
    'mod/images/fast_forward_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_idle_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image fast_forward_outline_hover = Transform(
    'mod/images/fast_forward_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_hover_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image fast_forward_outline_selected = Transform(
    'mod/images/fast_forward_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_selected_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image fast_forward_outline_insensitive = Transform(
    'mod/images/fast_forward_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_insensitive_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)

image fast_forward_solid_idle = Transform(
    'mod/images/fast_forward_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_idle_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image fast_forward_solid_hover = Transform(
    'mod/images/fast_forward_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_hover_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image fast_forward_solid_selected = Transform(
    'mod/images/fast_forward_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_selected_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image fast_forward_solid_insensitive = Transform(
    'mod/images/fast_forward_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_insensitive_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)

image fast_forward_button_idle = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " fast_forward_outline_idle",
    "persistent._use_outline_music_buttons", " fast_forward_solid_idle",
)

image fast_forward_button_hover = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " fast_forward_outline_hover",
    "persistent._use_outline_music_buttons", " fast_forward_solid_hover",
)

image fast_forward_button_selected = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " fast_forward_outline_selected",
    "persistent._use_outline_music_buttons", " fast_forward_solid_selected",
)

image fast_forward_button_insensitive = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " fast_forward_outline_insensitive",
    "persistent._use_outline_music_buttons", " fast_forward_solid_insensitive",
)

image pause_outline_idle = Transform(
    'mod/images/pause_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_idle_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image pause_outline_hover = Transform(
    'mod/images/pause_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_hover_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image pause_outline_selected = Transform(
    'mod/images/pause_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_selected_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image pause_outline_insensitive = Transform(
    'mod/images/pause_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_insensitive_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)

image pause_solid_idle = Transform(
    'mod/images/pause_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_idle_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image pause_solid_hover = Transform(
    'mod/images/pause_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_hover_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image pause_solid_selected = Transform(
    'mod/images/pause_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_selected_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image pause_solid_insensitive = Transform(
    'mod/images/pause_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_insensitive_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)

image pause_button_idle = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " pause_outline_idle",
    "persistent._use_outline_music_buttons", " pause_solid_idle",
)

image pause_button_hover = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " pause_outline_hover",
    "persistent._use_outline_music_buttons", " pause_solid_hover",
)

image pause_button_selected = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " pause_outline_selected",
    "persistent._use_outline_music_buttons", " pause_solid_selected",
)

image pause_button_insensitive = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " pause_outline_insensitive",
    "persistent._use_outline_music_buttons", " pause_solid_insensitive",
)


image repeat_once_outline_idle = Transform(
    'mod/images/repeat_once_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_idle_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image repeat_once_outline_hover = Transform(
    'mod/images/repeat_once_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_hover_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image repeat_once_outline_selected = Transform(
    'mod/images/repeat_once_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_selected_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image repeat_once_outline_insensitive = Transform(
    'mod/images/repeat_once_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_insensitive_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)

image repeat_once_solid_idle = Transform(
    'mod/images/repeat_once_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_idle_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image repeat_once_solid_hover = Transform(
    'mod/images/repeat_once_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_hover_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image repeat_once_solid_selected = Transform(
    'mod/images/repeat_once_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_selected_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image repeat_once_solid_insensitive = Transform(
    'mod/images/repeat_once_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_insensitive_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)

image repeat_once_button_idle = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " repeat_once_outline_idle",
    "persistent._use_outline_music_buttons", " repeat_once_solid_idle",
)

image repeat_once_button_hover = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " repeat_once_outline_hover",
    "persistent._use_outline_music_buttons", " repeat_once_solid_hover",
)

image repeat_once_button_selected = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " repeat_once_outline_selected",
    "persistent._use_outline_music_buttons", " repeat_once_solid_selected",
)

image repeat_once_button_insensitive = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " repeat_once_outline_insensitive",
    "persistent._use_outline_music_buttons", " repeat_once_solid_insensitive",
)

image repeat_outline_idle = Transform(
    'mod/images/repeat_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_idle_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image repeat_outline_hover = Transform(
    'mod/images/repeat_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_hover_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image repeat_outline_selected = Transform(
    'mod/images/repeat_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_selected_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image repeat_outline_insensitive = Transform(
    'mod/images/repeat_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_insensitive_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)

image repeat_solid_idle = Transform(
    'mod/images/repeat_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_idle_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image repeat_solid_hover = Transform(
    'mod/images/repeat_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_hover_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image repeat_solid_selected = Transform(
    'mod/images/repeat_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_selected_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image repeat_solid_insensitive = Transform(
    'mod/images/repeat_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_insensitive_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)

image repeat_button_idle = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " repeat_outline_idle",
    "persistent._use_outline_music_buttons", " repeat_solid_idle",
)

image repeat_button_hover = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " repeat_outline_hover",
    "persistent._use_outline_music_buttons", " repeat_solid_hover",
)

image repeat_button_selected = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " repeat_outline_selected",
    "persistent._use_outline_music_buttons", " repeat_solid_selected",
)

image repeat_button_insensitive = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " repeat_outline_insensitive",
    "persistent._use_outline_music_buttons", " repeat_solid_insensitive",
)

image rewind_outline_idle = Transform(
    'mod/images/rewind_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_idle_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image rewind_outline_hover = Transform(
    'mod/images/rewind_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_hover_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image rewind_outline_selected = Transform(
    'mod/images/rewind_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_selected_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image rewind_outline_insensitive = Transform(
    'mod/images/rewind_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_insensitive_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)

image rewind_solid_idle = Transform(
    'mod/images/rewind_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_idle_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image rewind_solid_hover = Transform(
    'mod/images/rewind_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_hover_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image rewind_solid_selected = Transform(
    'mod/images/rewind_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_selected_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image rewind_solid_insensitive = Transform(
    'mod/images/rewind_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_insensitive_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)

image rewind_button_idle = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " rewind_outline_idle",
    "persistent._use_outline_music_buttons", " rewind_solid_idle",
)

image rewind_button_hover = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " rewind_outline_hover",
    "persistent._use_outline_music_buttons", " rewind_solid_hover",
)

image rewind_button_selected = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " rewind_outline_selected",
    "persistent._use_outline_music_buttons", " rewind_solid_selected",
)

image rewind_button_insensitive = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " rewind_outline_insensitive",
    "persistent._use_outline_music_buttons", " rewind_solid_insensitive",
)


image shuffle_outline_idle = Transform(
    'mod/images/shuffle_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_idle_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image shuffle_outline_hover = Transform(
    'mod/images/shuffle_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_hover_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image shuffle_outline_selected = Transform(
    'mod/images/shuffle_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_selected_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image shuffle_outline_insensitive = Transform(
    'mod/images/shuffle_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_insensitive_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)

image shuffle_solid_idle = Transform(
    'mod/images/shuffle_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_idle_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image shuffle_solid_hover = Transform(
    'mod/images/shuffle_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_hover_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image shuffle_solid_selected = Transform(
    'mod/images/shuffle_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_selected_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image shuffle_solid_insensitive = Transform(
    'mod/images/shuffle_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_insensitive_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)

image shuffle_button_idle = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " shuffle_outline_idle",
    "persistent._use_outline_music_buttons", " shuffle_solid_idle",
)

image shuffle_button_hover = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " shuffle_outline_hover",
    "persistent._use_outline_music_buttons", " shuffle_solid_hover",
)

image shuffle_button_selected = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " shuffle_outline_selected",
    "persistent._use_outline_music_buttons", " shuffle_solid_selected",
)

image shuffle_button_insensitive = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " shuffle_outline_insensitive",
    "persistent._use_outline_music_buttons", " shuffle_solid_insensitive",
)

image shuffle_off_outline_idle = Transform(
    'mod/images/shuffle_off_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_idle_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image shuffle_off_outline_hover = Transform(
    'mod/images/shuffle_off_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_hover_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image shuffle_off_outline_selected = Transform(
    'mod/images/shuffle_off_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_selected_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image shuffle_off_outline_insensitive = Transform(
    'mod/images/shuffle_off_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_insensitive_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)

image shuffle_off_solid_idle = Transform(
    'mod/images/shuffle_off_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_idle_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image shuffle_off_solid_hover = Transform(
    'mod/images/shuffle_off_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_hover_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image shuffle_off_solid_selected = Transform(
    'mod/images/shuffle_off_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_selected_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)
image shuffle_off_solid_insensitive = Transform(
    'mod/images/shuffle_off_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_insensitive_color),
    xysize=(gui.button_size,gui.button_size),
    align=(0.5,0.5)
)

image shuffle_off_button_idle = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " shuffle_off_outline_idle",
    "persistent._use_outline_music_buttons", " shuffle_off_solid_idle",
)

image shuffle_off_button_hover = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " shuffle_off_outline_hover",
    "persistent._use_outline_music_buttons", " shuffle_off_solid_hover",
)

image shuffle_off_button_selected = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " shuffle_off_outline_selected",
    "persistent._use_outline_music_buttons", " shuffle_off_solid_selected",
)

image shuffle_off_button_insensitive = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " shuffle_off_outline_insensitive",
    "persistent._use_outline_music_buttons", " shuffle_off_solid_insensitive",
)

image silent_outline_idle = Transform(
    'mod/images/silent_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_idle_color),
    xysize=gui.button_size_mute,
    align=(0.5,0.5)
)
image silent_outline_hover = Transform(
    'mod/images/silent_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_hover_color),
    xysize=gui.button_size_mute,
    align=(0.5,0.5)
)
image silent_outline_selected = Transform(
    'mod/images/silent_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_selected_color),
    xysize=gui.button_size_mute,
    align=(0.5,0.5)
)
image silent_outline_insensitive = Transform(
    'mod/images/silent_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_insensitive_color),
    xysize=gui.button_size_mute,
    align=(0.5,0.5)
)

image silent_solid_idle = Transform(
    'mod/images/silent_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_idle_color),
    xysize=gui.button_size_mute,
    align=(0.5,0.5)
)
image silent_solid_hover = Transform(
    'mod/images/silent_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_hover_color),
    xysize=gui.button_size_mute,
    align=(0.5,0.5)
)
image silent_solid_selected = Transform(
    'mod/images/silent_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_selected_color),
    xysize=gui.button_size_mute,
    align=(0.5,0.5)
)
image silent_solid_insensitive = Transform(
    'mod/images/silent_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_insensitive_color),
    xysize=gui.button_size_mute,
    align=(0.5,0.5)
)

image silent_button_idle = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " silent_outline_idle",
    "persistent._use_outline_music_buttons", " silent_solid_idle",
)

image silent_button_hover = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " silent_outline_hover",
    "persistent._use_outline_music_buttons", " silent_solid_hover",
)

image silent_button_selected = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " silent_outline_selected",
    "persistent._use_outline_music_buttons", " silent_solid_selected",
)

image silent_button_insensitive = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " silent_outline_insensitive",
    "persistent._use_outline_music_buttons", " silent_solid_insensitive",
)


image volume_outline_idle = Transform(
    'mod/images/volume_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_idle_color),
    xysize=gui.button_size_mute,
    align=(0.5,0.5)
)
image volume_outline_hover = Transform(
    'mod/images/volume_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_hover_color),
    xysize=gui.button_size_mute,
    align=(0.5,0.5)
)
image volume_outline_selected = Transform(
    'mod/images/volume_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_selected_color),
    xysize=gui.button_size_mute,
    align=(0.5,0.5)
)
image volume_outline_insensitive = Transform(
    'mod/images/volume_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_insensitive_color),
    xysize=gui.button_size_mute,
    align=(0.5,0.5)
)

image volume_solid_idle = Transform(
    'mod/images/volume_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_idle_color),
    xysize=gui.button_size_mute,
    align=(0.5,0.5)
)
image volume_solid_hover = Transform(
    'mod/images/volume_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_hover_color),
    xysize=gui.button_size_mute,
    align=(0.5,0.5)
)
image volume_solid_selected = Transform(
    'mod/images/volume_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_selected_color),
    xysize=gui.button_size_mute,
    align=(0.5,0.5)
)
image volume_solid_insensitive = Transform(
    'mod/images/volume_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_insensitive_color),
    xysize=gui.button_size_mute,
    align=(0.5,0.5)
)

image volume_button_idle = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " volume_outline_idle",
    "persistent._use_outline_music_buttons", " volume_solid_idle",
)

image volume_button_hover = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " volume_outline_hover",
    "persistent._use_outline_music_buttons", " volume_solid_hover",
)

image volume_button_selected = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " volume_outline_selected",
    "persistent._use_outline_music_buttons", " volume_solid_selected",
)

image volume_button_insensitive = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " volume_outline_insensitive",
    "persistent._use_outline_music_buttons", " volume_solid_insensitive",
)

image volume_half_outline_idle = Transform(
    'mod/images/volume_half_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_idle_color),
    xysize=gui.button_size_mute,
    align=(0.5,0.5)
)
image volume_half_outline_hover = Transform(
    'mod/images/volume_half_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_hover_color),
    xysize=gui.button_size_mute,
    align=(0.5,0.5)
)
image volume_half_outline_selected = Transform(
    'mod/images/volume_half_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_selected_color),
    xysize=gui.button_size_mute,
    align=(0.5,0.5)
)
image volume_half_outline_insensitive = Transform(
    'mod/images/volume_half_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_insensitive_color),
    xysize=gui.button_size_mute,
    align=(0.5,0.5)
)

image volume_half_solid_idle = Transform(
    'mod/images/volume_half_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_idle_color),
    xysize=gui.button_size_mute,
    align=(0.5,0.5)
)
image volume_half_solid_hover = Transform(
    'mod/images/volume_half_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_hover_color),
    xysize=gui.button_size_mute,
    align=(0.5,0.5)
)
image volume_half_solid_selected = Transform(
    'mod/images/volume_half_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_selected_color),
    xysize=gui.button_size_mute,
    align=(0.5,0.5)
)
image volume_half_solid_insensitive = Transform(
    'mod/images/volume_half_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_insensitive_color),
    xysize=gui.button_size_mute,
    align=(0.5,0.5)
)

image volume_half_button_idle = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " volume_half_outline_idle",
    "persistent._use_outline_music_buttons", " volume_half_solid_idle",
)

image volume_half_button_hover = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " volume_half_outline_hover",
    "persistent._use_outline_music_buttons", " volume_half_solid_hover",
)

image volume_half_button_selected = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " volume_half_outline_selected",
    "persistent._use_outline_music_buttons", " volume_half_solid_selected",
)

image volume_half_button_insensitive = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " volume_half_outline_insensitive",
    "persistent._use_outline_music_buttons", " volume_half_solid_insensitive",
)

image mute_player_idle = ConditionSwitch(
    'get_mute(channel="music") == 0.0', "silent_button_idle",
    'get_mute(channel="music") > 0.0 and get_mute(channel="music") < 0.6', "volume_half_button_idle",
    'get_mute(channel="music") == 0.6', "volume_half_button_idle",
    'get_mute(channel="music") > 0.6 and get_mute(channel="music") <= 1.0', "volume_button_idle"
)

image mute_player_hover = ConditionSwitch(
    'get_mute(channel="music") == 0.0', "silent_button_hover",
    'get_mute(channel="music") > 0.0 and get_mute(channel="music") < 0.6', "volume_half_button_hover",
    'get_mute(channel="music") == 0.6', "volume_half_button_hover",
    'get_mute(channel="music") > 0.6 and get_mute(channel="music") <= 1.0', "volume_button_hover"
)

image mute_player_selected = ConditionSwitch(
    'get_mute(channel="music") == 0.0', "silent_button_selected",
    'get_mute(channel="music") > 0.0 and get_mute(channel="music") < 0.6', "volume_half_button_selected",
    'get_mute(channel="music") == 0.6', "volume_half_button_selected",
    'get_mute(channel="music") > 0.6 and get_mute(channel="music") <= 1.0', "volume_button_selected"
)

image mute_player_insensitive = ConditionSwitch(
    'get_mute(channel="music") == 0.0', "silent_button_insensitive",
    'get_mute(channel="music") > 0.0 and get_mute(channel="music") < 0.6', "volume_half_button_insensitive",
    'get_mute(channel="music") == 0.6', "volume_half_button_insensitive",
    'get_mute(channel="music") > 0.6 and get_mute(channel="music") <= 1.0', "volume_button_insensitive"
)

image readablePos = DynamicDisplayable(renpy.curry(music_pos)(
                    "music_room_time",gui.bar_size, 0.5))
image readableDur = DynamicDisplayable(renpy.curry(music_dur)(
                    "music_room_time",gui.bar_size, 0.5))
image readablePosTT = DynamicDisplayable(renpy.curry(music_postt)(
                    "music_room_time",gui.text_size -10))

image readableDurTT = DynamicDisplayable(renpy.curry(music_durtt)(
                    "music_room_time",gui.text_size -10))


image locked_outline_idle = Transform(
    'mod/images/locked_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_idle_color),
    xysize=(gui.button_size, gui.button_size),
    align=(0.5,0.5)
)
image locked_outline_hover = Transform(
    'mod/images/locked_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_hover_color),
    xysize=(gui.button_size, gui.button_size),
    align=(0.5,0.5)
)
image locked_outline_selected = Transform(
    'mod/images/locked_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_selected_color),
    xysize=(gui.button_size, gui.button_size),
    align=(0.5,0.5)
)
image locked_outline_insensitive = Transform(
    'mod/images/locked_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_insensitive_color),
    xysize=(gui.button_size, gui.button_size),
    align=(0.5,0.5)
)

image locked_solid_idle = Transform(
    'mod/images/locked_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_idle_color),
    xysize=(gui.button_size, gui.button_size),
    align=(0.5,0.5)
)
image locked_solid_hover = Transform(
    'mod/images/locked_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_hover_color),
    xysize=(gui.button_size, gui.button_size),
    align=(0.5,0.5)
)
image locked_solid_selected = Transform(
    'mod/images/locked_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_selected_color),
    xysize=(gui.button_size, gui.button_size),
    align=(0.5,0.5)
)
image locked_solid_insensitive = Transform(
    'mod/images/locked_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_insensitive_color),
    xysize=(gui.button_size, gui.button_size),
    align=(0.5,0.5)
)

image locked_button_idle = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " locked_outline_idle",
    "persistent._use_outline_music_buttons", " locked_solid_idle",
)

image locked_button_hover = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " locked_outline_hover",
    "persistent._use_outline_music_buttons", " locked_solid_hover",
)

image locked_button_selected = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " locked_outline_selected",
    "persistent._use_outline_music_buttons", " locked_solid_selected",
)

image locked_button_insensitive = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " locked_outline_insensitive",
    "persistent._use_outline_music_buttons", " locked_solid_insensitive",
)

image unlocked_outline_idle = Transform(
    'mod/images/unlocked_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_idle_color),
    xysize=(gui.button_size, gui.button_size),
    align=(0.5,0.5)
)
image unlocked_outline_hover = Transform(
    'mod/images/unlocked_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_hover_color),
    xysize=(gui.button_size, gui.button_size),
    align=(0.5,0.5)
)
image unlocked_outline_selected = Transform(
    'mod/images/unlocked_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_selected_color),
    xysize=(gui.button_size, gui.button_size),
    align=(0.5,0.5)
)
image unlocked_outline_insensitive = Transform(
    'mod/images/unlocked_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_insensitive_color),
    xysize=(gui.button_size, gui.button_size),
    align=(0.5,0.5)
)

image unlocked_solid_idle = Transform(
    'mod/images/unlocked_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_idle_color),
    xysize=(gui.button_size, gui.button_size),
    align=(0.5,0.5)
)
image unlocked_solid_hover = Transform(
    'mod/images/unlocked_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_hover_color),
    xysize=(gui.button_size, gui.button_size),
    align=(0.5,0.5)
)
image unlocked_solid_selected = Transform(
    'mod/images/unlocked_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_selected_color),
    xysize=(gui.button_size, gui.button_size),
    align=(0.5,0.5)
)
image unlocked_solid_insensitive = Transform(
    'mod/images/unlocked_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_insensitive_color),
    xysize=(gui.button_size, gui.button_size),
    align=(0.5,0.5)
)

image unlocked_button_idle = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " unlocked_outline_idle",
    "persistent._use_outline_music_buttons", " unlocked_solid_idle",
)

image unlocked_button_hover = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " unlocked_outline_hover",
    "persistent._use_outline_music_buttons", " unlocked_solid_hover",
)

image unlocked_button_selected = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " unlocked_outline_selected",
    "persistent._use_outline_music_buttons", " unlocked_solid_selected",
)

image unlocked_button_insensitive = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " unlocked_outline_insensitive",
    "persistent._use_outline_music_buttons", " unlocked_solid_insensitive",
)


image settings_outline_idle = Transform(
    'mod/images/settings_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_idle_color),
    xysize=(gui.button_size, gui.button_size),
    align=(0.5,0.5)
)
image settings_outline_hover = Transform(
    'mod/images/settings_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_hover_color),
    xysize=(gui.button_size, gui.button_size),
    align=(0.5,0.5)
)
image settings_outline_selected = Transform(
    'mod/images/settings_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_selected_color),
    xysize=(gui.button_size, gui.button_size),
    align=(0.5,0.5)
)
image settings_outline_insensitive = Transform(
    'mod/images/settings_outline.png',
    matrixcolor=ColorSingle(gui.music_icon_insensitive_color),
    xysize=(gui.button_size, gui.button_size),
    align=(0.5,0.5)
)

image settings_solid_idle = Transform(
    'mod/images/settings_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_idle_color),
    xysize=(gui.button_size, gui.button_size),
    align=(0.5,0.5)
)
image settings_solid_hover = Transform(
    'mod/images/settings_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_hover_color),
    xysize=(gui.button_size, gui.button_size),
    align=(0.5,0.5)
)
image settings_solid_selected = Transform(
    'mod/images/settings_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_selected_color),
    xysize=(gui.button_size, gui.button_size),
    align=(0.5,0.5)
)
image settings_solid_insensitive = Transform(
    'mod/images/settings_solid.png',
    matrixcolor=ColorSingle(gui.music_icon_insensitive_color),
    xysize=(gui.button_size, gui.button_size),
    align=(0.5,0.5)
)

image settings_button_idle = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " settings_outline_idle",
    "persistent._use_outline_music_buttons", " settings_solid_idle",
)

image settings_button_hover = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " settings_outline_hover",
    "persistent._use_outline_music_buttons", " settings_solid_hover",
)

image settings_button_selected = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " settings_outline_selected",
    "persistent._use_outline_music_buttons", " settings_solid_selected",
)

image settings_button_insensitive = ConditionSwitch(
    "not persistent._use_outline_music_buttons", " settings_outline_insensitive",
    "persistent._use_outline_music_buttons", " settings_solid_insensitive",
)

define gui.frame_alpha = 0.5
define gui.frame_color_border = gui.accent_color
define gui.frame_color_background = "#000"
define gui.bar_left_color = "#FB4301"
define gui.bar_right_color = "#000"
define gui.bar_bottom_color = gui.bar_right_color
define gui.bar_top_color = gui.bar_left_color

define gui.game_menu_navigation_frame_xsize = 840

define gui.musicroom_frame_background = Transform(
    Frame(
        "gui/frame.png",
        gui.frame_borders, tile=gui.frame_tile),
    matrixcolor=ColorizeMatrix(gui.frame_color_background, gui.frame_color_border),
    alpha=gui.frame_alpha)
define gui.musicroom_frame_padding = gui.frame_borders.padding
define gui.musicroom_frame_xsize = config.screen_width - 840 - (gui.bar_size*3)


define gui.music_icon_idle_color = "#FB4301"
define gui.music_icon_hover_color = "#000"
define gui.music_icon_selected_color = gui.selected_color
define gui.music_icon_insensitive_color = gui.insensitive_color
define gui.button_size = 54
define gui.button_size_mute = (81, 54)

define gui.musicroom_text_color = gui.text_color
define gui.musicroom_text_font = gui.text_font
define gui.musicroom_text_outlines = [(2, "#0009", 1, 1)]

define gui.musicroom_time_text_font = gui.text_font
define gui.musicroom_time_size = gui.text_size
define gui.musicroom_time_text_outlines = [(2, "#0009", 1, 1)]

define gui.musicroom_button_text_font = gui.text_font
define gui.musicroom_button_text_size = gui.text_size-10
define gui.musicroom_button_text_outlines = [(2, "#0009", 1, 1)]
define gui.musicroom_button_text_idle_color = "#FB4301"
define gui.musicroom_button_text_hover_color = "#000"
define gui.musicroom_button_text_selected_color = gui.selected_color
define gui.musicroom_button_text_insensitive_color = gui.insensitive_color


define gui.musicroom_bar_left_idle_color = gui.bar_left_color
define gui.musicroom_bar_left_hover_color = gui.bar_right_color

define gui.musicroom_bar_right_idle_color = gui.bar_right_color
define gui.musicroom_bar_right_hover_color = gui.bar_left_color

#define gui.musicroom_button_text_idle_outlines = [(2, "#0009", 1, 1)]
#define gui.musicroom_button_text_hover_outlines = [(2, "#0009", 1, 1)]
#define gui.musicroom_button_text_selected_outlines = [(2, "#0009", 1, 1)]
#define gui.musicroom_button_text_insensitive_outlines = [(2, "#0009", 1, 1)]