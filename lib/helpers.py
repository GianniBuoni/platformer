from settings import *

def load_img(*path, format = "png", alpha = True):
    full_path = join(*path) + f".{format}"
    return pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()

def load_dir(*path):
    frames = []

    for root, _, files in walk(join(*path)):
        for file in sorted(files, key = lambda x: int(x.split(".")[0])):
            full_path = join(root, file)
            frames.append(pygame.image.load(full_path))

    return frames
