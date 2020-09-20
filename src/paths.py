import os

PROJECT_DIRECTORY = os.path.abspath("./")

REQUIREMENTS = os.path.join(PROJECT_DIRECTORY, "requirements.txt")

# Assets
ASSETS_DIRECTORY = os.path.join(PROJECT_DIRECTORY, "assets")
IMGS_DIRECTORY = os.path.join(ASSETS_DIRECTORY, "imgs")

ACTORS_DIRECTORY = os.path.join(IMGS_DIRECTORY, "actors")

ACTOR_OLD_MAN_DIRECTORY = os.path.join(ACTORS_DIRECTORY, "1 Old_man")
OLD_MAN_SPRITE_SHEETS = {
    "ATTACK": os.path.join(ACTOR_OLD_MAN_DIRECTORY, "Old_man_attack.png"),
    "DEATH": os.path.join(ACTOR_OLD_MAN_DIRECTORY, "Old_man_death.png"),
    "HURT": os.path.join(ACTOR_OLD_MAN_DIRECTORY, "Old_man_hurt.png"),
    "IDLE": os.path.join(ACTOR_OLD_MAN_DIRECTORY, "Old_man_idle.png"),
    "WALK": os.path.join(ACTOR_OLD_MAN_DIRECTORY, "Old_man_walk.png"),
}

ACTOR_OLD_WOMAN_DIRECTORY = os.path.join(ACTORS_DIRECTORY, "2 Old_woman")
OLD_WOMAN_SPRITE_SHEETS = {
    "ATTACK": os.path.join(ACTOR_OLD_WOMAN_DIRECTORY, "Old_woman_attack.png"),
    "DEATH": os.path.join(ACTOR_OLD_WOMAN_DIRECTORY, "Old_woman_death.png"),
    "HURT": os.path.join(ACTOR_OLD_WOMAN_DIRECTORY, "Old_woman_hurt.png"),
    "IDLE": os.path.join(ACTOR_OLD_WOMAN_DIRECTORY, "Old_woman_idle.png"),
    "WALK": os.path.join(ACTOR_OLD_WOMAN_DIRECTORY, "Old_woman_walk.png"),
}

ACTOR_MAN_DIRECTORY = os.path.join(ACTORS_DIRECTORY, "3 Man")
MAN_SPRITE_SHEETS = {
    "ATTACK": os.path.join(ACTOR_MAN_DIRECTORY, "Man_attack.png"),
    "DEATH": os.path.join(ACTOR_MAN_DIRECTORY, "Man_death.png"),
    "HURT": os.path.join(ACTOR_MAN_DIRECTORY, "Man_hurt.png"),
    "IDLE": os.path.join(ACTOR_MAN_DIRECTORY, "Man_idle.png"),
    "WALK": os.path.join(ACTOR_MAN_DIRECTORY, "Man_walk.png"),
}

ACTOR_WOMAN_DIRECTORY = os.path.join(ACTORS_DIRECTORY, "4 Woman")
WOMAN_SPRITE_SHEETS = {
    "ATTACK": os.path.join(ACTOR_WOMAN_DIRECTORY, "Woman_attack.png"),
    "DEATH": os.path.join(ACTOR_WOMAN_DIRECTORY, "Woman_death.png"),
    "HURT": os.path.join(ACTOR_WOMAN_DIRECTORY, "Woman_hurt.png"),
    "IDLE": os.path.join(ACTOR_WOMAN_DIRECTORY, "Woman_idle.png"),
    "WALK": os.path.join(ACTOR_WOMAN_DIRECTORY, "Woman_walk.png"),
}

ACTOR_BOY_DIRECTORY = os.path.join(ACTORS_DIRECTORY, "5 Boy")
BOY_SPRITE_SHEETS = {
    "ATTACK": os.path.join(ACTOR_BOY_DIRECTORY, "Boy_attack.png"),
    "DEATH": os.path.join(ACTOR_BOY_DIRECTORY, "Boy_death.png"),
    "HURT": os.path.join(ACTOR_BOY_DIRECTORY, "Boy_hurt.png"),
    "IDLE": os.path.join(ACTOR_BOY_DIRECTORY, "Boy_idle.png"),
    "WALK": os.path.join(ACTOR_BOY_DIRECTORY, "Boy_walk.png"),
}

ACTOR_GIRL_DIRECTORY = os.path.join(ACTORS_DIRECTORY, "6 Girl")
GIRL_SPRITE_SHEETS = {
    "ATTACK": os.path.join(ACTOR_GIRL_DIRECTORY, "Girl_attack.png"),
    "DEATH": os.path.join(ACTOR_GIRL_DIRECTORY, "Girl_death.png"),
    "HURT": os.path.join(ACTOR_GIRL_DIRECTORY, "Girl_hurt.png"),
    "IDLE": os.path.join(ACTOR_GIRL_DIRECTORY, "Girl_idle.png"),
    "WALK": os.path.join(ACTOR_GIRL_DIRECTORY, "Girl_walk.png"),
}
