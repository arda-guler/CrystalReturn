import os
import random

def get_os_type():
    return os.name

def clear_cmd_terminal(os_name):
    if os_name == "nt":
        os.system("cls")
    else:
        os.system("clear")

os_name = get_os_type()
from pygame import mixer
clear_cmd_terminal(os_name) # __|__

bgms_lunar = {}
bgms_underworld = {}

def init_sound():
    global bgms_lunar, bgms_underworld
    mixer.init()

    try:
        for bgm in os.listdir("data/bgm/lunar"):
            newmsc = mixer.Sound("data/bgm/lunar/" + bgm)
            bgms_lunar[bgm[:-4]] = newmsc

        for bgm in os.listdir("data/bgm/underworld"):
            newmsc = mixer.Sound("data/bgm/underworld/" + bgm)
            bgms_underworld[bgm[:-4]] = newmsc

    except:
        pass

def play_sfx(track, loops=0, channel=1, volume=1):
    chn = mixer.Channel(channel)
    track_full = "data/sounds/" + str(track) + ".ogg"
    snd = mixer.Sound(track_full)
    chn.set_volume(volume)
    chn.play(snd, loops)

def get_channel_busy(channel):
    chn = mixer.Channel(channel)
    return chn.get_busy()

def is_music_playing():
    return get_channel_busy(7)

def set_channel_volume(channel, volume):
    channel = mixer.Channel(channel)
    channel.set_volume(volume)

def stop_channel(channel):
    channel = mixer.Channel(channel)
    channel.stop()

def fade_out_channel(channel_num):
    channel = mixer.Channel(channel_num)
    channel.fadeout(2000)

def fade_out_bgm(fade_time = 2000):
    chn = mixer.Channel(7)
    chn.fadeout(fade_time)

def play_bgm(track, world="lunar", channel=7):
    global bgms_lunar, bgms_underworld
    chn = mixer.Channel(7)

    if world == "lunar":
        msc = bgms_lunar[track]
    else:
        msc = bgms_underworld[track]
        
    chn.set_volume(1)
    chn.play(msc)

def play_random_bgm(world="lunar", channel=7):
    global bgms_lunar, bgms_underworld
    
    if world == "lunar" and not bgms_lunar:
        return
    elif world == "underworld" and not bgms_underworld:
        return
    
    chn = mixer.Channel(7)
    
    if get_channel_busy(7):
        chn.fadeout(2000)
        
    if world == "lunar":
        msc = random.choice(list(bgms_lunar.values()))
    else:
        msc = random.choice(list(bgms_underworld.values()))
        
    chn.set_volume(1)
    chn.play(msc)
