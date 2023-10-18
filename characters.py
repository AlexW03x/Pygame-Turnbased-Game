class YourChar():
    def __init__(self, chartype, vitality, strength, magic, speed, level, skillpoints, attributepoints, experience, experience_to_next_level):
        self.chartype = chartype
        self.hp = vitality
        self.power = strength
        self.magic = magic
        self.speed = speed
        self.level = level
        self.sp = skillpoints
        self.ap = attributepoints
        self.exp = experience
        self.expreq = experience_to_next_level

    def retrievestat(self, stat):
        if stat == "chartype":
            return self.chartype
        elif stat == "hp":
            return self.hp
        elif stat == "strength":
            return self.power
        elif stat == "magic":
            return self.magic
        elif stat == "speed":
            return self.speed
        elif stat == "level":
            return self.level
        elif stat == "sp":
            return self.sp
        elif stat == "ap":
            return self.ap
        elif stat == "exp":
            return self.exp
        elif stat == "expreq":
            return self.expreq
        else:
            return
    
    def modifystat(self, stat, modification):
        if stat == "chartype":
            self.chartype = modification
        elif stat == "hp":
            self.hp = modification
        elif stat == "magic":
            self.magic = modification
        elif stat == "speed":
            self.speed = modification
        elif stat == "level":
            self.level = modification
        elif stat == "sp":
            self.sp = modification
        elif stat == "ap":
            self.ap = modification
        elif stat == "exp":
            self.exp = modification
        elif stat == "expreq":
            self.expreq = modification
        else:
            pass

class Enemy():
    def __init__(self, enemyname, enemyicon, enemytexture, hp, strength, magic, speed, abilities):
        self.name = enemyname
        self.icon = enemyicon
        self.texture = enemytexture
        self.hp = hp
        self.strength = strength
        self.magic = magic
        self.speed = speed
        self.abilities = abilities

    def get(self, stat):
        if stat == "name":
            return self.name
        if stat == "icon":
            return self.icon
        if stat == "texture":
            return self.texture
        if stat == "hp":
            return self.hp
        if stat == "strength":
            return self.strength
        if stat == "magic":
            return self.magic
        if stat == "speed":
            return self.speed
        if stat == "abilities":
            return self.abilities
        
    def set(self, stat, modification):
        if stat == "name":
            self.name = modification
        if stat == "icon":
            self.icon = modification
        if stat == "texture":
            self.texture = modification
        if stat == "hp":
            self.hp = modification
        if stat == "strength":
            self.strength = modification
        if stat == "magic":
            self.magic = modification
        if stat == "speed":
            self.speed = modification
        if stat == "abilities":
            self.abilities = modification