import pygame

class Button:
    def __init__(self, image,scale, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.scale = scale
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)

        if self.image:

            self.image = pygame.transform.scale_by(self.image, self.scale)

        else:
            self.image = self.text

        self.rect = self.image.get_rect(center = (self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center = (self.x_pos, self.y_pos))



    def update(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)

        screen.blit(self.text, self.text_rect)



    def check_for_input(self, position):
        return self.rect.left <= position[0] <= self.rect.right and self.rect.top <= position[1] <= self.rect.bottom


    def change_color(self,position):
        if self.check_for_input(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)

        else:
            self.text = self.font.render(self.text_input, True, self.base_color)