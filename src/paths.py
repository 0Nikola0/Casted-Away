import os

PROJECT_DIRECTORY = os.path.abspath("./")

REQUIREMENTS = os.path.join(PROJECT_DIRECTORY, "requirements.txt")

# Assets
ASSETS_DIRECTORY = os.path.join(PROJECT_DIRECTORY, "assets")

MAP_DIRECTORY = os.path.join(ASSETS_DIRECTORY, "map")
MAP = os.path.join(MAP_DIRECTORY, "samplemap.tmx")

IMGS_DIRECTORY = os.path.join(ASSETS_DIRECTORY, "imgs")

ACTORS_DIRECTORY = os.path.join(IMGS_DIRECTORY, "actors")

IMG_ACTOR_OLD_MAN_DIRECTORY = os.path.join(ACTORS_DIRECTORY, "1 Old_man")
OLD_MAN_SPRITE_SHEETS = {
    "ATTACK": os.path.join(IMG_ACTOR_OLD_MAN_DIRECTORY, "Old_man_attack.png"),
    "DEATH": os.path.join(IMG_ACTOR_OLD_MAN_DIRECTORY, "Old_man_death.png"),
    "HURT": os.path.join(IMG_ACTOR_OLD_MAN_DIRECTORY, "Old_man_hurt.png"),
    "IDLE": os.path.join(IMG_ACTOR_OLD_MAN_DIRECTORY, "Old_man_idle.png"),
    "WALK": os.path.join(IMG_ACTOR_OLD_MAN_DIRECTORY, "Old_man_walk.png"),
    "WALK-L": os.path.join(IMG_ACTOR_OLD_MAN_DIRECTORY, "Old_man_walk_l.png"),

}

IMG_ACTOR_OLD_WOMAN_DIRECTORY = os.path.join(ACTORS_DIRECTORY, "2 Old_woman")
OLD_WOMAN_SPRITE_SHEETS = {
    "ATTACK": os.path.join(IMG_ACTOR_OLD_WOMAN_DIRECTORY, "Old_woman_attack.png"),
    "DEATH": os.path.join(IMG_ACTOR_OLD_WOMAN_DIRECTORY, "Old_woman_death.png"),
    "HURT": os.path.join(IMG_ACTOR_OLD_WOMAN_DIRECTORY, "Old_woman_hurt.png"),
    "IDLE": os.path.join(IMG_ACTOR_OLD_WOMAN_DIRECTORY, "Old_woman_idle.png"),
    "WALK": os.path.join(IMG_ACTOR_OLD_WOMAN_DIRECTORY, "Old_woman_walk.png"),
    "WALK-L": os.path.join(IMG_ACTOR_OLD_WOMAN_DIRECTORY, "Old_woman_walk_l.png"),

}

IMG_ACTOR_MAN_DIRECTORY = os.path.join(ACTORS_DIRECTORY, "3 Man")
MAN_SPRITE_SHEETS = {
    "ATTACK": os.path.join(IMG_ACTOR_MAN_DIRECTORY, "Man_attack.png"),
    "DEATH": os.path.join(IMG_ACTOR_MAN_DIRECTORY, "Man_death.png"),
    "HURT": os.path.join(IMG_ACTOR_MAN_DIRECTORY, "Man_hurt.png"),
    "IDLE": os.path.join(IMG_ACTOR_MAN_DIRECTORY, "Man_idle.png"),
    "WALK": os.path.join(IMG_ACTOR_MAN_DIRECTORY, "Man_walk.png"),
    "WALK-L": os.path.join(IMG_ACTOR_MAN_DIRECTORY, "Man_walk_l.png"),

}

