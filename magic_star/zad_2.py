import pygame
from gui import GUI


def main() -> None:
    pygame.init()
    background_image = pygame.image.load("images/Background.png")
    font_path = 'images/font.ttf'

    gui = GUI(background_image=background_image,font_path=font_path)
    gui.game_menu()




if __name__ == '__main__':
    main()
