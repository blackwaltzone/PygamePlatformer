from os import walk
import pygame

def import_folder(path):
    surface_list = []

    for _dir_name, _2, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            # make sure only image files are in folder
            img_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(img_surface)

    return surface_list