IMG_ACTOR_WOMAN_DIRECTORY = os.path.join(ACTORS_DIRECTORY, "4 Woman")
WOMAN_SPRITE_SHEETS = {
    "ATTACK": os.path.join(IMG_ACTOR_WOMAN_DIRECTORY, "Woman_attack.png"),
    "DEATH": os.path.join(IMG_ACTOR_WOMAN_DIRECTORY, "Woman_death.png"),
    "HURT": os.path.join(IMG_ACTOR_WOMAN_DIRECTORY, "Woman_hurt.png"),
    "IDLE": os.path.join(IMG_ACTOR_WOMAN_DIRECTORY, "Woman_idle.png"),
    "WALK": os.path.join(IMG_ACTOR_WOMAN_DIRECTORY, "Woman_walk.png"),
    "WALK-L": os.path.join(IMG_ACTOR_WOMAN_DIRECTORY, "Woman_walk_l.png"),

}

IMG_ACTOR_BOY_DIRECTORY = os.path.join(ACTORS_DIRECTORY, "5 Boy")
BOY_SPRITE_SHEETS = {
    "ATTACK": os.path.join(IMG_ACTOR_BOY_DIRECTORY, "Boy_attack.png"),
    "DEATH": os.path.join(IMG_ACTOR_BOY_DIRECTORY, "Boy_death.png"),
    "HURT": os.path.join(IMG_ACTOR_BOY_DIRECTORY, "Boy_hurt.png"),
    "IDLE": os.path.join(IMG_ACTOR_BOY_DIRECTORY, "Boy_idle.png"),
    "WALK": os.path.join(IMG_ACTOR_BOY_DIRECTORY, "Boy_walk.png"),
    "WALK-L": os.path.join(IMG_ACTOR_BOY_DIRECTORY, "Boy_walk_l.png"),

}

IMG_ACTOR_GIRL_DIRECTORY = os.path.join(ACTORS_DIRECTORY, "6 Girl")
GIRL_SPRITE_SHEETS = {
    "ATTACK": os.path.join(IMG_ACTOR_GIRL_DIRECTORY, "Girl_attack.png"),
    "DEATH": os.path.join(IMG_ACTOR_GIRL_DIRECTORY, "Girl_death.png"),
    "HURT": os.path.join(IMG_ACTOR_GIRL_DIRECTORY, "Girl_hurt.png"),
    "IDLE": os.path.join(IMG_ACTOR_GIRL_DIRECTORY, "Girl_idle.png"),
    "WALK": os.path.join(IMG_ACTOR_GIRL_DIRECTORY, "Girl_walk.png"),
    "WALK-L": os.path.join(IMG_ACTOR_GIRL_DIRECTORY, "Girl_walk_l.png"),
}

# Sounds
SOUNDS_DIRECTORY = os.path.join(ASSETS_DIRECTORY, "sounds")

SOUNDTRACKS_DIRECTORY = os.path.join(SOUNDS_DIRECTORY, "soundtracks")

SOUNDTRACKS = [
    os.path.join(SOUNDTRACKS_DIRECTORY, "soundtrack01.mp3"),
    os.path.join(SOUNDTRACKS_DIRECTORY, "soundtrack02.mp3"),
    os.path.join(SOUNDTRACKS_DIRECTORY, "soundtrack03.mp3"),
]

SOUNDS_ACTORS_DIRECTORY = os.path.join(SOUNDS_DIRECTORY, "actors")

SOUNDS_ACTOR_OLD_MAN_DIRECTORY = os.path.join(SOUNDS_ACTORS_DIRECTORY, "1 Old_man")
OLD_MAN_SOUNDS = {
    "SELECT1": os.path.join(SOUNDS_ACTOR_OLD_MAN_DIRECTORY, "select1.wav"),
    "SELECT2": os.path.join(SOUNDS_ACTOR_OLD_MAN_DIRECTORY, "select2.wav"),
    "HUNGRY": os.path.join(SOUNDS_ACTOR_OLD_MAN_DIRECTORY, "hungry.wav"),
    "EAT": os.path.join(SOUNDS_ACTOR_OLD_MAN_DIRECTORY, "eat.wav"),
}

# GUI
THEME = os.path.join(PROJECT_DIRECTORY, "src", "theme.json")
