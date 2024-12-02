from enum import Enum


class Colors(Enum):
    GREEN:tuple[int, int, int] = (0, 255, 0)
    RED:tuple[int, int, int] = (255, 0, 0)
    BLUE:tuple[int, int, int] = (0, 0, 255)
    YELLOW:tuple[int, int, int] = (255, 255, 0)
    CYAN:tuple[int, int, int] = (0, 100, 100)
    WHITE:tuple[int, int, int] = (255, 255, 255)
    BLACK: tuple[int, int, int] = (0, 0, 0)

    @classmethod
    def get_colours(cls):
        return list(cls)


    @classmethod
    def next(cls, current_colour, number_of_used_colors):
        members = cls.get_colours()
        index = (members.index(current_colour) + 1) % number_of_used_colors
        return members[index]