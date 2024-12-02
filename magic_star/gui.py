import re
import sys
import time
import pygame
import pygame_menu as pm
from Buttons import Button
from pygame_menu import Menu
from pygame.font import Font
from pygame.time import Clock
from pygame import Surface, image, mixer
from dataclasses import dataclass, field
from geometry import Point, Figure, Colors


@dataclass
class GUI:
    background_image:image
    font_path:str
    player_settings:dict=field(default_factory=dict)
    settings_menu:Menu = None
    screen_resolution:list[int] = (1280, 800)
    buttons_scale:list[float] = (1.0, 1.0)
    screen: Surface = pygame.display.set_mode(screen_resolution)
    music_on:bool = True
    main_theme_music_path:str =  'music/Red_Alert_3_Soviet_March_Instrumental.mp3'
    number_of_triangles:int = 6
    colors_number:int = 2
    difficulty:int = 10




    def get_font(self, size: int) -> Font:
        return Font(self.font_path, size)



    @staticmethod
    def get_resolutions(resolution: str) -> list[int]:
        return [int(r) for r in re.findall(r'\d{3,}', resolution)]

    def save_settings(self):
        settings_data = self.settings_menu.get_input_data()

        for key, data in settings_data.items():

            self.player_settings[key] = data[0][1] if isinstance(data, tuple) else data


    def load_settings(self):
        if self.player_settings:
            self.screen_resolution = self.get_resolutions(self.player_settings['window resolution'])
            self.screen = pygame.display.set_mode(self.screen_resolution)
            self.buttons_scale = [self.screen_resolution[0]/1280, self.screen_resolution[1]/800]
            self.music_on = self.player_settings['music']
            self.main_theme_music_path = self.player_settings['main music theme']
            self.number_of_triangles = int(self.player_settings['triangles number'])
            self.colors_number = self.player_settings['colors number']
            self.difficulty = self.player_settings['difficulty levels']



    def game_menu(self):

        pygame.display.set_mode(self.screen_resolution)
        pygame.display.set_caption("Basic triangle game")
        self.background_image = pygame.transform.scale(self.background_image, self.screen_resolution)

        MENU_TEXT = self.get_font(int(100*self.buttons_scale[0])).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(self.screen_resolution[0] // 2, int(0.125*self.screen_resolution[1])))

        PLAY_BUTTON = Button(
            image=pygame.image.load("images/Play Rect.png"),
            scale = self.buttons_scale,
            pos=(self.screen_resolution[0]//2, int(5*self.screen_resolution[1]/16)),
            text_input="Play",
            font=self.get_font(int(75*self.buttons_scale[0])),
            base_color="#d7fcd4",
            hovering_color = Colors.WHITE.value
        )

        OPTIONS_BUTTON = Button(
            image=pygame.image.load("images/Options Rect.png"),
            scale=self.buttons_scale,
            pos=(self.screen_resolution[0]//2, int(8*self.screen_resolution[1]/16)),
            text_input="Options",
            font=self.get_font(int(75*self.buttons_scale[0])),
            base_color="#d7fcd4",
            hovering_color=  Colors.WHITE.value
        )
        instruction_image = pygame.image.load("images/Options Rect.png")
        instruction_image = pygame.transform.scale_by(instruction_image, (1.5, 1.0))
        INSTRUCTION_BUTTON = Button(
            image=instruction_image,
            scale=self.buttons_scale,
            pos=(self.screen_resolution[0] // 2, int(11 * self.screen_resolution[1] / 16)),
            text_input="Instruction",
            font=self.get_font(int(75 * self.buttons_scale[0])),
            base_color="#d7fcd4",
            hovering_color=Colors.WHITE.value
        )


        QUIT_BUTTON = Button(
            image=pygame.image.load("images/Quit Rect.png"),
            scale=self.buttons_scale,
            pos=(self.screen_resolution[0]//2, int(14*self.screen_resolution[1]/16)),
            text_input="Quit",
            font=self.get_font(int(75*self.buttons_scale[0])),
            base_color="#d7fcd4",
            hovering_color= Colors.WHITE.value
        )

        while True:
            self.screen.blit(self.background_image, (0, 0))

            mouse_position = pygame.mouse.get_pos()

            self.screen.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, OPTIONS_BUTTON,INSTRUCTION_BUTTON,  QUIT_BUTTON]:
                button.change_color(mouse_position)
                button.update(self.screen)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.check_for_input(mouse_position):
                        self.play()
                    if OPTIONS_BUTTON.check_for_input(mouse_position):
                        self.options()

                    if INSTRUCTION_BUTTON.check_for_input(mouse_position):
                        self.instruction()
                    if QUIT_BUTTON.check_for_input(mouse_position):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

    def play(self):

        self.load_settings()
        self.screen.fill((0,0, 0))
        main_clock = Clock()
        if self.music_on:
            mixer.init()
            mixer.music.load(self.main_theme_music_path)
            mixer.music.set_volume(0.4)
            mixer.music.play(-1)


        moves_before_start = self.difficulty

        center = Point(self.screen_resolution[0] // 2, self.screen_resolution[1] // 2)
        figure = Figure(self.number_of_triangles,  [],self.colors_number, center, window=self.screen)
        figure.draw_figure()
        figure.shuffle(moves_before_start)

        BACK_TO_MENU = Button(
            image=None,
            scale=self.buttons_scale,
            pos=(int(0.82*self.screen_resolution[0]), int(0.93*self.screen_resolution[1])),
            text_input="Back to menu",
            font=self.get_font(int(30*self.buttons_scale[0])),
            base_color= Colors.WHITE.value,
            hovering_color= Colors.GREEN.value
        )

        paused = False
        while True:
            mouse_position = pygame.mouse.get_pos()
            BACK_TO_MENU.change_color(mouse_position)
            BACK_TO_MENU.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if BACK_TO_MENU.check_for_input(mouse_position):
                        mixer.music.pause()
                        self.game_menu()
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_SPACE:
                        paused = not paused

                        if paused:
                            mixer.music.pause()

                        else:
                            mixer.music.unpause()

            figure.show_number_of_moves()
            figure.show_number_of_green_triangles()
            if not paused:

                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    time.sleep(0.2)
                    figure.move(Point(pos[0], pos[1]))

            pygame.display.flip()
            main_clock.tick(60)

    def options(self):

        resolutions = [('640×480 ', '640×480 '), ('800×600', '800×600'), ('1280×800', '1280×800'),
                       ('1440×900', '1440×900'),
                       ('1920×1080', '1920×1080'), ('3072×1728', '3072×1728')]

        music_theme = [
            ('Soviet March','music/Red_Alert_3_Soviet_March_Instrumental.mp3') ,
            ('Duel of the fates','music/Star_Wars_Duel_of_The_Fates.mp3')
        ]

        difficulty_levels = [('Easy', 5), ('Medium', 15), ('Hard', 40)]

        colors_number = [('2', 2), ('3', 3), ('4', 4), ('5', 5)]

        self.settings_menu = pm.Menu(title="Settings",
                           width=self.screen_resolution[0],
                           height=self.screen_resolution[1],
                           theme=pm.themes.THEME_BLUE,
                           )


        self.settings_menu._theme.widget_font_size = 25
        self.settings_menu._theme.widget_font_color =  Colors.BLACK.value
        self.settings_menu._theme.widget_alignment = pm.locals.ALIGN_LEFT


        self.settings_menu.add.toggle_switch(
            title="Music", default=True, toggleswitch_id="music")

        self.settings_menu.add.dropselect(title='Main music theme', items=music_theme,
                                          dropselect_id='main music theme',
                                          default=0, open_middle=True, max_selected=1, selection_box_height=6)

        self.settings_menu.add.dropselect(title='Window resolution', items=resolutions, dropselect_id='window resolution',
                                default=2, open_middle=True, max_selected=1, selection_box_height=6)

        self.settings_menu.add.selector(title='Difficulty', items=difficulty_levels, selector_id='difficulty levels', default=1)

        self.settings_menu.add.selector(title='Number of colors', items=colors_number, selector_id='colors number', default=0,
                              style="fancy")

        self.settings_menu.add.range_slider(title='Number of triangles', default=6, rangeslider_id='triangles number',
                                  range_values=(3, 30), increment=1, value_format=lambda x: str(int(x)))

        self.settings_menu.add.clock(clock_format="%d-%m-%y %H:%M:%S",
                           title_format="Local Time : {0}")

        self.settings_menu.add.button(title="Restore Defaults", action=self.settings_menu.reset_value,
                            font_color=(255, 255, 255), background_color=  Colors.RED.value)

        self.settings_menu.add.button(title="Return To Main Menu",
                            action=self.game_menu, align=pm.locals.ALIGN_CENTER)

        self.settings_menu.add.button(title='Save', action=self.save_settings, background_color= Colors.GREEN.value)

        self.settings_menu.mainloop(self.screen)


    def instruction(self):


        INSTRUCTION_TEXT = self.get_font(int(60 * self.buttons_scale[0])).render("INSTRUCTION", True, "#b68f40")
        INSTRUCTION_RECT =  INSTRUCTION_TEXT.get_rect(center=(self.screen_resolution[0] // 2, int(0.125*self.screen_resolution[1])))

        BACK_TO_MENU = Button(
            image=None,
            scale=self.buttons_scale,
            pos=(self.screen_resolution[0] // 2, int(14 * self.screen_resolution[1] / 16)),
            text_input="Back to menu",
            font=self.get_font(int(50 * self.buttons_scale[0])),
            base_color="#d7fcd4",
            hovering_color=Colors.GREEN.value
        )

        instruction_text = (
            "The game goal is to achieve situations \n when each triangle on the board is green.\n"
            "The color of triangle will change when you click on it.\n"
            "\n"
            "The rules of triangles color updating:\n\n"
            "1. Should you click on triangles that lie inside the polygon,\n"
            "   all of its neighbors,that means each triangle that\n"
            "   have exactly two one sides with the clicked one,\n"
            "   and itself will be updated.\n"
            "\n"
            "2. When the 'outside' triangles are clicked not only its\n"
            "   standard neighborhood and itself will be updated,\n"
            "   but also all triangles having exactly one common \n"
            "   vertex with the one you have clicked.\n"
        )

        instruction_lines = instruction_text.split('\n')
        font_size = int(20 * self.buttons_scale[0])
        font = self.get_font(font_size)
        line_spacing = font_size + 5
        start_y = self.screen_resolution[1]//4



        while True:

            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(INSTRUCTION_TEXT, INSTRUCTION_RECT)
            mouse_position = pygame.mouse.get_pos()
            BACK_TO_MENU.change_color(mouse_position)
            BACK_TO_MENU.update(self.screen)

            for i, line in enumerate(instruction_lines):
                rendered_line = font.render(line, True, "#FFFFFF")
                line_rect = rendered_line.get_rect(center=(self.screen_resolution[0] //2, start_y + i * line_spacing))
                self.screen.blit(rendered_line, line_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if BACK_TO_MENU.check_for_input(mouse_position):
                        self.game_menu()

            pygame.display.update()

