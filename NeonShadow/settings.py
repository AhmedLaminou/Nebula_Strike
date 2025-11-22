# settings.py

# --- General Setup ---
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60
TILESIZE = 64
HITBOX_OFFSET = {
    'player': -26,
    'object': -40,
    'grass': -10,
    'invisible': 0
}

# --- UI Colors & Fonts ---
UI_FONT = 'arial'  # Placeholder, will load system font
UI_FONT_SIZE = 18
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# --- UI Colors ---
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# --- Upgrade Menu ---
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

# --- Inventory System ---
INVENTORY_WIDTH = 8  # Slots horizontally
INVENTORY_HEIGHT = 4 # Slots vertically
SLOT_SIZE = 64
SLOT_PADDING = 10
INVENTORY_BG_COLOR = '#1a1a1a'
SLOT_BG_COLOR = '#333333'
SLOT_BORDER_COLOR = '#555555'
SLOT_SELECTED_COLOR = '#EEEEEE'

# UI Textures (Colors for now)
ITEM_BOX_BG = '#222222'
ITEM_BOX_BORDER = '#111111'

# --- Weapons Data ---
# Add more entries here to increase code volume and game depth
weapon_data = {
    'sword': {
        'cooldown': 100,
        'damage': 15,
        'graphic': '../data/graphics/weapons/sword/full.png',
        'knockback': 20
    },
    'lance': {
        'cooldown': 400,
        'damage': 30,
        'graphic': '../data/graphics/weapons/lance/full.png',
        'knockback': 10
    },
    'axe': {
        'cooldown': 300,
        'damage': 20,
        'graphic': '../data/graphics/weapons/axe/full.png',
        'knockback': 30
    },
    'rapier': {
        'cooldown': 50,
        'damage': 8,
        'graphic': '../data/graphics/weapons/rapier/full.png',
        'knockback': 5
    },
    'sai': {
        'cooldown': 80,
        'damage': 10,
        'graphic': '../data/graphics/weapons/sai/full.png',
        'knockback': 8
    },
    # Placeholder for future legendary weapons
    'god_killer': {
        'cooldown': 0,
        'damage': 999,
        'graphic': '../data/graphics/weapons/god/full.png',
        'knockback': 100
    }
}

# --- Magic Data ---
magic_data = {
    'flame': {
        'strength': 5,
        'cost': 20,
        'graphic': '../data/graphics/particles/flame/fire.png'
    },
    'heal': {
        'strength': 20,
        'cost': 10,
        'graphic': '../data/graphics/particles/heal/heal.png'
    },
    'ice_spike': {
        'strength': 10,
        'cost': 15,
        'graphic': '../data/graphics/particles/ice/ice.png'
    }
}

# --- Enemy Data ---
monster_data = {
    'squid': {
        'health': 100,
        'exp': 100,
        'damage': 20,
        'attack_type': 'slash',
        'attack_sound': '../data/audio/attack/slash.wav',
        'speed': 3,
        'resistance': 3,
        'attack_radius': 80,
        'notice_radius': 360
    },
    'raccoon': {
        'health': 300,
        'exp': 250,
        'damage': 40,
        'attack_type': 'claw',
        'attack_sound': '../data/audio/attack/claw.wav',
        'speed': 2,
        'resistance': 3,
        'attack_radius': 120,
        'notice_radius': 400
    },
    'spirit': {
        'health': 100,
        'exp': 110,
        'damage': 8,
        'attack_type': 'thunder',
        'attack_sound': '../data/audio/attack/fireball.wav',
        'speed': 4,
        'resistance': 3,
        'attack_radius': 60,
        'notice_radius': 350
    },
    'bamboo': {
        'health': 70,
        'exp': 120,
        'damage': 6,
        'attack_type': 'leaf_air',
        'attack_sound': '../data/audio/attack/slash.wav',
        'speed': 3,
        'resistance': 3,
        'attack_radius': 50,
        'notice_radius': 300
    }
}

# --- Map Layers ---
LAYERS = {
    'water': 0,
    'ground': 1,
    'soil': 2,
    'soil_water': 3,
    'rain_floor': 4,
    'house_bottom': 5,
    'ground_plant': 6,
    'main': 7,
    'house_top': 8,
    'fruit': 9,
    'rain_drops': 10
}
# Massive Configuration File
