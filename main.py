import pygame
import os
import io
import math
import random

from characters import *
from functions import *

##create save game file if doesn't exist##
data = {} #build dictionary
if os.path.exists("data.dat"):
    f = open("data.dat", "r")
    for d in f:
        (k, v) = d.split()
        data[k] = v
    f.close()
else:
    try:
        with open("data.dat", "w") as f:
            f.write("width: 1280\nheight: 720\nframes: 120\naudio: ON") ##default settings##
            for d in f:
                (k, v) = d.split()
                data[k] = v
            f.close()
    except:
        pass
print(data) ##so I can review the data and properly import it into the code

##vars
global _width_
global _height_
global _fps_
_width_ = int(data['width:']) if "width:" in data else 1280
_height_ = int(data['height:']) if "height:" in data else 720
_fps_ = int(data['frames:']) if "frames:" in data else 120

options = ["Play Game", "Save Game", "Game Settings", "Exit"]
global _menu_option_
_menu_option_ = options[0]
global _cur_screen_
_cur_screen_ = "Home"
global _settings_option_
_settings_option_ = "Resolution"
global _char_option_
_char_option_ = "Knight"
pygame.font.init()

#setting up display
game = pygame.display.set_mode((_width_, _height_))
pygame.display.set_caption("AlexW03x Turn Based Game Project")
_logo_ = pygame.image.load(os.path.join("Assets", "Swords.png"))
pygame.display.set_icon(_logo_)

##sounds fetching
global soundon
soundon = True
if "audio:" in data:
    soundon = True if data["audio:"] == "ON" else False
pygame.mixer.init()
menusound = pygame.mixer.Sound(os.path.join("Assets/Sounds", "Menu_Click.wav"))
skillsound = pygame.mixer.Sound(os.path.join("Assets/Sounds", "Skills_Click.wav"))

#images fetching
_menu_bg_ = pygame.image.load(os.path.join("Assets", "Background.png"))
_knight_card_ = pygame.image.load(os.path.join("Assets", "Warrior Class Card.png"))
_wizard_card_ = pygame.image.load(os.path.join("Assets", "Wizard Class Card.png"))
_assassin_card_ = pygame.image.load(os.path.join("Assets", "Assassin Class Card.png"))
_char_bg_ = pygame.image.load(os.path.join("Assets", "Character_Background.png"))
_zone1_bg_ = pygame.image.load(os.path.join("Assets/Introduction", "Introduction_Background.png"))
_char_icon_knight_ = pygame.image.load(os.path.join("Assets", "Warrior_Icon.JPG"))
_char_icon_wizard_ = pygame.image.load(os.path.join("Assets", "Wizard_Icon.JPG"))
_char_icon_assassin_ = pygame.image.load(os.path.join("Assets", "Assassin_Icon.JPG"))
_char_knight_ = pygame.image.load(os.path.join("Assets", "Warrior.png"))
_char_wizard_ = pygame.image.load(os.path.join("Assets", "Wizard.png"))
_char_assassin_ = pygame.image.load(os.path.join("Assets", "Assassin.png"))
_tut_enemy_ = pygame.image.load(os.path.join("Assets/Introduction", "Tutorial Enemy.png"))
_tut_icon_ =pygame.image.load(os.path.join("Assets/Introduction", "Tutorial Icon.JPG"))
_skull_icon_ = pygame.image.load(os.path.join("Assets", "Skull.png"))

_l2_enemy_ = pygame.image.load(os.path.join("Assets/Level 2", "Robot.png"))
_l2_icon_ = pygame.image.load(os.path.join("Assets/Level 2", "Robot_Icon.JPG"))

_l3_enemy_ = pygame.image.load(os.path.join("Assets/Level 3", "The_Broken_One.png"))
_l3_icon_ = pygame.image.load(os.path.join("Assets/Level 3", "The_Broken_One_Icon.JPG"))

_l4_enemy_ = pygame.image.load(os.path.join("Assets/Level 4", "Gunner.png"))
_l4_icon_ = pygame.image.load(os.path.join("Assets/Level 4", "Gunner_Icon.JPG"))

#fetch basic skills
_basic_attack_ = pygame.image.load(os.path.join("Assets/Skills", "Basic Attack.png"))
_heal_ = pygame.image.load(os.path.join("Assets/Skills", "Heal.png"))
_mana_ = pygame.image.load(os.path.join("Assets/Skills", "Mana.png"))

#fetch knight skills
_slam_ = pygame.image.load(os.path.join("Assets/Skills/Knight", "Slam.png"))
_shield_ = pygame.image.load(os.path.join("Assets/Skills/Knight", "Shield.png"))
_ballistic_strike_ = pygame.image.load(os.path.join("Assets/Skills/Knight", "Ballistic Strike.png"))
_double_strike_ = pygame.image.load(os.path.join("Assets/Skills/Knight", "Double Strike.png"))
_puncture_ = pygame.image.load(os.path.join("Assets/Skills/Knight", "Puncture.png"))
_stun_ = pygame.image.load(os.path.join("Assets/Skills/Knight", "Stun.png"))
_suit_up_ = pygame.image.load(os.path.join("Assets/Skills/Knight", "Suit Up.png"))
_enrage_ = pygame.image.load(os.path.join("Assets/Skills/Knight", "Enrage.png"))
_vampire_strike_ = pygame.image.load(os.path.join("Assets/Skills/Knight", "Vampire Strike.png"))

#fetch wizard skills
_fireball_ = pygame.image.load(os.path.join("Assets/Skills/Wizard", "Fireball.png"))
_freeze_ = pygame.image.load(os.path.join("Assets/Skills/Wizard", "Freeze.png"))
_drain_ = pygame.image.load(os.path.join("Assets/Skills/Wizard", "Drain.png"))
_invert_ = pygame.image.load(os.path.join("Assets/Skills/Wizard", "Invert.png"))
_leech_ = pygame.image.load(os.path.join("Assets/Skills/Wizard", "Leech.png"))
_life_ = pygame.image.load(os.path.join("Assets/Skills/Wizard", "Life.png"))
_lightning_strike_ = pygame.image.load(os.path.join("Assets/Skills/Wizard", "Lightning Strike.png"))
_soul_crush_ = pygame.image.load(os.path.join("Assets/Skills/Wizard", "Soul Crush.png"))
_weakness_ = pygame.image.load(os.path.join("Assets/Skills/Wizard", "Weakness.png"))

#fetch assassin skills
_amputate_ = pygame.image.load(os.path.join("Assets/Skills/Assassin", "Amputate.png"))
_blindside_ = pygame.image.load(os.path.join("Assets/Skills/Assassin", "Blindside.png"))
_dragons_breath_ = pygame.image.load(os.path.join("Assets/Skills/Assassin", "Dragons Breath.png"))
_fury_strike_ = pygame.image.load(os.path.join("Assets/Skills/Assassin", "Fury Strike.png"))
_overcharge_ = pygame.image.load(os.path.join("Assets/Skills/Assassin", "Overcharge.png"))
_poison_ = pygame.image.load(os.path.join("Assets/Skills/Assassin", "Poison.png"))
_shuriken_ = pygame.image.load(os.path.join("Assets/Skills/Assassin", "Shuriken.png"))
_slash_ = pygame.image.load(os.path.join("Assets/Skills/Assassin", "Slash.png"))
_speed_ = pygame.image.load(os.path.join("Assets/SKills/Assassin", "Speed.png"))

_none_ = pygame.image.load(os.path.join("Assets/Skills", "None.png"))

#the camp assets

_camp_ = pygame.image.load(os.path.join("Assets", "Camp.jpg"))
_home_ = pygame.image.load(os.path.join("Assets", "Home.png"))
_shop_ = pygame.image.load(os.path.join("Assets", "character.png"))
_battle_ = pygame.image.load(os.path.join("Assets", "Battle.png"))
_return_ = pygame.image.load(os.path.join("Assets", "Completed.png"))

global skill1
global skill2
global skill3
global skill4
global skill5
global skill6
global skill7
global skill8
global skill9
global skill10

skill1 = pygame.Rect(300, _height_-100, 32, 32)
skill2 = pygame.Rect(340, _height_-100, 32, 32)
skill3 = pygame.Rect(380, _height_-100, 32, 32)
skill4 = pygame.Rect(420, _height_-100, 32, 32)
skill5 = pygame.Rect(460, _height_-100, 32, 32)
skill6 = pygame.Rect(300, _height_-50, 32, 32)
skill7 = pygame.Rect(340, _height_-50, 32, 32)
skill8 = pygame.Rect(380, _height_-50, 32, 32)
skill9 = pygame.Rect(420, _height_-50, 32, 32)
skill10 = pygame.Rect(460, _height_-50, 32, 32)

