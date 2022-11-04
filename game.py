import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
import os
import keyboard
import glfw
import time
import random
import math

from luna import *
from camera import *
from graphics import *
from mirage import *
from obstacles import *
from powerups import *
from sound import *
from terrain import *
from vector3 import *
from poems import poem_list

def get_os_type():
    return os.name

def clear_cmd_terminal(os_name):
    if os_name == "nt":
        os.system("cls")
    else:
        os.system("clear")

vp_size_changed = False
def resize_cb(window, w, h):
    global vp_size_changed
    vp_size_changed = True

def flush_input():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys, termios    #for linux/unix
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

def main():
    global vp_size_changed

    # INITIALIZE ESSENTIALS
    print("Initializing GLFW...")
    glfw.init()

    print("Initializing sound...")
    init_sound()

    print("Setting up graphics...")
    window_x = 1200
    window_y = 800
    mwin = glfw.create_window(window_x, window_y, "Crystal Return", None, None)
    glfw.set_window_pos(mwin, 50, 50)
    glfw.make_context_current(mwin)
    glfw.set_window_size_callback(mwin, resize_cb)

    gluPerspective(50, window_x/window_y, 0.005, 10000)
    glEnable(GL_CULL_FACE)
    glEnable(GL_POINT_SMOOTH)
    glClearColor(0.1, 0.1, 0.25, 1)
    glPointSize(3)

    os_name = str(get_os_type())

    dt = 0.001
    game_tick = 0

    print("Loading models...")
    # LOAD MODELS (so we do not load them each time an object is generated)
    model_rect_prism = pywavefront.Wavefront("data/models/cube.obj", collect_faces=True)
    
    model_crystals = []
    for f in os.listdir("data/models/crystals"):
        if f.endswith(".obj"):
            model_crystals.append(pywavefront.Wavefront("data/models/crystals/" + f, collect_faces=True))
            
    model_powerup_speed = pywavefront.Wavefront("data/models/powerup.obj", collect_faces=True)
    model_powerup_invul = pywavefront.Wavefront("data/models/shield.obj", collect_faces=True)

    print("Setting up the game scene...")
    # CREATE INITIAL GAME OBJECTS
    main_cam = camera("main_cam", vec3(0,0,0), [[1,0,0],[0,1,0],[0,0,1]], True)
    main_cam.move(vec3(0,-3,-13))

    floor = terrain()

    player = mirage("mirageAlpha", 100)
    luna = Luna(250)

    score = 0
    poem_index = random.randint(0, len(poem_list)-1)

    obstacles = []
    obstacle_num = 50
    # INIT SOME OBSTACLES
    while len(obstacles) < obstacle_num:
        new_model = random.choice(model_crystals)
        new_size = vec3(random.uniform(1, 5), random.uniform(0.5, 3), random.uniform(1, 5))
        new_pos = vec3(random.uniform(-250, 250), 0, -500 + random.uniform(-100, 300))
        new_rot = vec3(0, random.randint(0, 360), 0)
        new_obstacle = rectangular_prism(new_pos, new_rot, new_size, new_model)
        obstacles.append(new_obstacle)

    powerups = []
    powerups_max_num = 3

    wing_touch_volume = 0
    engine_volume = player.speed / (player.boost_speed * 4)
    play_sfx("engine", -1, 6, engine_volume)
    play_random_bgm()

    print("Starting...")
    while not glfw.window_should_close(mwin):
        glfw.poll_events()

        if vp_size_changed:
            vp_size_changed = False
            w, h = glfw.get_framebuffer_size(mwin)
            glViewport(0, 0, w, h)

        # CONTROLS
        bank_cmd = 0

        if keyboard.is_pressed("A"):
            bank_cmd = -1
        if keyboard.is_pressed("D"):
            bank_cmd = 1

        cycle_start = time.perf_counter()

        # OBSTACLE GENERATION
        while len(obstacles) < obstacle_num:
            new_model = random.choice(model_crystals)
            new_size = vec3(random.uniform(1, 5), random.uniform(0.5, 3), random.uniform(1, 5))
            new_pos = vec3(random.uniform(-250, 250), 0, -500 + random.uniform(-100, 100))
            new_rot = vec3(0, random.randint(0, 360), 0)
            new_obstacle = rectangular_prism(new_pos, new_rot, new_size, new_model)
            obstacles.append(new_obstacle)

        # POWERUP GENERATION
        if len(powerups) < powerups_max_num and random.randint(0, 1000) > 998:

            if luna.height > 0:
                chance_boost = max(min(1 - (luna.height/300), 1), 0)
            else:
                chance_boost = 1
                
            powerup_roll = random.uniform(0, 1)
            
            if powerup_roll > chance_boost:
                powerup_type = random.choice(["invulnerability"])
            else:
                powerup_type = "speed"
            
            if powerup_type == "speed":
                new_size = vec3(5, 5, 5)
                new_pos = vec3(random.uniform(-250, 250), new_size.y/2, -500 + random.uniform(-100, 100))
                new_powerup = speed_boost(new_pos, new_size, model_powerup_speed)

            elif powerup_type == "invulnerability":
                new_size = vec3(3, 3, 3)
                new_pos = vec3(random.uniform(-250, 250), new_size.y/2, -500 + random.uniform(-100, 100))
                new_powerup = invulnerability(new_pos, new_size, model_powerup_invul)
                
            powerups.append(new_powerup)

        # SCENE UPDATE
        player.update_speed(dt)
        player.update_bank(bank_cmd, dt)
        luna.update_height(player.speed, dt)

        # OBSTACLE UPDATE AND CLEANUP
        crash = False
        for o in obstacles:
            o.update_pos(player, dt)

            if o.pos.z > 10:
                obstacles.remove(o)
                del o

            else:
                if o.check_collision():
                    if player.shields_remaining <= 0:
                        crash = True
                        stop_channel(5)
                        stop_channel(6)
                        stop_channel(7)
                        play_sfx("crash", 0, 1, 1)
                        print("CRASH!")
                        time.sleep(5)
                        quit()

                    else:
                        play_sfx("shield_activate")
                        player.shields_remaining -= 1
                        obstacles.remove(o)
                        del o

        # POWERUP UPDATE AND CLEANUP
        for p in powerups:
            p.update_pos(player, dt)

            if p.pos.z > 10:
                powerups.remove(p)
                del p
                
            else:
                if p.check_collision():
                    if p.powerup_type == "speed_boost":
                        play_sfx("speed_boost", 0, 1, 0.4)
                        player.boost_remaining = 25
                        powerups.remove(p)
                        del p

                    elif p.powerup_type == "invulnerability" and player.shields_remaining < 2:
                        play_sfx("shield_pickup", 0, 1, 0.4)
                        player.shields_remaining += 1
                        powerups.remove(p)
                        del p

        # WING TOUCH
        if abs(player.bank) >= player.max_bank:
            
            if wing_touch_volume < 50:
                wing_touch_volume += 75 * dt

            elif wing_touch_volume > 50:
                wing_touch_volume = 50

        else:
            if wing_touch_volume > 0:
                wing_touch_volume -= 50 * dt

        if wing_touch_volume < 0:
            wing_touch_volume = 0

        if wing_touch_volume:
            if not get_channel_busy(5):
                play_sfx("wingtouch", 1, 5, wing_touch_volume/100)
            else:
                set_channel_volume(5, wing_touch_volume/100)

        else:
            if get_channel_busy(5):
                stop_channel(5)

        # ENGINE SFX
        engine_volume = player.speed / (player.boost_speed * 4)
        set_channel_volume(6, engine_volume)

        # BGM
        if not is_music_playing():
            play_random_bgm()

        # POEM
        poem_line = max(int((score-5000)/15000), -1)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        drawScene(main_cam, player, floor, obstacles, powerups, luna, dt, score,
                  player.shields_remaining, poem_index, poem_line)
        glfw.swap_buffers(mwin)

        dt = time.perf_counter() - cycle_start
        score += player.speed * dt
        game_tick += 1

main()
