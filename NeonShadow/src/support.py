# src/support.py
import pygame
from os import walk
from settings import TILESIZE


def import_folder(path):
    surface_list = []
    try:
        for _, __, img_files in walk(path):
            for image in img_files:
                full_path = path + '/' + image
                image_surf = pygame.image.load(full_path).convert_alpha()
                surface_list.append(image_surf)
    except FileNotFoundError:
        # Failsafe: Return colored rects if assets missing
        print(f"Warning: Asset path not found: {path}")
        fallback = pygame.Surface((TILESIZE, TILESIZE))
        fallback.fill('magenta')
        surface_list.append(fallback)
    return surface_list


def import_folder_dict(path):
    surface_dict = {}
    try:
        for _, __, img_files in walk(path):
            for image in img_files:
                full_path = path + '/' + image
                image_surf = pygame.image.load(full_path).convert_alpha()
                surface_dict[image.split('.')[0]] = image_surf
    except FileNotFoundError:
        print(f"Warning: Asset path not found: {path}")
    return surface_dict


def debug_rect_surface(width, height, color='red'):
    surf = pygame.Surface((width, height))
    surf.fill(color)
    return surf
# Asset Loading & Math Helpers