def main():
    global _menu_option_
    global _cur_screen_
    global _settings_option_
    global soundon
    global _width_
    global _height_
    global _fps_
    global _char_option_
    global skill1
    global skill2
    global skill3
    global skill4
    global skill5
    global skill6
    global skill7
    global skill8
    global skill9
    global skill10
    clock = pygame.time.Clock() ##create clock to set frames
    ##to ensure that battles doesnt reloop on initialisation##
    battlebegin = False #True prevents reheal and reset
    gamerun = True
    exiticon = pygame.Rect(_width_/2, _height_-90, 64, 64)
    battletimer = 0 #so that user has to decide their course of action in due time
    curTurn = "Self"
    skillused = "" #sets skill after event click
    levels = ["Tutorial Level", "Level 1", "Level 2", "Level 3", "Level 4", "Level 5"]
    counter = 0 #used to allow the text display to stay longer as intended without freezing game
    enemyset = False
    returnbutton = pygame.Rect((_width_/2)-20, 530, 150, 40)
    restartbutton = pygame.Rect((_width_/2)-20, 460, 150, 40)
    gotocampbtn = pygame.Rect((_width_/2)-20, 460, 150, 40)
    xp_slider = 0
    numset = False
    canattack = True

    #set active for skills that require so
    shield = False #for shield skill to be active
    shieldcount = 0
    shieldcooldown = 0
    bscount = 0
    bscooldown = 0
    dbcooldown = 0
    punccooldown = 0
    punc = 0
    stuncooldown = 0
    stun = 0
    slamdown = 0
    suitcooldown = 0
    suit = 0
    enrage = 0
    enragecooldown = 0
    vampirecooldown = 0
    fireballcooldown = 0
    fire = 0
    freeze = 0
    freezecooldown = 0
    draincooldown = 0
    invertcooldown = 0
    invert = 0
    leechcooldown = 0
    lifecooldown = 0
    life = 0
    lightning = 0
    lightningcooldown = 0
    soulcooldown = 0
    soul = 0
    weakness = 0
    weaknesscooldown = 0
    amputate = 0
    amputatecooldown = 0
    blindsidecooldown = 0
    dragon = 0
    dragoncooldown = 0
    furycooldown = 0
    overcharge = 0
    overchargecooldown = 0
    poison = 0
    poisoncooldown = 0
    shurikencooldown = 0
    slashcooldown = 0
    speed = 0
    speedcooldown = 0

    if "experience:" in data and "experience_to_next_level:" in data: #prevent crash bug
        xp_slider = int(data["experience:"]) / int(data["experience_to_next_level:"])
    xp_gained = 0
    if "skill1_item:" not in data: #### if the data doesn't exist originally set the data for tutorial level####
        skill1_item = "Basic Attack"
        skill1_img = _basic_attack_
    if "skill2_item:" not in data:
        skill2_item = "Heal"
        skill2_img = _heal_
    if "skill3_item:" not in data:
        skill3_item = "Mana"
        skill3_img = _mana_
    if "skill4_item:" not in data:
        skill4_item = "None"
        skill4_img = _none_
    if "skill5_item:" not in data:
        skill5_item = "None"
        skill5_img = _none_
    if "skill6_item:" not in data:
        skill6_item = "None"
        skill6_img = _none_
    if "skill7_item:" not in data:
        skill7_item = "None"
        skill7_img = _none_
    if "skill8_item:" not in data:
        skill8_item = "None"
        skill8_img = _none_
    if "skill9_item:" not in data:
        skill9_item = "None"
        skill9_img = _none_
    if "skill10_item:" not in data:
        skill10_item = "None"
        skill10_img = _none_

    skillselected = ""

    while gamerun:
        clock.tick(_fps_)

        #this iteration of ternary operators allows for skills to be swappable giving the player full control over their abilities.
        if "skill1_item:" in data: ## use data from the database if exists
            skill1_item = data["skill1_item:"]
            skill1_img = _basic_attack_ if data["skill1_item:"] == "Basic_Attack" else _heal_ if data["skill1_item:"] == "Heal" else _mana_ if data["skill1_item:"] == "Mana" else _amputate_ if data["skill1_item:"] == "Amputate" else _blindside_ if data["skill1_item:"] == "Blindside" else _dragons_breath_ if data["skill1_item:"] == "Dragons_Breath" else _fury_strike_ if data["skill1_item:"] == "Fury_Strike" else _overcharge_ if data["skill1_item:"] == "Overcharge" else _poison_ if data["skill1_item:"] == "Poison" else _shuriken_ if data["skill1_item:"] == "Shuriken" else _slash_ if data["skill1_item:"] == "Slash" else _speed_ if data["skill1_item:"] == "Speed" else _ballistic_strike_ if data["skill1_item:"] == "Ballistic_Strike" else _double_strike_ if data["skill1_item:"] == "Double_Strike" else _enrage_ if data["skill1_item:"] == "Enrage" else _puncture_ if data["skill1_item:"] == "Puncture" else _shield_ if data["skill1_item:"] == "Shield" else _slam_ if data["skill1_item:"] == "Slam" else _stun_ if data["skill1_item:"] == "Stun" else _suit_up_ if data["skill1_item:"] == "Suit_Up" else _vampire_strike_ if data["skill1_item:"] == "Vampire_Strike" else _drain_ if data["skill1_item:"] == "Drain" else _fireball_ if data["skill1_item:"] == "Fireball" else _freeze_ if data["skill1_item:"] == "Freeze" else _invert_ if data["skill1_item:"] == "Invert" else _leech_ if data["skill1_item:"] == "Leech" else _life_ if data["skill1_item:"] == "Life" else _lightning_strike_ if data["skill1_item:"] == "Lightning_Strike" else _soul_crush_ if data["skill1_item:"] == "Soul_Crush" else _weakness_ if data["skill1_item:"] == "Weakness" else _none_
        if "skill2_item:" in data:
            skill2_item = data["skill2_item:"]
            skill2_img = _basic_attack_ if data["skill2_item:"] == "Basic_Attack" else _heal_ if data["skill2_item:"] == "Heal" else _mana_ if data["skill2_item:"] == "Mana" else _amputate_ if data["skill2_item:"] == "Amputate" else _blindside_ if data["skill2_item:"] == "Blindside" else _dragons_breath_ if data["skill2_item:"] == "Dragons_Breath" else _fury_strike_ if data["skill2_item:"] == "Fury_Strike" else _overcharge_ if data["skill2_item:"] == "Overcharge" else _poison_ if data["skill2_item:"] == "Poison" else _shuriken_ if data["skill2_item:"] == "Shuriken" else _slash_ if data["skill2_item:"] == "Slash" else _speed_ if data["skill2_item:"] == "Speed" else _ballistic_strike_ if data["skill2_item:"] == "Ballistic_Strike" else _double_strike_ if data["skill2_item:"] == "Double_Strike" else _enrage_ if data["skill2_item:"] == "Enrage" else _puncture_ if data["skill2_item:"] == "Puncture" else _shield_ if data["skill2_item:"] == "Shield" else _slam_ if data["skill2_item:"] == "Slam" else _stun_ if data["skill2_item:"] == "Stun" else _suit_up_ if data["skill2_item:"] == "Suit_Up" else _vampire_strike_ if data["skill2_item:"] == "Vampire_Strike" else _drain_ if data["skill2_item:"] == "Drain" else _fireball_ if data["skill2_item:"] == "Fireball" else _freeze_ if data["skill2_item:"] == "Freeze" else _invert_ if data["skill2_item:"] == "Invert" else _leech_ if data["skill2_item:"] == "Leech" else _life_ if data["skill2_item:"] == "Life" else _lightning_strike_ if data["skill2_item:"] == "Lightning_Strike" else _soul_crush_ if data["skill2_item:"] == "Soul_Crush" else _weakness_ if data["skill2_item:"] == "Weakness" else _none_
        if "skill3_item:" in data:
            skill3_item = data["skill3_item:"]
            skill3_img = _basic_attack_ if data["skill3_item:"] == "Basic_Attack" else _heal_ if data["skill3_item:"] == "Heal" else _mana_ if data["skill3_item:"] == "Mana" else _amputate_ if data["skill3_item:"] == "Amputate" else _blindside_ if data["skill3_item:"] == "Blindside" else _dragons_breath_ if data["skill3_item:"] == "Dragons_Breath" else _fury_strike_ if data["skill3_item:"] == "Fury_Strike" else _overcharge_ if data["skill3_item:"] == "Overcharge" else _poison_ if data["skill3_item:"] == "Poison" else _shuriken_ if data["skill3_item:"] == "Shuriken" else _slash_ if data["skill3_item:"] == "Slash" else _speed_ if data["skill3_item:"] == "Speed" else _ballistic_strike_ if data["skill3_item:"] == "Ballistic_Strike" else _double_strike_ if data["skill3_item:"] == "Double_Strike" else _enrage_ if data["skill3_item:"] == "Enrage" else _puncture_ if data["skill3_item:"] == "Puncture" else _shield_ if data["skill3_item:"] == "Shield" else _slam_ if data["skill3_item:"] == "Slam" else _stun_ if data["skill3_item:"] == "Stun" else _suit_up_ if data["skill3_item:"] == "Suit_Up" else _vampire_strike_ if data["skill3_item:"] == "Vampire_Strike" else _drain_ if data["skill3_item:"] == "Drain" else _fireball_ if data["skill3_item:"] == "Fireball" else _freeze_ if data["skill3_item:"] == "Freeze" else _invert_ if data["skill3_item:"] == "Invert" else _leech_ if data["skill3_item:"] == "Leech" else _life_ if data["skill3_item:"] == "Life" else _lightning_strike_ if data["skill3_item:"] == "Lightning_Strike" else _soul_crush_ if data["skill3_item:"] == "Soul_Crush" else _weakness_ if data["skill3_item:"] == "Weakness" else _none_
        if "skill4_item:" in data:
            skill4_item = data["skill4_item:"]
            skill4_img = _basic_attack_ if data["skill4_item:"] == "Basic_Attack" else _heal_ if data["skill4_item:"] == "Heal" else _mana_ if data["skill4_item:"] == "Mana" else _amputate_ if data["skill4_item:"] == "Amputate" else _blindside_ if data["skill4_item:"] == "Blindside" else _dragons_breath_ if data["skill4_item:"] == "Dragons_Breath" else _fury_strike_ if data["skill4_item:"] == "Fury_Strike" else _overcharge_ if data["skill4_item:"] == "Overcharge" else _poison_ if data["skill4_item:"] == "Poison" else _shuriken_ if data["skill4_item:"] == "Shuriken" else _slash_ if data["skill4_item:"] == "Slash" else _speed_ if data["skill4_item:"] == "Speed" else _ballistic_strike_ if data["skill4_item:"] == "Ballistic_Strike" else _double_strike_ if data["skill4_item:"] == "Double_Strike" else _enrage_ if data["skill4_item:"] == "Enrage" else _puncture_ if data["skill4_item:"] == "Puncture" else _shield_ if data["skill4_item:"] == "Shield" else _slam_ if data["skill4_item:"] == "Slam" else _stun_ if data["skill4_item:"] == "Stun" else _suit_up_ if data["skill4_item:"] == "Suit_Up" else _vampire_strike_ if data["skill4_item:"] == "Vampire_Strike" else _drain_ if data["skill4_item:"] == "Drain" else _fireball_ if data["skill4_item:"] == "Fireball" else _freeze_ if data["skill4_item:"] == "Freeze" else _invert_ if data["skill4_item:"] == "Invert" else _leech_ if data["skill4_item:"] == "Leech" else _life_ if data["skill4_item:"] == "Life" else _lightning_strike_ if data["skill4_item:"] == "Lightning_Strike" else _soul_crush_ if data["skill4_item:"] == "Soul_Crush" else _weakness_ if data["skill4_item:"] == "Weakness" else _none_
        if "skill5_item:" in data:
            skill5_item = data["skill5_item:"]
            skill5_img = _basic_attack_ if data["skill5_item:"] == "Basic_Attack" else _heal_ if data["skill5_item:"] == "Heal" else _mana_ if data["skill5_item:"] == "Mana" else _amputate_ if data["skill5_item:"] == "Amputate" else _blindside_ if data["skill5_item:"] == "Blindside" else _dragons_breath_ if data["skill5_item:"] == "Dragons_Breath" else _fury_strike_ if data["skill5_item:"] == "Fury_Strike" else _overcharge_ if data["skill5_item:"] == "Overcharge" else _poison_ if data["skill5_item:"] == "Poison" else _shuriken_ if data["skill5_item:"] == "Shuriken" else _slash_ if data["skill5_item:"] == "Slash" else _speed_ if data["skill5_item:"] == "Speed" else _ballistic_strike_ if data["skill5_item:"] == "Ballistic_Strike" else _double_strike_ if data["skill5_item:"] == "Double_Strike" else _enrage_ if data["skill5_item:"] == "Enrage" else _puncture_ if data["skill5_item:"] == "Puncture" else _shield_ if data["skill5_item:"] == "Shield" else _slam_ if data["skill5_item:"] == "Slam" else _stun_ if data["skill5_item:"] == "Stun" else _suit_up_ if data["skill5_item:"] == "Suit_Up" else _vampire_strike_ if data["skill5_item:"] == "Vampire_Strike" else _drain_ if data["skill5_item:"] == "Drain" else _fireball_ if data["skill5_item:"] == "Fireball" else _freeze_ if data["skill5_item:"] == "Freeze" else _invert_ if data["skill5_item:"] == "Invert" else _leech_ if data["skill5_item:"] == "Leech" else _life_ if data["skill5_item:"] == "Life" else _lightning_strike_ if data["skill5_item:"] == "Lightning_Strike" else _soul_crush_ if data["skill5_item:"] == "Soul_Crush" else _weakness_ if data["skill5_item:"] == "Weakness" else _none_
        if "skill6_item:" in data:
            skill6_item = data["skill6_item:"]
            skill6_img = _basic_attack_ if data["skill6_item:"] == "Basic_Attack" else _heal_ if data["skill6_item:"] == "Heal" else _mana_ if data["skill6_item:"] == "Mana" else _amputate_ if data["skill6_item:"] == "Amputate" else _blindside_ if data["skill6_item:"] == "Blindside" else _dragons_breath_ if data["skill6_item:"] == "Dragons_Breath" else _fury_strike_ if data["skill6_item:"] == "Fury_Strike" else _overcharge_ if data["skill6_item:"] == "Overcharge" else _poison_ if data["skill6_item:"] == "Poison" else _shuriken_ if data["skill6_item:"] == "Shuriken" else _slash_ if data["skill6_item:"] == "Slash" else _speed_ if data["skill6_item:"] == "Speed" else _ballistic_strike_ if data["skill6_item:"] == "Ballistic_Strike" else _double_strike_ if data["skill6_item:"] == "Double_Strike" else _enrage_ if data["skill6_item:"] == "Enrage" else _puncture_ if data["skill6_item:"] == "Puncture" else _shield_ if data["skill6_item:"] == "Shield" else _slam_ if data["skill6_item:"] == "Slam" else _stun_ if data["skill6_item:"] == "Stun" else _suit_up_ if data["skill6_item:"] == "Suit_Up" else _vampire_strike_ if data["skill6_item:"] == "Vampire_Strike" else _drain_ if data["skill6_item:"] == "Drain" else _fireball_ if data["skill6_item:"] == "Fireball" else _freeze_ if data["skill6_item:"] == "Freeze" else _invert_ if data["skill6_item:"] == "Invert" else _leech_ if data["skill6_item:"] == "Leech" else _life_ if data["skill6_item:"] == "Life" else _lightning_strike_ if data["skill6_item:"] == "Lightning_Strike" else _soul_crush_ if data["skill6_item:"] == "Soul_Crush" else _weakness_ if data["skill6_item:"] == "Weakness" else _none_
        if "skill7_item:" in data:
            skill7_item = data["skill7_item:"]
            skill7_img = _basic_attack_ if data["skill7_item:"] == "Basic_Attack" else _heal_ if data["skill7_item:"] == "Heal" else _mana_ if data["skill7_item:"] == "Mana" else _amputate_ if data["skill7_item:"] == "Amputate" else _blindside_ if data["skill7_item:"] == "Blindside" else _dragons_breath_ if data["skill7_item:"] == "Dragons_Breath" else _fury_strike_ if data["skill7_item:"] == "Fury_Strike" else _overcharge_ if data["skill7_item:"] == "Overcharge" else _poison_ if data["skill7_item:"] == "Poison" else _shuriken_ if data["skill7_item:"] == "Shuriken" else _slash_ if data["skill7_item:"] == "Slash" else _speed_ if data["skill7_item:"] == "Speed" else _ballistic_strike_ if data["skill7_item:"] == "Ballistic_Strike" else _double_strike_ if data["skill7_item:"] == "Double_Strike" else _enrage_ if data["skill7_item:"] == "Enrage" else _puncture_ if data["skill7_item:"] == "Puncture" else _shield_ if data["skill7_item:"] == "Shield" else _slam_ if data["skill7_item:"] == "Slam" else _stun_ if data["skill7_item:"] == "Stun" else _suit_up_ if data["skill7_item:"] == "Suit_Up" else _vampire_strike_ if data["skill7_item:"] == "Vampire_Strike" else _drain_ if data["skill7_item:"] == "Drain" else _fireball_ if data["skill7_item:"] == "Fireball" else _freeze_ if data["skill7_item:"] == "Freeze" else _invert_ if data["skill7_item:"] == "Invert" else _leech_ if data["skill7_item:"] == "Leech" else _life_ if data["skill7_item:"] == "Life" else _lightning_strike_ if data["skill7_item:"] == "Lightning_Strike" else _soul_crush_ if data["skill7_item:"] == "Soul_Crush" else _weakness_ if data["skill7_item:"] == "Weakness" else _none_
        if "skill8_item:" in data:
            skill8_item = data["skill8_item:"]
            skill8_img = _basic_attack_ if data["skill8_item:"] == "Basic_Attack" else _heal_ if data["skill8_item:"] == "Heal" else _mana_ if data["skill8_item:"] == "Mana" else _amputate_ if data["skill8_item:"] == "Amputate" else _blindside_ if data["skill8_item:"] == "Blindside" else _dragons_breath_ if data["skill8_item:"] == "Dragons_Breath" else _fury_strike_ if data["skill8_item:"] == "Fury_Strike" else _overcharge_ if data["skill8_item:"] == "Overcharge" else _poison_ if data["skill8_item:"] == "Poison" else _shuriken_ if data["skill8_item:"] == "Shuriken" else _slash_ if data["skill8_item:"] == "Slash" else _speed_ if data["skill8_item:"] == "Speed" else _ballistic_strike_ if data["skill8_item:"] == "Ballistic_Strike" else _double_strike_ if data["skill8_item:"] == "Double_Strike" else _enrage_ if data["skill8_item:"] == "Enrage" else _puncture_ if data["skill8_item:"] == "Puncture" else _shield_ if data["skill8_item:"] == "Shield" else _slam_ if data["skill8_item:"] == "Slam" else _stun_ if data["skill8_item:"] == "Stun" else _suit_up_ if data["skill8_item:"] == "Suit_Up" else _vampire_strike_ if data["skill8_item:"] == "Vampire_Strike" else _drain_ if data["skill8_item:"] == "Drain" else _fireball_ if data["skill8_item:"] == "Fireball" else _freeze_ if data["skill8_item:"] == "Freeze" else _invert_ if data["skill8_item:"] == "Invert" else _leech_ if data["skill8_item:"] == "Leech" else _life_ if data["skill8_item:"] == "Life" else _lightning_strike_ if data["skill8_item:"] == "Lightning_Strike" else _soul_crush_ if data["skill8_item:"] == "Soul_Crush" else _weakness_ if data["skill8_item:"] == "Weakness" else _none_
        if "skill9_item:" in data:
            skill9_item = data["skill9_item:"]
            skill9_img = _basic_attack_ if data["skill9_item:"] == "Basic_Attack" else _heal_ if data["skill9_item:"] == "Heal" else _mana_ if data["skill9_item:"] == "Mana" else _amputate_ if data["skill9_item:"] == "Amputate" else _blindside_ if data["skill9_item:"] == "Blindside" else _dragons_breath_ if data["skill9_item:"] == "Dragons_Breath" else _fury_strike_ if data["skill9_item:"] == "Fury_Strike" else _overcharge_ if data["skill9_item:"] == "Overcharge" else _poison_ if data["skill9_item:"] == "Poison" else _shuriken_ if data["skill9_item:"] == "Shuriken" else _slash_ if data["skill9_item:"] == "Slash" else _speed_ if data["skill9_item:"] == "Speed" else _ballistic_strike_ if data["skill9_item:"] == "Ballistic_Strike" else _double_strike_ if data["skill9_item:"] == "Double_Strike" else _enrage_ if data["skill9_item:"] == "Enrage" else _puncture_ if data["skill9_item:"] == "Puncture" else _shield_ if data["skill9_item:"] == "Shield" else _slam_ if data["skill9_item:"] == "Slam" else _stun_ if data["skill9_item:"] == "Stun" else _suit_up_ if data["skill9_item:"] == "Suit_Up" else _vampire_strike_ if data["skill9_item:"] == "Vampire_Strike" else _drain_ if data["skill9_item:"] == "Drain" else _fireball_ if data["skill9_item:"] == "Fireball" else _freeze_ if data["skill9_item:"] == "Freeze" else _invert_ if data["skill9_item:"] == "Invert" else _leech_ if data["skill9_item:"] == "Leech" else _life_ if data["skill9_item:"] == "Life" else _lightning_strike_ if data["skill9_item:"] == "Lightning_Strike" else _soul_crush_ if data["skill9_item:"] == "Soul_Crush" else _weakness_ if data["skill9_item:"] == "Weakness" else _none_
        if "skill10_item:" in data:
            skill10_item = data["skill10_item:"]
            skill10_img = _basic_attack_ if data["skill10_item:"] == "Basic_Attack" else _heal_ if data["skill10_item:"] == "Heal" else _mana_ if data["skill10_item:"] == "Mana" else _amputate_ if data["skill10_item:"] == "Amputate" else _blindside_ if data["skill10_item:"] == "Blindside" else _dragons_breath_ if data["skill10_item:"] == "Dragons_Breath" else _fury_strike_ if data["skill10_item:"] == "Fury_Strike" else _overcharge_ if data["skill10_item:"] == "Overcharge" else _poison_ if data["skill10_item:"] == "Poison" else _shuriken_ if data["skill10_item:"] == "Shuriken" else _slash_ if data["skill10_item:"] == "Slash" else _speed_ if data["skill10_item:"] == "Speed" else _ballistic_strike_ if data["skill10_item:"] == "Ballistic_Strike" else _double_strike_ if data["skill10_item:"] == "Double_Strike" else _enrage_ if data["skill10_item:"] == "Enrage" else _puncture_ if data["skill10_item:"] == "Puncture" else _shield_ if data["skill10_item:"] == "Shield" else _slam_ if data["skill10_item:"] == "Slam" else _stun_ if data["skill10_item:"] == "Stun" else _suit_up_ if data["skill10_item:"] == "Suit_Up" else _vampire_strike_ if data["skill10_item:"] == "Vampire_Strike" else _drain_ if data["skill10_item:"] == "Drain" else _fireball_ if data["skill10_item:"] == "Fireball" else _freeze_ if data["skill10_item:"] == "Freeze" else _invert_ if data["skill10_item:"] == "Invert" else _leech_ if data["skill10_item:"] == "Leech" else _life_ if data["skill10_item:"] == "Life" else _lightning_strike_ if data["skill10_item:"] == "Lightning_Strike" else _soul_crush_ if data["skill10_item:"] == "Soul_Crush" else _weakness_ if data["skill10_item:"] == "Weakness" else _none_
            

        if _cur_screen_ == "Home":
            game.blit(transform(_menu_bg_, (_width_, _height_)), (0,0))
            game.blit(comicsans(40).render("AlexW03x Game", 1, WHITE), (_width_/2 - comicsans(40).render("AlexW03x Game", 1, WHITE).get_width()/2, 50))
            game.blit(comicsans(20).render("Play Game", 1, FOCUS if _menu_option_ == "Play Game" else WHITE), (_width_/2 - comicsans(20).render("Play Game", 1, WHITE).get_width()/2, 200))
            game.blit(comicsans(20).render("View Saved Game", 1, FOCUS if _menu_option_ == "Save Game" else WHITE), (_width_/2 - comicsans(20).render("View Saved Game", 1, WHITE).get_width()/2, 300))
            game.blit(comicsans(20).render("Game Settings", 1, FOCUS if _menu_option_ == "Game Settings" else WHITE), (_width_/2 - comicsans(20).render("Game Settings", 1, WHITE).get_width()/2, 400))
            game.blit(comicsans(20).render("Exit Game", 1, FOCUS if _menu_option_ == "Exit" else WHITE), (_width_/2 - comicsans(20).render("Exit Game", 1, WHITE).get_width()/2, 500))
        if _cur_screen_ == "Settings":
            game.blit(transform(_menu_bg_, (_width_, _height_)), (0,0))
            game.blit(comicsans(40).render("AlexW03x Game", 1, WHITE), (_width_/2 - comicsans(40).render("AlexW03x Game", 1, WHITE).get_width()/2, 50))
            game.blit(comicsans(20).render("Resolution: " + str(_width_) + "x" + str(_height_), 1, FOCUS if _settings_option_ == "Resolution" else WHITE), (_width_/2 - comicsans(20).render("Resolution: " + str(_width_) + "x" + str(_height_), 1, WHITE).get_width()/2, 200))
            game.blit(comicsans(20).render("Audio: " + ("ON" if soundon == True else "OFF"), 1, FOCUS if _settings_option_ == "Audio" else WHITE), (_width_/2 - comicsans(20).render("Audio:" + ("ON" if soundon == True else "OFF"), 1, WHITE).get_width()/2, 300))
            game.blit(comicsans(20).render("FPS: " + str(_fps_), 1, FOCUS if _settings_option_ == "FPS" else WHITE), (_width_/2 - comicsans(20).render("FPS: " + str(_fps_), 1, WHITE).get_width()/2, 400))
            game.blit(comicsans(20).render("Exit Settings", 1, FOCUS if _settings_option_ == "Exit" else WHITE), (_width_/2 - comicsans(20).render("Exit Settings", 1, WHITE).get_width()/2, 500))
        if _cur_screen_ == "Saves":
            game.blit(transform(_menu_bg_, (_width_, _height_)), (0,0))
            game.blit(comicsans(40).render("AlexW03x Game", 1, WHITE), (_width_/2 - comicsans(40).render("AlexW03x Game", 1, WHITE).get_width()/2, 50))
            ##save data to be displayed##
            game.blit(comicsans(20).render("Your Saved Data: ", 1, WHITE), (_width_/2 - comicsans(20).render("Your Saved Data: ", 1, WHITE).get_width()/2, 100))

            if "chartype:" in data:
                d1 = comicsans(20).render("Class Type: " + str(data["chartype:"]), 1, WHITE)
                d2 = comicsans(20).render("Level: " + str(data["level:"]), 1, WHITE)
                d3 = comicsans(20).render("Experience: " + str(data["experience:"]), 1, WHITE)
                d4 = comicsans(20).render("Experience To Next Level: " + str(data["experience_to_next_level:"]), 1, WHITE)
                d5 = comicsans(20).render("Skill Points: " + str(data["skillpoints:"]), 1, WHITE)
                d6 = comicsans(20).render("Attribute Points: " + str(data["attributepoints:"]), 1, WHITE)
                d7 = comicsans(20).render("Vitality: " + str(data["vitality:"]), 1, WHITE)
                d8 = comicsans(20).render("Magic: " + str(data["magic:"]), 1, WHITE)
                d9 = comicsans(20).render("Strength: " + str(data["strength:"]), 1, WHITE)
                d10 = comicsans(20).render("Speed: " + str(data["speed:"]), 1, WHITE)

                game.blit(d1, (_width_/2 - d1.get_width()/2, 150))
                game.blit(d2, (_width_/2 - d2.get_width()/2, 175))
                game.blit(d3, (_width_/2 - d3.get_width()/2, 200))
                game.blit(d4, (_width_/2 - d4.get_width()/2, 225))
                game.blit(d5, (_width_/2 - d5.get_width()/2, 250))
                game.blit(d6, (_width_/2 - d6.get_width()/2, 275))
                game.blit(d7, (_width_/2 - d7.get_width()/2, 300))
                game.blit(d8, (_width_/2 - d8.get_width()/2, 325))
                game.blit(d9, (_width_/2 - d9.get_width()/2, 350))
                game.blit(d10, (_width_/2 - d10.get_width()/2, 375))
            else:
                game.blit(comicsans(20).render("No character created!", 1, WHITE), (_width_/2 - comicsans(20).render("No character created!", 1, WHITE).get_width()/2, 150))

            
            escape = comicsans(20).render("Exit Saved Game Menu", 1, FOCUS)
            game.blit(escape, (_width_/2 - escape.get_width()/2, 500))

        if _cur_screen_ == "Play" and "chartype:" not in data:
            game.fill(BLACK)
            game.blit(comicsans(40).render("AlexW03x Game", 1, WHITE), (_width_/2 - comicsans(40).render("AlexW03x Game", 1, WHITE).get_width()/2, 50))    

            ##character cards##
            game.blit(transform(_knight_card_, (_width_/4, _height_/2)), (_width_/12, 150))   
            game.blit(transform(_wizard_card_, (_width_/4, _height_/2)), (_width_/2.7, 150))
            game.blit(transform(_assassin_card_, (_width_/4, _height_/2)), (_width_/1.5, 150))

            ##character selection##
            t1 = comicsans(20).render("Knight Class", 1, FOCUS if _char_option_ == "Knight" else WHITE)
            t2 = comicsans(20).render("Wizard Class", 1, FOCUS if _char_option_ == "Wizard" else WHITE)
            t3 = comicsans(20).render("Assassin Class", 1, FOCUS if _char_option_ == "Assassin" else WHITE)
            t4 = comicsans(20).render("Exit To Menu", 1, FOCUS if _char_option_ == "Exit" else WHITE)
            game.blit(t1, (_width_/6.6, 500 if _height_ == 660 else 540 if _height_ == 720 else 720))
            game.blit(t2, (_width_/2.3, 500 if _height_ == 660 else 540 if _height_ == 720 else 720))
            game.blit(t3, (_width_/1.37, 500 if _height_ == 660 else 540 if _height_ == 720 else 720))
            game.blit(t4, (_width_/6.6, _height_ * 0.9))

        if _cur_screen_ == "Play" and "chartype:" in data:
            if "game_level:" in data: ##goto tutorial level if 0 or return to camp
                if int(data["game_level:"]) == 0: #tutorial level
                    _cur_screen_ = "Tutorial Level"
                else:
                    _cur_screen_ = "Camp"
            else:
                data["game_level:"] = 0 #as no game level detected return to tutorial level
                savegame("data.dat", data)
                _cur_screen_ = "Tutorial Level"

        if _cur_screen_ == "Tutorial Level":
            game.blit(transform(_zone1_bg_, (_width_, _height_)), (0,-100))
            ##create characters##
            if battlebegin == False:
                myself = YourChar(data["chartype:"], int(data["vitality:"]), int(data["strength:"]), int(data["magic:"]), int(data["speed:"]), int(data["level:"]), int(data["skillpoints:"]), int(data["attributepoints:"]), int(data["experience:"]), int(data["experience_to_next_level:"]))
                myself_max_health = 100 + (myself.retrievestat("hp") * myself.retrievestat("strength"))
                myself_health = myself_max_health
                myself_max_mana = 50 + (myself.retrievestat("magic") * 2)
                myself_mana = myself_max_mana
                myself_power = myself.retrievestat("strength")
                myself_speed = myself.retrievestat("speed")
                myself_magic = myself.retrievestat("magic")
            ##add bottom part##
            footer = pygame.Rect(0, _height_-150, _width_, 150)
            pygame.draw.rect(game, DARKERGRAY, footer)
            _final_icon_ = _char_icon_knight_ if data["chartype:"] == "Knight" else _char_icon_wizard_ if data["chartype:"] == "Wizard" else _char_icon_assassin_
            _final_char_ = _char_knight_ if data["chartype:"] == "Knight" else _char_wizard_ if data["chartype:"] == "Wizard" else _char_assassin_
            heightvar = 320 if data["chartype:"] == "Knight" else 320 if data["chartype:"] == "Wizard" else 320
            selffix = pygame.Rect(50, _height_-100, 64, 64)
            game.blit(transform(_final_icon_, (64,64)), (50, _height_-100))

            if selffix.collidepoint(pygame.mouse.get_pos()): #hover over icon to see your own stats
                square = pygame.Rect(0, _height_-200, 100, 100)
                pygame.draw.rect(game, LIGHTGRAY, square)
                yourvitals = comicsans(9).render("Vitality: " + str(data["vitality:"]), 1, BLACK)
                yourstrength = comicsans(9).render("Strength: " + str(data["strength:"]), 1, BLACK)
                yourmagic = comicsans(9).render("Magic: " + str(data["magic:"]), 1, BLACK)
                yourspeed = comicsans(9).render("Speed: " + str(data["speed:"]), 1, BLACK)
                yourstats = comicsans(10).render("Your Stats: ", 1, BLACK)
                game.blit(yourstats, (square.x, square.y))
                game.blit(yourvitals, (square.x, square.y + 20))
                game.blit(yourstrength, (square.x, square.y + 30))
                game.blit(yourmagic, (square.x, square.y + 40))
                game.blit(yourspeed, (square.x, square.y + 50))
            selfpos = pygame.Rect(100, heightvar, 128, 128)
            game.blit(transform(_final_char_, (128,128)), (selfpos.x, selfpos.y))
            healthbarunder = pygame.Rect(120, _height_-85, 100, 10)
            pygame.draw.rect(game, DARKGREEN, healthbarunder)
            healthbarover = pygame.Rect(120, _height_-85, round(100 * (myself_health/myself_max_health), 0), 10)
            pygame.draw.rect(game, GREEN, healthbarover)
            displayhealth = comicsans(10).render("HP: " + str(myself_health), 1, WHITE)
            game.blit(displayhealth, (120,_height_-100))

            manabarunder = pygame.Rect(120, _height_-60, 100, 10)
            pygame.draw.rect(game, DARKERBLUE, manabarunder)
            manabarover = pygame.Rect(120, _height_-60, round(100 * (myself_mana/myself_max_mana), 0), 10)
            pygame.draw.rect(game, LIGHTBLUE, manabarover)
            displaymana = comicsans(10).render("MP: " + str(myself_mana), 1, WHITE)
            game.blit(displaymana, (120, _height_-75))

            ##add skills section##
            pygame.draw.rect(game, DARKGRAY, skill1)
            pygame.draw.rect(game, DARKGRAY, skill2)
            pygame.draw.rect(game, DARKGRAY, skill3)
            pygame.draw.rect(game, DARKGRAY, skill4)
            pygame.draw.rect(game, DARKGRAY, skill5)
            pygame.draw.rect(game, DARKGRAY, skill6)
            pygame.draw.rect(game, DARKGRAY, skill7)
            pygame.draw.rect(game, DARKGRAY, skill8)
            pygame.draw.rect(game, DARKGRAY, skill9)
            pygame.draw.rect(game, DARKGRAY, skill10)
            #add hover effect to skills to show user that they are currently selecting that skill
            if skill1.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill1)
            if skill2.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill2)
            if skill3.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill3)
            if skill4.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill4)
            if skill5.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill5)
            if skill6.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill6)
            if skill7.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill7)
            if skill8.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill8)
            if skill9.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill9)
            if skill10.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill10)
            #add skill images where applicable
            game.blit(transform(skill1_img, (32,32)), (skill1.x, skill1.y))
            game.blit(transform(skill2_img, (32,32)), (skill2.x, skill2.y))
            game.blit(transform(skill3_img, (32,32)), (skill3.x, skill3.y))
            game.blit(transform(skill4_img, (32,32)), (skill4.x, skill4.y))
            game.blit(transform(skill5_img, (32,32)), (skill5.x, skill5.y))
            game.blit(transform(skill6_img, (32,32)), (skill6.x, skill6.y))
            game.blit(transform(skill7_img, (32,32)), (skill7.x, skill7.y))
            game.blit(transform(skill8_img, (32,32)), (skill8.x, skill8.y))
            game.blit(transform(skill9_img, (32,32)), (skill9.x, skill9.y))
            game.blit(transform(skill10_img, (32,32)), (skill10.x, skill10.y))
            

            ##draw enemy
            enemy = Enemy("Bjorn", _tut_icon_, _tut_enemy_, 7, 15, 3, 5, ["Basic Attack", "Power Slash"])
            tutfix = pygame.Rect(_width_-110, _height_-100, 64, 64)
            game.blit(transform(_tut_icon_, (64,64)), (_width_-110, _height_-100))
            enemypos = pygame.Rect(_width_-200, 320, 128, 128)
            game.blit(transform(_tut_enemy_, (128,128)), (enemypos.x, enemypos.y))
            if battlebegin == False:
                enemy_max_health = 100 + (enemy.get("hp") * enemy.get("strength"))
                enemy_health = enemy_max_health
                enemy_max_mana = 50 + (enemy.get("magic") * 2)
                enemy_mana = enemy_max_mana
                enemy_power = enemy.get("strength")
                enemy_speed = enemy.get("speed")
                battlebegin = True #set true once both players have initialised stats
            enemyhealthbarunder = pygame.Rect(_width_-220, _height_-85, 100, 10)
            enemyhealthbarover = pygame.Rect(_width_-220, _height_-85, round(100 * (enemy_health/enemy_max_health), 0), 10)
            displayenemyhealth = comicsans(10).render("HP: " + str(enemy_health), 1, WHITE)
            pygame.draw.rect(game, DARKGREEN, enemyhealthbarunder)
            pygame.draw.rect(game, GREEN, enemyhealthbarover)
            game.blit(displayenemyhealth, (_width_-170, _height_-100))
            enemymanabarunder = pygame.Rect(_width_-220, _height_-60, 100, 10)
            enemymanabarover = pygame.Rect(_width_-220, _height_-60, round(100 * (enemy_mana/enemy_max_mana), 0), 10)
            displayenemymana = comicsans(10).render("MP: " + str(enemy_mana), 1, WHITE)
            pygame.draw.rect(game, DARKERBLUE, enemymanabarunder)
            pygame.draw.rect(game, LIGHTBLUE, enemymanabarover)
            game.blit(displayenemymana, (_width_-170, _height_-75))
            if tutfix.collidepoint(pygame.mouse.get_pos()):
                square2 = pygame.Rect(_width_-100, _height_-200, 100, 100)
                pygame.draw.rect(game, LIGHTGRAY, square2)
                enemyvitals = comicsans(9).render("Vitality: " + str(enemy.get("hp")), 1, BLACK)
                enemystrength = comicsans(9).render("Strength: " + str(enemy.get("strength")), 1, BLACK)
                enemymagic = comicsans(9).render("Magic: " + str(enemy.get("magic")), 1, BLACK)
                enemyspeed = comicsans(9).render("Speed: " + str(enemy.get("speed")), 1, BLACK)
                enemystats = comicsans(9).render("Enemy Stats: ", 1, BLACK)
                game.blit(enemystats, (square2.x, square2.y))
                game.blit(enemyvitals, (square2.x, square2.y + 20))
                game.blit(enemystrength, (square2.x, square2.y + 30))
                game.blit(enemymagic, (square2.x, square2.y + 40))
                game.blit(enemyspeed, (square2.x, square2.y + 50))

            ##draw area to exit##
            pygame.draw.rect(game, LIGHTGRAY, exiticon)
            pygame.draw.circle(game, (200,0,0), (exiticon.x + 32, exiticon.y + 32), 32)
            game.blit(comicsans(40).render("X", 1, WHITE), (exiticon.x + 18, exiticon.y + 1))
            if exiticon.collidepoint(pygame.mouse.get_pos()): #hover effect
                pygame.draw.rect(game, WHITE, exiticon)
                pygame.draw.circle(game, (150,0,0), (exiticon.x + 32, exiticon.y + 32), 32)
                game.blit(comicsans(40).render("X", 1, WHITE), (exiticon.x + 18, exiticon.y + 1))    
            ##draw text to identify current turn##
            turn = comicsans(20).render("Your Turn!" if curTurn == "Self" else "Enemy Turn!", 1, WHITE)
            game.blit(turn, (exiticon.x-20, exiticon.y-30)) 

            ## battle code for the enemy

            if curTurn == "Enemy" and battlebegin == True and enemy_health > 0:
                if stun > 0:
                    canattack = False
                    stun -= 1
                    if stun < 0:
                        stun = 0
                    curTurn = "Self"
                    enemyset = False
                    numset = False
                    skillused = ""

                if freeze > 0:
                    canattack = False
                    freeze -= 1
                    if freeze < 0:
                        freeze = 0
                    curTurn = "Self"
                    enemyset = False
                    numset = False
                    skillused = ""

                if lightning > 0:
                    canttack = False
                    lightning -= 1
                    if lightning < 0:
                        lightning = 0
                    curTurn = "Self"
                    enemyset = False
                    numset = False
                    skillused = ""


                if enemyset == False:
                    enemy_skills = enemy.get("abilities")
                    ranvalue = random.randint(0, len(enemy_skills)-1) #roll a random move for basic tier enemies so its automatic
                    ##check if enough mana
                    if enemy_skills[ranvalue] == "Basic Attack":
                        enemyset = True
                    if enemy_skills[ranvalue] == "Power Slash" and enemy_mana >= 15:
                        enemyset = True
                    
                if enemy_skills[ranvalue] == "Basic Attack" and canattack == True:
                    dmg = round(int(enemy_power)*1.5, 0)
                    ##chance to miss target based on target speed##
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if number < int(myself_speed): #if roll is less than target speed, means you are slower.
                        dmg = 0
                    elif shield == True:
                        dmg = round(int(enemy_power)*(0.75 - (myself_power*0.01)), 0)
                    elif suit > 0 and shield == False:
                        dmg = round(int(enemy_power)*(1.15),0)
                    elif suit > 0 and shield == True:
                        dmg = round(int(enemy_power) * ( 0.65 - (myself_power * 0.01)), 0)
                    elif weakness > 0:
                        dmg = round(dmg*0.1, 0)
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render(("-" if invert == 0 else "+") + str(dmg) if dmg != 0 else "MISSED!", 1, RED if invert == 0 else GREEN), (selfpos.x, selfpos.y - 100))
                        print("Enemy dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("Enemy used: Basic Attack", 1, WHITE), (_width_/2, 100))

                        if fire > 0:
                            burn = round(int(myself_magic) * 2, 0)
                            game.blit(comicsans(20).render("-" + str(burn), 1, RED), (enemypos.x, enemypos.y - 100))
                        if dragon > 0:
                            burn = round(int(myself_magic) * 1.5, 0)
                            game.blit(comicsans(20).render("-" + str(burn), 1, RED), (enemypos.x, enemypos.y - 100))
                        if poison > 0:
                            burn = round(int(myself_magic) * 1.5, 0)
                            game.blit(comicsans(20).render("-" + str(burn), 1, RED), (enemypos.x, enemypos.y - 100))
                    if counter == 70:
                        curTurn = "Self"
                        counter = 0
                        myself_health = myself_health - dmg if invert == 0 else myself_health + dmg
                        if myself_health < 0:
                            myself_health = 0
                        if myself_health > myself_max_health:
                            myself_health = myself_max_health
                            
                        enemy_mana = enemy_mana + round(enemy_max_mana*0.1,0)
                        if enemy_mana > enemy_max_mana:
                            enemy_mana = enemy_max_mana
                        if fire > 0:
                            enemy_health = enemy_health - burn
                            if enemy_health < 0:
                                enemy_health = 0
                        if dragon > 0:
                            enemy_health = enemy_health - burn
                            if enemy_health < 0:
                                enemy_health = 0
                        if poison > 0:
                            enemy_health = enemy_health - burn
                            if enemy_health < 0:
                                enemy_health = 0
                        if life > 0:
                            myself_health = myself_health + round(myself_max_health * 0.1, 0)
                            if myself_health > myself_max_health:
                                myself_health = myself_max_health
                        enemyset = False
                        numset = False
                        shieldcooldown-=1
                        shieldcount-=1
                        bscooldown -= 1
                        bscount -= 1
                        dbcooldown -= 1
                        punccooldown -= 1
                        punc -= 1
                        slamdown -= 1
                        suit -= 1
                        suitcooldown -= 1 
                        enrage -= 1
                        enragecooldown -= 1
                        fire -= 1
                        fireballcooldown -= 1
                        freeze -= 1
                        freezecooldown -= 1
                        draincooldown -= 1
                        invert -= 1
                        invertcooldown -= 1
                        leechcooldown -= 1
                        life -= 1
                        lifecooldown -= 1
                        lightningcooldown -= 1
                        lightning -= 1
                        soul -= 1
                        soulcooldown -= 1
                        weakness -= 1
                        weaknesscooldown -= 1
                        amputate -= 1
                        amputatecooldown -= 1
                        dragon -= 1
                        dragoncooldown -= 1
                        overcharge -= 1
                        overchargecooldown -= 1
                        poison -= 1
                        poisoncooldown -= 1
                        shurikencooldown -= 1
                        slashcooldown -= 1
                        speedcooldown -= 1
                        if shieldcooldown < 0:
                            shieldcooldown = 0
                        if shieldcount < 0:
                            shieldcount = 0
                            shield = False
                        if bscooldown < 0:
                            bscooldown = 0
                        if bscount < 0:
                            bscount = 0
                        if dbcooldown < 0:
                            dbcooldown = 0
                        if punccooldown < 0:
                            punccooldown = 0
                        if punc < 0:
                            punc = 0
                        if slamdown < 0:
                            slamdown = 0
                        if suit < 0:
                            suit = 0
                        if suitcooldown < 0:
                            suitcooldown = 0
                        if enrage < 0:
                            enrage = 0
                        if enragecooldown < 0:
                            enragecooldown = 0
                        if enrage == 0:
                            myself_power = myself.retrievestat("strength")
                        if fire == 0:
                            fire = 0
                        if fireballcooldown == 0:
                            fireballcooldown = 0
                        if freeze < 0:
                            freeze = 0
                        if freezecooldown < 0:
                            freezecooldown = 0
                        if draincooldown < 0:
                            draincooldown = 0
                        if invert < 0:
                            invert = 0
                        if invertcooldown < 0:
                            invertcooldown = 0
                        if leechcooldown < 0:
                            leechcooldown = 0
                        if life < 0:
                            life = 0
                        if lifecooldown < 0:
                            lifecooldown = 0
                        if lightningcooldown == 0:
                            lightningcooldown = 0
                        if lightning == 0:
                            lightning = 0
                        if soul < 0:
                            soul = 0
                        if soulcooldown < 0:
                            soulcooldown = 0
                        if weakness < 0:
                            weakness = 0
                        if weakness == 0:
                            myself_power = myself.retrievestat("strength")
                            myself_magic = myself.retrievestat("magic")
                        if weaknesscooldown < 0:
                            weaknesscooldown = 0
                        if amputate < 0:
                            amputate = 0
                        if amputatecooldown < 0:
                            amputatecooldown = 0
                        if dragon < 0:
                            dragon = 0
                        if dragoncooldown < 0:
                            dragoncooldown = 0
                        if overcharge < 0:
                            overcharge = 0
                        if overcharge == 0:
                            myself_power = myself.retrievestat("strength")
                            myself_magic = myself.retrievestat("magic")
                        if overchargecooldown < 0:
                            overchargecooldown = 0
                        if poison < 0:
                            poison = 0
                        if poisoncooldown < 0:
                            poisoncooldown = 0
                        if shurikencooldown < 0:
                            shurikencooldown = 0
                        if slashcooldown < 0:
                            slashcooldown = 0
                        if speedcooldown < 0:
                            speedcooldown = 0
                        if speedcooldown == 0:
                            myself_speed = myself.retrievestat("speed")
                
                if enemy_skills[ranvalue] == "Power Slash" and enemy_mana >= 15 and canattack == True: 
                    dmg = round(int(enemy_power)*2.25, 0)
                    if numset == False:
                        number = random.randint(0,100)
                        numset = True
                    if number < int(myself_speed):
                        dmg = 0
                    elif shield == True:
                        dmg = round(int(enemy_power) * (1.125 - (myself_power*0.01)), 0)
                    elif suit > 0 and shield == False:
                        dmg = round(int(enemy_power) * (1.75), 0)
                    elif suit > 0 and shield == True:
                        dmg = round(int(enemy_power) * (0.975 - (myself_power * 0.01)), 0)
                    elif weakness > 0:
                        dmg = round(dmg * 0.1, 0)
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render(("-" if invert == 0 else "+") + str(dmg) if dmg != 0 else "MISSED!", 1, RED if invert == 0 else GREEN), (selfpos.x, selfpos.y - 100))
                        print("Enemy dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("Enemy used: Power Slash", 1, WHITE), (_width_/2, 100))
                        if fire > 0:
                            burn = round(int(myself_magic) * 2, 0)
                            game.blit(comicsans(20).render("-" + str(burn), 1, RED), (enemypos.x, enemypos.y - 100))
                        if dragon > 0:
                            burn = round(int(myself_magic) * 1.5, 0)
                            game.blit(comicsans(20).render("-" + str(burn), 1, RED), (enemypos.x, enemypos.y - 100))
                        if poison > 0:
                            burn = round(int(myself_magic) * 1.5, 0)
                            game.blit(comicsans(20).render("-" + str(burn), 1, RED), (enemypos.x, enemypos.y - 100))
                    if counter == 70:
                        curTurn = "Self"
                        counter = 0
                        myself_health = myself_health - dmg if invert == 0 else myself_health + dmg
                        if myself_health > myself_max_health:
                            myself_health = myself_max_health
                        if myself_health < 0:
                            myself_health = 0
                        enemy_mana = enemy_mana - 15
                        if enemy_mana < 0:
                            enemy_mana = 0
                        if fire > 0:
                            enemy_health = enemy_health - burn
                            if enemy_health < 0:
                                enemy_health = 0
                        if dragon > 0:
                            enemy_health = enemy_health - burn
                            if enemy_health < 0:
                                enemy_health = 0
                        if poison > 0:
                            enemy_health = enemy_health - burn
                            if enemy_health < 0:
                                enemy_health = 0
                        if life > 0:
                            myself_health = myself_health + round(myself_max_health * 0.1, 0)
                            if myself_health > myself_max_health:
                                myself_health = myself_max_health
                        enemyset = False
                        numset = False
                        shieldcooldown-=1
                        shieldcount-=1
                        bscooldown-=1
                        bscount -= 1 
                        dbcooldown -= 1
                        punccooldown -= 1
                        punc -= 1
                        slamdown -= 1
                        suit -= 1
                        suitcooldown -= 1
                        fire -= 1
                        fireballcooldown -= 1
                        freeze -= 1
                        freezecooldown -= 1
                        draincooldown -= 1
                        invert -= 1
                        invertcooldown -= 1
                        leechcooldown -= 1
                        lifecooldown -= 1
                        life -= 1
                        lightningcooldown -= 1
                        lightning -= 1
                        soul -= 1
                        soulcooldown -= 1
                        weakness -= 1
                        weaknesscooldown -= 1
                        amputate -= 1
                        amputatecooldown -= 1
                        dragon -= 1
                        dragoncooldown -= 1
                        overcharge -= 1
                        overchargecooldown -= 1
                        poison -= 1
                        poisoncooldown -= 1
                        shurikencooldown -= 1
                        slashcooldown -= 1
                        speedcooldown -= 1
                        if shieldcooldown < 0:
                            shieldcooldown = 0
                        if shieldcount < 0:
                            shieldcount = 0
                            shield = False
                        if bscooldown < 0:
                            bscooldown = 0
                        if bscount < 0:
                            bscount = 0
                        if dbcooldown < 0:
                            dbcooldown = 0
                        if punccooldown < 0:
                            punccooldown = 0
                        if punc < 0:
                            punc = 0
                        if slamdown < 0:
                            slamdown = 0
                        if suit < 0:
                            suit = 0
                        if suitcooldown < 0:
                            suitcooldown = 0
                        if enrage < 0:
                            enrage = 0
                        if enragecooldown < 0:
                            enragecooldown = 0
                        if enrage == 0:
                            myself_power = myself.retrievestat("strength")
                        if fire < 0:
                            fire = 0
                        if fireballcooldown < 0:
                            fireballcooldown = 0
                        if freeze < 0:
                            freeze = 0
                        if freezecooldown < 0:
                            freezecooldown = 0
                        if draincooldown < 0:
                            draincooldown = 0
                        if invert < 0:
                            invert = 0
                        if invertcooldown < 0:
                            invertcooldown = 0
                        if leechcooldown < 0:
                            leechcooldown = 0
                        if life < 0:
                            life = 0
                        if lifecooldown < 0:
                            lifecooldown = 0
                        if lightningcooldown < 0:
                            lightningcooldown -= 1
                        if lightning == 1:
                            lightning = 0
                        if soul < 0:
                            soul = 0
                        if soulcooldown < 0:
                            soulcooldown = 0
                        if weakness == 0:
                            myself_power = myself.retrievestat("strength")
                            myself_magic = myself.retrievestat("magic")
                        if weakness < 0:
                            weakness = 0
                        if weaknesscooldown < 0:
                            weaknesscooldown = 0
                        if amputate < 0:
                            amputate = 0
                        if amputatecooldown < 0:
                            amputatecooldown = 0
                        if dragon < 0:
                            dragon = 0
                        if dragoncooldown < 0:
                            dragoncooldown = 0
                        if overcharge < 0:
                            overcharge = 0
                        if overcharge == 0:
                            myself_power = myself.retrievestat("strength")
                            myself_magic = myself.retrievestat("magic")
                        if overchargecooldown < 0:
                            overchargecooldown = 0
                        if poison < 0:
                            poison = 0
                        if poisoncooldown < 0:
                            poisoncooldown = 0
                        if shurikencooldown < 0:
                            shurikencooldown = 0
                        if slashcooldown < 0:
                            slashcooldown = 0
                        if speedcooldown == 0:
                            myself_speed = myself.retrievestat("speed")
                        if speedcooldown < 0:
                            speedcooldown = 0

                if freeze == 0:
                    canttack = True
                if stun == 0:
                    canattack = True

            ##battle code for self player

            if curTurn == "Self" and battlebegin == True and myself_health > 0: #design skills via if statements
                if skillused == "Basic_Attack": ## basic attack utilising characters strength
                    dmg = round(int(myself_power)*1.5, 0)
                    if punc > 0:
                        dmg = round(dmg * 1.15, 0)
                    mana_gained = round(int(myself_max_mana)*0.1, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if bscount > 0:
                        if number < round(int(enemy_speed)/1.5, 0):
                            dmg = 0
                    elif soul > 0:
                        if number < round(int(enemy_speed)*0.6, 0):
                            dmg = 0
                    elif amputate > 0:
                        if number < round(int(enemy_speed) * 0.8, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70: ##to add some delay allowing for the game to show the text
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        print("You dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("You used: Basic Attack", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana + mana_gained
                        if myself_mana > myself_max_mana:
                            myself_mana = myself_max_mana

                        #make sure enemy health isnt glitched visually
                        if enemy_health < 0: #if enemy is killed
                            enemy_health = 0
                        skillused = "" # reset the skills
                        numset = False

                if skillused == "Heal" and myself_mana >= 20: #check for mana to be filled
                    heal = round(int(myself_max_health * (0.5 + myself.retrievestat("magic")/100)))
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+" + str(heal), 1, GREEN), (selfpos.x, selfpos.y - 100))
                        print("You healed yourself for: " + str(heal) + " HP!")
                        game.blit(comicsans(20).render("You used: Healing", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        myself_health = myself_health + heal
                        if myself_health > myself_max_health: ##prevent over healing
                            myself_health = myself_max_health
                        myself_mana = myself_mana - 20
                        if myself_mana < 0:
                            myself_mana = 0
                        skillused = ""

                if skillused == "Mana" and myself_mana >= 10:
                    mana = round(int(myself_max_mana * (0.6 + myself.retrievestat("magic")/100)))
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+" + str(mana), 1, LIGHTBLUE), (selfpos.x, selfpos.y - 100))
                        print("You gained " + str(mana) + " MP!")
                        game.blit(comicsans(20).render("You used: Mana", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        myself_mana = myself_mana + mana - 10
                        if myself_mana > myself_max_mana:
                            myself_mana = myself_max_mana
                        skillused = ""
                
                #knight skillset
                if skillused == "Slam" and myself_mana >= 15 and slamdown == 0:
                    dmg = round((int(myself_power) + (int(myself_power)*0.25)) * 1.75, 0)
                    if punc > 0:
                        dmg = round(dmg * 1.15, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if bscount > 0:
                        if number < round(int(enemy_speed)/1.5, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y-100))
                        print("You dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("You used: Slam", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 15
                        if myself_mana < 0:
                            myself_mana = 0
                        
                        if enemy_health < 0:
                            enemy_health = 0
                        slamdown = 3
                        skillused = ""
                        numset = False

                if skillused == "Shield" and myself_mana >= 20 and shieldcooldown == 0:
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+SHIELDED!", 1, LIGHTBLUE), (selfpos.x, selfpos.y - 100))
                        print("You used shield!")
                        game.blit(comicsans(20).render("You used: Shield", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        shield = True
                        shieldcount = 2
                        shieldcooldown = 4
                        print(str(shieldcount) + ", " + str(shieldcooldown) + ", " + str(shield))
                        curTurn = "Enemy"
                        counter = 0
                        myself_mana = myself_mana - 20
                        if myself_mana < 0:
                            myself_mana = 0
                        skillused = ""

                if skillused == "Ballistic_Strike" and myself_mana >= 25 and bscooldown == 0:
                    dmg = round((int(myself_power) * 1.75) + (int(myself_power) * 0.3), 0)
                    if punc > 0:
                        dmg = round(dmg * 1.15, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if bscount > 0:
                        if number < round(int(enemy_speed)/1.5, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y-100))
                        print("You dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("You used: Ballistic Strike!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 25
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        bscooldown = 3
                        if dmg != 0: #to ensure that affects only apply if strikes are hit
                            bscount = 2
                        skillused = ""
                        numset = False

                if skillused == "Double_Strike" and myself_mana >= 20 and dbcooldown == 0:
                    dmg = round((int(myself_power) * 3), 0)
                    if punc > 0:
                        dmg = round(dmg * 1.15, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if bscount > 0:
                        if number < round(int(enemy_speed)/1.5, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y-100))
                        print("You dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("You used: Double Strike!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 20
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        dbcooldown = 5
                        skillused = ""
                        numset = False

                if skillused == "Puncture" and myself_mana >= 35 and punccooldown == 0:
                    dmg = round((int(myself_power) * 3.5), 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if bscount > 0:
                        if number < round(int(enemy_speed)/1.5, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        print("You dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("You used: Puncture", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 35
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        punccooldown = 4
                        if dmg != 0:
                            punc = 3
                        skillused = ""
                        numset = False

                if skillused == "Stun" and myself_mana >= 20 and stuncooldown == 0:
                    dmg = round((int(myself_power) * 1.85), 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if bscount > 0:
                        if number < round(int(enemy_speed)/1.5, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        print("You dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("You used: Stun", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 20
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        stuncooldown = 5
                        if dmg != 0:
                            stun = 1
                        skillused = ""
                        numset = False
                
                if skillused == "Suit_Up" and myself_mana >= 40 and suitcooldown == 0:
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+SUITED!", 1, LIGHTBLUE), (selfpos.x, selfpos.y - 100))
                        print("You used: Suit Up!")
                        game.blit(comicsans(20).render("You used: Suit Up!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        suit = 5
                        suitcooldown = 9
                        curTurn = "Enemy"
                        counter = 0
                        myself_mana = myself_mana - 40
                        if myself_mana < 0:
                            myself_mana = 0
                        
                        skillused = ""
                
                if skillused == "Enrage" and myself_mana >= 50 and enragecooldown == 0:
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+ENRAGED!", 1, LIGHTBLUE), (selfpos.x, selfpos.y - 100))
                        print("You used: Enraged!")
                        game.blit(comicsans(20).render("You used: Enraged!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        enrage = 3
                        enragecooldown = 10
                        myself_power = myself.retrievestat("strength") * 2.5
                        curTurn = "Enemy"
                        counter = 0
                        myself_mana = myself_mana - 50
                        if myself_mana < 0:
                            myself_mana = 0

                        skillused = ""
                if skillused == "Vampire_Strike" and myself_mana >= 45 and vampirecooldown == 0:
                    dmg = round((int(myself_power) * 3.75), 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if bscount > 0:
                        if number < round(int(enemy_speed) / 1.5, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        print("You dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("You used: Vampire Strike!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 45
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        vampirecooldown = 4
                        if dmg != 0:
                            myself_health = myself_health + round((dmg * 0.3), 0)
                            if myself_health > myself_max_health:
                                myself_health = myself_max_health
                        skillused = ""
                        numset = False

                ##wizard skillset
                if skillused == "Fireball" and myself_mana >= 20 and fireballcooldown == 0:
                    dmg = round(int(myself_power) * 1.5, 0)
                    dmg = round(dmg + (int(myself_magic)*1.2), 0)
                    if numset == False:
                        number = random.randint(0,100)
                        numset = True
                    if soul > 0:
                        if number < round(int(enemy_speed)*0.6, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        print("You dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("You used: Fireball!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 20
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        if dmg != 0:
                            fire = 2
                        fireballcooldown = 4
                        skillused = ""
                        numset = False

                if skillused == "Freeze" and myself_mana >= 25 and freezecooldown == 0:
                        dmg = round(int(myself_magic) * 1.25, 0)
                        if numset == False:
                            number = random.randint(0, 100)
                            numset = True
                        if soul > 0:
                            if number < round(int(enemy_speed)*0.6, 0):
                                dmg = 0
                        elif number < int(enemy_speed):
                            dmg = 0
                        if counter != 70:
                            counter += 1
                            game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                            game.blit(comicsans(20).render("You used: Freeze", 1, WHITE), (_width_/2, 100))
                        if counter == 70:
                            curTurn = "Enemy"
                            counter = 0
                            enemy_health = enemy_health - dmg
                            myself_mana = myself_mana - 25
                            if myself_mana < 0:
                                myself_mana = 0
                            if enemy_health < 0:
                                enemy_health = 0
                            if dmg != 0:
                                freeze = 2
                            freezecooldown = 5
                            skillused = ""
                            numset = False

                if skillused == "Drain" and myself_mana >= 15 and draincooldown == 0:
                    drain = round(enemy_mana / 2, 0)
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(drain) + "MP!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Drain", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_mana = enemy_mana - drain
                        if enemy_mana < 0:
                            enemy_mana = 0
                        myself_mana = myself_mana - 15
                        if myself_mana < 0:
                            myself_mana = 0
                        myself_mana = myself_mana + drain
                        if myself_mana > myself_max_mana:
                            myself_mana = myself_max_mana
                        skillused = ""
                        numset = False
                        draincooldown = 4
                
                if skillused == "Invert" and myself_mana >= 35 and invertcooldown == 0:
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("INVERTED!", 1, RED), (enemypos.x, enemypos.y-100))
                        game.blit(comicsans(20).render("You used: Inverted!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        myself_mana = myself_mana - 35
                        if myself_mana < 0:
                            myself_mana = 0
                        skillused = ""
                        numset = False
                        invertcooldown = 6
                        invert = 1

                if skillused == "Leech" and myself_mana >= 45 and leechcooldown == 0:
                    hp = round(enemy_health * 0.2, 0)
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(hp), 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Leech", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - hp
                        myself_mana = myself_mana - 45
                        myself_health = myself_health + hp
                        if myself_health > 0:
                            myself_health = myself_max_health
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        leechcooldown = 5
                        skillused = ""
                        numset = False

                if skillused == "Life" and myself_mana >= 40 and lifecooldown == 0:
                    hp = round(myself_max_health * 0.1, 0)
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+" + str(hp), 1, GREEN), (selfpos.x, selfpos.y - 100))
                        game.blit(comicsans(20).render("You used: Life", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        myself_health = myself_health + hp
                        if myself_health > 0:
                            myself_health = myself_max_health
                        myself_mana = myself_mana - 40
                        if myself_mana < 0:
                            myself_mana = 0
                        lifecooldown = 8
                        life = 5
                        skillused = ""
                        numset = False
                if skillused == "Lightning_Strike" and myself_mana >= 30 and lightningcooldown == 0:
                    dmg = round(int(myself_magic) * 4.5, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if soul > 0:
                        if number < round(int(enemy_speed)*0.6, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Lightning Strike", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 30
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        if dmg != 0:
                            lightning = 1
                        lightningcooldown = 7
                        skillused = ""
                        numset = False
                if skillused == "Soul_Crush" and myself_mana >= 50 and soulcooldown == 0:
                    dmg = round(int(myself_magic) * 5.5, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if soul > 0:
                        if number < round(int(enemy_speed)*0.6, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Soul Crush", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 50
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        if dmg != 0:
                            soul = 4
                        soulcooldown = 10
                        skillused = ""
                        numset = False
                if skillused == "Weakness" and myself_mana >= 60 and weaknesscooldown == 0:
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+WEAKNESS", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Weakness", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        myself_power = myself.retrievestat("strength") * 1.9
                        myself_magic = myself.retrievestat("magic") * 1.9
                        myself_mana = myself_mana - 60
                        if myself_mana < 0:
                            myself_mana = 0
                        weakness = 4
                        weaknesscooldown = 12
                        skillused = ""
                        numset = False
                
                if skillused == "Amputate" and myself_mana >= 20 and amputatecooldown == 0:
                    dmg = round(int(myself_power) * 2, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Amputate!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 20
                        if enemy_health < 0:
                            enemy_health = 0
                        if myself_mana < 0:
                            myself_mana = 0
                        if dmg != 0:
                            amputate = 2
                        amputatecooldown = 4
                        skillused = ""
                        numset = False
                if skillused == "Blindside" and myself_mana >= 25 and blindsidecooldown == 0:
                    dmg = round(int(myself_power) * 1.75, 0)
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg), 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Blindside", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 25
                        if enemy_health < 0:
                            enemy_health = 0
                        if myself_mana < 0:
                            myself_mana = 0
                        blindsidecooldown = 3
                        skillused = ""
                        numset = False
                if skillused == "Dragons_Breath" and myself_mana >= 40 and dragoncooldown == 0:
                    dmg = round(int(myself_power) * 2.25, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if amputate > 0:
                        if number < round(int(enemy_speed) * 0.8, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Dragons Breath", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health -dmg
                        myself_mana = myself_mana - 40
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        if dmg != 0:
                            dragon = 5
                        dragoncooldown = 10
                        skillused = ""
                        numset = False
                if skillused == "Fury_Strike" and myself_mana >= 15 and furycooldown == 0:
                    dmg = round(int(myself_power) * 3, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if amputate > 0:
                        if number < round(int(enemy_speed) * 0.8, 0)*2:
                            dmg = 0
                    elif number < int(enemy_speed)*2:
                        dmg = 0 
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Fury Strike", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 15
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        furycooldown = 4
                        skillused = ""
                        numset = False
                if skillused == "Overcharge" and myself_mana >= 50 and overchargecooldown == 0:
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+OVERCHARGED!", 1, LIGHTBLUE), (selfpos.x, selfpos.y - 100))
                        game.blit(comicsans(20).render("You used: Overcharge", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        myself_mana = myself_mana - 50
                        if myself_mana < 0:
                            myself_mana = 0
                        overchargecooldown = 8
                        overcharge = 3
                        myself_power = myself.retrievestat("strength") * 1.5
                        myself_magic = myself.retrievestat("magic") * 1.5
                        skillused = ""
                        numset = False
                if skillused == "Poison" and myself_mana >= 30 and poisoncooldown == 0:
                    dmg = round(int(myself_magic) * 3, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if amputate > 0:
                        if number < round(int(enemy_speed) * 0.8, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Poison", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 30
                        if enemy_health < 0:
                            enemy_health = 0
                        if myself_mana < 0:
                            myself_mana = 0
                        if dmg != 0:
                            poison = 4
                        poisoncooldown = 7
                        skillused = ""
                        numset = False
                if skillused == "Shuriken" and myself_mana >= 20 and shurikencooldown == 0:
                    dmg = round(int(myself_power) * 2.1, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if amputate > 0:
                        if number < round(int(enemy_speed) * 0.45, 0):
                            dmg = 0
                    elif number < round(int(enemy_speed) * 0.55, 0):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Shuriken", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 20
                        if enemy_health < 0:
                            enemy_health = 0
                        if myself_mana < 0:
                            myself_mana = 0
                        shurikencooldown = 4
                        skillused = ""
                        numset = False
                if skillused == "Slash" and myself_mana >= 30 and slashcooldown == 0:
                    dmg = round(int(myself_power) * 2.5, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if amputate > 0:
                        if number < round(int(enemy_speed) * 0.8, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Slash!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - dmg
                        if enemy_health < 0:
                            enemy_health = 0
                        if myself_mana < 0:
                            myself_mana = 0
                        slashcooldown = 5
                        skillused = ""
                        numset = False
                if skillused == "Speed" and myself_mana >= 50 and speedcooldown == 0:
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+SPEED!", 1, LIGHTBLUE), (selfpos.x, selfpos.y-100))
                        game.blit(comicsans(20).render("You used: Speed!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        myself_mana = myself_mana - 50
                        if myself_mana < 0:
                            myself_mana = 0
                        speedcooldown = 10
                        myself_speed = 100
                        skillused = ""
                        numset = False

                    
                    

            
            if enemy_health <= 0: #winning screen
                blackscreen = pygame.Rect(0,0, _width_, _height_)
                pygame.draw.rect(game, BLACK, blackscreen)
                game.blit(comicsans(20).render("You won!", 1, GREEN), (_width_/2, 100))
                experience_bar = pygame.Rect((_width_/2)-100, 200, 300, 15)
                pygame.draw.rect(game, DARKERGRAY, experience_bar)
                pygame.draw.rect(game, GREEN, pygame.Rect((_width_/2)-100, 200, 300 * xp_slider, 15)) ##xp animation bar
                if xp_slider >= 1.00:
                    game.blit(comicsans(15).render("Levelled Up!", 1, FOCUS), (_width_/2, 150))
                    game.blit(comicsans(15).render("Your Level: " + str(int(data["level:"]) + 1), 1, WHITE), (_width_/2, 175))
                else:
                    game.blit(comicsans(15).render("Your Level: " + str(data["level:"]), 1, WHITE), ((_width_/2)-100, 150))
                    game.blit(comicsans(12).render("EXP: " + str(data["experience:"]) + " / " + str(data["experience_to_next_level:"]), 1, WHITE), ((_width_/2)+125, 150))
                if xp_gained < 101:
                    xp_gained += 1
                    data["experience:"] = str(int(data["experience:"])+1)
                    xp_slider = int(data["experience:"])/int(data["experience_to_next_level:"])
                pygame.draw.rect(game, LIGHTGRAY, gotocampbtn)
                pygame.draw.rect(game, LIGHTGRAY, returnbutton)
                if returnbutton.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(game, WHITE, returnbutton)
                if gotocampbtn.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(game, WHITE, gotocampbtn)
                game.blit(comicsans(20).render("Return to Menu", 1, BLACK), (returnbutton.x, returnbutton.y))
                game.blit(comicsans(20).render("Go To Camp", 1, BLACK), (gotocampbtn.x, gotocampbtn.y))




            if myself_health <= 0: #losing screen
                blackscreen = pygame.Rect(0, 0, _width_, _height_)
                pygame.draw.rect(game, BLACK, blackscreen)
                game.blit(comicsans(20).render("You've lost!", 1, RED), (_width_/2, 100))
                pygame.draw.rect(game, LIGHTGRAY, restartbutton)
                if restartbutton.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(game, WHITE, restartbutton)
                game.blit(comicsans(20).render("Restart Battle", 1, BLACK), (restartbutton.x+10, restartbutton.y))

                pygame.draw.rect(game, LIGHTGRAY, returnbutton)
                if returnbutton.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(game, WHITE, returnbutton)
                game.blit(comicsans(20).render("Return To Menu", 1, BLACK), (returnbutton.x, returnbutton.y))
                game.blit(transform(_skull_icon_, (128,128)), (_width_/2, 200))

        if _cur_screen_ == "Level 2":
            game.blit(transform(_zone1_bg_, (_width_, _height_)), (0,-100))
            ##create characters##
            if battlebegin == False:
                myself = YourChar(data["chartype:"], int(data["vitality:"]), int(data["strength:"]), int(data["magic:"]), int(data["speed:"]), int(data["level:"]), int(data["skillpoints:"]), int(data["attributepoints:"]), int(data["experience:"]), int(data["experience_to_next_level:"]))
                myself_max_health = 100 + (myself.retrievestat("hp") * myself.retrievestat("strength"))
                myself_health = myself_max_health
                myself_max_mana = 50 + (myself.retrievestat("magic") * 2)
                myself_mana = myself_max_mana
                myself_power = myself.retrievestat("strength")
                myself_speed = myself.retrievestat("speed")
                myself_magic = myself.retrievestat("magic")
            ##add bottom part##
            footer = pygame.Rect(0, _height_-150, _width_, 150)
            pygame.draw.rect(game, DARKERGRAY, footer)
            _final_icon_ = _char_icon_knight_ if data["chartype:"] == "Knight" else _char_icon_wizard_ if data["chartype:"] == "Wizard" else _char_icon_assassin_
            _final_char_ = _char_knight_ if data["chartype:"] == "Knight" else _char_wizard_ if data["chartype:"] == "Wizard" else _char_assassin_
            heightvar = 320 if data["chartype:"] == "Knight" else 320 if data["chartype:"] == "Wizard" else 320
            selffix = pygame.Rect(50, _height_-100, 64, 64)
            game.blit(transform(_final_icon_, (64,64)), (50, _height_-100))

            if selffix.collidepoint(pygame.mouse.get_pos()): #hover over icon to see your own stats
                square = pygame.Rect(0, _height_-200, 100, 100)
                pygame.draw.rect(game, LIGHTGRAY, square)
                yourvitals = comicsans(9).render("Vitality: " + str(data["vitality:"]), 1, BLACK)
                yourstrength = comicsans(9).render("Strength: " + str(data["strength:"]), 1, BLACK)
                yourmagic = comicsans(9).render("Magic: " + str(data["magic:"]), 1, BLACK)
                yourspeed = comicsans(9).render("Speed: " + str(data["speed:"]), 1, BLACK)
                yourstats = comicsans(10).render("Your Stats: ", 1, BLACK)
                game.blit(yourstats, (square.x, square.y))
                game.blit(yourvitals, (square.x, square.y + 20))
                game.blit(yourstrength, (square.x, square.y + 30))
                game.blit(yourmagic, (square.x, square.y + 40))
                game.blit(yourspeed, (square.x, square.y + 50))
            selfpos = pygame.Rect(100, heightvar, 128, 128)
            game.blit(transform(_final_char_, (128,128)), (selfpos.x, selfpos.y))
            healthbarunder = pygame.Rect(120, _height_-85, 100, 10)
            pygame.draw.rect(game, DARKGREEN, healthbarunder)
            healthbarover = pygame.Rect(120, _height_-85, round(100 * (myself_health/myself_max_health), 0), 10)
            pygame.draw.rect(game, GREEN, healthbarover)
            displayhealth = comicsans(10).render("HP: " + str(myself_health), 1, WHITE)
            game.blit(displayhealth, (120,_height_-100))

            manabarunder = pygame.Rect(120, _height_-60, 100, 10)
            pygame.draw.rect(game, DARKERBLUE, manabarunder)
            manabarover = pygame.Rect(120, _height_-60, round(100 * (myself_mana/myself_max_mana), 0), 10)
            pygame.draw.rect(game, LIGHTBLUE, manabarover)
            displaymana = comicsans(10).render("MP: " + str(myself_mana), 1, WHITE)
            game.blit(displaymana, (120, _height_-75))

            ##add skills section##
            pygame.draw.rect(game, DARKGRAY, skill1)
            pygame.draw.rect(game, DARKGRAY, skill2)
            pygame.draw.rect(game, DARKGRAY, skill3)
            pygame.draw.rect(game, DARKGRAY, skill4)
            pygame.draw.rect(game, DARKGRAY, skill5)
            pygame.draw.rect(game, DARKGRAY, skill6)
            pygame.draw.rect(game, DARKGRAY, skill7)
            pygame.draw.rect(game, DARKGRAY, skill8)
            pygame.draw.rect(game, DARKGRAY, skill9)
            pygame.draw.rect(game, DARKGRAY, skill10)
            #add hover effect to skills to show user that they are currently selecting that skill
            if skill1.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill1)
            if skill2.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill2)
            if skill3.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill3)
            if skill4.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill4)
            if skill5.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill5)
            if skill6.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill6)
            if skill7.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill7)
            if skill8.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill8)
            if skill9.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill9)
            if skill10.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill10)
            #add skill images where applicable
            game.blit(transform(skill1_img, (32,32)), (skill1.x, skill1.y))
            game.blit(transform(skill2_img, (32,32)), (skill2.x, skill2.y))
            game.blit(transform(skill3_img, (32,32)), (skill3.x, skill3.y))
            game.blit(transform(skill4_img, (32,32)), (skill4.x, skill4.y))
            game.blit(transform(skill5_img, (32,32)), (skill5.x, skill5.y))
            game.blit(transform(skill6_img, (32,32)), (skill6.x, skill6.y))
            game.blit(transform(skill7_img, (32,32)), (skill7.x, skill7.y))
            game.blit(transform(skill8_img, (32,32)), (skill8.x, skill8.y))
            game.blit(transform(skill9_img, (32,32)), (skill9.x, skill9.y))
            game.blit(transform(skill10_img, (32,32)), (skill10.x, skill10.y))
            

            ##draw enemy
            enemy = Enemy("Remiro", _l2_icon_, _l2_enemy_, 7, 12, 5, 15, ["Basic Attack", "Power Slash"])
            tutfix = pygame.Rect(_width_-110, _height_-100, 64, 64)
            game.blit(transform(_l2_icon_, (64,64)), (_width_-110, _height_-100))
            enemypos = pygame.Rect(_width_-200, 320, 128, 128)
            game.blit(transform(_l2_enemy_, (128,128)), (enemypos.x, enemypos.y))
            if battlebegin == False:
                enemy_max_health = 300 + (enemy.get("hp") * enemy.get("strength"))
                enemy_health = enemy_max_health
                enemy_max_mana = 60 + (enemy.get("magic") * 2)
                enemy_mana = enemy_max_mana
                enemy_power = enemy.get("strength")
                enemy_speed = enemy.get("speed")
                battlebegin = True #set true once both players have initialised stats
            enemyhealthbarunder = pygame.Rect(_width_-220, _height_-85, 100, 10)
            enemyhealthbarover = pygame.Rect(_width_-220, _height_-85, round(100 * (enemy_health/enemy_max_health), 0), 10)
            displayenemyhealth = comicsans(10).render("HP: " + str(enemy_health), 1, WHITE)
            pygame.draw.rect(game, DARKGREEN, enemyhealthbarunder)
            pygame.draw.rect(game, GREEN, enemyhealthbarover)
            game.blit(displayenemyhealth, (_width_-170, _height_-100))
            enemymanabarunder = pygame.Rect(_width_-220, _height_-60, 100, 10)
            enemymanabarover = pygame.Rect(_width_-220, _height_-60, round(100 * (enemy_mana/enemy_max_mana), 0), 10)
            displayenemymana = comicsans(10).render("MP: " + str(enemy_mana), 1, WHITE)
            pygame.draw.rect(game, DARKERBLUE, enemymanabarunder)
            pygame.draw.rect(game, LIGHTBLUE, enemymanabarover)
            game.blit(displayenemymana, (_width_-170, _height_-75))
            if tutfix.collidepoint(pygame.mouse.get_pos()):
                square2 = pygame.Rect(_width_-100, _height_-200, 100, 100)
                pygame.draw.rect(game, LIGHTGRAY, square2)
                enemyvitals = comicsans(9).render("Vitality: " + str(enemy.get("hp")), 1, BLACK)
                enemystrength = comicsans(9).render("Strength: " + str(enemy.get("strength")), 1, BLACK)
                enemymagic = comicsans(9).render("Magic: " + str(enemy.get("magic")), 1, BLACK)
                enemyspeed = comicsans(9).render("Speed: " + str(enemy.get("speed")), 1, BLACK)
                enemystats = comicsans(9).render("Enemy Stats: ", 1, BLACK)
                game.blit(enemystats, (square2.x, square2.y))
                game.blit(enemyvitals, (square2.x, square2.y + 20))
                game.blit(enemystrength, (square2.x, square2.y + 30))
                game.blit(enemymagic, (square2.x, square2.y + 40))
                game.blit(enemyspeed, (square2.x, square2.y + 50))

            ##draw area to exit##
            pygame.draw.rect(game, LIGHTGRAY, exiticon)
            pygame.draw.circle(game, (200,0,0), (exiticon.x + 32, exiticon.y + 32), 32)
            game.blit(comicsans(40).render("X", 1, WHITE), (exiticon.x + 18, exiticon.y + 1))
            if exiticon.collidepoint(pygame.mouse.get_pos()): #hover effect
                pygame.draw.rect(game, WHITE, exiticon)
                pygame.draw.circle(game, (150,0,0), (exiticon.x + 32, exiticon.y + 32), 32)
                game.blit(comicsans(40).render("X", 1, WHITE), (exiticon.x + 18, exiticon.y + 1))    
            ##draw text to identify current turn##
            turn = comicsans(20).render("Your Turn!" if curTurn == "Self" else "Enemy Turn!", 1, WHITE)
            game.blit(turn, (exiticon.x-20, exiticon.y-30)) 

            ## battle code for the enemy

            if curTurn == "Enemy" and battlebegin == True and enemy_health > 0:
                if stun > 0:
                    canattack = False
                    stun -= 1
                    if stun < 0:
                        stun = 0
                    curTurn = "Self"
                    enemyset = False
                    numset = False
                    skillused = ""

                if freeze > 0:
                    canattack = False
                    freeze -= 1
                    if freeze < 0:
                        freeze = 0
                    curTurn = "Self"
                    enemyset = False
                    numset = False
                    skillused = ""

                if lightning > 0:
                    canttack = False
                    lightning -= 1
                    if lightning < 0:
                        lightning = 0
                    curTurn = "Self"
                    enemyset = False
                    numset = False
                    skillused = ""


                if enemyset == False:
                    enemy_skills = enemy.get("abilities")
                    ranvalue = random.randint(0, len(enemy_skills)-1) #roll a random move for basic tier enemies so its automatic
                    ##check if enough mana
                    if enemy_skills[ranvalue] == "Basic Attack":
                        enemyset = True
                    if enemy_skills[ranvalue] == "Power Slash" and enemy_mana >= 15:
                        enemyset = True
                    
                if enemy_skills[ranvalue] == "Basic Attack" and canattack == True:
                    dmg = round(int(enemy_power)*1.5, 0)
                    ##chance to miss target based on target speed##
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if number < int(myself_speed): #if roll is less than target speed, means you are slower.
                        dmg = 0
                    elif shield == True:
                        dmg = round(int(enemy_power)*(0.75 - (myself_power*0.01)), 0)
                    elif suit > 0 and shield == False:
                        dmg = round(int(enemy_power)*(1.15),0)
                    elif suit > 0 and shield == True:
                        dmg = round(int(enemy_power) * ( 0.65 - (myself_power * 0.01)), 0)
                    elif weakness > 0:
                        dmg = round(dmg*0.1, 0)
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render(("-" if invert == 0 else "+") + str(dmg) if dmg != 0 else "MISSED!", 1, RED if invert == 0 else GREEN), (selfpos.x, selfpos.y - 100))
                        print("Enemy dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("Enemy used: Basic Attack", 1, WHITE), (_width_/2, 100))

                        if fire > 0:
                            burn = round(int(myself_magic) * 2, 0)
                            game.blit(comicsans(20).render("-" + str(burn), 1, RED), (enemypos.x, enemypos.y - 100))
                        if dragon > 0:
                            burn = round(int(myself_magic) * 1.5, 0)
                            game.blit(comicsans(20).render("-" + str(burn), 1, RED), (enemypos.x, enemypos.y - 100))
                        if poison > 0:
                            burn = round(int(myself_magic) * 1.5, 0)
                            game.blit(comicsans(20).render("-" + str(burn), 1, RED), (enemypos.x, enemypos.y - 100))
                    if counter == 70:
                        curTurn = "Self"
                        counter = 0
                        myself_health = myself_health - dmg if invert == 0 else myself_health + dmg
                        if myself_health < 0:
                            myself_health = 0
                        if myself_health > myself_max_health:
                            myself_health = myself_max_health
                            
                        enemy_mana = enemy_mana + round(enemy_max_mana*0.1,0)
                        if enemy_mana > enemy_max_mana:
                            enemy_mana = enemy_max_mana
                        if fire > 0:
                            enemy_health = enemy_health - burn
                            if enemy_health < 0:
                                enemy_health = 0
                        if dragon > 0:
                            enemy_health = enemy_health - burn
                            if enemy_health < 0:
                                enemy_health = 0
                        if poison > 0:
                            enemy_health = enemy_health - burn
                            if enemy_health < 0:
                                enemy_health = 0
                        if life > 0:
                            myself_health = myself_health + round(myself_max_health * 0.1, 0)
                            if myself_health > myself_max_health:
                                myself_health = myself_max_health
                        enemyset = False
                        numset = False
                        shieldcooldown-=1
                        shieldcount-=1
                        bscooldown -= 1
                        bscount -= 1
                        dbcooldown -= 1
                        punccooldown -= 1
                        punc -= 1
                        slamdown -= 1
                        suit -= 1
                        suitcooldown -= 1 
                        enrage -= 1
                        enragecooldown -= 1
                        fire -= 1
                        fireballcooldown -= 1
                        freeze -= 1
                        freezecooldown -= 1
                        draincooldown -= 1
                        invert -= 1
                        invertcooldown -= 1
                        leechcooldown -= 1
                        life -= 1
                        lifecooldown -= 1
                        lightningcooldown -= 1
                        lightning -= 1
                        soul -= 1
                        soulcooldown -= 1
                        weakness -= 1
                        weaknesscooldown -= 1
                        amputate -= 1
                        amputatecooldown -= 1
                        dragon -= 1
                        dragoncooldown -= 1
                        overcharge -= 1
                        overchargecooldown -= 1
                        poison -= 1
                        poisoncooldown -= 1
                        shurikencooldown -= 1
                        slashcooldown -= 1
                        speedcooldown -= 1
                        if shieldcooldown < 0:
                            shieldcooldown = 0
                        if shieldcount < 0:
                            shieldcount = 0
                            shield = False
                        if bscooldown < 0:
                            bscooldown = 0
                        if bscount < 0:
                            bscount = 0
                        if dbcooldown < 0:
                            dbcooldown = 0
                        if punccooldown < 0:
                            punccooldown = 0
                        if punc < 0:
                            punc = 0
                        if slamdown < 0:
                            slamdown = 0
                        if suit < 0:
                            suit = 0
                        if suitcooldown < 0:
                            suitcooldown = 0
                        if enrage < 0:
                            enrage = 0
                        if enragecooldown < 0:
                            enragecooldown = 0
                        if enrage == 0:
                            myself_power = myself.retrievestat("strength")
                        if fire == 0:
                            fire = 0
                        if fireballcooldown == 0:
                            fireballcooldown = 0
                        if freeze < 0:
                            freeze = 0
                        if freezecooldown < 0:
                            freezecooldown = 0
                        if draincooldown < 0:
                            draincooldown = 0
                        if invert < 0:
                            invert = 0
                        if invertcooldown < 0:
                            invertcooldown = 0
                        if leechcooldown < 0:
                            leechcooldown = 0
                        if life < 0:
                            life = 0
                        if lifecooldown < 0:
                            lifecooldown = 0
                        if lightningcooldown == 0:
                            lightningcooldown = 0
                        if lightning == 0:
                            lightning = 0
                        if soul < 0:
                            soul = 0
                        if soulcooldown < 0:
                            soulcooldown = 0
                        if weakness < 0:
                            weakness = 0
                        if weakness == 0:
                            myself_power = myself.retrievestat("strength")
                            myself_magic = myself.retrievestat("magic")
                        if weaknesscooldown < 0:
                            weaknesscooldown = 0
                        if amputate < 0:
                            amputate = 0
                        if amputatecooldown < 0:
                            amputatecooldown = 0
                        if dragon < 0:
                            dragon = 0
                        if dragoncooldown < 0:
                            dragoncooldown = 0
                        if overcharge < 0:
                            overcharge = 0
                        if overcharge == 0:
                            myself_power = myself.retrievestat("strength")
                            myself_magic = myself.retrievestat("magic")
                        if overchargecooldown < 0:
                            overchargecooldown = 0
                        if poison < 0:
                            poison = 0
                        if poisoncooldown < 0:
                            poisoncooldown = 0
                        if shurikencooldown < 0:
                            shurikencooldown = 0
                        if slashcooldown < 0:
                            slashcooldown = 0
                        if speedcooldown < 0:
                            speedcooldown = 0
                        if speedcooldown == 0:
                            myself_speed = myself.retrievestat("speed")
                
                if enemy_skills[ranvalue] == "Power Slash" and enemy_mana >= 15 and canattack == True: 
                    dmg = round(int(enemy_power)*2.25, 0)
                    if numset == False:
                        number = random.randint(0,100)
                        numset = True
                    if number < int(myself_speed):
                        dmg = 0
                    elif shield == True:
                        dmg = round(int(enemy_power) * (1.125 - (myself_power*0.01)), 0)
                    elif suit > 0 and shield == False:
                        dmg = round(int(enemy_power) * (1.75), 0)
                    elif suit > 0 and shield == True:
                        dmg = round(int(enemy_power) * (0.975 - (myself_power * 0.01)), 0)
                    elif weakness > 0:
                        dmg = round(dmg * 0.1, 0)
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render(("-" if invert == 0 else "+") + str(dmg) if dmg != 0 else "MISSED!", 1, RED if invert == 0 else GREEN), (selfpos.x, selfpos.y - 100))
                        print("Enemy dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("Enemy used: Power Slash", 1, WHITE), (_width_/2, 100))
                        if fire > 0:
                            burn = round(int(myself_magic) * 2, 0)
                            game.blit(comicsans(20).render("-" + str(burn), 1, RED), (enemypos.x, enemypos.y - 100))
                        if dragon > 0:
                            burn = round(int(myself_magic) * 1.5, 0)
                            game.blit(comicsans(20).render("-" + str(burn), 1, RED), (enemypos.x, enemypos.y - 100))
                        if poison > 0:
                            burn = round(int(myself_magic) * 1.5, 0)
                            game.blit(comicsans(20).render("-" + str(burn), 1, RED), (enemypos.x, enemypos.y - 100))
                    if counter == 70:
                        curTurn = "Self"
                        counter = 0
                        myself_health = myself_health - dmg if invert == 0 else myself_health + dmg
                        if myself_health > myself_max_health:
                            myself_health = myself_max_health
                        if myself_health < 0:
                            myself_health = 0
                        enemy_mana = enemy_mana - 15
                        if enemy_mana < 0:
                            enemy_mana = 0
                        if fire > 0:
                            enemy_health = enemy_health - burn
                            if enemy_health < 0:
                                enemy_health = 0
                        if dragon > 0:
                            enemy_health = enemy_health - burn
                            if enemy_health < 0:
                                enemy_health = 0
                        if poison > 0:
                            enemy_health = enemy_health - burn
                            if enemy_health < 0:
                                enemy_health = 0
                        if life > 0:
                            myself_health = myself_health + round(myself_max_health * 0.1, 0)
                            if myself_health > myself_max_health:
                                myself_health = myself_max_health
                        enemyset = False
                        numset = False
                        shieldcooldown-=1
                        shieldcount-=1
                        bscooldown-=1
                        bscount -= 1 
                        dbcooldown -= 1
                        punccooldown -= 1
                        punc -= 1
                        slamdown -= 1
                        suit -= 1
                        suitcooldown -= 1
                        fire -= 1
                        fireballcooldown -= 1
                        freeze -= 1
                        freezecooldown -= 1
                        draincooldown -= 1
                        invert -= 1
                        invertcooldown -= 1
                        leechcooldown -= 1
                        lifecooldown -= 1
                        life -= 1
                        lightningcooldown -= 1
                        lightning -= 1
                        soul -= 1
                        soulcooldown -= 1
                        weakness -= 1
                        weaknesscooldown -= 1
                        amputate -= 1
                        amputatecooldown -= 1
                        dragon -= 1
                        dragoncooldown -= 1
                        overcharge -= 1
                        overchargecooldown -= 1
                        poison -= 1
                        poisoncooldown -= 1
                        shurikencooldown -= 1
                        slashcooldown -= 1
                        speedcooldown -= 1
                        if shieldcooldown < 0:
                            shieldcooldown = 0
                        if shieldcount < 0:
                            shieldcount = 0
                            shield = False
                        if bscooldown < 0:
                            bscooldown = 0
                        if bscount < 0:
                            bscount = 0
                        if dbcooldown < 0:
                            dbcooldown = 0
                        if punccooldown < 0:
                            punccooldown = 0
                        if punc < 0:
                            punc = 0
                        if slamdown < 0:
                            slamdown = 0
                        if suit < 0:
                            suit = 0
                        if suitcooldown < 0:
                            suitcooldown = 0
                        if enrage < 0:
                            enrage = 0
                        if enragecooldown < 0:
                            enragecooldown = 0
                        if enrage == 0:
                            myself_power = myself.retrievestat("strength")
                        if fire < 0:
                            fire = 0
                        if fireballcooldown < 0:
                            fireballcooldown = 0
                        if freeze < 0:
                            freeze = 0
                        if freezecooldown < 0:
                            freezecooldown = 0
                        if draincooldown < 0:
                            draincooldown = 0
                        if invert < 0:
                            invert = 0
                        if invertcooldown < 0:
                            invertcooldown = 0
                        if leechcooldown < 0:
                            leechcooldown = 0
                        if life < 0:
                            life = 0
                        if lifecooldown < 0:
                            lifecooldown = 0
                        if lightningcooldown < 0:
                            lightningcooldown -= 1
                        if lightning == 1:
                            lightning = 0
                        if soul < 0:
                            soul = 0
                        if soulcooldown < 0:
                            soulcooldown = 0
                        if weakness == 0:
                            myself_power = myself.retrievestat("strength")
                            myself_magic = myself.retrievestat("magic")
                        if weakness < 0:
                            weakness = 0
                        if weaknesscooldown < 0:
                            weaknesscooldown = 0
                        if amputate < 0:
                            amputate = 0
                        if amputatecooldown < 0:
                            amputatecooldown = 0
                        if dragon < 0:
                            dragon = 0
                        if dragoncooldown < 0:
                            dragoncooldown = 0
                        if overcharge < 0:
                            overcharge = 0
                        if overcharge == 0:
                            myself_power = myself.retrievestat("strength")
                            myself_magic = myself.retrievestat("magic")
                        if overchargecooldown < 0:
                            overchargecooldown = 0
                        if poison < 0:
                            poison = 0
                        if poisoncooldown < 0:
                            poisoncooldown = 0
                        if shurikencooldown < 0:
                            shurikencooldown = 0
                        if slashcooldown < 0:
                            slashcooldown = 0
                        if speedcooldown == 0:
                            myself_speed = myself.retrievestat("speed")
                        if speedcooldown < 0:
                            speedcooldown = 0

                if freeze == 0:
                    canttack = True
                if stun == 0:
                    canattack = True

            ##battle code for self player

            if curTurn == "Self" and battlebegin == True and myself_health > 0: #design skills via if statements
                if skillused == "Basic_Attack": ## basic attack utilising characters strength
                    dmg = round(int(myself_power)*1.5, 0)
                    if punc > 0:
                        dmg = round(dmg * 1.15, 0)
                    mana_gained = round(int(myself_max_mana)*0.1, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if bscount > 0:
                        if number < round(int(enemy_speed)/1.5, 0):
                            dmg = 0
                    elif soul > 0:
                        if number < round(int(enemy_speed)*0.6, 0):
                            dmg = 0
                    elif amputate > 0:
                        if number < round(int(enemy_speed) * 0.8, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70: ##to add some delay allowing for the game to show the text
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        print("You dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("You used: Basic Attack", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana + mana_gained
                        if myself_mana > myself_max_mana:
                            myself_mana = myself_max_mana

                        #make sure enemy health isnt glitched visually
                        if enemy_health < 0: #if enemy is killed
                            enemy_health = 0
                        skillused = "" # reset the skills
                        numset = False

                if skillused == "Heal" and myself_mana >= 20: #check for mana to be filled
                    heal = round(int(myself_max_health * (0.5 + myself.retrievestat("magic")/100)))
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+" + str(heal), 1, GREEN), (selfpos.x, selfpos.y - 100))
                        print("You healed yourself for: " + str(heal) + " HP!")
                        game.blit(comicsans(20).render("You used: Healing", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        myself_health = myself_health + heal
                        if myself_health > myself_max_health: ##prevent over healing
                            myself_health = myself_max_health
                        myself_mana = myself_mana - 20
                        if myself_mana < 0:
                            myself_mana = 0
                        skillused = ""

                if skillused == "Mana" and myself_mana >= 10:
                    mana = round(int(myself_max_mana * (0.6 + myself.retrievestat("magic")/100)))
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+" + str(mana), 1, LIGHTBLUE), (selfpos.x, selfpos.y - 100))
                        print("You gained " + str(mana) + " MP!")
                        game.blit(comicsans(20).render("You used: Mana", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        myself_mana = myself_mana + mana - 10
                        if myself_mana > myself_max_mana:
                            myself_mana = myself_max_mana
                        skillused = ""
                
                #knight skillset
                if skillused == "Slam" and myself_mana >= 15 and slamdown == 0:
                    dmg = round((int(myself_power) + (int(myself_power)*0.25)) * 1.75, 0)
                    if punc > 0:
                        dmg = round(dmg * 1.15, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if bscount > 0:
                        if number < round(int(enemy_speed)/1.5, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y-100))
                        print("You dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("You used: Slam", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 15
                        if myself_mana < 0:
                            myself_mana = 0
                        
                        if enemy_health < 0:
                            enemy_health = 0
                        slamdown = 3
                        skillused = ""
                        numset = False

                if skillused == "Shield" and myself_mana >= 20 and shieldcooldown == 0:
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+SHIELDED!", 1, LIGHTBLUE), (selfpos.x, selfpos.y - 100))
                        print("You used shield!")
                        game.blit(comicsans(20).render("You used: Shield", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        shield = True
                        shieldcount = 2
                        shieldcooldown = 4
                        print(str(shieldcount) + ", " + str(shieldcooldown) + ", " + str(shield))
                        curTurn = "Enemy"
                        counter = 0
                        myself_mana = myself_mana - 20
                        if myself_mana < 0:
                            myself_mana = 0
                        skillused = ""

                if skillused == "Ballistic_Strike" and myself_mana >= 25 and bscooldown == 0:
                    dmg = round((int(myself_power) * 1.75) + (int(myself_power) * 0.3), 0)
                    if punc > 0:
                        dmg = round(dmg * 1.15, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if bscount > 0:
                        if number < round(int(enemy_speed)/1.5, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y-100))
                        print("You dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("You used: Ballistic Strike!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 25
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        bscooldown = 3
                        if dmg != 0: #to ensure that affects only apply if strikes are hit
                            bscount = 2
                        skillused = ""
                        numset = False

                if skillused == "Double_Strike" and myself_mana >= 20 and dbcooldown == 0:
                    dmg = round((int(myself_power) * 3), 0)
                    if punc > 0:
                        dmg = round(dmg * 1.15, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if bscount > 0:
                        if number < round(int(enemy_speed)/1.5, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y-100))
                        print("You dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("You used: Double Strike!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 20
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        dbcooldown = 5
                        skillused = ""
                        numset = False

                if skillused == "Puncture" and myself_mana >= 35 and punccooldown == 0:
                    dmg = round((int(myself_power) * 3.5), 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if bscount > 0:
                        if number < round(int(enemy_speed)/1.5, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        print("You dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("You used: Puncture", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 35
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        punccooldown = 4
                        if dmg != 0:
                            punc = 3
                        skillused = ""
                        numset = False

                if skillused == "Stun" and myself_mana >= 20 and stuncooldown == 0:
                    dmg = round((int(myself_power) * 1.85), 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if bscount > 0:
                        if number < round(int(enemy_speed)/1.5, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        print("You dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("You used: Stun", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 20
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        stuncooldown = 5
                        if dmg != 0:
                            stun = 1
                        skillused = ""
                        numset = False
                
                if skillused == "Suit_Up" and myself_mana >= 40 and suitcooldown == 0:
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+SUITED!", 1, LIGHTBLUE), (selfpos.x, selfpos.y - 100))
                        print("You used: Suit Up!")
                        game.blit(comicsans(20).render("You used: Suit Up!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        suit = 5
                        suitcooldown = 9
                        curTurn = "Enemy"
                        counter = 0
                        myself_mana = myself_mana - 40
                        if myself_mana < 0:
                            myself_mana = 0
                        
                        skillused = ""
                
                if skillused == "Enrage" and myself_mana >= 50 and enragecooldown == 0:
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+ENRAGED!", 1, LIGHTBLUE), (selfpos.x, selfpos.y - 100))
                        print("You used: Enraged!")
                        game.blit(comicsans(20).render("You used: Enraged!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        enrage = 3
                        enragecooldown = 10
                        myself_power = myself.retrievestat("strength") * 2.5
                        curTurn = "Enemy"
                        counter = 0
                        myself_mana = myself_mana - 50
                        if myself_mana < 0:
                            myself_mana = 0

                        skillused = ""
                if skillused == "Vampire_Strike" and myself_mana >= 45 and vampirecooldown == 0:
                    dmg = round((int(myself_power) * 3.75), 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if bscount > 0:
                        if number < round(int(enemy_speed) / 1.5, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        print("You dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("You used: Vampire Strike!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 45
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        vampirecooldown = 4
                        if dmg != 0:
                            myself_health = myself_health + round((dmg * 0.3), 0)
                            if myself_health > myself_max_health:
                                myself_health = myself_max_health
                        skillused = ""
                        numset = False

                ##wizard skillset
                if skillused == "Fireball" and myself_mana >= 20 and fireballcooldown == 0:
                    dmg = round(int(myself_power) * 1.5, 0)
                    dmg = round(dmg + (int(myself_magic)*1.2), 0)
                    if numset == False:
                        number = random.randint(0,100)
                        numset = True
                    if soul > 0:
                        if number < round(int(enemy_speed)*0.6, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        print("You dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("You used: Fireball!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 20
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        if dmg != 0:
                            fire = 2
                        fireballcooldown = 4
                        skillused = ""
                        numset = False

                if skillused == "Freeze" and myself_mana >= 25 and freezecooldown == 0:
                        dmg = round(int(myself_magic) * 1.25, 0)
                        if numset == False:
                            number = random.randint(0, 100)
                            numset = True
                        if soul > 0:
                            if number < round(int(enemy_speed)*0.6, 0):
                                dmg = 0
                        elif number < int(enemy_speed):
                            dmg = 0
                        if counter != 70:
                            counter += 1
                            game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                            game.blit(comicsans(20).render("You used: Freeze", 1, WHITE), (_width_/2, 100))
                        if counter == 70:
                            curTurn = "Enemy"
                            counter = 0
                            enemy_health = enemy_health - dmg
                            myself_mana = myself_mana - 25
                            if myself_mana < 0:
                                myself_mana = 0
                            if enemy_health < 0:
                                enemy_health = 0
                            if dmg != 0:
                                freeze = 2
                            freezecooldown = 5
                            skillused = ""
                            numset = False

                if skillused == "Drain" and myself_mana >= 15 and draincooldown == 0:
                    drain = round(enemy_mana / 2, 0)
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(drain) + "MP!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Drain", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_mana = enemy_mana - drain
                        if enemy_mana < 0:
                            enemy_mana = 0
                        myself_mana = myself_mana - 15
                        if myself_mana < 0:
                            myself_mana = 0
                        myself_mana = myself_mana + drain
                        if myself_mana > myself_max_mana:
                            myself_mana = myself_max_mana
                        skillused = ""
                        numset = False
                        draincooldown = 4
                
                if skillused == "Invert" and myself_mana >= 35 and invertcooldown == 0:
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("INVERTED!", 1, RED), (enemypos.x, enemypos.y-100))
                        game.blit(comicsans(20).render("You used: Inverted!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        myself_mana = myself_mana - 35
                        if myself_mana < 0:
                            myself_mana = 0
                        skillused = ""
                        numset = False
                        invertcooldown = 6
                        invert = 1

                if skillused == "Leech" and myself_mana >= 45 and leechcooldown == 0:
                    hp = round(enemy_health * 0.2, 0)
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(hp), 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Leech", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - hp
                        myself_mana = myself_mana - 45
                        myself_health = myself_health + hp
                        if myself_health > 0:
                            myself_health = myself_max_health
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        leechcooldown = 5
                        skillused = ""
                        numset = False

                if skillused == "Life" and myself_mana >= 40 and lifecooldown == 0:
                    hp = round(myself_max_health * 0.1, 0)
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+" + str(hp), 1, GREEN), (selfpos.x, selfpos.y - 100))
                        game.blit(comicsans(20).render("You used: Life", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        myself_health = myself_health + hp
                        if myself_health > 0:
                            myself_health = myself_max_health
                        myself_mana = myself_mana - 40
                        if myself_mana < 0:
                            myself_mana = 0
                        lifecooldown = 8
                        life = 5
                        skillused = ""
                        numset = False
                if skillused == "Lightning_Strike" and myself_mana >= 30 and lightningcooldown == 0:
                    dmg = round(int(myself_magic) * 4.5, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if soul > 0:
                        if number < round(int(enemy_speed)*0.6, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Lightning Strike", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 30
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        if dmg != 0:
                            lightning = 1
                        lightningcooldown = 7
                        skillused = ""
                        numset = False
                if skillused == "Soul_Crush" and myself_mana >= 50 and soulcooldown == 0:
                    dmg = round(int(myself_magic) * 5.5, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if soul > 0:
                        if number < round(int(enemy_speed)*0.6, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Soul Crush", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 50
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        if dmg != 0:
                            soul = 4
                        soulcooldown = 10
                        skillused = ""
                        numset = False
                if skillused == "Weakness" and myself_mana >= 60 and weaknesscooldown == 0:
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+WEAKNESS", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Weakness", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        myself_power = myself.retrievestat("strength") * 1.9
                        myself_magic = myself.retrievestat("magic") * 1.9
                        myself_mana = myself_mana - 60
                        if myself_mana < 0:
                            myself_mana = 0
                        weakness = 4
                        weaknesscooldown = 12
                        skillused = ""
                        numset = False
                
                if skillused == "Amputate" and myself_mana >= 20 and amputatecooldown == 0:
                    dmg = round(int(myself_power) * 2, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Amputate!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 20
                        if enemy_health < 0:
                            enemy_health = 0
                        if myself_mana < 0:
                            myself_mana = 0
                        if dmg != 0:
                            amputate = 2
                        amputatecooldown = 4
                        skillused = ""
                        numset = False
                if skillused == "Blindside" and myself_mana >= 25 and blindsidecooldown == 0:
                    dmg = round(int(myself_power) * 1.75, 0)
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg), 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Blindside", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 25
                        if enemy_health < 0:
                            enemy_health = 0
                        if myself_mana < 0:
                            myself_mana = 0
                        blindsidecooldown = 3
                        skillused = ""
                        numset = False
                if skillused == "Dragons_Breath" and myself_mana >= 40 and dragoncooldown == 0:
                    dmg = round(int(myself_power) * 2.25, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if amputate > 0:
                        if number < round(int(enemy_speed) * 0.8, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Dragons Breath", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health -dmg
                        myself_mana = myself_mana - 40
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        if dmg != 0:
                            dragon = 5
                        dragoncooldown = 10
                        skillused = ""
                        numset = False
                if skillused == "Fury_Strike" and myself_mana >= 15 and furycooldown == 0:
                    dmg = round(int(myself_power) * 3, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if amputate > 0:
                        if number < round(int(enemy_speed) * 0.8, 0)*2:
                            dmg = 0
                    elif number < int(enemy_speed)*2:
                        dmg = 0 
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Fury Strike", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 15
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        furycooldown = 4
                        skillused = ""
                        numset = False
                if skillused == "Overcharge" and myself_mana >= 50 and overchargecooldown == 0:
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+OVERCHARGED!", 1, LIGHTBLUE), (selfpos.x, selfpos.y - 100))
                        game.blit(comicsans(20).render("You used: Overcharge", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        myself_mana = myself_mana - 50
                        if myself_mana < 0:
                            myself_mana = 0
                        overchargecooldown = 8
                        overcharge = 3
                        myself_power = myself.retrievestat("strength") * 1.5
                        myself_magic = myself.retrievestat("magic") * 1.5
                        skillused = ""
                        numset = False
                if skillused == "Poison" and myself_mana >= 30 and poisoncooldown == 0:
                    dmg = round(int(myself_magic) * 3, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if amputate > 0:
                        if number < round(int(enemy_speed) * 0.8, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Poison", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 30
                        if enemy_health < 0:
                            enemy_health = 0
                        if myself_mana < 0:
                            myself_mana = 0
                        if dmg != 0:
                            poison = 4
                        poisoncooldown = 7
                        skillused = ""
                        numset = False
                if skillused == "Shuriken" and myself_mana >= 20 and shurikencooldown == 0:
                    dmg = round(int(myself_power) * 2.1, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if amputate > 0:
                        if number < round(int(enemy_speed) * 0.45, 0):
                            dmg = 0
                    elif number < round(int(enemy_speed) * 0.55, 0):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Shuriken", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 20
                        if enemy_health < 0:
                            enemy_health = 0
                        if myself_mana < 0:
                            myself_mana = 0
                        shurikencooldown = 4
                        skillused = ""
                        numset = False
                if skillused == "Slash" and myself_mana >= 30 and slashcooldown == 0:
                    dmg = round(int(myself_power) * 2.5, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if amputate > 0:
                        if number < round(int(enemy_speed) * 0.8, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Slash!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - dmg
                        if enemy_health < 0:
                            enemy_health = 0
                        if myself_mana < 0:
                            myself_mana = 0
                        slashcooldown = 5
                        skillused = ""
                        numset = False
                if skillused == "Speed" and myself_mana >= 50 and speedcooldown == 0:
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+SPEED!", 1, LIGHTBLUE), (selfpos.x, selfpos.y-100))
                        game.blit(comicsans(20).render("You used: Speed!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        myself_mana = myself_mana - 50
                        if myself_mana < 0:
                            myself_mana = 0
                        speedcooldown = 10
                        myself_speed = 100
                        skillused = ""
                        numset = False

                    
                    

            
            if enemy_health <= 0: #winning screen
                blackscreen = pygame.Rect(0,0, _width_, _height_)
                pygame.draw.rect(game, BLACK, blackscreen)
                game.blit(comicsans(20).render("You won!", 1, GREEN), (_width_/2, 100))
                experience_bar = pygame.Rect((_width_/2)-100, 200, 300, 15)
                pygame.draw.rect(game, DARKERGRAY, experience_bar)
                pygame.draw.rect(game, GREEN, pygame.Rect((_width_/2)-100, 200, 300 * xp_slider, 15)) ##xp animation bar
                if xp_slider >= 1.00:
                    game.blit(comicsans(15).render("Levelled Up!", 1, FOCUS), (_width_/2, 150))
                    game.blit(comicsans(15).render("Your Level: " + str(int(data["level:"]) + 1), 1, WHITE), (_width_/2, 175))
                else:
                    game.blit(comicsans(15).render("Your Level: " + str(data["level:"]), 1, WHITE), ((_width_/2)-100, 150))
                    game.blit(comicsans(12).render("EXP: " + str(data["experience:"]) + " / " + str(data["experience_to_next_level:"]), 1, WHITE), ((_width_/2)+125, 150))
                if xp_gained < 401:
                    xp_gained += 1
                    data["experience:"] = str(int(data["experience:"])+1)
                    xp_slider = int(data["experience:"])/int(data["experience_to_next_level:"])
                pygame.draw.rect(game, LIGHTGRAY, gotocampbtn)
                pygame.draw.rect(game, LIGHTGRAY, returnbutton)
                if returnbutton.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(game, WHITE, returnbutton)
                if gotocampbtn.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(game, WHITE, gotocampbtn)
                game.blit(comicsans(20).render("Return to Menu", 1, BLACK), (returnbutton.x, returnbutton.y))
                game.blit(comicsans(20).render("Go To Camp", 1, BLACK), (gotocampbtn.x, gotocampbtn.y))




            if myself_health <= 0: #losing screen
                blackscreen = pygame.Rect(0, 0, _width_, _height_)
                pygame.draw.rect(game, BLACK, blackscreen)
                game.blit(comicsans(20).render("You've lost!", 1, RED), (_width_/2, 100))
                pygame.draw.rect(game, LIGHTGRAY, restartbutton)
                if restartbutton.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(game, WHITE, restartbutton)
                game.blit(comicsans(20).render("Restart Battle", 1, BLACK), (restartbutton.x+10, restartbutton.y))

                pygame.draw.rect(game, LIGHTGRAY, returnbutton)
                if returnbutton.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(game, WHITE, returnbutton)
                game.blit(comicsans(20).render("Return To Menu", 1, BLACK), (returnbutton.x, returnbutton.y))
                game.blit(transform(_skull_icon_, (128,128)), (_width_/2, 200))

        if _cur_screen_ == "Level 4":
            game.blit(transform(_zone1_bg_, (_width_, _height_)), (0,-100))
            ##create characters##
            if battlebegin == False:
                myself = YourChar(data["chartype:"], int(data["vitality:"]), int(data["strength:"]), int(data["magic:"]), int(data["speed:"]), int(data["level:"]), int(data["skillpoints:"]), int(data["attributepoints:"]), int(data["experience:"]), int(data["experience_to_next_level:"]))
                myself_max_health = 100 + (myself.retrievestat("hp") * myself.retrievestat("strength"))
                myself_health = myself_max_health
                myself_max_mana = 50 + (myself.retrievestat("magic") * 2)
                myself_mana = myself_max_mana
                myself_power = myself.retrievestat("strength")
                myself_speed = myself.retrievestat("speed")
                myself_magic = myself.retrievestat("magic")
            ##add bottom part##
            footer = pygame.Rect(0, _height_-150, _width_, 150)
            pygame.draw.rect(game, DARKERGRAY, footer)
            _final_icon_ = _char_icon_knight_ if data["chartype:"] == "Knight" else _char_icon_wizard_ if data["chartype:"] == "Wizard" else _char_icon_assassin_
            _final_char_ = _char_knight_ if data["chartype:"] == "Knight" else _char_wizard_ if data["chartype:"] == "Wizard" else _char_assassin_
            heightvar = 320 if data["chartype:"] == "Knight" else 320 if data["chartype:"] == "Wizard" else 320
            selffix = pygame.Rect(50, _height_-100, 64, 64)
            game.blit(transform(_final_icon_, (64,64)), (50, _height_-100))

            if selffix.collidepoint(pygame.mouse.get_pos()): #hover over icon to see your own stats
                square = pygame.Rect(0, _height_-200, 100, 100)
                pygame.draw.rect(game, LIGHTGRAY, square)
                yourvitals = comicsans(9).render("Vitality: " + str(data["vitality:"]), 1, BLACK)
                yourstrength = comicsans(9).render("Strength: " + str(data["strength:"]), 1, BLACK)
                yourmagic = comicsans(9).render("Magic: " + str(data["magic:"]), 1, BLACK)
                yourspeed = comicsans(9).render("Speed: " + str(data["speed:"]), 1, BLACK)
                yourstats = comicsans(10).render("Your Stats: ", 1, BLACK)
                game.blit(yourstats, (square.x, square.y))
                game.blit(yourvitals, (square.x, square.y + 20))
                game.blit(yourstrength, (square.x, square.y + 30))
                game.blit(yourmagic, (square.x, square.y + 40))
                game.blit(yourspeed, (square.x, square.y + 50))
            selfpos = pygame.Rect(100, heightvar, 128, 128)
            game.blit(transform(_final_char_, (128,128)), (selfpos.x, selfpos.y))
            healthbarunder = pygame.Rect(120, _height_-85, 100, 10)
            pygame.draw.rect(game, DARKGREEN, healthbarunder)
            healthbarover = pygame.Rect(120, _height_-85, round(100 * (myself_health/myself_max_health), 0), 10)
            pygame.draw.rect(game, GREEN, healthbarover)
            displayhealth = comicsans(10).render("HP: " + str(myself_health), 1, WHITE)
            game.blit(displayhealth, (120,_height_-100))

            manabarunder = pygame.Rect(120, _height_-60, 100, 10)
            pygame.draw.rect(game, DARKERBLUE, manabarunder)
            manabarover = pygame.Rect(120, _height_-60, round(100 * (myself_mana/myself_max_mana), 0), 10)
            pygame.draw.rect(game, LIGHTBLUE, manabarover)
            displaymana = comicsans(10).render("MP: " + str(myself_mana), 1, WHITE)
            game.blit(displaymana, (120, _height_-75))

            ##add skills section##
            pygame.draw.rect(game, DARKGRAY, skill1)
            pygame.draw.rect(game, DARKGRAY, skill2)
            pygame.draw.rect(game, DARKGRAY, skill3)
            pygame.draw.rect(game, DARKGRAY, skill4)
            pygame.draw.rect(game, DARKGRAY, skill5)
            pygame.draw.rect(game, DARKGRAY, skill6)
            pygame.draw.rect(game, DARKGRAY, skill7)
            pygame.draw.rect(game, DARKGRAY, skill8)
            pygame.draw.rect(game, DARKGRAY, skill9)
            pygame.draw.rect(game, DARKGRAY, skill10)
            #add hover effect to skills to show user that they are currently selecting that skill
            if skill1.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill1)
            if skill2.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill2)
            if skill3.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill3)
            if skill4.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill4)
            if skill5.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill5)
            if skill6.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill6)
            if skill7.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill7)
            if skill8.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill8)
            if skill9.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill9)
            if skill10.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill10)
            #add skill images where applicable
            game.blit(transform(skill1_img, (32,32)), (skill1.x, skill1.y))
            game.blit(transform(skill2_img, (32,32)), (skill2.x, skill2.y))
            game.blit(transform(skill3_img, (32,32)), (skill3.x, skill3.y))
            game.blit(transform(skill4_img, (32,32)), (skill4.x, skill4.y))
            game.blit(transform(skill5_img, (32,32)), (skill5.x, skill5.y))
            game.blit(transform(skill6_img, (32,32)), (skill6.x, skill6.y))
            game.blit(transform(skill7_img, (32,32)), (skill7.x, skill7.y))
            game.blit(transform(skill8_img, (32,32)), (skill8.x, skill8.y))
            game.blit(transform(skill9_img, (32,32)), (skill9.x, skill9.y))
            game.blit(transform(skill10_img, (32,32)), (skill10.x, skill10.y))
            

            ##draw enemy
            enemy = Enemy("The Gunner", _l4_icon_, _l4_enemy_, 15, 15, 5, 35, ["Basic Shot", "Marksmen", "Explode"])
            tutfix = pygame.Rect(_width_-110, _height_-100, 64, 64)
            game.blit(transform(_l4_icon_, (64,64)), (_width_-110, _height_-100))
            enemypos = pygame.Rect(_width_-200, 320, 128, 128)
            game.blit(transform(_l4_enemy_, (128,128)), (enemypos.x, enemypos.y))
            if battlebegin == False:
                enemy_max_health = 100 + (enemy.get("hp") * enemy.get("strength"))
                enemy_health = enemy_max_health
                enemy_max_mana = 50 + (enemy.get("magic") * 2)
                enemy_mana = enemy_max_mana
                enemy_power = enemy.get("strength")
                enemy_speed = enemy.get("speed")
                battlebegin = True #set true once both players have initialised stats
            enemyhealthbarunder = pygame.Rect(_width_-220, _height_-85, 100, 10)
            enemyhealthbarover = pygame.Rect(_width_-220, _height_-85, round(100 * (enemy_health/enemy_max_health), 0), 10)
            displayenemyhealth = comicsans(10).render("HP: " + str(enemy_health), 1, WHITE)
            pygame.draw.rect(game, DARKGREEN, enemyhealthbarunder)
            pygame.draw.rect(game, GREEN, enemyhealthbarover)
            game.blit(displayenemyhealth, (_width_-170, _height_-100))
            enemymanabarunder = pygame.Rect(_width_-220, _height_-60, 100, 10)
            enemymanabarover = pygame.Rect(_width_-220, _height_-60, round(100 * (enemy_mana/enemy_max_mana), 0), 10)
            displayenemymana = comicsans(10).render("MP: " + str(enemy_mana), 1, WHITE)
            pygame.draw.rect(game, DARKERBLUE, enemymanabarunder)
            pygame.draw.rect(game, LIGHTBLUE, enemymanabarover)
            game.blit(displayenemymana, (_width_-170, _height_-75))
            if tutfix.collidepoint(pygame.mouse.get_pos()):
                square2 = pygame.Rect(_width_-100, _height_-200, 100, 100)
                pygame.draw.rect(game, LIGHTGRAY, square2)
                enemyvitals = comicsans(9).render("Vitality: " + str(enemy.get("hp")), 1, BLACK)
                enemystrength = comicsans(9).render("Strength: " + str(enemy.get("strength")), 1, BLACK)
                enemymagic = comicsans(9).render("Magic: " + str(enemy.get("magic")), 1, BLACK)
                enemyspeed = comicsans(9).render("Speed: " + str(enemy.get("speed")), 1, BLACK)
                enemystats = comicsans(9).render("Enemy Stats: ", 1, BLACK)
                game.blit(enemystats, (square2.x, square2.y))
                game.blit(enemyvitals, (square2.x, square2.y + 20))
                game.blit(enemystrength, (square2.x, square2.y + 30))
                game.blit(enemymagic, (square2.x, square2.y + 40))
                game.blit(enemyspeed, (square2.x, square2.y + 50))

            ##draw area to exit##
            pygame.draw.rect(game, LIGHTGRAY, exiticon)
            pygame.draw.circle(game, (200,0,0), (exiticon.x + 32, exiticon.y + 32), 32)
            game.blit(comicsans(40).render("X", 1, WHITE), (exiticon.x + 18, exiticon.y + 1))
            if exiticon.collidepoint(pygame.mouse.get_pos()): #hover effect
                pygame.draw.rect(game, WHITE, exiticon)
                pygame.draw.circle(game, (150,0,0), (exiticon.x + 32, exiticon.y + 32), 32)
                game.blit(comicsans(40).render("X", 1, WHITE), (exiticon.x + 18, exiticon.y + 1))    
            ##draw text to identify current turn##
            turn = comicsans(20).render("Your Turn!" if curTurn == "Self" else "Enemy Turn!", 1, WHITE)
            game.blit(turn, (exiticon.x-20, exiticon.y-30)) 

            ## battle code for the enemy

            if curTurn == "Enemy" and battlebegin == True and enemy_health > 0:
                if stun > 0:
                    canattack = False
                    stun -= 1
                    if stun < 0:
                        stun = 0
                    curTurn = "Self"
                    enemyset = False
                    numset = False
                    skillused = ""

                if freeze > 0:
                    canattack = False
                    freeze -= 1
                    if freeze < 0:
                        freeze = 0
                    curTurn = "Self"
                    enemyset = False
                    numset = False
                    skillused = ""

                if lightning > 0:
                    canttack = False
                    lightning -= 1
                    if lightning < 0:
                        lightning = 0
                    curTurn = "Self"
                    enemyset = False
                    numset = False
                    skillused = ""


                if enemyset == False:
                    enemy_skills = enemy.get("abilities")
                    ranvalue = random.randint(0, len(enemy_skills)-1) #roll a random move for basic tier enemies so its automatic
                    ##check if enough mana
                    if enemy_skills[ranvalue] == "Basic Attack":
                        enemyset = True
                    if enemy_skills[ranvalue] == "Power Slash" and enemy_mana >= 15:
                        enemyset = True
                    
                if enemy_skills[ranvalue] == "Basic Shot" and canattack == True:
                    dmg = round(int(enemy_power)*1.5, 0)
                    ##chance to miss target based on target speed##
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if number < int(myself_speed): #if roll is less than target speed, means you are slower.
                        dmg = 0
                    elif shield == True:
                        dmg = round(int(enemy_power)*(0.75 - (myself_power*0.01)), 0)
                    elif suit > 0 and shield == False:
                        dmg = round(int(enemy_power)*(1.15),0)
                    elif suit > 0 and shield == True:
                        dmg = round(int(enemy_power) * ( 0.65 - (myself_power * 0.01)), 0)
                    elif weakness > 0:
                        dmg = round(dmg*0.1, 0)
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render(("-" if invert == 0 else "+") + str(dmg) if dmg != 0 else "MISSED!", 1, RED if invert == 0 else GREEN), (selfpos.x, selfpos.y - 100))
                        print("Enemy dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("Enemy used: Basic Attack", 1, WHITE), (_width_/2, 100))

                        if fire > 0:
                            burn = round(int(myself_magic) * 2, 0)
                            game.blit(comicsans(20).render("-" + str(burn), 1, RED), (enemypos.x, enemypos.y - 100))
                        if dragon > 0:
                            burn = round(int(myself_magic) * 1.5, 0)
                            game.blit(comicsans(20).render("-" + str(burn), 1, RED), (enemypos.x, enemypos.y - 100))
                        if poison > 0:
                            burn = round(int(myself_magic) * 1.5, 0)
                            game.blit(comicsans(20).render("-" + str(burn), 1, RED), (enemypos.x, enemypos.y - 100))
                    if counter == 70:
                        curTurn = "Self"
                        counter = 0
                        myself_health = myself_health - dmg if invert == 0 else myself_health + dmg
                        if myself_health < 0:
                            myself_health = 0
                        if myself_health > myself_max_health:
                            myself_health = myself_max_health
                            
                        enemy_mana = enemy_mana + round(enemy_max_mana*0.1,0)
                        if enemy_mana > enemy_max_mana:
                            enemy_mana = enemy_max_mana
                        if fire > 0:
                            enemy_health = enemy_health - burn
                            if enemy_health < 0:
                                enemy_health = 0
                        if dragon > 0:
                            enemy_health = enemy_health - burn
                            if enemy_health < 0:
                                enemy_health = 0
                        if poison > 0:
                            enemy_health = enemy_health - burn
                            if enemy_health < 0:
                                enemy_health = 0
                        if life > 0:
                            myself_health = myself_health + round(myself_max_health * 0.1, 0)
                            if myself_health > myself_max_health:
                                myself_health = myself_max_health
                        enemyset = False
                        numset = False
                        shieldcooldown-=1
                        shieldcount-=1
                        bscooldown -= 1
                        bscount -= 1
                        dbcooldown -= 1
                        punccooldown -= 1
                        punc -= 1
                        slamdown -= 1
                        suit -= 1
                        suitcooldown -= 1 
                        enrage -= 1
                        enragecooldown -= 1
                        fire -= 1
                        fireballcooldown -= 1
                        freeze -= 1
                        freezecooldown -= 1
                        draincooldown -= 1
                        invert -= 1
                        invertcooldown -= 1
                        leechcooldown -= 1
                        life -= 1
                        lifecooldown -= 1
                        lightningcooldown -= 1
                        lightning -= 1
                        soul -= 1
                        soulcooldown -= 1
                        weakness -= 1
                        weaknesscooldown -= 1
                        amputate -= 1
                        amputatecooldown -= 1
                        dragon -= 1
                        dragoncooldown -= 1
                        overcharge -= 1
                        overchargecooldown -= 1
                        poison -= 1
                        poisoncooldown -= 1
                        shurikencooldown -= 1
                        slashcooldown -= 1
                        speedcooldown -= 1
                        if shieldcooldown < 0:
                            shieldcooldown = 0
                        if shieldcount < 0:
                            shieldcount = 0
                            shield = False
                        if bscooldown < 0:
                            bscooldown = 0
                        if bscount < 0:
                            bscount = 0
                        if dbcooldown < 0:
                            dbcooldown = 0
                        if punccooldown < 0:
                            punccooldown = 0
                        if punc < 0:
                            punc = 0
                        if slamdown < 0:
                            slamdown = 0
                        if suit < 0:
                            suit = 0
                        if suitcooldown < 0:
                            suitcooldown = 0
                        if enrage < 0:
                            enrage = 0
                        if enragecooldown < 0:
                            enragecooldown = 0
                        if enrage == 0:
                            myself_power = myself.retrievestat("strength")
                        if fire == 0:
                            fire = 0
                        if fireballcooldown == 0:
                            fireballcooldown = 0
                        if freeze < 0:
                            freeze = 0
                        if freezecooldown < 0:
                            freezecooldown = 0
                        if draincooldown < 0:
                            draincooldown = 0
                        if invert < 0:
                            invert = 0
                        if invertcooldown < 0:
                            invertcooldown = 0
                        if leechcooldown < 0:
                            leechcooldown = 0
                        if life < 0:
                            life = 0
                        if lifecooldown < 0:
                            lifecooldown = 0
                        if lightningcooldown == 0:
                            lightningcooldown = 0
                        if lightning == 0:
                            lightning = 0
                        if soul < 0:
                            soul = 0
                        if soulcooldown < 0:
                            soulcooldown = 0
                        if weakness < 0:
                            weakness = 0
                        if weakness == 0:
                            myself_power = myself.retrievestat("strength")
                            myself_magic = myself.retrievestat("magic")
                        if weaknesscooldown < 0:
                            weaknesscooldown = 0
                        if amputate < 0:
                            amputate = 0
                        if amputatecooldown < 0:
                            amputatecooldown = 0
                        if dragon < 0:
                            dragon = 0
                        if dragoncooldown < 0:
                            dragoncooldown = 0
                        if overcharge < 0:
                            overcharge = 0
                        if overcharge == 0:
                            myself_power = myself.retrievestat("strength")
                            myself_magic = myself.retrievestat("magic")
                        if overchargecooldown < 0:
                            overchargecooldown = 0
                        if poison < 0:
                            poison = 0
                        if poisoncooldown < 0:
                            poisoncooldown = 0
                        if shurikencooldown < 0:
                            shurikencooldown = 0
                        if slashcooldown < 0:
                            slashcooldown = 0
                        if speedcooldown < 0:
                            speedcooldown = 0
                        if speedcooldown == 0:
                            myself_speed = myself.retrievestat("speed")
                
                if enemy_skills[ranvalue] == "Marksmen" and enemy_mana >= 15 and canattack == True: 
                    dmg = round(int(enemy_power)*2.25, 0)
                    if numset == False:
                        number = random.randint(0,100)
                        numset = True
                    if number < int(myself_speed):
                        dmg = 0
                    elif shield == True:
                        dmg = round(int(enemy_power) * (1.125 - (myself_power*0.01)), 0)
                    elif suit > 0 and shield == False:
                        dmg = round(int(enemy_power) * (1.75), 0)
                    elif suit > 0 and shield == True:
                        dmg = round(int(enemy_power) * (0.975 - (myself_power * 0.01)), 0)
                    elif weakness > 0:
                        dmg = round(dmg * 0.1, 0)
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render(("-" if invert == 0 else "+") + str(dmg) if dmg != 0 else "MISSED!", 1, RED if invert == 0 else GREEN), (selfpos.x, selfpos.y - 100))
                        print("Enemy dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("Enemy used: Power Slash", 1, WHITE), (_width_/2, 100))
                        if fire > 0:
                            burn = round(int(myself_magic) * 2, 0)
                            game.blit(comicsans(20).render("-" + str(burn), 1, RED), (enemypos.x, enemypos.y - 100))
                        if dragon > 0:
                            burn = round(int(myself_magic) * 1.5, 0)
                            game.blit(comicsans(20).render("-" + str(burn), 1, RED), (enemypos.x, enemypos.y - 100))
                        if poison > 0:
                            burn = round(int(myself_magic) * 1.5, 0)
                            game.blit(comicsans(20).render("-" + str(burn), 1, RED), (enemypos.x, enemypos.y - 100))
                    if counter == 70:
                        curTurn = "Self"
                        counter = 0
                        myself_health = myself_health - dmg if invert == 0 else myself_health + dmg
                        if myself_health > myself_max_health:
                            myself_health = myself_max_health
                        if myself_health < 0:
                            myself_health = 0
                        enemy_mana = enemy_mana - 15
                        if enemy_mana < 0:
                            enemy_mana = 0
                        if fire > 0:
                            enemy_health = enemy_health - burn
                            if enemy_health < 0:
                                enemy_health = 0
                        if dragon > 0:
                            enemy_health = enemy_health - burn
                            if enemy_health < 0:
                                enemy_health = 0
                        if poison > 0:
                            enemy_health = enemy_health - burn
                            if enemy_health < 0:
                                enemy_health = 0
                        if life > 0:
                            myself_health = myself_health + round(myself_max_health * 0.1, 0)
                            if myself_health > myself_max_health:
                                myself_health = myself_max_health
                        enemyset = False
                        numset = False
                        shieldcooldown-=1
                        shieldcount-=1
                        bscooldown-=1
                        bscount -= 1 
                        dbcooldown -= 1
                        punccooldown -= 1
                        punc -= 1
                        slamdown -= 1
                        suit -= 1
                        suitcooldown -= 1
                        fire -= 1
                        fireballcooldown -= 1
                        freeze -= 1
                        freezecooldown -= 1
                        draincooldown -= 1
                        invert -= 1
                        invertcooldown -= 1
                        leechcooldown -= 1
                        lifecooldown -= 1
                        life -= 1
                        lightningcooldown -= 1
                        lightning -= 1
                        soul -= 1
                        soulcooldown -= 1
                        weakness -= 1
                        weaknesscooldown -= 1
                        amputate -= 1
                        amputatecooldown -= 1
                        dragon -= 1
                        dragoncooldown -= 1
                        overcharge -= 1
                        overchargecooldown -= 1
                        poison -= 1
                        poisoncooldown -= 1
                        shurikencooldown -= 1
                        slashcooldown -= 1
                        speedcooldown -= 1
                        if shieldcooldown < 0:
                            shieldcooldown = 0
                        if shieldcount < 0:
                            shieldcount = 0
                            shield = False
                        if bscooldown < 0:
                            bscooldown = 0
                        if bscount < 0:
                            bscount = 0
                        if dbcooldown < 0:
                            dbcooldown = 0
                        if punccooldown < 0:
                            punccooldown = 0
                        if punc < 0:
                            punc = 0
                        if slamdown < 0:
                            slamdown = 0
                        if suit < 0:
                            suit = 0
                        if suitcooldown < 0:
                            suitcooldown = 0
                        if enrage < 0:
                            enrage = 0
                        if enragecooldown < 0:
                            enragecooldown = 0
                        if enrage == 0:
                            myself_power = myself.retrievestat("strength")
                        if fire < 0:
                            fire = 0
                        if fireballcooldown < 0:
                            fireballcooldown = 0
                        if freeze < 0:
                            freeze = 0
                        if freezecooldown < 0:
                            freezecooldown = 0
                        if draincooldown < 0:
                            draincooldown = 0
                        if invert < 0:
                            invert = 0
                        if invertcooldown < 0:
                            invertcooldown = 0
                        if leechcooldown < 0:
                            leechcooldown = 0
                        if life < 0:
                            life = 0
                        if lifecooldown < 0:
                            lifecooldown = 0
                        if lightningcooldown < 0:
                            lightningcooldown -= 1
                        if lightning == 1:
                            lightning = 0
                        if soul < 0:
                            soul = 0
                        if soulcooldown < 0:
                            soulcooldown = 0
                        if weakness == 0:
                            myself_power = myself.retrievestat("strength")
                            myself_magic = myself.retrievestat("magic")
                        if weakness < 0:
                            weakness = 0
                        if weaknesscooldown < 0:
                            weaknesscooldown = 0
                        if amputate < 0:
                            amputate = 0
                        if amputatecooldown < 0:
                            amputatecooldown = 0
                        if dragon < 0:
                            dragon = 0
                        if dragoncooldown < 0:
                            dragoncooldown = 0
                        if overcharge < 0:
                            overcharge = 0
                        if overcharge == 0:
                            myself_power = myself.retrievestat("strength")
                            myself_magic = myself.retrievestat("magic")
                        if overchargecooldown < 0:
                            overchargecooldown = 0
                        if poison < 0:
                            poison = 0
                        if poisoncooldown < 0:
                            poisoncooldown = 0
                        if shurikencooldown < 0:
                            shurikencooldown = 0
                        if slashcooldown < 0:
                            slashcooldown = 0
                        if speedcooldown == 0:
                            myself_speed = myself.retrievestat("speed")
                        if speedcooldown < 0:
                            speedcooldown = 0
                if enemy_skills[ranvalue] == "Explode" and enemy_mana >= 35 and canattack == True: 
                    dmg = round(int(enemy_power)*3.25, 0)
                    if numset == False:
                        number = random.randint(0,100)
                        numset = True
                    if number < int(myself_speed):
                        dmg = 0
                    elif shield == True:
                        dmg = round(int(enemy_power) * (1.125 - (myself_power*0.01)), 0)
                    elif suit > 0 and shield == False:
                        dmg = round(int(enemy_power) * (1.75), 0)
                    elif suit > 0 and shield == True:
                        dmg = round(int(enemy_power) * (0.975 - (myself_power * 0.01)), 0)
                    elif weakness > 0:
                        dmg = round(dmg * 0.1, 0)
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render(("-" if invert == 0 else "+") + str(dmg) if dmg != 0 else "MISSED!", 1, RED if invert == 0 else GREEN), (selfpos.x, selfpos.y - 100))
                        print("Enemy dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("Enemy used: Power Slash", 1, WHITE), (_width_/2, 100))
                        if fire > 0:
                            burn = round(int(myself_magic) * 2, 0)
                            game.blit(comicsans(20).render("-" + str(burn), 1, RED), (enemypos.x, enemypos.y - 100))
                        if dragon > 0:
                            burn = round(int(myself_magic) * 1.5, 0)
                            game.blit(comicsans(20).render("-" + str(burn), 1, RED), (enemypos.x, enemypos.y - 100))
                        if poison > 0:
                            burn = round(int(myself_magic) * 1.5, 0)
                            game.blit(comicsans(20).render("-" + str(burn), 1, RED), (enemypos.x, enemypos.y - 100))
                    if counter == 70:
                        curTurn = "Self"
                        counter = 0
                        myself_health = myself_health - dmg if invert == 0 else myself_health + dmg
                        if myself_health > myself_max_health:
                            myself_health = myself_max_health
                        if myself_health < 0:
                            myself_health = 0
                        enemy_mana = enemy_mana - 15
                        if enemy_mana < 0:
                            enemy_mana = 0
                        if fire > 0:
                            enemy_health = enemy_health - burn
                            if enemy_health < 0:
                                enemy_health = 0
                        if dragon > 0:
                            enemy_health = enemy_health - burn
                            if enemy_health < 0:
                                enemy_health = 0
                        if poison > 0:
                            enemy_health = enemy_health - burn
                            if enemy_health < 0:
                                enemy_health = 0
                        if life > 0:
                            myself_health = myself_health + round(myself_max_health * 0.1, 0)
                            if myself_health > myself_max_health:
                                myself_health = myself_max_health
                        enemyset = False
                        numset = False
                        shieldcooldown-=1
                        shieldcount-=1
                        bscooldown-=1
                        bscount -= 1 
                        dbcooldown -= 1
                        punccooldown -= 1
                        punc -= 1
                        slamdown -= 1
                        suit -= 1
                        suitcooldown -= 1
                        fire -= 1
                        fireballcooldown -= 1
                        freeze -= 1
                        freezecooldown -= 1
                        draincooldown -= 1
                        invert -= 1
                        invertcooldown -= 1
                        leechcooldown -= 1
                        lifecooldown -= 1
                        life -= 1
                        lightningcooldown -= 1
                        lightning -= 1
                        soul -= 1
                        soulcooldown -= 1
                        weakness -= 1
                        weaknesscooldown -= 1
                        amputate -= 1
                        amputatecooldown -= 1
                        dragon -= 1
                        dragoncooldown -= 1
                        overcharge -= 1
                        overchargecooldown -= 1
                        poison -= 1
                        poisoncooldown -= 1
                        shurikencooldown -= 1
                        slashcooldown -= 1
                        speedcooldown -= 1
                        if shieldcooldown < 0:
                            shieldcooldown = 0
                        if shieldcount < 0:
                            shieldcount = 0
                            shield = False
                        if bscooldown < 0:
                            bscooldown = 0
                        if bscount < 0:
                            bscount = 0
                        if dbcooldown < 0:
                            dbcooldown = 0
                        if punccooldown < 0:
                            punccooldown = 0
                        if punc < 0:
                            punc = 0
                        if slamdown < 0:
                            slamdown = 0
                        if suit < 0:
                            suit = 0
                        if suitcooldown < 0:
                            suitcooldown = 0
                        if enrage < 0:
                            enrage = 0
                        if enragecooldown < 0:
                            enragecooldown = 0
                        if enrage == 0:
                            myself_power = myself.retrievestat("strength")
                        if fire < 0:
                            fire = 0
                        if fireballcooldown < 0:
                            fireballcooldown = 0
                        if freeze < 0:
                            freeze = 0
                        if freezecooldown < 0:
                            freezecooldown = 0
                        if draincooldown < 0:
                            draincooldown = 0
                        if invert < 0:
                            invert = 0
                        if invertcooldown < 0:
                            invertcooldown = 0
                        if leechcooldown < 0:
                            leechcooldown = 0
                        if life < 0:
                            life = 0
                        if lifecooldown < 0:
                            lifecooldown = 0
                        if lightningcooldown < 0:
                            lightningcooldown -= 1
                        if lightning == 1:
                            lightning = 0
                        if soul < 0:
                            soul = 0
                        if soulcooldown < 0:
                            soulcooldown = 0
                        if weakness == 0:
                            myself_power = myself.retrievestat("strength")
                            myself_magic = myself.retrievestat("magic")
                        if weakness < 0:
                            weakness = 0
                        if weaknesscooldown < 0:
                            weaknesscooldown = 0
                        if amputate < 0:
                            amputate = 0
                        if amputatecooldown < 0:
                            amputatecooldown = 0
                        if dragon < 0:
                            dragon = 0
                        if dragoncooldown < 0:
                            dragoncooldown = 0
                        if overcharge < 0:
                            overcharge = 0
                        if overcharge == 0:
                            myself_power = myself.retrievestat("strength")
                            myself_magic = myself.retrievestat("magic")
                        if overchargecooldown < 0:
                            overchargecooldown = 0
                        if poison < 0:
                            poison = 0
                        if poisoncooldown < 0:
                            poisoncooldown = 0
                        if shurikencooldown < 0:
                            shurikencooldown = 0
                        if slashcooldown < 0:
                            slashcooldown = 0
                        if speedcooldown == 0:
                            myself_speed = myself.retrievestat("speed")
                        if speedcooldown < 0:
                            speedcooldown = 0
                if freeze == 0:
                    canttack = True
                if stun == 0:
                    canattack = True

            ##battle code for self player

            if curTurn == "Self" and battlebegin == True and myself_health > 0: #design skills via if statements
                if skillused == "Basic_Attack": ## basic attack utilising characters strength
                    dmg = round(int(myself_power)*1.5, 0)
                    if punc > 0:
                        dmg = round(dmg * 1.15, 0)
                    mana_gained = round(int(myself_max_mana)*0.1, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if bscount > 0:
                        if number < round(int(enemy_speed)/1.5, 0):
                            dmg = 0
                    elif soul > 0:
                        if number < round(int(enemy_speed)*0.6, 0):
                            dmg = 0
                    elif amputate > 0:
                        if number < round(int(enemy_speed) * 0.8, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70: ##to add some delay allowing for the game to show the text
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        print("You dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("You used: Basic Attack", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana + mana_gained
                        if myself_mana > myself_max_mana:
                            myself_mana = myself_max_mana

                        #make sure enemy health isnt glitched visually
                        if enemy_health < 0: #if enemy is killed
                            enemy_health = 0
                        skillused = "" # reset the skills
                        numset = False

                if skillused == "Heal" and myself_mana >= 20: #check for mana to be filled
                    heal = round(int(myself_max_health * (0.5 + myself.retrievestat("magic")/100)))
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+" + str(heal), 1, GREEN), (selfpos.x, selfpos.y - 100))
                        print("You healed yourself for: " + str(heal) + " HP!")
                        game.blit(comicsans(20).render("You used: Healing", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        myself_health = myself_health + heal
                        if myself_health > myself_max_health: ##prevent over healing
                            myself_health = myself_max_health
                        myself_mana = myself_mana - 20
                        if myself_mana < 0:
                            myself_mana = 0
                        skillused = ""

                if skillused == "Mana" and myself_mana >= 10:
                    mana = round(int(myself_max_mana * (0.6 + myself.retrievestat("magic")/100)))
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+" + str(mana), 1, LIGHTBLUE), (selfpos.x, selfpos.y - 100))
                        print("You gained " + str(mana) + " MP!")
                        game.blit(comicsans(20).render("You used: Mana", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        myself_mana = myself_mana + mana - 10
                        if myself_mana > myself_max_mana:
                            myself_mana = myself_max_mana
                        skillused = ""
                
                #knight skillset
                if skillused == "Slam" and myself_mana >= 15 and slamdown == 0:
                    dmg = round((int(myself_power) + (int(myself_power)*0.25)) * 1.75, 0)
                    if punc > 0:
                        dmg = round(dmg * 1.15, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if bscount > 0:
                        if number < round(int(enemy_speed)/1.5, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y-100))
                        print("You dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("You used: Slam", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 15
                        if myself_mana < 0:
                            myself_mana = 0
                        
                        if enemy_health < 0:
                            enemy_health = 0
                        slamdown = 3
                        skillused = ""
                        numset = False

                if skillused == "Shield" and myself_mana >= 20 and shieldcooldown == 0:
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+SHIELDED!", 1, LIGHTBLUE), (selfpos.x, selfpos.y - 100))
                        print("You used shield!")
                        game.blit(comicsans(20).render("You used: Shield", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        shield = True
                        shieldcount = 2
                        shieldcooldown = 4
                        print(str(shieldcount) + ", " + str(shieldcooldown) + ", " + str(shield))
                        curTurn = "Enemy"
                        counter = 0
                        myself_mana = myself_mana - 20
                        if myself_mana < 0:
                            myself_mana = 0
                        skillused = ""

                if skillused == "Ballistic_Strike" and myself_mana >= 25 and bscooldown == 0:
                    dmg = round((int(myself_power) * 1.75) + (int(myself_power) * 0.3), 0)
                    if punc > 0:
                        dmg = round(dmg * 1.15, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if bscount > 0:
                        if number < round(int(enemy_speed)/1.5, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y-100))
                        print("You dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("You used: Ballistic Strike!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 25
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        bscooldown = 3
                        if dmg != 0: #to ensure that affects only apply if strikes are hit
                            bscount = 2
                        skillused = ""
                        numset = False

                if skillused == "Double_Strike" and myself_mana >= 20 and dbcooldown == 0:
                    dmg = round((int(myself_power) * 3), 0)
                    if punc > 0:
                        dmg = round(dmg * 1.15, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if bscount > 0:
                        if number < round(int(enemy_speed)/1.5, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y-100))
                        print("You dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("You used: Double Strike!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 20
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        dbcooldown = 5
                        skillused = ""
                        numset = False

                if skillused == "Puncture" and myself_mana >= 35 and punccooldown == 0:
                    dmg = round((int(myself_power) * 3.5), 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if bscount > 0:
                        if number < round(int(enemy_speed)/1.5, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        print("You dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("You used: Puncture", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 35
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        punccooldown = 4
                        if dmg != 0:
                            punc = 3
                        skillused = ""
                        numset = False

                if skillused == "Stun" and myself_mana >= 20 and stuncooldown == 0:
                    dmg = round((int(myself_power) * 1.85), 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if bscount > 0:
                        if number < round(int(enemy_speed)/1.5, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        print("You dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("You used: Stun", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 20
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        stuncooldown = 5
                        if dmg != 0:
                            stun = 1
                        skillused = ""
                        numset = False
                
                if skillused == "Suit_Up" and myself_mana >= 40 and suitcooldown == 0:
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+SUITED!", 1, LIGHTBLUE), (selfpos.x, selfpos.y - 100))
                        print("You used: Suit Up!")
                        game.blit(comicsans(20).render("You used: Suit Up!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        suit = 5
                        suitcooldown = 9
                        curTurn = "Enemy"
                        counter = 0
                        myself_mana = myself_mana - 40
                        if myself_mana < 0:
                            myself_mana = 0
                        
                        skillused = ""
                
                if skillused == "Enrage" and myself_mana >= 50 and enragecooldown == 0:
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+ENRAGED!", 1, LIGHTBLUE), (selfpos.x, selfpos.y - 100))
                        print("You used: Enraged!")
                        game.blit(comicsans(20).render("You used: Enraged!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        enrage = 3
                        enragecooldown = 10
                        myself_power = myself.retrievestat("strength") * 2.5
                        curTurn = "Enemy"
                        counter = 0
                        myself_mana = myself_mana - 50
                        if myself_mana < 0:
                            myself_mana = 0

                        skillused = ""
                if skillused == "Vampire_Strike" and myself_mana >= 45 and vampirecooldown == 0:
                    dmg = round((int(myself_power) * 3.75), 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if bscount > 0:
                        if number < round(int(enemy_speed) / 1.5, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        print("You dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("You used: Vampire Strike!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 45
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        vampirecooldown = 4
                        if dmg != 0:
                            myself_health = myself_health + round((dmg * 0.3), 0)
                            if myself_health > myself_max_health:
                                myself_health = myself_max_health
                        skillused = ""
                        numset = False

                ##wizard skillset
                if skillused == "Fireball" and myself_mana >= 20 and fireballcooldown == 0:
                    dmg = round(int(myself_power) * 1.5, 0)
                    dmg = round(dmg + (int(myself_magic)*1.2), 0)
                    if numset == False:
                        number = random.randint(0,100)
                        numset = True
                    if soul > 0:
                        if number < round(int(enemy_speed)*0.6, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        print("You dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("You used: Fireball!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 20
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        if dmg != 0:
                            fire = 2
                        fireballcooldown = 4
                        skillused = ""
                        numset = False

                if skillused == "Freeze" and myself_mana >= 25 and freezecooldown == 0:
                        dmg = round(int(myself_magic) * 1.25, 0)
                        if numset == False:
                            number = random.randint(0, 100)
                            numset = True
                        if soul > 0:
                            if number < round(int(enemy_speed)*0.6, 0):
                                dmg = 0
                        elif number < int(enemy_speed):
                            dmg = 0
                        if counter != 70:
                            counter += 1
                            game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                            game.blit(comicsans(20).render("You used: Freeze", 1, WHITE), (_width_/2, 100))
                        if counter == 70:
                            curTurn = "Enemy"
                            counter = 0
                            enemy_health = enemy_health - dmg
                            myself_mana = myself_mana - 25
                            if myself_mana < 0:
                                myself_mana = 0
                            if enemy_health < 0:
                                enemy_health = 0
                            if dmg != 0:
                                freeze = 2
                            freezecooldown = 5
                            skillused = ""
                            numset = False

                if skillused == "Drain" and myself_mana >= 15 and draincooldown == 0:
                    drain = round(enemy_mana / 2, 0)
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(drain) + "MP!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Drain", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_mana = enemy_mana - drain
                        if enemy_mana < 0:
                            enemy_mana = 0
                        myself_mana = myself_mana - 15
                        if myself_mana < 0:
                            myself_mana = 0
                        myself_mana = myself_mana + drain
                        if myself_mana > myself_max_mana:
                            myself_mana = myself_max_mana
                        skillused = ""
                        numset = False
                        draincooldown = 4
                
                if skillused == "Invert" and myself_mana >= 35 and invertcooldown == 0:
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("INVERTED!", 1, RED), (enemypos.x, enemypos.y-100))
                        game.blit(comicsans(20).render("You used: Inverted!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        myself_mana = myself_mana - 35
                        if myself_mana < 0:
                            myself_mana = 0
                        skillused = ""
                        numset = False
                        invertcooldown = 6
                        invert = 1

                if skillused == "Leech" and myself_mana >= 45 and leechcooldown == 0:
                    hp = round(enemy_health * 0.2, 0)
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(hp), 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Leech", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - hp
                        myself_mana = myself_mana - 45
                        myself_health = myself_health + hp
                        if myself_health > 0:
                            myself_health = myself_max_health
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        leechcooldown = 5
                        skillused = ""
                        numset = False

                if skillused == "Life" and myself_mana >= 40 and lifecooldown == 0:
                    hp = round(myself_max_health * 0.1, 0)
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+" + str(hp), 1, GREEN), (selfpos.x, selfpos.y - 100))
                        game.blit(comicsans(20).render("You used: Life", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        myself_health = myself_health + hp
                        if myself_health > 0:
                            myself_health = myself_max_health
                        myself_mana = myself_mana - 40
                        if myself_mana < 0:
                            myself_mana = 0
                        lifecooldown = 8
                        life = 5
                        skillused = ""
                        numset = False
                if skillused == "Lightning_Strike" and myself_mana >= 30 and lightningcooldown == 0:
                    dmg = round(int(myself_magic) * 4.5, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if soul > 0:
                        if number < round(int(enemy_speed)*0.6, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Lightning Strike", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 30
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        if dmg != 0:
                            lightning = 1
                        lightningcooldown = 7
                        skillused = ""
                        numset = False
                if skillused == "Soul_Crush" and myself_mana >= 50 and soulcooldown == 0:
                    dmg = round(int(myself_magic) * 5.5, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if soul > 0:
                        if number < round(int(enemy_speed)*0.6, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Soul Crush", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 50
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        if dmg != 0:
                            soul = 4
                        soulcooldown = 10
                        skillused = ""
                        numset = False
                if skillused == "Weakness" and myself_mana >= 60 and weaknesscooldown == 0:
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+WEAKNESS", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Weakness", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        myself_power = myself.retrievestat("strength") * 1.9
                        myself_magic = myself.retrievestat("magic") * 1.9
                        myself_mana = myself_mana - 60
                        if myself_mana < 0:
                            myself_mana = 0
                        weakness = 4
                        weaknesscooldown = 12
                        skillused = ""
                        numset = False
                
                if skillused == "Amputate" and myself_mana >= 20 and amputatecooldown == 0:
                    dmg = round(int(myself_power) * 2, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Amputate!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 20
                        if enemy_health < 0:
                            enemy_health = 0
                        if myself_mana < 0:
                            myself_mana = 0
                        if dmg != 0:
                            amputate = 2
                        amputatecooldown = 4
                        skillused = ""
                        numset = False
                if skillused == "Blindside" and myself_mana >= 25 and blindsidecooldown == 0:
                    dmg = round(int(myself_power) * 1.75, 0)
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg), 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Blindside", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 25
                        if enemy_health < 0:
                            enemy_health = 0
                        if myself_mana < 0:
                            myself_mana = 0
                        blindsidecooldown = 3
                        skillused = ""
                        numset = False
                if skillused == "Dragons_Breath" and myself_mana >= 40 and dragoncooldown == 0:
                    dmg = round(int(myself_power) * 2.25, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if amputate > 0:
                        if number < round(int(enemy_speed) * 0.8, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Dragons Breath", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health -dmg
                        myself_mana = myself_mana - 40
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        if dmg != 0:
                            dragon = 5
                        dragoncooldown = 10
                        skillused = ""
                        numset = False
                if skillused == "Fury_Strike" and myself_mana >= 15 and furycooldown == 0:
                    dmg = round(int(myself_power) * 3, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if amputate > 0:
                        if number < round(int(enemy_speed) * 0.8, 0)*2:
                            dmg = 0
                    elif number < int(enemy_speed)*2:
                        dmg = 0 
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Fury Strike", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 15
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        furycooldown = 4
                        skillused = ""
                        numset = False
                if skillused == "Overcharge" and myself_mana >= 50 and overchargecooldown == 0:
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+OVERCHARGED!", 1, LIGHTBLUE), (selfpos.x, selfpos.y - 100))
                        game.blit(comicsans(20).render("You used: Overcharge", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        myself_mana = myself_mana - 50
                        if myself_mana < 0:
                            myself_mana = 0
                        overchargecooldown = 8
                        overcharge = 3
                        myself_power = myself.retrievestat("strength") * 1.5
                        myself_magic = myself.retrievestat("magic") * 1.5
                        skillused = ""
                        numset = False
                if skillused == "Poison" and myself_mana >= 30 and poisoncooldown == 0:
                    dmg = round(int(myself_magic) * 3, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if amputate > 0:
                        if number < round(int(enemy_speed) * 0.8, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Poison", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 30
                        if enemy_health < 0:
                            enemy_health = 0
                        if myself_mana < 0:
                            myself_mana = 0
                        if dmg != 0:
                            poison = 4
                        poisoncooldown = 7
                        skillused = ""
                        numset = False
                if skillused == "Shuriken" and myself_mana >= 20 and shurikencooldown == 0:
                    dmg = round(int(myself_power) * 2.1, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if amputate > 0:
                        if number < round(int(enemy_speed) * 0.45, 0):
                            dmg = 0
                    elif number < round(int(enemy_speed) * 0.55, 0):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Shuriken", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 20
                        if enemy_health < 0:
                            enemy_health = 0
                        if myself_mana < 0:
                            myself_mana = 0
                        shurikencooldown = 4
                        skillused = ""
                        numset = False
                if skillused == "Slash" and myself_mana >= 30 and slashcooldown == 0:
                    dmg = round(int(myself_power) * 2.5, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if amputate > 0:
                        if number < round(int(enemy_speed) * 0.8, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Slash!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - dmg
                        if enemy_health < 0:
                            enemy_health = 0
                        if myself_mana < 0:
                            myself_mana = 0
                        slashcooldown = 5
                        skillused = ""
                        numset = False
                if skillused == "Speed" and myself_mana >= 50 and speedcooldown == 0:
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+SPEED!", 1, LIGHTBLUE), (selfpos.x, selfpos.y-100))
                        game.blit(comicsans(20).render("You used: Speed!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        myself_mana = myself_mana - 50
                        if myself_mana < 0:
                            myself_mana = 0
                        speedcooldown = 10
                        myself_speed = 100
                        skillused = ""
                        numset = False

                    
                    

            
            if enemy_health <= 0: #winning screen
                blackscreen = pygame.Rect(0,0, _width_, _height_)
                pygame.draw.rect(game, BLACK, blackscreen)
                game.blit(comicsans(20).render("You won!", 1, GREEN), (_width_/2, 100))
                experience_bar = pygame.Rect((_width_/2)-100, 200, 300, 15)
                pygame.draw.rect(game, DARKERGRAY, experience_bar)
                pygame.draw.rect(game, GREEN, pygame.Rect((_width_/2)-100, 200, 300 * xp_slider, 15)) ##xp animation bar
                if xp_slider >= 1.00:
                    game.blit(comicsans(15).render("Levelled Up!", 1, FOCUS), (_width_/2, 150))
                    game.blit(comicsans(15).render("Your Level: " + str(int(data["level:"]) + 1), 1, WHITE), (_width_/2, 175))
                else:
                    game.blit(comicsans(15).render("Your Level: " + str(data["level:"]), 1, WHITE), ((_width_/2)-100, 150))
                    game.blit(comicsans(12).render("EXP: " + str(data["experience:"]) + " / " + str(data["experience_to_next_level:"]), 1, WHITE), ((_width_/2)+125, 150))
                if xp_gained < 101:
                    xp_gained += 1
                    data["experience:"] = str(int(data["experience:"])+1)
                    xp_slider = int(data["experience:"])/int(data["experience_to_next_level:"])
                pygame.draw.rect(game, LIGHTGRAY, gotocampbtn)
                pygame.draw.rect(game, LIGHTGRAY, returnbutton)
                if returnbutton.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(game, WHITE, returnbutton)
                if gotocampbtn.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(game, WHITE, gotocampbtn)
                game.blit(comicsans(20).render("Return to Menu", 1, BLACK), (returnbutton.x, returnbutton.y))
                game.blit(comicsans(20).render("Go To Camp", 1, BLACK), (gotocampbtn.x, gotocampbtn.y))




            if myself_health <= 0: #losing screen
                blackscreen = pygame.Rect(0, 0, _width_, _height_)
                pygame.draw.rect(game, BLACK, blackscreen)
                game.blit(comicsans(20).render("You've lost!", 1, RED), (_width_/2, 100))
                pygame.draw.rect(game, LIGHTGRAY, restartbutton)
                if restartbutton.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(game, WHITE, restartbutton)
                game.blit(comicsans(20).render("Restart Battle", 1, BLACK), (restartbutton.x+10, restartbutton.y))

                pygame.draw.rect(game, LIGHTGRAY, returnbutton)
                if returnbutton.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(game, WHITE, returnbutton)
                game.blit(comicsans(20).render("Return To Menu", 1, BLACK), (returnbutton.x, returnbutton.y))
                game.blit(transform(_skull_icon_, (128,128)), (_width_/2, 200))

        if _cur_screen_ == "Level 3":
            game.blit(transform(_zone1_bg_, (_width_, _height_)), (0,-100))
            ##create characters##
            if battlebegin == False:
                myself = YourChar(data["chartype:"], int(data["vitality:"]), int(data["strength:"]), int(data["magic:"]), int(data["speed:"]), int(data["level:"]), int(data["skillpoints:"]), int(data["attributepoints:"]), int(data["experience:"]), int(data["experience_to_next_level:"]))
                myself_max_health = 100 + (myself.retrievestat("hp") * myself.retrievestat("strength"))
                myself_health = myself_max_health
                myself_max_mana = 50 + (myself.retrievestat("magic") * 2)
                myself_mana = myself_max_mana
                myself_power = myself.retrievestat("strength")
                myself_speed = myself.retrievestat("speed")
                myself_magic = myself.retrievestat("magic")
            ##add bottom part##
            footer = pygame.Rect(0, _height_-150, _width_, 150)
            pygame.draw.rect(game, DARKERGRAY, footer)
            _final_icon_ = _char_icon_knight_ if data["chartype:"] == "Knight" else _char_icon_wizard_ if data["chartype:"] == "Wizard" else _char_icon_assassin_
            _final_char_ = _char_knight_ if data["chartype:"] == "Knight" else _char_wizard_ if data["chartype:"] == "Wizard" else _char_assassin_
            heightvar = 320 if data["chartype:"] == "Knight" else 320 if data["chartype:"] == "Wizard" else 320
            selffix = pygame.Rect(50, _height_-100, 64, 64)
            game.blit(transform(_final_icon_, (64,64)), (50, _height_-100))

            if selffix.collidepoint(pygame.mouse.get_pos()): #hover over icon to see your own stats
                square = pygame.Rect(0, _height_-200, 100, 100)
                pygame.draw.rect(game, LIGHTGRAY, square)
                yourvitals = comicsans(9).render("Vitality: " + str(data["vitality:"]), 1, BLACK)
                yourstrength = comicsans(9).render("Strength: " + str(data["strength:"]), 1, BLACK)
                yourmagic = comicsans(9).render("Magic: " + str(data["magic:"]), 1, BLACK)
                yourspeed = comicsans(9).render("Speed: " + str(data["speed:"]), 1, BLACK)
                yourstats = comicsans(10).render("Your Stats: ", 1, BLACK)
                game.blit(yourstats, (square.x, square.y))
                game.blit(yourvitals, (square.x, square.y + 20))
                game.blit(yourstrength, (square.x, square.y + 30))
                game.blit(yourmagic, (square.x, square.y + 40))
                game.blit(yourspeed, (square.x, square.y + 50))
            selfpos = pygame.Rect(100, heightvar, 128, 128)
            game.blit(transform(_final_char_, (128,128)), (selfpos.x, selfpos.y))
            healthbarunder = pygame.Rect(120, _height_-85, 100, 10)
            pygame.draw.rect(game, DARKGREEN, healthbarunder)
            healthbarover = pygame.Rect(120, _height_-85, round(100 * (myself_health/myself_max_health), 0), 10)
            pygame.draw.rect(game, GREEN, healthbarover)
            displayhealth = comicsans(10).render("HP: " + str(myself_health), 1, WHITE)
            game.blit(displayhealth, (120,_height_-100))

            manabarunder = pygame.Rect(120, _height_-60, 100, 10)
            pygame.draw.rect(game, DARKERBLUE, manabarunder)
            manabarover = pygame.Rect(120, _height_-60, round(100 * (myself_mana/myself_max_mana), 0), 10)
            pygame.draw.rect(game, LIGHTBLUE, manabarover)
            displaymana = comicsans(10).render("MP: " + str(myself_mana), 1, WHITE)
            game.blit(displaymana, (120, _height_-75))

            ##add skills section##
            pygame.draw.rect(game, DARKGRAY, skill1)
            pygame.draw.rect(game, DARKGRAY, skill2)
            pygame.draw.rect(game, DARKGRAY, skill3)
            pygame.draw.rect(game, DARKGRAY, skill4)
            pygame.draw.rect(game, DARKGRAY, skill5)
            pygame.draw.rect(game, DARKGRAY, skill6)
            pygame.draw.rect(game, DARKGRAY, skill7)
            pygame.draw.rect(game, DARKGRAY, skill8)
            pygame.draw.rect(game, DARKGRAY, skill9)
            pygame.draw.rect(game, DARKGRAY, skill10)
            #add hover effect to skills to show user that they are currently selecting that skill
            if skill1.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill1)
            if skill2.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill2)
            if skill3.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill3)
            if skill4.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill4)
            if skill5.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill5)
            if skill6.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill6)
            if skill7.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill7)
            if skill8.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill8)
            if skill9.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill9)
            if skill10.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill10)
            #add skill images where applicable
            game.blit(transform(skill1_img, (32,32)), (skill1.x, skill1.y))
            game.blit(transform(skill2_img, (32,32)), (skill2.x, skill2.y))
            game.blit(transform(skill3_img, (32,32)), (skill3.x, skill3.y))
            game.blit(transform(skill4_img, (32,32)), (skill4.x, skill4.y))
            game.blit(transform(skill5_img, (32,32)), (skill5.x, skill5.y))
            game.blit(transform(skill6_img, (32,32)), (skill6.x, skill6.y))
            game.blit(transform(skill7_img, (32,32)), (skill7.x, skill7.y))
            game.blit(transform(skill8_img, (32,32)), (skill8.x, skill8.y))
            game.blit(transform(skill9_img, (32,32)), (skill9.x, skill9.y))
            game.blit(transform(skill10_img, (32,32)), (skill10.x, skill10.y))
            

            ##draw enemy
            enemy = Enemy("The Broken One", _l3_icon_, _l3_enemy_, 25, 20, 10, 1, ["Basic Attack", "Super Punch", "Enrage Punch"])
            tutfix = pygame.Rect(_width_-110, _height_-100, 64, 64)
            game.blit(transform(_l3_icon_, (64,64)), (_width_-110, _height_-100))
            enemypos = pygame.Rect(_width_-200, 320, 128, 128)
            game.blit(transform(_l3_enemy_, (128,128)), (enemypos.x, enemypos.y))
            if battlebegin == False:
                enemy_max_health = 100 + (enemy.get("hp") * enemy.get("strength"))
                enemy_health = enemy_max_health
                enemy_max_mana = 50 + (enemy.get("magic") * 2)
                enemy_mana = enemy_max_mana
                enemy_power = enemy.get("strength")
                enemy_speed = enemy.get("speed")
                battlebegin = True #set true once both players have initialised stats
            enemyhealthbarunder = pygame.Rect(_width_-220, _height_-85, 100, 10)
            enemyhealthbarover = pygame.Rect(_width_-220, _height_-85, round(100 * (enemy_health/enemy_max_health), 0), 10)
            displayenemyhealth = comicsans(10).render("HP: " + str(enemy_health), 1, WHITE)
            pygame.draw.rect(game, DARKGREEN, enemyhealthbarunder)
            pygame.draw.rect(game, GREEN, enemyhealthbarover)
            game.blit(displayenemyhealth, (_width_-170, _height_-100))
            enemymanabarunder = pygame.Rect(_width_-220, _height_-60, 100, 10)
            enemymanabarover = pygame.Rect(_width_-220, _height_-60, round(100 * (enemy_mana/enemy_max_mana), 0), 10)
            displayenemymana = comicsans(10).render("MP: " + str(enemy_mana), 1, WHITE)
            pygame.draw.rect(game, DARKERBLUE, enemymanabarunder)
            pygame.draw.rect(game, LIGHTBLUE, enemymanabarover)
            game.blit(displayenemymana, (_width_-170, _height_-75))
            if tutfix.collidepoint(pygame.mouse.get_pos()):
                square2 = pygame.Rect(_width_-100, _height_-200, 100, 100)
                pygame.draw.rect(game, LIGHTGRAY, square2)
                enemyvitals = comicsans(9).render("Vitality: " + str(enemy.get("hp")), 1, BLACK)
                enemystrength = comicsans(9).render("Strength: " + str(enemy.get("strength")), 1, BLACK)
                enemymagic = comicsans(9).render("Magic: " + str(enemy.get("magic")), 1, BLACK)
                enemyspeed = comicsans(9).render("Speed: " + str(enemy.get("speed")), 1, BLACK)
                enemystats = comicsans(9).render("Enemy Stats: ", 1, BLACK)
                game.blit(enemystats, (square2.x, square2.y))
                game.blit(enemyvitals, (square2.x, square2.y + 20))
                game.blit(enemystrength, (square2.x, square2.y + 30))
                game.blit(enemymagic, (square2.x, square2.y + 40))
                game.blit(enemyspeed, (square2.x, square2.y + 50))

            ##draw area to exit##
            pygame.draw.rect(game, LIGHTGRAY, exiticon)
            pygame.draw.circle(game, (200,0,0), (exiticon.x + 32, exiticon.y + 32), 32)
            game.blit(comicsans(40).render("X", 1, WHITE), (exiticon.x + 18, exiticon.y + 1))
            if exiticon.collidepoint(pygame.mouse.get_pos()): #hover effect
                pygame.draw.rect(game, WHITE, exiticon)
                pygame.draw.circle(game, (150,0,0), (exiticon.x + 32, exiticon.y + 32), 32)
                game.blit(comicsans(40).render("X", 1, WHITE), (exiticon.x + 18, exiticon.y + 1))    
            ##draw text to identify current turn##
            turn = comicsans(20).render("Your Turn!" if curTurn == "Self" else "Enemy Turn!", 1, WHITE)
            game.blit(turn, (exiticon.x-20, exiticon.y-30)) 

            ## battle code for the enemy

            if curTurn == "Enemy" and battlebegin == True and enemy_health > 0:
                if stun > 0:
                    canattack = False
                    stun -= 1
                    if stun < 0:
                        stun = 0
                    curTurn = "Self"
                    enemyset = False
                    numset = False
                    skillused = ""

                if freeze > 0:
                    canattack = False
                    freeze -= 1
                    if freeze < 0:
                        freeze = 0
                    curTurn = "Self"
                    enemyset = False
                    numset = False
                    skillused = ""

                if lightning > 0:
                    canttack = False
                    lightning -= 1
                    if lightning < 0:
                        lightning = 0
                    curTurn = "Self"
                    enemyset = False
                    numset = False
                    skillused = ""


                if enemyset == False:
                    enemy_skills = enemy.get("abilities")
                    ranvalue = random.randint(0, len(enemy_skills)-1) #roll a random move for basic tier enemies so its automatic
                    ##check if enough mana
                    if enemy_skills[ranvalue] == "Basic Attack":
                        enemyset = True
                    if enemy_skills[ranvalue] == "Power Slash" and enemy_mana >= 15:
                        enemyset = True
                    
                if enemy_skills[ranvalue] == "Basic Attack" and canattack == True:
                    dmg = round(int(enemy_power)*1.5, 0)
                    ##chance to miss target based on target speed##
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if number < int(myself_speed): #if roll is less than target speed, means you are slower.
                        dmg = 0
                    elif shield == True:
                        dmg = round(int(enemy_power)*(0.75 - (myself_power*0.01)), 0)
                    elif suit > 0 and shield == False:
                        dmg = round(int(enemy_power)*(1.15),0)
                    elif suit > 0 and shield == True:
                        dmg = round(int(enemy_power) * ( 0.65 - (myself_power * 0.01)), 0)
                    elif weakness > 0:
                        dmg = round(dmg*0.1, 0)
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render(("-" if invert == 0 else "+") + str(dmg) if dmg != 0 else "MISSED!", 1, RED if invert == 0 else GREEN), (selfpos.x, selfpos.y - 100))
                        print("Enemy dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("Enemy used: Basic Attack", 1, WHITE), (_width_/2, 100))

                        if fire > 0:
                            burn = round(int(myself_magic) * 2, 0)
                            game.blit(comicsans(20).render("-" + str(burn), 1, RED), (enemypos.x, enemypos.y - 100))
                        if dragon > 0:
                            burn = round(int(myself_magic) * 1.5, 0)
                            game.blit(comicsans(20).render("-" + str(burn), 1, RED), (enemypos.x, enemypos.y - 100))
                        if poison > 0:
                            burn = round(int(myself_magic) * 1.5, 0)
                            game.blit(comicsans(20).render("-" + str(burn), 1, RED), (enemypos.x, enemypos.y - 100))
                    if counter == 70:
                        curTurn = "Self"
                        counter = 0
                        myself_health = myself_health - dmg if invert == 0 else myself_health + dmg
                        if myself_health < 0:
                            myself_health = 0
                        if myself_health > myself_max_health:
                            myself_health = myself_max_health
                            
                        enemy_mana = enemy_mana + round(enemy_max_mana*0.1,0)
                        if enemy_mana > enemy_max_mana:
                            enemy_mana = enemy_max_mana
                        if fire > 0:
                            enemy_health = enemy_health - burn
                            if enemy_health < 0:
                                enemy_health = 0
                        if dragon > 0:
                            enemy_health = enemy_health - burn
                            if enemy_health < 0:
                                enemy_health = 0
                        if poison > 0:
                            enemy_health = enemy_health - burn
                            if enemy_health < 0:
                                enemy_health = 0
                        if life > 0:
                            myself_health = myself_health + round(myself_max_health * 0.1, 0)
                            if myself_health > myself_max_health:
                                myself_health = myself_max_health
                        enemyset = False
                        numset = False
                        shieldcooldown-=1
                        shieldcount-=1
                        bscooldown -= 1
                        bscount -= 1
                        dbcooldown -= 1
                        punccooldown -= 1
                        punc -= 1
                        slamdown -= 1
                        suit -= 1
                        suitcooldown -= 1 
                        enrage -= 1
                        enragecooldown -= 1
                        fire -= 1
                        fireballcooldown -= 1
                        freeze -= 1
                        freezecooldown -= 1
                        draincooldown -= 1
                        invert -= 1
                        invertcooldown -= 1
                        leechcooldown -= 1
                        life -= 1
                        lifecooldown -= 1
                        lightningcooldown -= 1
                        lightning -= 1
                        soul -= 1
                        soulcooldown -= 1
                        weakness -= 1
                        weaknesscooldown -= 1
                        amputate -= 1
                        amputatecooldown -= 1
                        dragon -= 1
                        dragoncooldown -= 1
                        overcharge -= 1
                        overchargecooldown -= 1
                        poison -= 1
                        poisoncooldown -= 1
                        shurikencooldown -= 1
                        slashcooldown -= 1
                        speedcooldown -= 1
                        if shieldcooldown < 0:
                            shieldcooldown = 0
                        if shieldcount < 0:
                            shieldcount = 0
                            shield = False
                        if bscooldown < 0:
                            bscooldown = 0
                        if bscount < 0:
                            bscount = 0
                        if dbcooldown < 0:
                            dbcooldown = 0
                        if punccooldown < 0:
                            punccooldown = 0
                        if punc < 0:
                            punc = 0
                        if slamdown < 0:
                            slamdown = 0
                        if suit < 0:
                            suit = 0
                        if suitcooldown < 0:
                            suitcooldown = 0
                        if enrage < 0:
                            enrage = 0
                        if enragecooldown < 0:
                            enragecooldown = 0
                        if enrage == 0:
                            myself_power = myself.retrievestat("strength")
                        if fire == 0:
                            fire = 0
                        if fireballcooldown == 0:
                            fireballcooldown = 0
                        if freeze < 0:
                            freeze = 0
                        if freezecooldown < 0:
                            freezecooldown = 0
                        if draincooldown < 0:
                            draincooldown = 0
                        if invert < 0:
                            invert = 0
                        if invertcooldown < 0:
                            invertcooldown = 0
                        if leechcooldown < 0:
                            leechcooldown = 0
                        if life < 0:
                            life = 0
                        if lifecooldown < 0:
                            lifecooldown = 0
                        if lightningcooldown == 0:
                            lightningcooldown = 0
                        if lightning == 0:
                            lightning = 0
                        if soul < 0:
                            soul = 0
                        if soulcooldown < 0:
                            soulcooldown = 0
                        if weakness < 0:
                            weakness = 0
                        if weakness == 0:
                            myself_power = myself.retrievestat("strength")
                            myself_magic = myself.retrievestat("magic")
                        if weaknesscooldown < 0:
                            weaknesscooldown = 0
                        if amputate < 0:
                            amputate = 0
                        if amputatecooldown < 0:
                            amputatecooldown = 0
                        if dragon < 0:
                            dragon = 0
                        if dragoncooldown < 0:
                            dragoncooldown = 0
                        if overcharge < 0:
                            overcharge = 0
                        if overcharge == 0:
                            myself_power = myself.retrievestat("strength")
                            myself_magic = myself.retrievestat("magic")
                        if overchargecooldown < 0:
                            overchargecooldown = 0
                        if poison < 0:
                            poison = 0
                        if poisoncooldown < 0:
                            poisoncooldown = 0
                        if shurikencooldown < 0:
                            shurikencooldown = 0
                        if slashcooldown < 0:
                            slashcooldown = 0
                        if speedcooldown < 0:
                            speedcooldown = 0
                        if speedcooldown == 0:
                            myself_speed = myself.retrievestat("speed")
                
                if enemy_skills[ranvalue] == "Super Punch" and enemy_mana >= 15 and canattack == True: 
                    dmg = round(int(enemy_power)*2.25, 0)
                    if numset == False:
                        number = random.randint(0,100)
                        numset = True
                    if number < int(myself_speed):
                        dmg = 0
                    elif shield == True:
                        dmg = round(int(enemy_power) * (1.125 - (myself_power*0.01)), 0)
                    elif suit > 0 and shield == False:
                        dmg = round(int(enemy_power) * (1.75), 0)
                    elif suit > 0 and shield == True:
                        dmg = round(int(enemy_power) * (0.975 - (myself_power * 0.01)), 0)
                    elif weakness > 0:
                        dmg = round(dmg * 0.1, 0)
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render(("-" if invert == 0 else "+") + str(dmg) if dmg != 0 else "MISSED!", 1, RED if invert == 0 else GREEN), (selfpos.x, selfpos.y - 100))
                        print("Enemy dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("Enemy used: Power Slash", 1, WHITE), (_width_/2, 100))
                        if fire > 0:
                            burn = round(int(myself_magic) * 2, 0)
                            game.blit(comicsans(20).render("-" + str(burn), 1, RED), (enemypos.x, enemypos.y - 100))
                        if dragon > 0:
                            burn = round(int(myself_magic) * 1.5, 0)
                            game.blit(comicsans(20).render("-" + str(burn), 1, RED), (enemypos.x, enemypos.y - 100))
                        if poison > 0:
                            burn = round(int(myself_magic) * 1.5, 0)
                            game.blit(comicsans(20).render("-" + str(burn), 1, RED), (enemypos.x, enemypos.y - 100))
                    if counter == 70:
                        curTurn = "Self"
                        counter = 0
                        myself_health = myself_health - dmg if invert == 0 else myself_health + dmg
                        if myself_health > myself_max_health:
                            myself_health = myself_max_health
                        if myself_health < 0:
                            myself_health = 0
                        enemy_mana = enemy_mana - 15
                        if enemy_mana < 0:
                            enemy_mana = 0
                        if fire > 0:
                            enemy_health = enemy_health - burn
                            if enemy_health < 0:
                                enemy_health = 0
                        if dragon > 0:
                            enemy_health = enemy_health - burn
                            if enemy_health < 0:
                                enemy_health = 0
                        if poison > 0:
                            enemy_health = enemy_health - burn
                            if enemy_health < 0:
                                enemy_health = 0
                        if life > 0:
                            myself_health = myself_health + round(myself_max_health * 0.1, 0)
                            if myself_health > myself_max_health:
                                myself_health = myself_max_health
                        enemyset = False
                        numset = False
                        shieldcooldown-=1
                        shieldcount-=1
                        bscooldown-=1
                        bscount -= 1 
                        dbcooldown -= 1
                        punccooldown -= 1
                        punc -= 1
                        slamdown -= 1
                        suit -= 1
                        suitcooldown -= 1
                        fire -= 1
                        fireballcooldown -= 1
                        freeze -= 1
                        freezecooldown -= 1
                        draincooldown -= 1
                        invert -= 1
                        invertcooldown -= 1
                        leechcooldown -= 1
                        lifecooldown -= 1
                        life -= 1
                        lightningcooldown -= 1
                        lightning -= 1
                        soul -= 1
                        soulcooldown -= 1
                        weakness -= 1
                        weaknesscooldown -= 1
                        amputate -= 1
                        amputatecooldown -= 1
                        dragon -= 1
                        dragoncooldown -= 1
                        overcharge -= 1
                        overchargecooldown -= 1
                        poison -= 1
                        poisoncooldown -= 1
                        shurikencooldown -= 1
                        slashcooldown -= 1
                        speedcooldown -= 1
                        if shieldcooldown < 0:
                            shieldcooldown = 0
                        if shieldcount < 0:
                            shieldcount = 0
                            shield = False
                        if bscooldown < 0:
                            bscooldown = 0
                        if bscount < 0:
                            bscount = 0
                        if dbcooldown < 0:
                            dbcooldown = 0
                        if punccooldown < 0:
                            punccooldown = 0
                        if punc < 0:
                            punc = 0
                        if slamdown < 0:
                            slamdown = 0
                        if suit < 0:
                            suit = 0
                        if suitcooldown < 0:
                            suitcooldown = 0
                        if enrage < 0:
                            enrage = 0
                        if enragecooldown < 0:
                            enragecooldown = 0
                        if enrage == 0:
                            myself_power = myself.retrievestat("strength")
                        if fire < 0:
                            fire = 0
                        if fireballcooldown < 0:
                            fireballcooldown = 0
                        if freeze < 0:
                            freeze = 0
                        if freezecooldown < 0:
                            freezecooldown = 0
                        if draincooldown < 0:
                            draincooldown = 0
                        if invert < 0:
                            invert = 0
                        if invertcooldown < 0:
                            invertcooldown = 0
                        if leechcooldown < 0:
                            leechcooldown = 0
                        if life < 0:
                            life = 0
                        if lifecooldown < 0:
                            lifecooldown = 0
                        if lightningcooldown < 0:
                            lightningcooldown -= 1
                        if lightning == 1:
                            lightning = 0
                        if soul < 0:
                            soul = 0
                        if soulcooldown < 0:
                            soulcooldown = 0
                        if weakness == 0:
                            myself_power = myself.retrievestat("strength")
                            myself_magic = myself.retrievestat("magic")
                        if weakness < 0:
                            weakness = 0
                        if weaknesscooldown < 0:
                            weaknesscooldown = 0
                        if amputate < 0:
                            amputate = 0
                        if amputatecooldown < 0:
                            amputatecooldown = 0
                        if dragon < 0:
                            dragon = 0
                        if dragoncooldown < 0:
                            dragoncooldown = 0
                        if overcharge < 0:
                            overcharge = 0
                        if overcharge == 0:
                            myself_power = myself.retrievestat("strength")
                            myself_magic = myself.retrievestat("magic")
                        if overchargecooldown < 0:
                            overchargecooldown = 0
                        if poison < 0:
                            poison = 0
                        if poisoncooldown < 0:
                            poisoncooldown = 0
                        if shurikencooldown < 0:
                            shurikencooldown = 0
                        if slashcooldown < 0:
                            slashcooldown = 0
                        if speedcooldown == 0:
                            myself_speed = myself.retrievestat("speed")
                        if speedcooldown < 0:
                            speedcooldown = 0
                if enemy_skills[ranvalue] == "Enrage Punch" and enemy_mana >= 35 and canattack == True: 
                    dmg = round(int(enemy_power)*3.25, 0)
                    if numset == False:
                        number = random.randint(0,100)
                        numset = True
                    if number < int(myself_speed):
                        dmg = 0
                    elif shield == True:
                        dmg = round(int(enemy_power) * (1.125 - (myself_power*0.01)), 0)
                    elif suit > 0 and shield == False:
                        dmg = round(int(enemy_power) * (1.75), 0)
                    elif suit > 0 and shield == True:
                        dmg = round(int(enemy_power) * (0.975 - (myself_power * 0.01)), 0)
                    elif weakness > 0:
                        dmg = round(dmg * 0.1, 0)
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render(("-" if invert == 0 else "+") + str(dmg) if dmg != 0 else "MISSED!", 1, RED if invert == 0 else GREEN), (selfpos.x, selfpos.y - 100))
                        print("Enemy dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("Enemy used: Power Slash", 1, WHITE), (_width_/2, 100))
                        if fire > 0:
                            burn = round(int(myself_magic) * 2, 0)
                            game.blit(comicsans(20).render("-" + str(burn), 1, RED), (enemypos.x, enemypos.y - 100))
                        if dragon > 0:
                            burn = round(int(myself_magic) * 1.5, 0)
                            game.blit(comicsans(20).render("-" + str(burn), 1, RED), (enemypos.x, enemypos.y - 100))
                        if poison > 0:
                            burn = round(int(myself_magic) * 1.5, 0)
                            game.blit(comicsans(20).render("-" + str(burn), 1, RED), (enemypos.x, enemypos.y - 100))
                    if counter == 70:
                        curTurn = "Self"
                        counter = 0
                        myself_health = myself_health - dmg if invert == 0 else myself_health + dmg
                        if myself_health > myself_max_health:
                            myself_health = myself_max_health
                        if myself_health < 0:
                            myself_health = 0
                        enemy_mana = enemy_mana - 15
                        if enemy_mana < 0:
                            enemy_mana = 0
                        if fire > 0:
                            enemy_health = enemy_health - burn
                            if enemy_health < 0:
                                enemy_health = 0
                        if dragon > 0:
                            enemy_health = enemy_health - burn
                            if enemy_health < 0:
                                enemy_health = 0
                        if poison > 0:
                            enemy_health = enemy_health - burn
                            if enemy_health < 0:
                                enemy_health = 0
                        if life > 0:
                            myself_health = myself_health + round(myself_max_health * 0.1, 0)
                            if myself_health > myself_max_health:
                                myself_health = myself_max_health
                        enemyset = False
                        numset = False
                        shieldcooldown-=1
                        shieldcount-=1
                        bscooldown-=1
                        bscount -= 1 
                        dbcooldown -= 1
                        punccooldown -= 1
                        punc -= 1
                        slamdown -= 1
                        suit -= 1
                        suitcooldown -= 1
                        fire -= 1
                        fireballcooldown -= 1
                        freeze -= 1
                        freezecooldown -= 1
                        draincooldown -= 1
                        invert -= 1
                        invertcooldown -= 1
                        leechcooldown -= 1
                        lifecooldown -= 1
                        life -= 1
                        lightningcooldown -= 1
                        lightning -= 1
                        soul -= 1
                        soulcooldown -= 1
                        weakness -= 1
                        weaknesscooldown -= 1
                        amputate -= 1
                        amputatecooldown -= 1
                        dragon -= 1
                        dragoncooldown -= 1
                        overcharge -= 1
                        overchargecooldown -= 1
                        poison -= 1
                        poisoncooldown -= 1
                        shurikencooldown -= 1
                        slashcooldown -= 1
                        speedcooldown -= 1
                        if shieldcooldown < 0:
                            shieldcooldown = 0
                        if shieldcount < 0:
                            shieldcount = 0
                            shield = False
                        if bscooldown < 0:
                            bscooldown = 0
                        if bscount < 0:
                            bscount = 0
                        if dbcooldown < 0:
                            dbcooldown = 0
                        if punccooldown < 0:
                            punccooldown = 0
                        if punc < 0:
                            punc = 0
                        if slamdown < 0:
                            slamdown = 0
                        if suit < 0:
                            suit = 0
                        if suitcooldown < 0:
                            suitcooldown = 0
                        if enrage < 0:
                            enrage = 0
                        if enragecooldown < 0:
                            enragecooldown = 0
                        if enrage == 0:
                            myself_power = myself.retrievestat("strength")
                        if fire < 0:
                            fire = 0
                        if fireballcooldown < 0:
                            fireballcooldown = 0
                        if freeze < 0:
                            freeze = 0
                        if freezecooldown < 0:
                            freezecooldown = 0
                        if draincooldown < 0:
                            draincooldown = 0
                        if invert < 0:
                            invert = 0
                        if invertcooldown < 0:
                            invertcooldown = 0
                        if leechcooldown < 0:
                            leechcooldown = 0
                        if life < 0:
                            life = 0
                        if lifecooldown < 0:
                            lifecooldown = 0
                        if lightningcooldown < 0:
                            lightningcooldown -= 1
                        if lightning == 1:
                            lightning = 0
                        if soul < 0:
                            soul = 0
                        if soulcooldown < 0:
                            soulcooldown = 0
                        if weakness == 0:
                            myself_power = myself.retrievestat("strength")
                            myself_magic = myself.retrievestat("magic")
                        if weakness < 0:
                            weakness = 0
                        if weaknesscooldown < 0:
                            weaknesscooldown = 0
                        if amputate < 0:
                            amputate = 0
                        if amputatecooldown < 0:
                            amputatecooldown = 0
                        if dragon < 0:
                            dragon = 0
                        if dragoncooldown < 0:
                            dragoncooldown = 0
                        if overcharge < 0:
                            overcharge = 0
                        if overcharge == 0:
                            myself_power = myself.retrievestat("strength")
                            myself_magic = myself.retrievestat("magic")
                        if overchargecooldown < 0:
                            overchargecooldown = 0
                        if poison < 0:
                            poison = 0
                        if poisoncooldown < 0:
                            poisoncooldown = 0
                        if shurikencooldown < 0:
                            shurikencooldown = 0
                        if slashcooldown < 0:
                            slashcooldown = 0
                        if speedcooldown == 0:
                            myself_speed = myself.retrievestat("speed")
                        if speedcooldown < 0:
                            speedcooldown = 0
                if freeze == 0:
                    canttack = True
                if stun == 0:
                    canattack = True

            ##battle code for self player

            if curTurn == "Self" and battlebegin == True and myself_health > 0: #design skills via if statements
                if skillused == "Basic_Attack": ## basic attack utilising characters strength
                    dmg = round(int(myself_power)*1.5, 0)
                    if punc > 0:
                        dmg = round(dmg * 1.15, 0)
                    mana_gained = round(int(myself_max_mana)*0.1, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if bscount > 0:
                        if number < round(int(enemy_speed)/1.5, 0):
                            dmg = 0
                    elif soul > 0:
                        if number < round(int(enemy_speed)*0.6, 0):
                            dmg = 0
                    elif amputate > 0:
                        if number < round(int(enemy_speed) * 0.8, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70: ##to add some delay allowing for the game to show the text
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        print("You dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("You used: Basic Attack", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana + mana_gained
                        if myself_mana > myself_max_mana:
                            myself_mana = myself_max_mana

                        #make sure enemy health isnt glitched visually
                        if enemy_health < 0: #if enemy is killed
                            enemy_health = 0
                        skillused = "" # reset the skills
                        numset = False

                if skillused == "Heal" and myself_mana >= 20: #check for mana to be filled
                    heal = round(int(myself_max_health * (0.5 + myself.retrievestat("magic")/100)))
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+" + str(heal), 1, GREEN), (selfpos.x, selfpos.y - 100))
                        print("You healed yourself for: " + str(heal) + " HP!")
                        game.blit(comicsans(20).render("You used: Healing", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        myself_health = myself_health + heal
                        if myself_health > myself_max_health: ##prevent over healing
                            myself_health = myself_max_health
                        myself_mana = myself_mana - 20
                        if myself_mana < 0:
                            myself_mana = 0
                        skillused = ""

                if skillused == "Mana" and myself_mana >= 10:
                    mana = round(int(myself_max_mana * (0.6 + myself.retrievestat("magic")/100)))
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+" + str(mana), 1, LIGHTBLUE), (selfpos.x, selfpos.y - 100))
                        print("You gained " + str(mana) + " MP!")
                        game.blit(comicsans(20).render("You used: Mana", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        myself_mana = myself_mana + mana - 10
                        if myself_mana > myself_max_mana:
                            myself_mana = myself_max_mana
                        skillused = ""
                
                #knight skillset
                if skillused == "Slam" and myself_mana >= 15 and slamdown == 0:
                    dmg = round((int(myself_power) + (int(myself_power)*0.25)) * 1.75, 0)
                    if punc > 0:
                        dmg = round(dmg * 1.15, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if bscount > 0:
                        if number < round(int(enemy_speed)/1.5, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y-100))
                        print("You dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("You used: Slam", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 15
                        if myself_mana < 0:
                            myself_mana = 0
                        
                        if enemy_health < 0:
                            enemy_health = 0
                        slamdown = 3
                        skillused = ""
                        numset = False

                if skillused == "Shield" and myself_mana >= 20 and shieldcooldown == 0:
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+SHIELDED!", 1, LIGHTBLUE), (selfpos.x, selfpos.y - 100))
                        print("You used shield!")
                        game.blit(comicsans(20).render("You used: Shield", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        shield = True
                        shieldcount = 2
                        shieldcooldown = 4
                        print(str(shieldcount) + ", " + str(shieldcooldown) + ", " + str(shield))
                        curTurn = "Enemy"
                        counter = 0
                        myself_mana = myself_mana - 20
                        if myself_mana < 0:
                            myself_mana = 0
                        skillused = ""

                if skillused == "Ballistic_Strike" and myself_mana >= 25 and bscooldown == 0:
                    dmg = round((int(myself_power) * 1.75) + (int(myself_power) * 0.3), 0)
                    if punc > 0:
                        dmg = round(dmg * 1.15, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if bscount > 0:
                        if number < round(int(enemy_speed)/1.5, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y-100))
                        print("You dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("You used: Ballistic Strike!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 25
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        bscooldown = 3
                        if dmg != 0: #to ensure that affects only apply if strikes are hit
                            bscount = 2
                        skillused = ""
                        numset = False

                if skillused == "Double_Strike" and myself_mana >= 20 and dbcooldown == 0:
                    dmg = round((int(myself_power) * 3), 0)
                    if punc > 0:
                        dmg = round(dmg * 1.15, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if bscount > 0:
                        if number < round(int(enemy_speed)/1.5, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y-100))
                        print("You dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("You used: Double Strike!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 20
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        dbcooldown = 5
                        skillused = ""
                        numset = False

                if skillused == "Puncture" and myself_mana >= 35 and punccooldown == 0:
                    dmg = round((int(myself_power) * 3.5), 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if bscount > 0:
                        if number < round(int(enemy_speed)/1.5, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        print("You dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("You used: Puncture", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 35
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        punccooldown = 4
                        if dmg != 0:
                            punc = 3
                        skillused = ""
                        numset = False

                if skillused == "Stun" and myself_mana >= 20 and stuncooldown == 0:
                    dmg = round((int(myself_power) * 1.85), 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if bscount > 0:
                        if number < round(int(enemy_speed)/1.5, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        print("You dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("You used: Stun", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 20
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        stuncooldown = 5
                        if dmg != 0:
                            stun = 1
                        skillused = ""
                        numset = False
                
                if skillused == "Suit_Up" and myself_mana >= 40 and suitcooldown == 0:
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+SUITED!", 1, LIGHTBLUE), (selfpos.x, selfpos.y - 100))
                        print("You used: Suit Up!")
                        game.blit(comicsans(20).render("You used: Suit Up!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        suit = 5
                        suitcooldown = 9
                        curTurn = "Enemy"
                        counter = 0
                        myself_mana = myself_mana - 40
                        if myself_mana < 0:
                            myself_mana = 0
                        
                        skillused = ""
                
                if skillused == "Enrage" and myself_mana >= 50 and enragecooldown == 0:
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+ENRAGED!", 1, LIGHTBLUE), (selfpos.x, selfpos.y - 100))
                        print("You used: Enraged!")
                        game.blit(comicsans(20).render("You used: Enraged!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        enrage = 3
                        enragecooldown = 10
                        myself_power = myself.retrievestat("strength") * 2.5
                        curTurn = "Enemy"
                        counter = 0
                        myself_mana = myself_mana - 50
                        if myself_mana < 0:
                            myself_mana = 0

                        skillused = ""
                if skillused == "Vampire_Strike" and myself_mana >= 45 and vampirecooldown == 0:
                    dmg = round((int(myself_power) * 3.75), 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if bscount > 0:
                        if number < round(int(enemy_speed) / 1.5, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        print("You dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("You used: Vampire Strike!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 45
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        vampirecooldown = 4
                        if dmg != 0:
                            myself_health = myself_health + round((dmg * 0.3), 0)
                            if myself_health > myself_max_health:
                                myself_health = myself_max_health
                        skillused = ""
                        numset = False

                ##wizard skillset
                if skillused == "Fireball" and myself_mana >= 20 and fireballcooldown == 0:
                    dmg = round(int(myself_power) * 1.5, 0)
                    dmg = round(dmg + (int(myself_magic)*1.2), 0)
                    if numset == False:
                        number = random.randint(0,100)
                        numset = True
                    if soul > 0:
                        if number < round(int(enemy_speed)*0.6, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        print("You dealt " + str(dmg) + " DMG!")
                        game.blit(comicsans(20).render("You used: Fireball!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 20
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        if dmg != 0:
                            fire = 2
                        fireballcooldown = 4
                        skillused = ""
                        numset = False

                if skillused == "Freeze" and myself_mana >= 25 and freezecooldown == 0:
                        dmg = round(int(myself_magic) * 1.25, 0)
                        if numset == False:
                            number = random.randint(0, 100)
                            numset = True
                        if soul > 0:
                            if number < round(int(enemy_speed)*0.6, 0):
                                dmg = 0
                        elif number < int(enemy_speed):
                            dmg = 0
                        if counter != 70:
                            counter += 1
                            game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                            game.blit(comicsans(20).render("You used: Freeze", 1, WHITE), (_width_/2, 100))
                        if counter == 70:
                            curTurn = "Enemy"
                            counter = 0
                            enemy_health = enemy_health - dmg
                            myself_mana = myself_mana - 25
                            if myself_mana < 0:
                                myself_mana = 0
                            if enemy_health < 0:
                                enemy_health = 0
                            if dmg != 0:
                                freeze = 2
                            freezecooldown = 5
                            skillused = ""
                            numset = False

                if skillused == "Drain" and myself_mana >= 15 and draincooldown == 0:
                    drain = round(enemy_mana / 2, 0)
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(drain) + "MP!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Drain", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_mana = enemy_mana - drain
                        if enemy_mana < 0:
                            enemy_mana = 0
                        myself_mana = myself_mana - 15
                        if myself_mana < 0:
                            myself_mana = 0
                        myself_mana = myself_mana + drain
                        if myself_mana > myself_max_mana:
                            myself_mana = myself_max_mana
                        skillused = ""
                        numset = False
                        draincooldown = 4
                
                if skillused == "Invert" and myself_mana >= 35 and invertcooldown == 0:
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("INVERTED!", 1, RED), (enemypos.x, enemypos.y-100))
                        game.blit(comicsans(20).render("You used: Inverted!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        myself_mana = myself_mana - 35
                        if myself_mana < 0:
                            myself_mana = 0
                        skillused = ""
                        numset = False
                        invertcooldown = 6
                        invert = 1

                if skillused == "Leech" and myself_mana >= 45 and leechcooldown == 0:
                    hp = round(enemy_health * 0.2, 0)
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(hp), 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Leech", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - hp
                        myself_mana = myself_mana - 45
                        myself_health = myself_health + hp
                        if myself_health > 0:
                            myself_health = myself_max_health
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        leechcooldown = 5
                        skillused = ""
                        numset = False

                if skillused == "Life" and myself_mana >= 40 and lifecooldown == 0:
                    hp = round(myself_max_health * 0.1, 0)
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+" + str(hp), 1, GREEN), (selfpos.x, selfpos.y - 100))
                        game.blit(comicsans(20).render("You used: Life", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        myself_health = myself_health + hp
                        if myself_health > 0:
                            myself_health = myself_max_health
                        myself_mana = myself_mana - 40
                        if myself_mana < 0:
                            myself_mana = 0
                        lifecooldown = 8
                        life = 5
                        skillused = ""
                        numset = False
                if skillused == "Lightning_Strike" and myself_mana >= 30 and lightningcooldown == 0:
                    dmg = round(int(myself_magic) * 4.5, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if soul > 0:
                        if number < round(int(enemy_speed)*0.6, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Lightning Strike", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 30
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        if dmg != 0:
                            lightning = 1
                        lightningcooldown = 7
                        skillused = ""
                        numset = False
                if skillused == "Soul_Crush" and myself_mana >= 50 and soulcooldown == 0:
                    dmg = round(int(myself_magic) * 5.5, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if soul > 0:
                        if number < round(int(enemy_speed)*0.6, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Soul Crush", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 50
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        if dmg != 0:
                            soul = 4
                        soulcooldown = 10
                        skillused = ""
                        numset = False
                if skillused == "Weakness" and myself_mana >= 60 and weaknesscooldown == 0:
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+WEAKNESS", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Weakness", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        myself_power = myself.retrievestat("strength") * 1.9
                        myself_magic = myself.retrievestat("magic") * 1.9
                        myself_mana = myself_mana - 60
                        if myself_mana < 0:
                            myself_mana = 0
                        weakness = 4
                        weaknesscooldown = 12
                        skillused = ""
                        numset = False
                
                if skillused == "Amputate" and myself_mana >= 20 and amputatecooldown == 0:
                    dmg = round(int(myself_power) * 2, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Amputate!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 20
                        if enemy_health < 0:
                            enemy_health = 0
                        if myself_mana < 0:
                            myself_mana = 0
                        if dmg != 0:
                            amputate = 2
                        amputatecooldown = 4
                        skillused = ""
                        numset = False
                if skillused == "Blindside" and myself_mana >= 25 and blindsidecooldown == 0:
                    dmg = round(int(myself_power) * 1.75, 0)
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg), 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Blindside", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 25
                        if enemy_health < 0:
                            enemy_health = 0
                        if myself_mana < 0:
                            myself_mana = 0
                        blindsidecooldown = 3
                        skillused = ""
                        numset = False
                if skillused == "Dragons_Breath" and myself_mana >= 40 and dragoncooldown == 0:
                    dmg = round(int(myself_power) * 2.25, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if amputate > 0:
                        if number < round(int(enemy_speed) * 0.8, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Dragons Breath", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health -dmg
                        myself_mana = myself_mana - 40
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        if dmg != 0:
                            dragon = 5
                        dragoncooldown = 10
                        skillused = ""
                        numset = False
                if skillused == "Fury_Strike" and myself_mana >= 15 and furycooldown == 0:
                    dmg = round(int(myself_power) * 3, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if amputate > 0:
                        if number < round(int(enemy_speed) * 0.8, 0)*2:
                            dmg = 0
                    elif number < int(enemy_speed)*2:
                        dmg = 0 
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Fury Strike", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 15
                        if myself_mana < 0:
                            myself_mana = 0
                        if enemy_health < 0:
                            enemy_health = 0
                        furycooldown = 4
                        skillused = ""
                        numset = False
                if skillused == "Overcharge" and myself_mana >= 50 and overchargecooldown == 0:
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+OVERCHARGED!", 1, LIGHTBLUE), (selfpos.x, selfpos.y - 100))
                        game.blit(comicsans(20).render("You used: Overcharge", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        myself_mana = myself_mana - 50
                        if myself_mana < 0:
                            myself_mana = 0
                        overchargecooldown = 8
                        overcharge = 3
                        myself_power = myself.retrievestat("strength") * 1.5
                        myself_magic = myself.retrievestat("magic") * 1.5
                        skillused = ""
                        numset = False
                if skillused == "Poison" and myself_mana >= 30 and poisoncooldown == 0:
                    dmg = round(int(myself_magic) * 3, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if amputate > 0:
                        if number < round(int(enemy_speed) * 0.8, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Poison", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 30
                        if enemy_health < 0:
                            enemy_health = 0
                        if myself_mana < 0:
                            myself_mana = 0
                        if dmg != 0:
                            poison = 4
                        poisoncooldown = 7
                        skillused = ""
                        numset = False
                if skillused == "Shuriken" and myself_mana >= 20 and shurikencooldown == 0:
                    dmg = round(int(myself_power) * 2.1, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if amputate > 0:
                        if number < round(int(enemy_speed) * 0.45, 0):
                            dmg = 0
                    elif number < round(int(enemy_speed) * 0.55, 0):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Shuriken", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - 20
                        if enemy_health < 0:
                            enemy_health = 0
                        if myself_mana < 0:
                            myself_mana = 0
                        shurikencooldown = 4
                        skillused = ""
                        numset = False
                if skillused == "Slash" and myself_mana >= 30 and slashcooldown == 0:
                    dmg = round(int(myself_power) * 2.5, 0)
                    if numset == False:
                        number = random.randint(0, 100)
                        numset = True
                    if amputate > 0:
                        if number < round(int(enemy_speed) * 0.8, 0):
                            dmg = 0
                    elif number < int(enemy_speed):
                        dmg = 0
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("-" + str(dmg) if dmg != 0 else "MISSED!", 1, RED), (enemypos.x, enemypos.y - 100))
                        game.blit(comicsans(20).render("You used: Slash!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        enemy_health = enemy_health - dmg
                        myself_mana = myself_mana - dmg
                        if enemy_health < 0:
                            enemy_health = 0
                        if myself_mana < 0:
                            myself_mana = 0
                        slashcooldown = 5
                        skillused = ""
                        numset = False
                if skillused == "Speed" and myself_mana >= 50 and speedcooldown == 0:
                    if counter != 70:
                        counter += 1
                        game.blit(comicsans(20).render("+SPEED!", 1, LIGHTBLUE), (selfpos.x, selfpos.y-100))
                        game.blit(comicsans(20).render("You used: Speed!", 1, WHITE), (_width_/2, 100))
                    if counter == 70:
                        curTurn = "Enemy"
                        counter = 0
                        myself_mana = myself_mana - 50
                        if myself_mana < 0:
                            myself_mana = 0
                        speedcooldown = 10
                        myself_speed = 100
                        skillused = ""
                        numset = False

                    
                    

            
            if enemy_health <= 0: #winning screen
                blackscreen = pygame.Rect(0,0, _width_, _height_)
                pygame.draw.rect(game, BLACK, blackscreen)
                game.blit(comicsans(20).render("You won!", 1, GREEN), (_width_/2, 100))
                experience_bar = pygame.Rect((_width_/2)-100, 200, 300, 15)
                pygame.draw.rect(game, DARKERGRAY, experience_bar)
                pygame.draw.rect(game, GREEN, pygame.Rect((_width_/2)-100, 200, 300 * xp_slider, 15)) ##xp animation bar
                if xp_slider >= 1.00:
                    game.blit(comicsans(15).render("Levelled Up!", 1, FOCUS), (_width_/2, 150))
                    game.blit(comicsans(15).render("Your Level: " + str(int(data["level:"]) + 1), 1, WHITE), (_width_/2, 175))
                else:
                    game.blit(comicsans(15).render("Your Level: " + str(data["level:"]), 1, WHITE), ((_width_/2)-100, 150))
                    game.blit(comicsans(12).render("EXP: " + str(data["experience:"]) + " / " + str(data["experience_to_next_level:"]), 1, WHITE), ((_width_/2)+125, 150))
                if xp_gained < 601:
                    xp_gained += 1
                    data["experience:"] = str(int(data["experience:"])+1)
                    xp_slider = int(data["experience:"])/int(data["experience_to_next_level:"])
                pygame.draw.rect(game, LIGHTGRAY, gotocampbtn)
                pygame.draw.rect(game, LIGHTGRAY, returnbutton)
                if returnbutton.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(game, WHITE, returnbutton)
                if gotocampbtn.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(game, WHITE, gotocampbtn)
                game.blit(comicsans(20).render("Return to Menu", 1, BLACK), (returnbutton.x, returnbutton.y))
                game.blit(comicsans(20).render("Go To Camp", 1, BLACK), (gotocampbtn.x, gotocampbtn.y))




            if myself_health <= 0: #losing screen
                blackscreen = pygame.Rect(0, 0, _width_, _height_)
                pygame.draw.rect(game, BLACK, blackscreen)
                game.blit(comicsans(20).render("You've lost!", 1, RED), (_width_/2, 100))
                pygame.draw.rect(game, LIGHTGRAY, restartbutton)
                if restartbutton.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(game, WHITE, restartbutton)
                game.blit(comicsans(20).render("Restart Battle", 1, BLACK), (restartbutton.x+10, restartbutton.y))

                pygame.draw.rect(game, LIGHTGRAY, returnbutton)
                if returnbutton.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(game, WHITE, returnbutton)
                game.blit(comicsans(20).render("Return To Menu", 1, BLACK), (returnbutton.x, returnbutton.y))
                game.blit(transform(_skull_icon_, (128,128)), (_width_/2, 200))

        if _cur_screen_ == "Camp": ##UI for accessing attributes, skills, shops, replaying missions, and starting new ones.
            game.blit(transform(_camp_, (_width_, _height_)), (0,0))
            bottomui = pygame.Rect(0, _height_-100, _width_, 100)
            pygame.draw.rect(game, DARKERGRAY, bottomui)

            exit_camp = pygame.Rect((_width_/2)-50, _height_-80, 64, 64)
            pygame.draw.rect(game, LIGHTGRAY, exit_camp)
            if exit_camp.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, exit_camp)
            game.blit(transform(_home_, (64, 64)), (exit_camp.x, exit_camp.y))

            shop = pygame.Rect(270, 386, 64, 64)
            pygame.draw.rect(game, LIGHTGRAY, shop)
            if shop.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, shop)
            game.blit(transform(_shop_, (64,64)), (shop.x, shop.y))

            battle = pygame.Rect(600, 350, 64, 64)
            pygame.draw.rect(game, LIGHTGRAY, battle)
            if battle.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, battle)
            game.blit(transform(_battle_, (64, 64)), (battle.x, battle.y))

            battle_return = pygame.Rect(840, 416, 64, 64)
            pygame.draw.rect(game, LIGHTGRAY, battle_return)
            if battle_return.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, battle_return)
            game.blit(transform(_return_, (64,64)), (battle_return.x, battle_return.y))



        if _cur_screen_ == "Selection":
            pygame.draw.rect(game, BLACK, pygame.Rect(0,0, _width_, _height_))
            game.blit(comicsans(20).render("Repeat Levels", 1, WHITE), ((_width_/2)-25, 50))

            game.blit(comicsans(20).render("Zone 1", 1, WHITE), (165, 140))

            exitsel = pygame.Rect(_width_-100, 50, 32, 32)
            pygame.draw.rect(game, RED, exitsel)
            if exitsel.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, (154, 5, 0), exitsel)
            game.blit(comicsans(20).render("X", 1, WHITE), (exitsel.x+8, exitsel.y))

            tutbtn = pygame.Rect(100, 200, 200, 32)
            pygame.draw.rect(game, LIGHTGRAY, tutbtn)
            if tutbtn.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, tutbtn)
            game.blit(comicsans(15).render("Tutorial Level", 1, BLACK), (tutbtn.x + 45, tutbtn.y + 5))

            level2 = pygame.Rect(100, 270, 200, 32)
            pygame.draw.rect(game, LIGHTGRAY, level2)
            if level2.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, level2)
            game.blit(comicsans(15).render("Level 2", 1, BLACK), (level2.x + 70, level2.y + 5))

            level3 = pygame.Rect(100, 340, 200, 32)
            pygame.draw.rect(game, LIGHTGRAY, level3)
            if level3.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, level3)
            game.blit(comicsans(15).render("Level 3", 1, BLACK), (level3.x + 70, level3.y + 5))

            level4 = pygame.Rect(100, 410, 200, 32)
            pygame.draw.rect(game, LIGHTGRAY, level4)
            if level4.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, level4)
            game.blit(comicsans(15).render("Level 4", 1, BLACK), (level4.x + 70, level4.y + 5))

            level5 = pygame.Rect(100, 480, 200, 32)
            pygame.draw.rect(game, LIGHTGRAY, level5)
            if level5.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, level5)
            game.blit(comicsans(15).render("Level 5", 1, BLACK), (level5.x + 70, level5.y + 5))

            game.blit(comicsans(20).render("Playing levels on repeat will provide", 1, WHITE), ((_width_/2)-100, 180))
            game.blit(comicsans(20).render("same experience gains as the levels gave", 1, WHITE), ((_width_/2)-100, 220))
            game.blit(comicsans(20).render("you originally so the harder the level", 1, WHITE), ((_width_/2)-100, 260))
            game.blit(comicsans(20).render("the more experience gains you will get!", 1, WHITE), ((_width_/2)-100, 300))

        if _cur_screen_ == "Shop": ##interface for buying skills, adding attribute points and changing skills
            pygame.draw.rect(game, BLACK, pygame.Rect(0,0,_width_, _height_))
            
            
            if _width_ == 1280:
                skills_rect = pygame.Rect(50, 60, 300, 600)
                attributes_rect = pygame.Rect(490, 60, 300, 600)
                palette_rect = pygame.Rect(910, 60, 300, 600)
                game.blit(comicsans(20).render("Skills", 1, WHITE), (170, 10))
                pygame.draw.rect(game, DARKERGRAY, skills_rect)
                game.blit(comicsans(20).render("Attributes", 1, WHITE), (600, 10))
                pygame.draw.rect(game, DARKERGRAY, attributes_rect)
                game.blit(comicsans(20).render("Skill Palette", 1, WHITE), (1000, 10))
                pygame.draw.rect(game, DARKERGRAY, palette_rect)
            else:
                skills_rect = pygame.Rect(50, 60, 300, 550)
                attributes_rect = pygame.Rect(385, 60, 300, 550)
                palette_rect = pygame.Rect(720, 60, 300, 550)
                game.blit(comicsans(20).render("Skills", 1, WHITE), (170, 10))
                pygame.draw.rect(game, DARKERGRAY, skills_rect)
                game.blit(comicsans(20).render("Attributes", 1, WHITE), (500, 10))
                pygame.draw.rect(game, DARKERGRAY, attributes_rect)
                game.blit(comicsans(20).render("Skill Palette", 1, WHITE), (815, 10))
                pygame.draw.rect(game, DARKERGRAY, palette_rect)          

            ##add skills to skill panel
            #knights#
            skill_slam = pygame.Rect(skills_rect.x + 10, skills_rect.y + 10, 48, 48)
            pygame.draw.rect(game, LIGHTBLUE if skillselected == "Slam" else WHITE if data["skill_k_slam:"] == "True" else LIGHTGRAY, skill_slam)
            if skill_slam.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill_slam)
            game.blit(transform(_slam_, (48, 48)), (skill_slam.x, skill_slam.y))
            skill_shield = pygame.Rect(skills_rect.x + 10, skills_rect.y + 65, 48, 48)
            pygame.draw.rect(game, LIGHTBLUE if skillselected == "Shield" else WHITE if data["skill_k_shield:"] == "True" else LIGHTGRAY, skill_shield)
            if skill_shield.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill_shield)
            game.blit(transform(_shield_, (48,48)), (skill_shield.x, skill_shield.y))
            skill_ballistic = pygame.Rect(skills_rect.x + 10, skills_rect.y + 120, 48, 48)
            pygame.draw.rect(game, LIGHTBLUE if skillselected == "Ballistic_Strike" else WHITE if data["skill_k_ballistic_strike:"] == "True" else LIGHTGRAY, skill_ballistic)
            if skill_ballistic.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill_ballistic)
            game.blit(transform(_ballistic_strike_, (48,48)), (skill_ballistic.x, skill_ballistic.y))
            skill_double = pygame.Rect(skills_rect.x + 10, skills_rect.y + 175, 48, 48)
            pygame.draw.rect(game, LIGHTBLUE if skillselected == "Double_Strike" else WHITE if data["skill_k_double_strike:"] == "True" else LIGHTGRAY, skill_double)
            if skill_double.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill_double)
            game.blit(transform(_double_strike_, (48,48)), (skill_double.x, skill_double.y))
            skill_puncture = pygame.Rect(skills_rect.x + 10, skills_rect.y + 230, 48, 48)
            pygame.draw.rect(game, LIGHTBLUE if skillselected == "Puncture" else WHITE if data["skill_k_puncture:"] == "True" else LIGHTGRAY, skill_puncture)
            if skill_puncture.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill_puncture)
            game.blit(transform(_puncture_, (48,48)), (skill_puncture.x, skill_puncture.y))
            skill_stun = pygame.Rect(skills_rect.x + 10, skills_rect.y + 285, 48, 48)
            pygame.draw.rect(game, LIGHTBLUE if skillselected == "Stun" else WHITE if data["skill_k_stun:"] == "True" else LIGHTGRAY, skill_stun)
            if skill_stun.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill_stun)
            game.blit(transform(_stun_, (48,48)), (skill_stun.x, skill_stun.y))
            skill_suit = pygame.Rect(skills_rect.x + 10, skills_rect.y + 340, 48, 48)
            pygame.draw.rect(game, LIGHTBLUE if skillselected == "Suit_Up" else WHITE if data["skill_k_suitup:"] == "True" else LIGHTGRAY, skill_suit)
            if skill_suit.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill_suit)
            game.blit(transform(_suit_up_, (48,48)), (skill_suit.x, skill_suit.y))
            skill_enrage = pygame.Rect(skills_rect.x + 10, skills_rect.y + 395, 48, 48)
            pygame.draw.rect(game, LIGHTBLUE if skillselected == "Enrage" else WHITE if data["skill_k_enrage:"] == "True" else LIGHTGRAY, skill_enrage)
            if skill_enrage.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill_enrage)
            game.blit(transform(_enrage_, (48,48)), (skill_enrage.x, skill_enrage.y))
            skill_vampire = pygame.Rect(skills_rect.x + 10, skills_rect.y + 450, 48, 48)
            pygame.draw.rect(game, LIGHTBLUE if skillselected == "Vampire_Strike" else WHITE if data["skill_k_vampire_strike:"] == "True" else LIGHTGRAY, skill_vampire)
            if skill_vampire.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill_vampire)
            game.blit(transform(_vampire_strike_, (48,48)), (skill_vampire.x, skill_vampire.y))

            #wizards
            skill_fireball = pygame.Rect(skills_rect.x + 120, skills_rect.y + 10, 48, 48)
            pygame.draw.rect(game, LIGHTBLUE if skillselected == "Fireball" else WHITE if data["skill_w_fireball:"] == "True" else LIGHTGRAY, skill_fireball)
            if skill_fireball.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill_fireball)
            game.blit(transform(_fireball_, (48,48)), (skill_fireball.x, skill_fireball.y))
            skill_freeze = pygame.Rect(skills_rect.x + 120, skills_rect.y + 65, 48, 48)
            pygame.draw.rect(game, LIGHTBLUE if skillselected == "Freeze" else WHITE if data["skill_w_freeze:"] == "True" else LIGHTGRAY, skill_freeze)
            if skill_freeze.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill_freeze)
            game.blit(transform(_freeze_, (48,48)), (skill_freeze.x, skill_freeze.y))
            skill_drain = pygame.Rect(skills_rect.x + 120, skills_rect.y + 120, 48, 48)
            pygame.draw.rect(game, LIGHTBLUE if skillselected == "Drain" else WHITE if data["skill_w_drain:"] == "True" else LIGHTGRAY, skill_drain)
            if skill_drain.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill_drain)
            game.blit(transform(_drain_, (48,48)), (skill_drain.x, skill_drain.y))
            skill_invert = pygame.Rect(skills_rect.x + 120, skills_rect.y + 175, 48, 48)
            pygame.draw.rect(game, LIGHTBLUE if skillselected == "Invert" else WHITE if data["skill_w_invert:"] == "True" else LIGHTGRAY, skill_invert)
            if skill_invert.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill_invert)
            game.blit(transform(_invert_, (48,48)), (skill_invert.x, skill_invert.y))
            skill_leech = pygame.Rect(skills_rect.x + 120, skills_rect.y + 230, 48, 48)
            pygame.draw.rect(game, LIGHTBLUE if skillselected == "Leech" else WHITE if data["skill_w_leech:"] == "True" else LIGHTGRAY, skill_leech)
            if skill_leech.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill_leech)
            game.blit(transform(_leech_, (48,48)), (skill_leech.x, skill_leech.y))
            skill_life = pygame.Rect(skills_rect.x + 120, skills_rect.y + 285, 48, 48)
            pygame.draw.rect(game, LIGHTBLUE if skillselected == "Life" else WHITE if data["skill_w_life:"] == "True" else LIGHTGRAY, skill_life)
            if skill_life.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill_life)
            game.blit(transform(_life_, (48,48)), (skill_life.x, skill_life.y))
            skill_lightning = pygame.Rect(skills_rect.x + 120, skills_rect.y + 340, 48, 48)
            pygame.draw.rect(game, LIGHTBLUE if skillselected == "Lightning_Strike" else WHITE if data["skill_w_lightning_strike:"] == "True" else LIGHTGRAY, skill_lightning)
            if skill_lightning.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill_lightning)
            game.blit(transform(_lightning_strike_, (48,48)), (skill_lightning.x, skill_lightning.y))
            skill_soul = pygame.Rect(skills_rect.x + 120, skills_rect.y + 395, 48, 48)
            pygame.draw.rect(game, LIGHTBLUE if skillselected == "Soul_Crush" else WHITE if data["skill_w_soul_crush:"] == "True" else LIGHTGRAY, skill_soul)
            if skill_soul.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill_soul)
            game.blit(transform(_soul_crush_, (48,48)), (skill_soul.x, skill_soul.y))
            skill_weakness = pygame.Rect(skills_rect.x + 120, skills_rect.y + 450, 48, 48)
            pygame.draw.rect(game, LIGHTBLUE if skillselected == "Weakness" else WHITE if data["skill_w_weakness:"] == "True" else LIGHTGRAY, skill_weakness)
            if skill_weakness.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill_weakness)
            game.blit(transform(_weakness_, (48,48)), (skill_weakness.x, skill_weakness.y))

            #assassin
            skill_amputate = pygame.Rect(skills_rect.x + 230, skills_rect.y + 10, 48, 48)
            pygame.draw.rect(game, LIGHTBLUE if skillselected == "Amputate" else WHITE if data["skill_a_amputate:"] == "True" else LIGHTGRAY, skill_amputate)
            if skill_amputate.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill_amputate)
            game.blit(transform(_amputate_, (48,48)), (skill_amputate.x, skill_amputate.y))
            skill_blindside = pygame.Rect(skills_rect.x + 230, skills_rect.y + 65, 48, 48)
            pygame.draw.rect(game, LIGHTBLUE if skillselected == "Blindside" else WHITE if data["skill_a_blindside:"] == "True" else LIGHTGRAY, skill_blindside)
            if skill_blindside.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill_blindside)
            game.blit(transform(_blindside_, (48,48)), (skill_blindside.x, skill_blindside.y))
            skill_dragon = pygame.Rect(skills_rect.x + 230, skills_rect.y + 120, 48, 48)
            pygame.draw.rect(game, LIGHTBLUE if skillselected == "Dragons_Breath" else WHITE if data["skill_a_dragons_breath:"] == "True" else LIGHTGRAY, skill_dragon)
            if skill_dragon.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill_dragon)
            game.blit(transform(_dragons_breath_, (48,48)), (skill_dragon.x, skill_dragon.y))
            skill_fury = pygame.Rect(skills_rect.x + 230, skills_rect.y + 175, 48, 48)
            pygame.draw.rect(game, LIGHTBLUE if skillselected == "Fury_Strike" else WHITE if data["skill_a_fury_strike:"] == "True" else LIGHTGRAY, skill_fury)
            if skill_fury.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill_fury)
            game.blit(transform(_fury_strike_, (48,48)), (skill_fury.x, skill_fury.y))
            skill_overcharge = pygame.Rect(skills_rect.x + 230, skills_rect.y + 230, 48, 48)
            pygame.draw.rect(game, LIGHTBLUE if skillselected == "Overcharge" else WHITE if data["skill_a_overcharge:"] == "True" else LIGHTGRAY, skill_overcharge)
            if skill_overcharge.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill_overcharge)
            game.blit(transform(_overcharge_, (48,48)), (skill_overcharge.x, skill_overcharge.y))
            skill_poison = pygame.Rect(skills_rect.x + 230, skills_rect.y + 285, 48, 48)
            pygame.draw.rect(game, LIGHTBLUE if skillselected == "Poison" else WHITE if data["skill_a_poison:"] == "True" else LIGHTGRAY, skill_poison)
            if skill_poison.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill_poison)
            game.blit(transform(_poison_, (48,48)), (skill_poison.x, skill_poison.y))
            skill_shuriken = pygame.Rect(skills_rect.x + 230, skills_rect.y + 340, 48, 48)
            pygame.draw.rect(game, LIGHTBLUE if skillselected == "Shuriken" else WHITE if data["skill_a_shuriken:"] == "True" else LIGHTGRAY, skill_shuriken)
            if skill_shuriken.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill_shuriken)
            game.blit(transform(_shuriken_, (48,48)), (skill_shuriken.x, skill_shuriken.y))
            skill_slash = pygame.Rect(skills_rect.x + 230, skills_rect.y + 395, 48, 48)
            pygame.draw.rect(game, LIGHTBLUE if skillselected == "Slash" else WHITE if data["skill_a_slash:"] == "True" else LIGHTGRAY, skill_slash)
            if skill_slash.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill_slash)
            game.blit(transform(_slash_, (48,48)), (skill_slash.x, skill_slash.y))
            skill_speed = pygame.Rect(skills_rect.x + 230, skills_rect.y + 450, 48, 48)
            pygame.draw.rect(game, LIGHTBLUE if skillselected == "Speed" else WHITE if data["skill_a_speed:"] == "True" else LIGHTGRAY, skill_speed)
            if skill_speed.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, skill_speed)
            game.blit(transform(_speed_, (48,48)), (skill_speed.x, skill_speed.y))

            ##design hover text area to show skill desc, skill cost, skill mana requirements, skill name
            skilltextarea = pygame.Rect(skills_rect.x + 10, skills_rect.y + 505, 280, 50)
            pygame.draw.rect(game, WHITE, skilltextarea)
            game.blit(comicsans(20).render("Skill Points: " + str(data["skillpoints:"]), 1, WHITE), (skills_rect.x + 10, skills_rect.y + 560))
            if skill_slam.collidepoint(pygame.mouse.get_pos()):
                game.blit(comicsans(10).render("Skill: Slam", 1, BLACK), (skilltextarea.x, skilltextarea.y))
                game.blit(comicsans(10).render("Mana Cost: 15", 1, BLACK), (skilltextarea.x, skilltextarea.y + 10))
                game.blit(comicsans(10).render("Uses 25% strength to deal powerful damage.", 1, BLACK), (skilltextarea.x, skilltextarea.y + 20))
                game.blit(comicsans(10).render("Cooldown: 3 Rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y + 30))
            elif skill_shield.collidepoint(pygame.mouse.get_pos()):
                game.blit(comicsans(10).render("Skill: Shield", 1, BLACK), (skilltextarea.x, skilltextarea.y))
                game.blit(comicsans(10).render("Mana Cost: 20", 1, BLACK), (skilltextarea.x, skilltextarea.y + 10))
                game.blit(comicsans(10).render("Blocks 50% damage with added strength bonuses.", 1, BLACK), (skilltextarea.x, skilltextarea.y + 20))
                game.blit(comicsans(10).render("Cooldown: 4 Rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y + 30))
            elif skill_ballistic.collidepoint(pygame.mouse.get_pos()):
                game.blit(comicsans(10).render("Skill: Ballistic Strike", 1, BLACK), (skilltextarea.x, skilltextarea.y))
                game.blit(comicsans(10).render("Mana Cost: 25", 1, BLACK), (skilltextarea.x, skilltextarea.y + 10))
                game.blit(comicsans(10).render("Deals 30% strength dmg and slows enemy for 2 rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y + 20))
                game.blit(comicsans(10).render("Cooldown: 3 Rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y + 30))
            elif skill_double.collidepoint(pygame.mouse.get_pos()):
                game.blit(comicsans(10).render("Skill: Double Strike", 1, BLACK), (skilltextarea.x, skilltextarea.y))
                game.blit(comicsans(10).render("Mana Cost: 20", 1, BLACK), (skilltextarea.x, skilltextarea.y + 10))
                game.blit(comicsans(10).render("Does 2x Basic Attack damage", 1, BLACK), (skilltextarea.x, skilltextarea.y + 20))
                game.blit(comicsans(10).render("Cooldown: 5 Rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y + 30))
            elif skill_puncture.collidepoint(pygame.mouse.get_pos()):
                game.blit(comicsans(10).render("Skill: Puncture", 1, BLACK), (skilltextarea.x, skilltextarea.y))
                game.blit(comicsans(10).render("Mana Cost: 35", 1, BLACK), (skilltextarea.x, skilltextarea.y + 10))
                game.blit(comicsans(10).render("Weakens the enemy's defenses by 15% for 3 rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y + 20))
                game.blit(comicsans(10).render("Cooldown: 4 Rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y + 30))
            elif skill_stun.collidepoint(pygame.mouse.get_pos()):
                game.blit(comicsans(10).render("Skill: Stun", 1, BLACK), (skilltextarea.x, skilltextarea.y))
                game.blit(comicsans(10).render("Mana Cost: 20", 1, BLACK), (skilltextarea.x, skilltextarea.y + 10))
                game.blit(comicsans(10).render("Stuns enemy for 1 round skipping their next move", 1, BLACK), (skilltextarea.x, skilltextarea.y + 20))
                game.blit(comicsans(10).render("Cooldown: 5 Rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y + 30))
            elif skill_suit.collidepoint(pygame.mouse.get_pos()):
                game.blit(comicsans(10).render("Skill: Suit Up", 1, BLACK), (skilltextarea.x, skilltextarea.y))
                game.blit(comicsans(10).render("Mana Cost: 40", 1, BLACK), (skilltextarea.x, skilltextarea.y + 10))
                game.blit(comicsans(10).render("Increases damage resistance for 5 rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y + 20))    
                game.blit(comicsans(10).render("Cooldown: 9 Rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y + 30))    
            elif skill_enrage.collidepoint(pygame.mouse.get_pos()):
                game.blit(comicsans(10).render("Skill: Enrage", 1, BLACK), (skilltextarea.x, skilltextarea.y))
                game.blit(comicsans(10).render("Mana Cost: 50", 1, BLACK), (skilltextarea.x, skilltextarea.y + 10))
                game.blit(comicsans(10).render("Increases strength by 250% for 3 rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y + 20))
                game.blit(comicsans(10).render("Cooldown: 10 Rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y + 30))
            elif skill_vampire.collidepoint(pygame.mouse.get_pos()):
                game.blit(comicsans(10).render("Skill: Vampire Strike", 1, BLACK), (skilltextarea.x, skilltextarea.y))
                game.blit(comicsans(10).render("Mana Cost: 45", 1, BLACK), (skilltextarea.x, skilltextarea.y + 10))
                game.blit(comicsans(10).render("Deals 50% of strength dmg and heals back 30%", 1, BLACK), (skilltextarea.x, skilltextarea.y + 20))
                game.blit(comicsans(10).render("Cooldown: 4 Rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y + 30))       
            elif skill_fireball.collidepoint(pygame.mouse.get_pos()):
                game.blit(comicsans(10).render("Skill: Fireball", 1, BLACK), (skilltextarea.x, skilltextarea.y))
                game.blit(comicsans(10).render("Mana Costs: 20", 1, BLACK), (skilltextarea.x, skilltextarea.y + 10))
                game.blit(comicsans(10).render("Deals 20% magic dmg and burns enemy for 2 rounds",1, BLACK), (skilltextarea.x, skilltextarea.y + 20))
                game.blit(comicsans(10).render("Cooldown: 4 Rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y + 30)) 
            elif skill_freeze.collidepoint(pygame.mouse.get_pos()):
                game.blit(comicsans(10).render("Skill: Freeze", 1, BLACK), (skilltextarea.x, skilltextarea.y))
                game.blit(comicsans(10).render("Mana Costs: 25", 1, BLACK), (skilltextarea.x, skilltextarea.y + 10))
                game.blit(comicsans(10).render("Freezes the enemy for 2 rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y + 20)) 
                game.blit(comicsans(10).render("Cooldown: 5 Rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y + 30))
            elif skill_drain.collidepoint(pygame.mouse.get_pos()):
                game.blit(comicsans(10).render("Skill: Drain", 1, BLACK), (skilltextarea.x, skilltextarea.y))
                game.blit(comicsans(10).render("Mana Costs: 15", 1, BLACK), (skilltextarea.x, skilltextarea.y + 10))
                game.blit(comicsans(10).render("Steals the 50% enemy's mana for your own", 1, BLACK), (skilltextarea.x, skilltextarea.y + 20))
                game.blit(comicsans(10).render("Cooldown: 4 Rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y + 30)) 
            elif skill_invert.collidepoint(pygame.mouse.get_pos()):
                game.blit(comicsans(10).render("Skill: Invert", 1, BLACK), (skilltextarea.x, skilltextarea.y))
                game.blit(comicsans(10).render("Mana Costs: 35", 1, BLACK), (skilltextarea.x, skilltextarea.y + 10))
                game.blit(comicsans(10).render("Inverts the opponents dmg -> hp and hp -> dmg", 1, BLACK), (skilltextarea.x, skilltextarea.y + 20))
                game.blit(comicsans(10).render("Cooldown: 6 Rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y + 30))
            elif skill_leech.collidepoint(pygame.mouse.get_pos()):
                game.blit(comicsans(10).render("Skill: Leech", 1, BLACK), (skilltextarea.x, skilltextarea.y))
                game.blit(comicsans(10).render("Mana Costs: 45", 1, BLACK), (skilltextarea.x, skilltextarea.y + 10))
                game.blit(comicsans(10).render("Steals 20% + magic bonuses of opponents health", 1, BLACK), (skilltextarea.x, skilltextarea.y + 20))
                game.blit(comicsans(10).render("Cooldown: 5 Rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y + 30))
            elif skill_life.collidepoint(pygame.mouse.get_pos()):
                game.blit(comicsans(10).render("Skill: Life", 1, BLACK), (skilltextarea.x, skilltextarea.y))
                game.blit(comicsans(10).render("Mana Cost: 40", 1, BLACK), (skilltextarea.x, skilltextarea.y + 10))
                game.blit(comicsans(10).render("Heal yourself for 10% of max health for 5 rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y + 20))
                game.blit(comicsans(10).render("Cooldown: 8 Rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y + 30))
            elif skill_lightning.collidepoint(pygame.mouse.get_pos()):
                game.blit(comicsans(10).render("Skill: Lightning Strike", 1, BLACK), (skilltextarea.x, skilltextarea.y))
                game.blit(comicsans(10).render("Mana Cost: 30", 1, BLACK), (skilltextarea.x, skilltextarea.y + 10))
                game.blit(comicsans(10).render("Does 100% magic damage and stuns enemy for 1 round", 1, BLACK), (skilltextarea.x, skilltextarea.y + 20))
                game.blit(comicsans(10).render("Cooldown: 7 Rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y + 30))
            elif skill_soul.collidepoint(pygame.mouse.get_pos()):
                game.blit(comicsans(10).render("Skill: Soul Crush", 1, BLACK), (skilltextarea.x, skilltextarea.y))
                game.blit(comicsans(10).render("Mana Cost: 50", 1, BLACK), (skilltextarea.x, skilltextarea.y + 10))
                game.blit(comicsans(10).render("Reduces enemy speed by 60% for 4 rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y + 20))
                game.blit(comicsans(10).render("Cooldown: 10 Rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y + 30))
            elif skill_weakness.collidepoint(pygame.mouse.get_pos()):
                game.blit(comicsans(10).render("Skill: Weakness", 1, BLACK), (skilltextarea.x, skilltextarea.y))
                game.blit(comicsans(10).render("Mana Cost: 60", 1, BLACK), (skilltextarea.x, skilltextarea.y + 10))
                game.blit(comicsans(10).render("Weakens the enemy by 90% for 4 rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y + 20))
                game.blit(comicsans(10).render("Cooldown: 12 Rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y + 30))
            elif skill_amputate.collidepoint(pygame.mouse.get_pos()):
                game.blit(comicsans(10).render("Skill: Amputate", 1, BLACK), (skilltextarea.x, skilltextarea.y))
                game.blit(comicsans(10).render("Mana Cost: 20", 1, BLACK), (skilltextarea.x, skilltextarea.y+10))
                game.blit(comicsans(10).render("Deals increased damage and slows the enemy for 1 round.", 1, BLACK), (skilltextarea.x, skilltextarea.y + 20))
                game.blit(comicsans(10).render("Cooldown: 4 Rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y+30))
            elif skill_blindside.collidepoint(pygame.mouse.get_pos()):
                game.blit(comicsans(10).render("Skill: Blindside", 1, BLACK), (skilltextarea.x, skilltextarea.y))
                game.blit(comicsans(10).render("Mana Cost: 25", 1, BLACK), (skilltextarea.x, skilltextarea.y+10))
                game.blit(comicsans(10).render("Uses speed to attack the enemy ignoring miss chance", 1, BLACK), (skilltextarea.x, skilltextarea.y+20))
                game.blit(comicsans(10).render("Cooldown: 3 Rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y+30))
            elif skill_dragon.collidepoint(pygame.mouse.get_pos()):
                game.blit(comicsans(10).render("Skill: Dragons Breath", 1, BLACK), (skilltextarea.x, skilltextarea.y))
                game.blit(comicsans(10).render("Mana Cost: 40", 1, BLACK), (skilltextarea.x, skilltextarea.y+10))
                game.blit(comicsans(10).render("Deals burning damage that lasts 5 rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y + 20))
                game.blit(comicsans(10).render("Cooldown: 10 Rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y+30))
            elif skill_fury.collidepoint(pygame.mouse.get_pos()):
                game.blit(comicsans(10).render("Skill: Fury Strike", 1, BLACK), (skilltextarea.x, skilltextarea.y))
                game.blit(comicsans(10).render("Mana Cost: 15", 1, BLACK), (skilltextarea.x, skilltextarea.y + 10))
                game.blit(comicsans(10).render("Deals heavy damage but has more chance of missing", 1, BLACK), (skilltextarea.x, skilltextarea.y + 20))
                game.blit(comicsans(10).render("Cooldown: 4 Rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y + 30))
            elif skill_overcharge.collidepoint(pygame.mouse.get_pos()):
                game.blit(comicsans(10).render("Skill: Overcharge", 1, BLACK), (skilltextarea.x, skilltextarea.y))
                game.blit(comicsans(10).render("Mana Cost: 50", 1, BLACK), (skilltextarea.x, skilltextarea.y + 10))
                game.blit(comicsans(10).render("Fuel your energy with 50% extra strength for 3 rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y + 20))
                game.blit(comicsans(10).render("Cooldown: 8 Rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y + 30))
            elif skill_poison.collidepoint(pygame.mouse.get_pos()):
                game.blit(comicsans(10).render("Skill: Poison", 1, BLACK), (skilltextarea.x, skilltextarea.y))
                game.blit(comicsans(10).render("Mana Cost: 30", 1, BLACK), (skilltextarea.x, skilltextarea.y + 10))
                game.blit(comicsans(10).render("Poison the enemy with 150% magic for 4 rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y + 20))
                game.blit(comicsans(10).render("Cooldown: 7 Rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y + 30))
            elif skill_shuriken.collidepoint(pygame.mouse.get_pos()):
                game.blit(comicsans(10).render("Skill: Shuriken", 1, BLACK), (skilltextarea.x, skilltextarea.y))
                game.blit(comicsans(10).render("Mana Cost: 20", 1, BLACK), (skilltextarea.x, skilltextarea.y + 10))
                game.blit(comicsans(10).render("Throw shurikens at fast speed dealing 110% strength dmg", 1, BLACK), (skilltextarea.x, skilltextarea.y + 20))
                game.blit(comicsans(10).render("Cooldown: 4 Rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y + 30))
            elif skill_slash.collidepoint(pygame.mouse.get_pos()):
                game.blit(comicsans(10).render("Skill: Slash", 1, BLACK), (skilltextarea.x, skilltextarea.y))
                game.blit(comicsans(10).render("Mana Cost: 30", 1, BLACK), (skilltextarea.x, skilltextarea.y + 10))
                game.blit(comicsans(10).render("Slash your enemies with fury dealing 150% strength dmg", 1, BLACK), (skilltextarea.x, skilltextarea.y + 20))
                game.blit(comicsans(10).render("Cooldown: 5 Rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y + 30))
            elif skill_speed.collidepoint(pygame.mouse.get_pos()):
                game.blit(comicsans(10).render("Skill: Speed", 1, BLACK), (skilltextarea.x, skilltextarea.y))
                game.blit(comicsans(10).render("Mana Cost: 50", 1, BLACK), (skilltextarea.x, skilltextarea.y + 10))
                game.blit(comicsans(10).render("Increases speed to max stat making enemies miss you", 1, BLACK), (skilltextarea.x, skilltextarea.y + 20))
                game.blit(comicsans(10).render("Cooldown: 10 Rounds", 1, BLACK), (skilltextarea.x, skilltextarea.y + 30))
            else:
                game.blit(comicsans(10).render("Hover over any skill", 1, BLACK), (skilltextarea.x, skilltextarea.y))
                game.blit(comicsans(10).render("to see description!", 1, BLACK), (skilltextarea.x, skilltextarea.y + 10))
                game.blit(comicsans(10).render("You can only acquire skills of your class type so", 1, BLACK), (skilltextarea.x, skilltextarea.y + 20))
                game.blit(comicsans(10).render("Knights is left, Wizards middle, Assassins is right", 1, BLACK), (skilltextarea.x, skilltextarea.y + 30))

            resetskills = pygame.Rect(skills_rect.x + 170, skills_rect.y + 565, 100, 20)
            pygame.draw.rect(game, LIGHTGRAY, resetskills)
            if resetskills.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, resetskills) 
            game.blit(comicsans(12).render("Reset Skills", 1, BLACK), (resetskills.x + 15, resetskills.y))

            ##attributes modification area##
            game.blit(comicsans(20).render("Your stats:", 1, WHITE), (attributes_rect.x + 100, attributes_rect.y))

            game.blit(comicsans(15).render("Vitality: " + str(data["vitality:"]), 1, WHITE), (attributes_rect.x + 120, attributes_rect.y + 60))
            minus_vitality = pygame.Rect(attributes_rect.x + 20, attributes_rect.y + 60, 50, 20)
            pygame.draw.rect(game, LIGHTGRAY, minus_vitality)
            if minus_vitality.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, minus_vitality)
            game.blit(comicsans(20).render("-", 1, BLACK), (minus_vitality.x+20, minus_vitality.y-7))
            add_vitality = pygame.Rect(attributes_rect.x + 230, attributes_rect.y + 60, 50, 20)
            pygame.draw.rect(game, LIGHTGRAY, add_vitality)
            if add_vitality.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, add_vitality)
            game.blit(comicsans(20).render("+", 1, BLACK), (add_vitality.x + 20, add_vitality.y-7))

            game.blit(comicsans(15).render("Strength: " + str(data["strength:"]), 1, WHITE), (attributes_rect.x + 120, attributes_rect.y + 110))
            minus_strength = pygame.Rect(attributes_rect.x + 20, attributes_rect.y + 110, 50, 20)
            pygame.draw.rect(game, LIGHTGRAY, minus_strength)
            if minus_strength.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, minus_strength)
            game.blit(comicsans(20).render("-", 1, BLACK), (minus_strength.x+20, minus_strength.y-7))
            add_strength = pygame.Rect(attributes_rect.x + 230, attributes_rect.y + 110, 50, 20)
            pygame.draw.rect(game, LIGHTGRAY, add_strength)
            if add_strength.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, add_strength)
            game.blit(comicsans(20).render("+", 1, BLACK), (add_strength.x+20, add_strength.y-7))

            game.blit(comicsans(15).render("Magic: " + str(data["magic:"]), 1, WHITE), (attributes_rect.x + 120, attributes_rect.y + 160))
            minus_magic = pygame.Rect(attributes_rect.x + 20, attributes_rect.y + 160, 50, 20)
            pygame.draw.rect(game, LIGHTGRAY, minus_magic)
            if minus_magic.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, minus_magic)
            game.blit(comicsans(20).render("-", 1, BLACK), (minus_magic.x + 20, minus_magic.y - 7))
            add_magic = pygame.Rect(attributes_rect.x + 230, attributes_rect.y + 160, 50, 20)
            pygame.draw.rect(game, LIGHTGRAY, add_magic)
            if add_magic.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, add_magic)
            game.blit(comicsans(20).render("+", 1, BLACK), (add_magic.x + 20, add_magic.y - 7))

            game.blit(comicsans(15).render("Speed: " + str(data["speed:"]), 1, WHITE), (attributes_rect.x + 120, attributes_rect.y + 210))
            minus_speed = pygame.Rect(attributes_rect.x + 20, attributes_rect.y + 210, 50, 20)
            pygame.draw.rect(game, LIGHTGRAY, minus_speed)
            if minus_speed.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, minus_speed)
            game.blit(comicsans(20).render("-", 1, BLACK), (minus_speed.x + 20, minus_speed.y - 7))
            add_speed = pygame.Rect(attributes_rect.x + 230, attributes_rect.y + 210, 50, 20)
            pygame.draw.rect(game, LIGHTGRAY, add_speed)
            if add_speed.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, WHITE, add_speed)
            game.blit(comicsans(20).render("+", 1, BLACK), (add_speed.x + 20, add_speed.y - 7))

            #show attribute points
            game.blit(comicsans(20).render("Attribute Points: " + str(data["attributepoints:"]), 1, WHITE), (attributes_rect.x + 60, attributes_rect.y + 250))
            game.blit(comicsans(12).render("You may reset attribute points as ", 1, WHITE), (attributes_rect.x + 55, attributes_rect.y + 290))
            game.blit(comicsans(12).render("many times as you like however it ", 1, WHITE), (attributes_rect.x + 55, attributes_rect.y + 310))
            game.blit(comicsans(12).render("cap at base stats for your class!", 1, WHITE), (attributes_rect.x + 55, attributes_rect.y + 330))

            #add skill unlock notice
            game.blit(comicsans(20).render("Skill Slot Notice: ", 1, WHITE), (attributes_rect.x + 60, attributes_rect.y + 380))
            game.blit(comicsans(12).render("Additional skill slots will be unlocked", 1, WHITE), (attributes_rect.x + 50, attributes_rect.y + 420))
            game.blit(comicsans(12).render("as you level up in game levels and all", 1, WHITE), (attributes_rect.x + 50, attributes_rect.y + 440))
            game.blit(comicsans(12).render("should be unlocked by player level 10", 1, WHITE), (attributes_rect.x + 50, attributes_rect.y + 460))

            #add exit shop button
            exit_shop = pygame.Rect(_width_*0.95, 10, 32, 32)
            pygame.draw.rect(game, RED, exit_shop)
            if exit_shop.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, (122, 15, 13), exit_shop)
            game.blit(comicsans(24).render("X", 1, WHITE), (exit_shop.x + 6, exit_shop.y))

            ##draw personal skill palette section
            s1 = pygame.Rect(palette_rect.x+10, palette_rect.y+10, 48, 48)
            pygame.draw.rect(game, WHITE if data["skill1:"] == "True" else LIGHTGRAY, s1)
            if s1.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, LIGHTBLUE if data["skill1:"] == "True" else WHITE, s1)
            game.blit(transform(skill1_img, (48,48)), (s1.x, s1.y))
            s2 = pygame.Rect(palette_rect.x + 65, palette_rect.y + 10, 48, 48)
            pygame.draw.rect(game, WHITE if data["skill2:"] == "True" else LIGHTGRAY, s2)
            if s2.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, LIGHTBLUE if data["skill2:"] == "True" else WHITE, s2)
            game.blit(transform(skill2_img, (48,48)), (s2.x, s2.y))
            s3 = pygame.Rect(palette_rect.x + 120, palette_rect.y + 10, 48, 48)
            pygame.draw.rect(game, WHITE if data["skill3:"] == "True" else LIGHTGRAY, s3)
            if s3.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, LIGHTBLUE if data["skill3:"] == "True" else WHITE, s3)
            game.blit(transform(skill3_img, (48,48)), (s3.x, s3.y))
            s4 = pygame.Rect(palette_rect.x + 175, palette_rect.y + 10, 48, 48)
            pygame.draw.rect(game, WHITE if data["skill4:"] == "True" else LIGHTGRAY, s4)
            if s4.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, LIGHTBLUE if data["skill4:"] == "True" else WHITE, s4)
            game.blit(transform(skill4_img, (48,48)), (s4.x, s4.y))
            s5 = pygame.Rect(palette_rect.x + 230, palette_rect.y + 10, 48, 48)
            pygame.draw.rect(game, WHITE if data["skill5:"] == "True" else LIGHTGRAY, s5)
            if s5.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, LIGHTBLUE if data["skill5:"] == "True" else WHITE, s5)
            game.blit(transform(skill5_img, (48,48)), (s5.x, s5.y))
            s6 = pygame.Rect(palette_rect.x + 10, palette_rect.y + 80, 48, 48)
            pygame.draw.rect(game, WHITE if data["skill6:"] == "True" else LIGHTGRAY, s6)
            if s6.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, LIGHTBLUE if data["skill6:"] == "True" else WHITE, s6)
            game.blit(transform(skill6_img, (48,48)), (s6.x, s6.y))
            s7 = pygame.Rect(palette_rect.x + 65, palette_rect.y + 80, 48, 48)
            pygame.draw.rect(game, WHITE if data["skill7:"] == "True" else LIGHTGRAY, s7)
            if s7.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, LIGHTBLUE if data["skill7:"] == "True" else WHITE, s7)
            game.blit(transform(skill7_img, (48,48)), (s7.x, s7.y))
            s8 = pygame.Rect(palette_rect.x + 120, palette_rect.y + 80, 48, 48)
            pygame.draw.rect(game, WHITE if data["skill8:"] == "True" else LIGHTGRAY, s8)
            if s8.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, LIGHTBLUE if data["skill8:"] == "True" else WHITE, s8)
            game.blit(transform(skill8_img, (48,48)), (s8.x, s8.y))                
            s9 = pygame.Rect(palette_rect.x + 175, palette_rect.y + 80, 48, 48)
            pygame.draw.rect(game, WHITE if data["skill9:"] == "True" else LIGHTGRAY, s9)
            if s9.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, LIGHTBLUE if data["skill9:"] == "True" else WHITE, s9)
            game.blit(transform(skill9_img, (48,48)), (s9.x, s9.y))
            s10 = pygame.Rect(palette_rect.x + 230, palette_rect.y + 80, 48, 48)
            pygame.draw.rect(game, WHITE if data["skill10:"] == "True" else LIGHTGRAY, s10)
            if s10.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(game, LIGHTBLUE if data["skill10:"] == "True" else WHITE, s10)
            game.blit(transform(skill10_img, (48,48)), (s10.x, s10.y))

            game.blit(comicsans(20).render("How To Change Skills?", 1, WHITE), (palette_rect.x + 50, palette_rect.y + 180))
            game.blit(comicsans(12).render("Click on any unlocked skills from SKILLS", 1, WHITE), (palette_rect.x + 40, palette_rect.y + 220))
            game.blit(comicsans(12).render("Then click on any unlocked slot in PALETTE", 1, WHITE), (palette_rect.x + 37, palette_rect.y + 240))
            game.blit(comicsans(12).render("This won't work with the first three SKILLS", 1, WHITE), (palette_rect.x + 30, palette_rect.y + 260))
                      

            
        if _cur_screen_ == "Home" or _cur_screen_ == "Settings" or _cur_screen_ == "Saves":
            game.blit(comicsans(20).render("The Keys To Navigate:", 1, WHITE), (_width_*0.8, _height_*0.7))
            game.blit(comicsans(20).render("W / Arrow Up = UP", 1, WHITE), (_width_*0.8, _height_*0.75))
            game.blit(comicsans(20).render("S / Arrow Dn = DN", 1, WHITE), (_width_*0.8, _height_*0.8))
            game.blit(comicsans(20).render("Spacebar to Confirm", 1, WHITE), (_width_*0.8, _height_*0.85))
        
        for e in pygame.event.get(): ##allow for application to quit
            if e.type == pygame.QUIT:
                gamerun = False
                pygame.quit()

            if e.type == pygame.MOUSEBUTTONDOWN and _cur_screen_ == "Selection":
                if e.button == 1:
                    if exitsel.collidepoint(pygame.mouse.get_pos()):
                        _cur_screen_ = "Camp"
                        menusound.play()
                    if tutbtn.collidepoint(pygame.mouse.get_pos()):
                        _cur_screen_ = "Tutorial Level"
                    if level2.collidepoint(pygame.mouse.get_pos()) and int(data["game_level:"]) > 0:
                        _cur_screen_ = "Level 2"
                    if level3.collidepoint(pygame.mouse.get_pos()) and int(data["game_level:"]) > 1:
                        _cur_screen_ = "Level 3"
                    if level4.collidepoint(pygame.mouse.get_pos()) and int(data["game_level:"]) > 2:
                        _cur_screen_ = "Level 4"
                    if level5.collidepoint(pygame.mouse.get_pos()) and int(data["game_level:"]) > 3:
                        _cur_screen_ = "Level 5"

            if e.type == pygame.MOUSEBUTTONDOWN and _cur_screen_ == "Shop":
                if e.button == 1:
                    if s4.collidepoint(pygame.mouse.get_pos()) and data["skill4:"] == "True":
                        data["skill4_item:"] = skillselected
                        savegame("data.dat", data)
                    if s5.collidepoint(pygame.mouse.get_pos()) and data["skill5:"] == "True":
                        data["skill5_item:"] = skillselected
                        savegame("data.dat", data)
                    if s6.collidepoint(pygame.mouse.get_pos()) and data["skill6:"] == "True":
                        data["skill6_item:"] = skillselected
                        savegame("data.dat", data)
                    if s7.collidepoint(pygame.mouse.get_pos()) and data["skill7:"] == "True":
                        data["skill7_item:"] = skillselected
                        savegame("data.dat", data)
                    if s8.collidepoint(pygame.mouse.get_pos()) and data["skill8:"] == "True":
                        data["skill8_item:"] = skillselected
                        savegame("data.dat", data)
                    if s9.collidepoint(pygame.mouse.get_pos()) and data["skill9:"] == "True":
                        data["skill9_item:"] = skillselected
                        savegame("data.dat", data)
                    if s10.collidepoint(pygame.mouse.get_pos()) and data["skill10:"] == "True":
                        data["skill10_item:"] = skillselected
                        savegame("data.dat", data)


                    if data["chartype:"] == "Knight":
                        if skill_slam.collidepoint(pygame.mouse.get_pos()):
                            if data["skill_k_slam:"] == "False" and int(data["skillpoints:"]) > 0:
                                data["skill_k_slam:"] = "True"
                                data["skillpoints:"] = str(int(data["skillpoints:"]) - 1)
                            elif data["skill_k_slam:"] == "True":
                                skillselected = "Slam" #for skill switching
                            savegame("data.dat", data)
                        if skill_ballistic.collidepoint(pygame.mouse.get_pos()):
                            if data["skill_k_ballistic_strike:"] == "False" and int(data["skillpoints:"]) > 0:
                                data["skill_k_ballistic_strike:"] = "True"
                                data["skillpoints:"] = str(int(data["skillpoints:"]) - 1)
                            elif data["skill_k_ballistic_strike:"] == "True":
                                skillselected = "Ballistic_Strike"
                            savegame("data.dat", data)
                        if skill_shield.collidepoint(pygame.mouse.get_pos()):
                            if data["skill_k_shield:"] == "False" and int(data["skillpoints:"]) > 0:
                                data["skill_k_shield:"] = "True"
                                data["skillpoints:"] = str(int(data["skillpoints:"]) - 1)
                            elif data["skill_k_shield:"] == "True":
                                skillselected = "Shield"
                            savegame("data.dat", data)
                        if skill_double.collidepoint(pygame.mouse.get_pos()):
                            if data["skill_k_double_strike:"] == "False" and int(data["skillpoints:"]) > 0:
                                data["skill_k_double_strike:"] = "True"
                                data["skillpoints:"] = str(int(data["skillpoints:"]) - 1)
                            elif data["skill_k_double_strike:"] == "True":
                                skillselected = "Double_Strike"
                            savegame("data.dat", data)
                        if skill_puncture.collidepoint(pygame.mouse.get_pos()):
                            if data["skill_k_puncture:"] == "False" and int(data["skillpoints:"]) > 0:
                                data["skill_k_puncture:"] = "True"
                                data["skillpoints:"] = str(int(data["skillpoints:"]) - 1)
                            elif data["skill_k_puncture:"] == "True":
                                skillselected = "Puncture"
                            savegame("data.dat", data)
                        if skill_stun.collidepoint(pygame.mouse.get_pos()):
                            if data["skill_k_stun:"] == "False" and int(data["skillpoints:"]) > 0:
                                data["skill_k_stun:"] = "True"
                                data["skillpoints:"] = str(int(data["skillpoints:"]) - 1)
                            elif data["skill_k_stun:"] == "True":
                                skillselected = "Stun"
                        if skill_suit.collidepoint(pygame.mouse.get_pos()):
                            if data["skill_k_suitup:"] == "False" and int(data["skillpoints:"]) > 0:
                                data["skill_k_suitup:"] = "True"
                                data["skillpoints:"] = str(int(data["skillpoints:"]) - 1)
                            elif data["skill_k_suitup:"] == "True":
                                skillselected = "Suit_Up"
                        if skill_enrage.collidepoint(pygame.mouse.get_pos()):
                            if data["skill_k_enrage:"] == "False" and int(data["skillpoints:"]) > 0:
                                data["skill_k_enrage:"] = "True"
                                data["skillpoints:"] = str(int(data["skillpoints:"]) - 1)
                            elif data["skill_k_enrage:"] == "True":
                                skillselected = "Enrage"
                        if skill_vampire.collidepoint(pygame.mouse.get_pos()):
                            if data["skill_k_vampire_strike:"] == "False" and int(data["skillpoints:"]) > 0:
                                data["skill_k_vampire_strike:"] = "True"
                                data["skillpoints:"] = str(int(data["skillpoints:"]) - 1)
                            elif data["skill_k_vampire_strike:"] == "True":
                                skillselected = "Vampire_Strike"
                    if data["chartype:"] == "Wizard":
                        if skill_fireball.collidepoint(pygame.mouse.get_pos()):
                            if data["skill_w_fireball:"] == "False" and int(data["skillpoints:"]) > 0:
                                data["skill_w_fireball:"] = "True"
                                data["skillpoints:"] = str(int(data["skillpoints:"]) - 1)
                            elif data["skill_w_fireball:"] == "True":
                                skillselected = "Fireball"
                        if skill_freeze.collidepoint(pygame.mouse.get_pos()):
                            if data["skill_w_freeze:"] == "False" and int(data["skillpoints:"]) > 0:
                                data["skill_w_freeze:"] = "True"
                                data["skillpoints:"] = str(int(data["skillpoints:"]) - 1)
                            elif data["skill_w_freeze:"] == "True":
                                skillselected = "Freeze"
                        if skill_drain.collidepoint(pygame.mouse.get_pos()):
                            if data["skill_w_drain:"] == "False" and int(data["skillpoints:"]) > 0:
                                data["skill_w_drain:"] = "True"
                                data["skillpoints:"] = str(int(data["skillpoints:"]) - 1)
                            elif data["skill_w_drain:"] == "True":
                                skillselected = "Drain"
                        if skill_invert.collidepoint(pygame.mouse.get_pos()):
                            if data["skill_w_invert:"] == "False" and int(data["skillpoints:"]) > 0:
                                data["skill_w_invert:"] = "True"
                                data["skillpoints:"] = str(int(data["skillpoints:"]) - 1)
                            elif data["skill_w_invert:"] == "True":
                                skillselected = "Invert"
                        if skill_leech.collidepoint(pygame.mouse.get_pos()):
                            if data["skill_w_leech:"] == "False" and int(data["skillpoints:"]) > 0:
                                data["skill_w_leech:"] = "True"
                                data["skillpoints:"] = str(int(data["skillpoints:"]) - 1)
                            elif data["skill_w_leech:"] == "True":
                                skillselected = "Leech"
                        if skill_life.collidepoint(pygame.mouse.get_pos()):
                            if data["skill_w_life:"] == "False" and int(data["skillpoints:"]) > 0:
                                data["skill_w_life:"] = "True"
                                data["skillpoints:"] = str(int(data["skillpoints:"]) - 1)
                            elif data["skill_w_life:"] == "True":
                                skillselected = "Life"
                        if skill_lightning.collidepoint(pygame.mouse.get_pos()):
                            if data["skill_w_lightning_strike:"] == "False" and int(data["skillpoints:"]) > 0:
                                data["skill_w_lightning_strike:"] = "True"
                                data["skillpoints:"] = str(int(data["skillpoints:"]) - 1)
                            elif data["skill_w_lightning_strike:"] == "True":
                                skillselected = "Lightning_Strike"
                        if skill_soul.collidepoint(pygame.mouse.get_pos()):
                            if data["skill_w_soul_crush:"] == "False" and int(data["skillpoints:"]) > 0:
                                data["skill_w_soul_crush:"] = "True"
                                data["skillpoints:"] = str(int(data["skillpoints:"]) - 1)
                            elif data["skill_w_soul_crush:"] == "True":
                                skillselected = "Soul_Crush"
                        if skill_weakness.collidepoint(pygame.mouse.get_pos()):
                            if data["skill_w_weakness:"] == "False" and int(data["skillpoints:"]) > 0:
                                data["skill_w_weakness:"] = "True"
                                data["skillpoints:"] = str(int(data["skillpoints:"]) - 1)
                            elif data["skill_w_weakness:"] == "True":
                                skillselected = "Weakness"

                    if data["chartype:"] == "Assassin":
                        if skill_amputate.collidepoint(pygame.mouse.get_pos()):
                            if data["skill_a_amputate:"] == "False" and int(data["skillpoints:"]) > 0:
                                data["skill_a_amputate:"] = "True"
                                data["skillpoints:"] = str(int(data["skillpoints:"]) - 1)
                            elif data["skill_a_amputate:"] == "True":
                                skillselected = "Amputate"
                        if skill_blindside.collidepoint(pygame.mouse.get_pos()):
                            if data["skill_a_blindside:"] == "False" and int(data["skillpoints:"]) > 0:
                                data["skill_a_blindside:"] = "True"
                                data["skillpoints:"] = str(int(data["skillpoints:"]) - 1)
                            elif data["skill_a_blindside:"] == "True":
                                skillselected = "Blindside"
                        if skill_dragon.collidepoint(pygame.mouse.get_pos()):
                            if data["skill_a_dragons_breath:"] == "False" and int(data["skillpoints:"]) > 0:
                                data["skill_a_dragons_breath:"] = "True"
                                data["skillpoints:"] = str(int(data["skillpoints:"]) - 1)
                            elif data["skill_a_dragons_breath:"] == "True":
                                skillselected = "Dragons_Breath"
                        if skill_fury.collidepoint(pygame.mouse.get_pos()):
                            if data["skill_a_fury_strike:"] == "False" and int(data["skillpoints:"]) > 0:
                                data["skill_a_fury_strike:"] = "True"
                                data["skillpoints:"] = str(int(data["skillpoints:"]) - 1)
                            elif data["skill_a_fury_strike:"] == "True":
                                skillselected = "Fury_Strike"
                        if skill_overcharge.collidepoint(pygame.mouse.get_pos()):
                            if data["skill_a_overcharge:"] == "False" and int(data["skillpoints:"]) > 0:
                                data["skill_a_overcharge:"] = "True"
                                data["skillpoints:"] = str(int(data["skillpoints:"]) - 1)
                            elif data["skill_a_overcharge:"] == "True":
                                skillselected = "Overcharge"
                        if skill_poison.collidepoint(pygame.mouse.get_pos()):
                            if data["skill_a_poison:"] == "False" and int(data["skillpoints:"]) > 0:
                                data["skill_a_poison:"] = "True"
                                data["skillpoints:"] = str(int(data["skillpoints:"]) - 1)
                            elif data["skill_a_poison:"] == "True":
                                skillselected = "Poison"
                        if skill_shuriken.collidepoint(pygame.mouse.get_pos()):
                            if data["skill_a_shuriken:"] == "False" and int(data["skillpoints:"]) > 0:
                                data["skill_a_shuriken:"] = "True"
                                data["skillpoints:"] = str(int(data["skillpoints:"]) - 1)
                            elif data["skill_a_shuriken:"] == "True":
                                skillselected = "Shuriken"
                        if skill_slash.collidepoint(pygame.mouse.get_pos()):
                            if data["skill_a_slash:"] == "False" and int(data["skillpoints:"]) > 0:
                                data["skill_a_slash:"] = "True"
                                data["skillpoints:"] = str(int(data["skillpoints:"]) - 1)
                            elif data["skill_a_slash:"] == "True":
                                skillselected = "Slash"
                        if skill_speed.collidepoint(pygame.mouse.get_pos()):
                            if data["skill_a_speed:"] == "False" and int(data["skillpoints:"]) > 0:
                                data["skill_a_speed:"] = "True"
                                data["skillpoints:"] = str(int(data["skillpoints:"]) - 1)
                            elif data["skill_a_speed:"] == "True":
                                skillselected = "Speed"


                    if resetskills.collidepoint(pygame.mouse.get_pos()):
                        #make sure that the skill slots get their items removed too
                        data["skill4_item:"] = "None"
                        data["skill5_item:"] = "None"
                        data["skill6_item:"] = "None"
                        data["skill7_item:"] = "None"
                        data["skill8_item:"] = "None"
                        data["skill9_item:"] = "None"
                        data["skill10_item:"] = "None"
                        #removing skills individually process
                        if data["skill_k_slam:"] == "True":
                            data["skill_k_slam:"] = "False"
                            data["skillpoints:"] = str(int(data["skillpoints:"]) + 1)
                        if data["skill_k_ballistic_strike:"] == "True":
                            data["skill_k_ballistic_strike:"] = "False"
                            data["skillpoints:"] = str(int(data["skillpoints:"]) + 1)
                        if data["skill_k_shield:"] == "True":
                            data["skill_k_shield:"] = "False"
                            data["skillpoints:"] = str(int(data["skillpoints:"]) + 1)
                        if data["skill_k_stun:"] == "True":
                            data["skill_k_stun:"] = "False"
                            data["skillpoints:"] = str(int(data["skillpoints:"]) + 1)
                        if data["skill_k_double_strike:"] == "True":
                            data["skill_k_double_strike:"] = "False"
                            data["skillpoints:"] = str(int(data["skillpoints:"]) + 1)
                        if data["skill_k_enrage:"] == "True":
                            data["skill_k_enrage:"] = "False"
                            data["skillpoints:"] = str(int(data["skillpoints:"]) + 1)
                        if data["skill_k_puncture:"] == "True":
                            data["skill_k_puncture:"] = "False"
                            data["skillpoints:"] = str(int(data["skillpoints:"]) + 1)
                        if data["skill_k_suitup:"] == "True":
                            data["skill_k_suitup:"] = "False"
                            data["skillpoints:"] = str(int(data["skillpoints:"]) + 1)
                        if data["skill_k_vampire_strike:"] == "True":
                            data["skill_k_vampire_strike:"] = "False"
                            data["skillpoints:"] = str(int(data["skillpoints:"]) + 1)

                        if data["skill_w_fireball:"] == "True":
                            data["skill_w_fireball:"] = "False"
                            data["skillpoints:"] = str(int(data["skillpoints:"]) + 1)
                        if data["skill_w_freeze:"] == "True":
                            data["skill_w_freeze:"] = "False"
                            data["skillpoints:"] = str(int(data["skillpoints:"]) + 1)
                        if data["skill_w_invert:"] == "True":
                            data["skill_w_invert:"] = "False"
                            data["skillpoints:"] = str(int(data["skillpoints:"]) + 1)
                        if data["skill_w_life:"] == "True":
                            data["skill_w_life:"] = "False"
                            data["skillpoints:"] = str(int(data["skillpoints:"]) + 1)
                        if data["skill_w_drain:"] == "True":
                            data["skill_w_drain:"] = "False"
                            data["skillpoints:"] = str(int(data["skillpoints:"]) + 1)
                        if data["skill_w_lightning_strike:"] == "True":
                            data["skill_w_lightning_strike:"] = "False"
                            data["skillpoints:"] = str(int(data["skillpoints:"]) + 1)
                        if data["skill_w_weakness:"] == "True":
                            data["skill_w_weakness:"] = "False"
                            data["skillpoints:"] = str(int(data["skillpoints:"]) + 1)
                        if data["skill_w_soul_crush:"] == "True":
                            data["skill_w_soul_crush:"] = "False"
                            data["skillpoints:"] = str(int(data["skillpoints:"]) + 1)
                        if data["skill_w_leech:"] == "True":
                            data["skill_w_leech:"] = "False"
                            data["skillpoints:"] = str(int(data["skillpoints:"]) + 1)

                        if data["skill_a_slash:"] == "True":
                            data["skill_a_slash:"] = "False"
                            data["skillpoints:"] = str(int(data["skillpoints:"]) + 1)
                        if data["skill_a_poison:"] == "True":
                            data["skill_a_poison:"] = "False"
                            data["skillpoints:"] = str(int(data["skillpoints:"]) + 1)
                        if data["skill_a_speed:"] == "True":
                            data["skill_a_speed:"] = "False"
                            data["skillpoints:"] = str(int(data["skillpoints:"]) + 1)
                        if data["skill_a_blindside:"] == "True":
                            data["skill_a_blindside:"] = "False"
                            data["skillpoints:"] = str(int(data["skillpoints:"]) + 1)
                        if data["skill_a_shuriken:"] == "True":
                            data["skill_a_shuriken:"] = "False"
                            data["skillpoints:"] = str(int(data["skillpoints:"]) + 1)
                        if data["skill_a_fury_strike:"] == "True":
                            data["skill_a_fury_strike:"] = "False"
                            data["skillpoints:"] = str(int(data["skillpoints:"]) + 1)
                        if data["skill_a_dragons_breath:"] == "True":
                            data["skill_a_dragons_breath:"] = "False"
                            data["skillpoints:"] = str(int(data["skillpoints:"]) + 1)
                        if data["skill_a_overcharge:"] == "True":
                            data["skill_a_overcharge:"] = "False"
                            data["skillpoints:"] = str(int(data["skillpoints:"]) + 1)
                        if data["skill_a_amputate:"] == "True":
                            data["skill_a_amputate:"] = "False"
                            data["skillpoints:"] = str(int(data["skillpoints:"]) + 1)

                    if exit_shop.collidepoint(pygame.mouse.get_pos()):
                        _cur_screen_ = "Camp"
                        ##events for when attributes are modified
                    if add_vitality.collidepoint(pygame.mouse.get_pos()):
                        if int(data["attributepoints:"]) > 0:
                            data["vitality:"] = str(int(data["vitality:"]) + 1)
                            data["attributepoints:"] = str(int(data["attributepoints:"]) - 1)
                            savegame("data.dat", data)
                    if minus_vitality.collidepoint(pygame.mouse.get_pos()):
                        if data["chartype:"] == "Knight" or data["chartype:"] == "Wizard" or data["chartype:"] == "Assassin":
                            if int(data["vitality:"]) < 11:
                                data["vitality:"] = "10"
                            else:
                                data["vitality:"] = str(int(data["vitality:"]) - 1)
                                data["attributepoints:"] = str(int(data["attributepoints:"]) + 1)
                        savegame("data.dat", data)
                    if add_strength.collidepoint(pygame.mouse.get_pos()):
                        if int(data["attributepoints:"]) > 0:
                            data["strength:"] = str(int(data["strength:"]) + 1)
                            data["attributepoints:"] = str(int(data["attributepoints:"]) - 1)
                            savegame("data.dat", data)
                    if minus_strength.collidepoint(pygame.mouse.get_pos()):
                        if data["chartype:"] == "Knight" and int(data["strength:"]) < 16:
                            data["strength:"] = "15"
                        elif data["chartype:"] == "Wizard" and int(data["strength:"]) < 5:
                            data["strength:"] = "4"
                        elif data["chartype:"] == "Assassin" and int(data["strength:"]) < 6:
                            data["strength:"] = "5"
                        else:
                            data["strength:"] = str(int(data["strength:"]) - 1)
                            data["attributepoints:"] = str(int(data["attributepoints:"]) + 1)
                        savegame("data.dat", data)
                    if add_magic.collidepoint(pygame.mouse.get_pos()):
                        if int(data["attributepoints:"]) > 0:
                            data["magic:"] = str(int(data["magic:"]) + 1)
                            data["attributepoints:"] = str(int(data["attributepoints:"]) - 1)
                            savegame("data.dat", data)
                    if minus_magic.collidepoint(pygame.mouse.get_pos()):
                            if data["chartype:"] == "Knight" and int(data["magic:"]) < 3:
                                data["magic:"] = "2"
                            elif data["chartype:"] == "Wizard" and int(data["magic:"]) < 11:
                                data["magic:"] = "10"
                            elif data["chartype:"] == "Assassin" and int(data["magic:"]) < 6:
                                data["magic:"] = "5"
                            else:
                                data["magic:"] = str(int(data["magic:"]) - 1)
                                data["attributepoints:"] = str(int(data["attributepoints:"]) + 1)
                    if add_speed.collidepoint(pygame.mouse.get_pos()):
                        if int(data["attributepoints:"]) > 0:
                            data["speed:"] = str(int(data["speed:"]) + 1)
                            data["attributepoints:"] = str(int(data["attributepoints:"]) - 1)
                            savegame("data.dat", data)
                    if minus_speed.collidepoint(pygame.mouse.get_pos()):
                        if data["chartype:"] == "Knight" and int(data["speed:"]) < 4:
                            data["speed:"] = "3"
                        elif data["chartype:"] == "Wizard" and int(data["speed:"]) < 7:
                            data["speed:"] = "6"
                        elif data["chartype:"] == "Assassin" and int(data["speed:"]) < 11:
                            data["speed:"] = "10"
                        else:
                            data["speed:"] = str(int(data["speed:"]) - 1)
                            data["attributepoints:"] = str(int(data["attributepoints:"]) + 1)
                    

            if e.type == pygame.MOUSEBUTTONDOWN and _cur_screen_ == "Camp":
                if e.button == 1:
                    if exit_camp.collidepoint(pygame.mouse.get_pos()):
                        _cur_screen_ = "Home"
                        battlebegin = False
                        battletimer = 0
                        if soundon == True:
                            menusound.play()
                    if shop.collidepoint(pygame.mouse.get_pos()):
                        _cur_screen_ = "Shop"
                    if battle.collidepoint(pygame.mouse.get_pos()):
                        if int(data["game_level:"]) == 1:
                            _cur_screen_ = "Level 2"
                        elif int(data["game_level:"]) == 2:
                            _cur_screen_ = "Level 3"
                        elif int(data["game_level:"]) == 3:
                            _cur_screen_ = "Level 4"
                        elif int(data["game_level:"]) == 4:
                            _cur_screen_ = "Level 5"
                    if battle_return.collidepoint(pygame.mouse.get_pos()):
                        _cur_screen_ = "Selection"

            if e.type == pygame.MOUSEBUTTONDOWN and exiticon.collidepoint(pygame.mouse.get_pos()) and (_cur_screen_ == "Tutorial Level" or _cur_screen_ == "Level 2" or _cur_screen_ == "Level 3" or _cur_screen_ == "Level 4" or _cur_screen_ == "Level 5"):
                if e.button == 1: #reset all cooldowns and variables so battles are not bugged
                    if data["game_level:"] == "0":
                        _cur_screen_ = "Home"
                    else:
                        _cur_screen_ = "Camp"
                    curTurn = "Self"
                    battlebegin = False
                    battletimer = 0
                    numset = False
                    enemyset = False
                    skillused = ""
                    punc = 0
                    dbcooldown = 0
                    punccooldown = 0
                    bscooldown = 0
                    bscount = 0
                    stuncooldown = 0
                    stun = 0
                    shieldcount = 0
                    shieldcooldown = 0
                    slamdown = 0
                    enrage = 0
                    enragecooldown = 0
                    vampirecooldown = 0
                    suit = 0
                    suitcooldown = 0

                    fire = 0
                    fireballcooldown = 0
                    freeze = 0
                    freezecooldown = 0
                    draincooldown = 0
                    invert = 0
                    invertcooldown = 0
                    leechcooldown = 0
                    lifecooldown = 0
                    life = 0
                    lightning = 0
                    lightningcooldown = 0
                    soul = 0
                    soulcooldown = 0
                    weakness = 0
                    weaknesscooldown = 0

                    amputate = 0
                    amputatecooldown = 0
                    blindsidecooldown = 0
                    dragon = 0
                    dragoncooldown = 0
                    furycooldown = 0
                    overcharge = 0
                    overchargecooldown = 0
                    poison = 0
                    poisoncooldown = 0
                    shurikencooldown = 0
                    slashcooldown = 0
                    speed = 0
                    speedcooldown = 0
                
                    if soundon == True:
                        menusound.play()

            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    if restartbutton.collidepoint(pygame.mouse.get_pos()):
                        if _cur_screen_ == "Tutorial Level":
                            _cur_screen_ = "Tutorial Level"
                        if _cur_screen_ == "Level 2":
                            _cur_screen_ = "Level 2"
                        if _cur_screen_ == "Level 3":
                            _cur_screen_ = "Level 3"
                        if _cur_screen_ == "Level 4":
                            _cur_screen_ = "Level 4"
                        if _cur_screen_ == "Level 5":
                            _cur_screen_ = "Level 5"
                        curTurn = "Self"
                        battlebegin = False
                        battletimer = 0
                        numset = False
                        enemyset = False
                        skillused = ""
                        punc = 0
                        dbcooldown = 0
                        punccooldown = 0
                        bscooldown = 0
                        bscount = 0
                        stuncooldown = 0
                        stun = 0
                        shieldcount = 0
                        shieldcooldown = 0
                        slamdown = 0
                        enrage = 0
                        enragecooldown = 0
                        vampirecooldown = 0
                        suit = 0
                        suitcooldown = 0

                        fire = 0
                        fireballcooldown = 0
                        freeze = 0
                        freezecooldown = 0
                        draincooldown = 0
                        invert = 0
                        invertcooldown = 0
                        leechcooldown = 0
                        lifecooldown = 0
                        life = 0
                        lightning = 0
                        lightningcooldown = 0
                        soul = 0
                        soulcooldown = 0
                        weakness = 0
                        weaknesscooldown = 0

                        amputate = 0
                        amputatecooldown = 0
                        blindsidecooldown = 0
                        dragon = 0
                        dragoncooldown = 0
                        furycooldown = 0
                        overcharge = 0
                        overchargecooldown = 0
                        poison = 0
                        poisoncooldown = 0
                        shurikencooldown = 0
                        slashcooldown = 0
                        speed = 0
                        speedcooldown = 0
                        if soundon == True:
                            menusound.play()
                    
                    if returnbutton.collidepoint(pygame.mouse.get_pos()):
                        _cur_screen_ = "Camp"
                        curTurn = "Self"
                        battlebegin = False
                        battletimer = 0
                        numset = False
                        enemyset = False
                        skillused = ""
                        punc = 0
                        dbcooldown = 0
                        punccooldown = 0
                        bscooldown = 0
                        bscount = 0
                        stuncooldown = 0
                        stun = 0
                        shieldcount = 0
                        shieldcooldown = 0
                        slamdown = 0
                        enrage = 0
                        enragecooldown = 0
                        vampirecooldown = 0
                        suit = 0
                        suitcooldown = 0

                        fire = 0
                        fireballcooldown = 0
                        freeze = 0
                        freezecooldown = 0
                        draincooldown = 0
                        invert = 0
                        invertcooldown = 0
                        leechcooldown = 0
                        lifecooldown = 0
                        life = 0
                        lightning = 0
                        lightningcooldown = 0
                        soul = 0
                        soulcooldown = 0
                        weakness = 0
                        weaknesscooldown = 0

                        amputate = 0
                        amputatecooldown = 0
                        blindsidecooldown = 0
                        dragon = 0
                        dragoncooldown = 0
                        furycooldown = 0
                        overcharge = 0
                        overchargecooldown = 0
                        poison = 0
                        poisoncooldown = 0
                        shurikencooldown = 0
                        slashcooldown = 0
                        speed = 0
                        speedcooldown = 0
                        xp_gained = 0
                        if data["level:"] == "0":
                            data["level:"] = str(int(data["level:"]) + 1)
                        if data["level:"] == "1":
                            data["level:"] = str(int(data["level:"]) + 1)
                        if data["level:"] == "2":
                            data["level:"] = str(int(data["level:"]) + 1)
                        if data["level:"] == "3":
                            data["level:"] = str(int(data["level:"]) + 1)
                        savegame("data.dat", data)
                        if xp_slider > 1.00: #if decimal is equal to 100% or greater add levelling up bonuses to character data
                            data["experience_to_next_level:"] = str(int(data["experience_to_next_level:"])*2) ##double the amount of xp needed each time
                            data["skillpoints:"] = str(int(data["skillpoints:"]) + 2)
                            data["game_level:"] = str(int(data["game_level:"])+1)
                            data["experience:"] = 0 #fresh start the experience
                            data["attributepoints:"] = str(int(data["attributepoints:"]) + 5)
                            if data["level:"] == "2":
                                data["skill4:"] = "True"
                                data["skill4_item:"] = "None"
                            if data["level:"] == "4":
                                data["skill5:"] = "True"
                                data["skill5_item:"] = "None"
                            if data["level:"] == "5":
                                data["skill6:"] = "True"
                                data["skill6_item:"] = "None"
                            if data["level:"] == "7":
                                data["skill7:"] = "True"
                                data["skill7_item:"] = "None"
                            if data["level:"] == "8":
                                data["skill8:"] = "True"
                                data["skill8_item:"] = "None"
                            if data["level:"] == "9":
                                data["skill9:"] = "True"
                                data["skill9_item:"] = "None"
                            if data["level:"] == "10":
                                data["skill10:"] = "True"
                                data["skill10_item:"] = "None"
                            savegame("data.dat", data)
                            xp_slider = int(data["experience:"]) / int(data["experience_to_next_level:"])
                        if soundon == True:
                            menusound.play()

                    if gotocampbtn.collidepoint(pygame.mouse.get_pos()):
                        _cur_screen_ = "Camp"
                        curTurn = "Self"
                        battlebegin = False
                        battletimer = 0
                        numset = False
                        enemyset = False
                        skillused = ""
                        punc = 0
                        dbcooldown = 0
                        punccooldown = 0
                        bscooldown = 0
                        bscount = 0
                        stuncooldown = 0
                        stun = 0
                        shieldcount = 0
                        shieldcooldown = 0
                        slamdown = 0
                        enrage = 0
                        enragecooldown = 0
                        vampirecooldown = 0
                        suit = 0
                        suitcooldown = 0

                        fire = 0
                        fireballcooldown = 0
                        freeze = 0
                        freezecooldown = 0
                        draincooldown = 0
                        invert = 0
                        invertcooldown = 0
                        leechcooldown = 0
                        lifecooldown = 0
                        life = 0
                        lightning = 0
                        lightningcooldown = 0
                        soul = 0
                        soulcooldown = 0
                        weakness = 0
                        weaknesscooldown = 0

                        amputate = 0
                        amputatecooldown = 0
                        blindsidecooldown = 0
                        dragon = 0
                        dragoncooldown = 0
                        furycooldown = 0
                        overcharge = 0
                        overchargecooldown = 0
                        poison = 0
                        poisoncooldown = 0
                        shurikencooldown = 0
                        slashcooldown = 0
                        speed = 0
                        speedcooldown = 0
                        xp_gained = 0
                        if data["level:"] == "0":
                            data["level:"] = str(int(data["level:"]) + 1)
                        if data["level:"] == "1":
                            data["level:"] = str(int(data["level:"]) + 1)
                        if data["level:"] == "2":
                            data["level:"] = str(int(data["level:"]) + 1)
                        if data["level:"] == "3":
                            data["level:"] = str(int(data["level:"]) + 1)
                        savegame("data.dat", data)
                        if xp_slider > 1.00: #if decimal is equal to 100% or greater add levelling up bonuses to character data
                            data["experience_to_next_level:"] = str(int(data["experience_to_next_level:"])*2) ##double the amount of xp needed each time
                            data["skillpoints:"] = str(int(data["skillpoints:"]) + 2)
                            data["game_level:"] = str(int(data["game_level:"])+1)
                            data["experience:"] = 0 #fresh start the experience
                            data["attributepoints:"] = str(int(data["attributepoints:"]) + 5)
                            if data["level:"] == "2":
                                data["skill4:"] = "True"
                                data["skill4_item:"] = "None"
                            if data["level:"] == "4":
                                data["skill5:"] = "True"
                                data["skill5_item:"] = "None"
                            if data["level:"] == "5":
                                data["skill6:"] = "True"
                                data["skill6_item:"] = "None"
                            if data["level:"] == "7":
                                data["skill7:"] = "True"
                                data["skill7_item:"] = "None"
                            if data["level:"] == "8":
                                data["skill8:"] = "True"
                                data["skill8_item:"] = "None"
                            if data["level:"] == "9":
                                data["skill9:"] = "True"
                                data["skill9_item:"] = "None"
                            if data["level:"] == "10":
                                data["skill10:"] = "True"
                                data["skill10_item:"] = "None"
                            savegame("data.dat", data)
                            xp_slider = int(data["experience:"]) / int(data["experience_to_next_level:"])
                        if soundon == True:
                            menusound.play()
                        


            if e.type == pygame.KEYDOWN and _cur_screen_ == "Home":
                if e.key == pygame.K_w or e.key == pygame.K_UP:
                    if _menu_option_ == options[0]:
                        _menu_option_ = options[0]
                    elif _menu_option_ == options[1]:
                        _menu_option_ = options[0]
                    elif _menu_option_ == options[2]:
                        _menu_option_ = options[1]
                    elif _menu_option_ == options[3]:
                        _menu_option_ = options[2]
                    else:
                        _menu_option_ = options[0]
                    if soundon == True:
                        menusound.play()

                if e.key == pygame.K_s or e.key == pygame.K_DOWN:
                    if _menu_option_ == options[0]:
                        _menu_option_ = options[1]
                    elif _menu_option_ == options[1]:
                        _menu_option_ = options[2]
                    elif _menu_option_ == options[2]:
                        _menu_option_ = options[3]
                    elif _menu_option_ == options[3]:
                        _menu_option_ = options[3]
                    else:
                        _menu_option_ = options[3]
                    if soundon==True:
                        menusound.play()

                if e.key == pygame.K_SPACE:
                    if _menu_option_ == options[0]:
                        _cur_screen_ = "Play"
                        _menu_option_ = options[0] #reset
                    elif _menu_option_ == options[1]:
                        _cur_screen_ = "Saves"
                        _menu_option_ = options[0] # reset
                    elif _menu_option_ == options[2]:
                        _cur_screen_ = "Settings"
                        _menu_option_ = options[0] # reset
                    elif _menu_option_ == options[3]:
                        gamerun = False
                        pygame.quit()
                    if soundon==True:
                        menusound.play()

            elif e.type == pygame.KEYDOWN and _cur_screen_ == "Settings":
                if e.key == pygame.K_w or e.key == pygame.K_UP:
                    if _settings_option_ == "Resolution":
                        _settings_option_ = "Resolution"
                    elif _settings_option_ == "Audio":
                        _settings_option_ = "Resolution"
                    elif _settings_option_ == "FPS":
                        _settings_option_ = "Audio"
                    elif _settings_option_ == "Exit":
                        _settings_option_ = "FPS"
                    if soundon == True:
                        menusound.play()

                if e.key == pygame.K_s or e.key == pygame.K_DOWN:
                    if _settings_option_ == "Resolution":
                        _settings_option_ = "Audio"
                    elif _settings_option_ == "Audio":
                        _settings_option_ = "FPS"
                    elif _settings_option_ == "FPS":
                        _settings_option_ = "Exit"
                    if soundon==True:
                        menusound.play()

                if e.key == pygame.K_SPACE:
                    if _settings_option_ == "Resolution":
                        if _width_ == 1280 and _height_ == 720:
                            _width_ = 1080
                            _height_ = 660
                            pygame.display.set_mode((_width_, _height_))
                        #elif _width_ == 1920 and _height_ == 1080: removed due to scaling issues
                        #    _width_ = 1080
                        #    _height_ = 660
                        #    pygame.display.set_mode((_width_, _height_))
                        elif _width_ == 1080 and _height_ == 660:
                            _width_ = 1280
                            _height_ = 720
                            pygame.display.set_mode((_width_, _height_))
                        data["width:"] = _width_
                        data["height:"] = _height_
                    elif _settings_option_ == "Audio":
                        if soundon == True:
                            soundon = False
                        else:
                            soundon = True
                        data["audio:"] = "ON" if soundon == True else "OFF"
                    elif _settings_option_ == "FPS":
                        if _fps_ == 30:
                            _fps_ = 60
                        elif _fps_ == 60:
                            _fps_ = 90
                        elif _fps_ == 90:
                            _fps_ = 120
                        elif _fps_ == 120:
                            _fps_ = 144
                        elif _fps_ == 144:
                            _fps_ = 165
                        elif _fps_ == 165:
                            _fps_ = 30
                        data["frames:"] = _fps_
                    elif _settings_option_ == "Exit":
                        _cur_screen_ = "Home"
                        _settings_option_ = "Resolution" #reset
                    if soundon==True:
                        menusound.play()
                    savegame("data.dat", data)

            elif e.type == pygame.KEYDOWN and _cur_screen_ == "Saves":
                if e.key == pygame.K_SPACE:
                    _cur_screen_ = "Home"
                    if soundon == True:
                        menusound.play()

            elif e.type == pygame.KEYDOWN and _cur_screen_ == "Play":
                if e.key == pygame.K_d or e.key == pygame.K_RIGHT:
                    if _char_option_ == "Knight":
                        _char_option_ = "Wizard"
                    elif _char_option_ == "Wizard":
                        _char_option_ = "Assassin"
                    elif _char_option_ == "Assassin":
                        _char_option_ = "Assassin"
                    if soundon == True:
                        menusound.play()
                if e.key == pygame.K_a or e.key == pygame.K_LEFT:
                    if _char_option_ == "Knight":
                        _char_option_ = "Knight"
                    elif _char_option_ == "Wizard":
                        _char_option_ = "Knight"
                    elif _char_option_ == "Assassin":
                        _char_option_ = "Wizard"
                    if soundon == True:
                        menusound.play()

                if e.key == pygame.K_s or e.key == pygame.K_DOWN:
                    _char_option_ = "Exit"
                    if soundon == True:
                        menusound.play()
                if e.key == pygame.K_w or e.key == pygame.K_UP:
                    if _char_option_ == "Exit":
                        _char_option_ = "Knight"
                    if soundon == True:
                        menusound.play()

                
                if e.key == pygame.K_SPACE:
                    if _char_option_ == "Knight":
                        #time to create new data sets
                        data["chartype:"] = "Knight"
                        data["vitality:"] = 10
                        data["magic:"] = 2
                        data["strength:"] = 15
                        data["speed:"] = 3
                        data["level:"] = 1
                        data["skillpoints:"] = 0
                        data["attributepoints:"] = 0
                        data["experience:"] = 0
                        data["experience_to_next_level:"] = 100
                        data["game_level:"] = 0
                    elif _char_option_ == "Wizard":
                        data["chartype:"] = "Wizard"
                        data["vitality:"] = 10
                        data["magic:"] = 10
                        data["strength:"] = 4
                        data["speed:"] = 6
                        data["level:"] = 1
                        data["skillpoints:"] = 0
                        data["attributepoints:"] = 0
                        data["experience:"] = 0
                        data["experience_to_next_level:"] = 100
                        data["game_level:"] = 0
                    elif _char_option_ == "Assassin":
                        data["chartype:"] = "Assassin"
                        data["vitality:"] = 10
                        data["magic:"] = 5
                        data["strength:"] = 5
                        data["speed:"] = 10
                        data["level:"] = 1
                        data["skillpoints:"] = 0
                        data["attributepoints:"] = 0
                        data["experience:"] = 0
                        data["experience_to_next_level:"] = 100
                        data["game_level:"] = 0
                    elif _char_option_ == "Exit":
                        _cur_screen_ = "Home"
                        _char_option_ = "Knight"
                    if soundon == True:
                        menusound.play()
                    ##create skills data that allows the game to understand whats unlocked and what isn't
                    data["skill_basic:"] = True
                    data["skill_heal:"] = True
                    data["skill_mana:"] = True
                    #add entries for each class skills
                    #--knight skills--
                    data["skill_k_slam:"] = False 
                    data["skill_k_ballistic_strike:"] = False 
                    data["skill_k_shield:"] = False 
                    data["skill_k_stun:"] = False 
                    data["skill_k_double_strike:"] = False 
                    data["skill_k_enrage:"] = False 
                    data["skill_k_puncture:"] = False 
                    data["skill_k_suitup:"] = False 
                    data["skill_k_vampire_strike:"] = False 

                    #--Wizard Skills--
                    data["skill_w_fireball:"] = False 
                    data["skill_w_freeze:"] = False
                    data["skill_w_invert:"] = False 
                    data["skill_w_life:"] = False 
                    data["skill_w_drain:"] = False 
                    data["skill_w_lightning_strike:"] = False
                    data["skill_w_weakness:"] = False 
                    data["skill_w_soul_crush:"] = False 
                    data["skill_w_leech:"] = False 

                    #--Assassin Skills--
                    data["skill_a_slash:"] = False 
                    data["skill_a_poison:"] = False 
                    data["skill_a_speed:"] = False 
                    data["skill_a_blindside:"] = False 
                    data["skill_a_shuriken:"] = False 
                    data["skill_a_fury_strike:"] = False
                    data["skill_a_dragons_breath:"] = False 
                    data["skill_a_overcharge:"] = False 
                    data["skill_a_amputate:"] = False 

                    #make the slots unlockable
                    data["skill1:"] = True
                    data["skill2:"] = True
                    data["skill3:"] = True
                    data["skill4:"] = False
                    data["skill5:"] = False
                    data["skill6:"] = False
                    data["skill7:"] = False
                    data["skill8:"] = False
                    data["skill9:"] = False
                    data["skill10:"] = False

                    ##add data that identifies what skills link to which slots
                    data["skill1_item:"] = "Basic_Attack"
                    data["skill2_item:"] = "Heal"
                    data["skill3_item:"] = "Mana"
                    data["skill4_item:"] = "None"
                    data["skill5_item:"] = "None"
                    data["skill6_item:"] = "None"
                    data["skill7_item:"] = "None"
                    data["skill8_item:"] = "None"
                    data["skill9_item:"] = "None"
                    data["skill10_item:"] = "None"
                    savegame("data.dat", data)
                    #fix xp slider
                    xp_slider = int(data["experience:"]) / int(data["experience_to_next_level:"])
            elif _cur_screen_ in levels and curTurn == "Self":
                if e.type == pygame.MOUSEBUTTONDOWN and skill1.collidepoint(pygame.mouse.get_pos()):
                    if e.button == 1:
                        skillused = data["skill1_item:"]
                        if soundon == True:
                            skillsound.play()
                if e.type == pygame.MOUSEBUTTONDOWN and skill2.collidepoint(pygame.mouse.get_pos()):
                    if e.button == 1:
                        skillused = data["skill2_item:"]
                        if soundon == True:
                            skillsound.play()
                if e.type == pygame.MOUSEBUTTONDOWN and skill3.collidepoint(pygame.mouse.get_pos()):
                    if e.button == 1:
                        skillused = data["skill3_item:"]
                        if soundon == True:
                            skillsound.play()
                if e.type == pygame.MOUSEBUTTONDOWN and skill4.collidepoint(pygame.mouse.get_pos()):
                    if e.button == 1:
                        skillused = data["skill4_item:"]
                        if soundon == True:
                            skillsound.play()
                if e.type == pygame.MOUSEBUTTONDOWN and skill5.collidepoint(pygame.mouse.get_pos()):
                    if e.button == 1:
                        skillused = data["skill5_item:"]
                        if soundon == True:
                            skillsound.play()
                if e.type == pygame.MOUSEBUTTONDOWN and skill6.collidepoint(pygame.mouse.get_pos()):
                    if e.button == 1:
                        skillused = data["skill6_item:"]
                        if soundon == True:
                            skillsound.play()
                if e.type == pygame.MOUSEBUTTONDOWN and skill7.collidepoint(pygame.mouse.get_pos()):
                    if e.button == 1:
                        skillused = data["skill7_item:"]
                        if soundon == True:
                            skillsound.play()
                if e.type == pygame.MOUSEBUTTONDOWN and skill8.collidepoint(pygame.mouse.get_pos()):
                    if e.button == 1:
                        skillused = data["skill8_item:"]
                        if soundon == True:
                            skillsound.play()
                if e.type == pygame.MOUSEBUTTONDOWN and skill9.collidepoint(pygame.mouse.get_pos()):
                    if e.button == 1:
                        skillused = data["skill9_item:"]
                        if soundon == True:
                            skillsound.play()
                if e.type == pygame.MOUSEBUTTONDOWN and skill10.collidepoint(pygame.mouse.get_pos()):
                    if e.button == 1:
                        skillused = data["skill10_item:"]
                        if soundon == True:
                            skillsound.play()

        update()
    
    pygame.quit()

if __name__ == "__main__":
    main()

