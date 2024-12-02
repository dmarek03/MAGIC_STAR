import math
import pygame
from random import randint
from typing import Callable
from dataclasses import  dataclass
from colors_enum import Colors
from pygame import Surface,freetype, gfxdraw


@dataclass
class Point:
    x: float
    y: float


@dataclass
class Triangle:
    vertex_1: Point
    vertex_2: Point
    vertex_3: Point
    neighbours:list[Point]|None
    number_of_used_colors: int
    colour: Colors = Colors.GREEN
    is_special:bool = False
    window:Surface = None


    def vertices_to_list(self) -> list[Point]:
        return [self.vertex_1, self.vertex_2, self.vertex_3]


    def vertices_to_list_of_tuples(self) -> list[tuple[float, float]]:
        return [(self.vertex_1.x, self.vertex_1.y),(self.vertex_2.x, self.vertex_2.y),(self.vertex_3.x, self.vertex_3.y)]


    def add_neighbour(self, triangle):
        if triangle not in self.neighbours:
            self.neighbours.append(triangle)


    def update(self):
        self.colour = Colors.next(self.colour, self.number_of_used_colors)
        self.draw_triangle()
        pygame.display.update()


    def draw_triangle(self):

        gfxdraw.filled_polygon(self.window,  self.vertices_to_list_of_tuples(), self.colour.value)
        gfxdraw.aapolygon(self.window,  self.vertices_to_list_of_tuples(), Colors.WHITE.value)


    def count_common_vertices(self, other) -> int:
        common_vertex_cnt = 0
        vertices_1 = self.vertices_to_list()
        vertices_2 = other.vertices_to_list()

        for v1 in vertices_1:
            for v2 in vertices_2:
                if v1 == v2:
                    common_vertex_cnt += 1

        return common_vertex_cnt


    def has_common_side(self, other) -> bool:
        return self.count_common_vertices(other) == 2


    def has_special_common_side(self, other) -> bool:
        return self.count_common_vertices(other) == 1


    def contains_point(self, point:Point) -> bool:
        return all(True if 0 <=  factor <= 1 else False  for factor in self.calculate_factors(point))


    def calculate_factors(self, point:Point):
        factor_1 = (
                           (self.vertex_2.y - self.vertex_3.y) * (point.x - self.vertex_3.x) +
                           (self.vertex_3.x - self.vertex_2.x) * (point.y - self.vertex_3.y)
                   ) / self.calculate_det(self.vertex_1, self.vertex_2, self.vertex_3)
        factor_2 = ((
                           (self.vertex_3.y - self.vertex_1.y) * (point.x - self.vertex_3.x) +
                           (self.vertex_1.x - self.vertex_3.x) * (point.y - self.vertex_3.y))
                    / self.calculate_det(self.vertex_1, self.vertex_2, self.vertex_3))

        factor_3 = 1 - factor_1 - factor_2
        return [factor_1, factor_2, factor_3]

    @staticmethod
    def calculate_det(p1:Point, p2:Point, p3:Point) -> float:
        return (p1.x-p3.x)*(p2.y-p3.y) - (p2.x-p3.x)*(p1.y-p3.y)


@dataclass
class Figure:
    num_triangles:int
    triangles:list[Triangle]
    num_of_used_colors:int
    mid_point: Point
    window: Surface
    radius:float = 200
    moves_cnt: int = 0



    def add_triangle(self, triangle:Triangle) -> None:
        self.triangles.append(triangle)

    def calculate_regular_polygon_vertices(self):
        if self.num_triangles < 3:
            raise ValueError("Polygon must have at least 3 sides")
        vertices = []
        self.radius = self.window.get_height()//4

        angle = 360 / self.num_triangles
        for i in range(self.num_triangles):
            x = round(self.mid_point.x + self.radius * math.cos(math.radians(angle * i)), 4)
            y = round(self.mid_point.y + self.radius * math.sin(math.radians(angle * i)), 4)
            vertices.append(Point(x, y))


        return vertices


    def calculate_special_vertices(self,  vertices:list[Point]):
        if self.num_triangles < 3:
            raise ValueError("Polygon must have at least 3 sides")
        extra_vertices = []
        for i in range(self.num_triangles):
            next_vertex = (i + 1) % self.num_triangles
            tmp_x = (vertices[i].x + vertices[next_vertex].x) / 2
            tmp_y = (vertices[i].y + vertices[next_vertex].y) / 2
            x_s = 2 * tmp_x - self.mid_point.x
            y_s = 2 * tmp_y - self.mid_point.y
            extra_vertices.append(Point(x_s, y_s))


        return extra_vertices


    def draw_figure(self):
        polygon_vertices = self.calculate_regular_polygon_vertices()
        extra_vertices = self.calculate_special_vertices(polygon_vertices)

        for i in range(self.num_triangles):
            next_index = (i + 1) % self.num_triangles
            t1 = Triangle(
                polygon_vertices[i],
                self.mid_point,
                polygon_vertices[next_index],
                [],
                window=self.window,
                number_of_used_colors=self.num_of_used_colors
            )
            t2 = Triangle(
                polygon_vertices[i],
                extra_vertices[i],
                polygon_vertices[next_index],
                [],
                is_special=True,
                window=self.window,
                number_of_used_colors=self.num_of_used_colors
            )
            self.add_triangle(t1)
            self.add_triangle(t2)
            t1.draw_triangle()
            t2.draw_triangle()

        self.create_neighbourhoods()


    def create_neighbourhoods(self) -> None:
        for t1 in self.triangles:
            for t2 in self.triangles:
                if t1.has_common_side(t2):
                    t1.add_neighbour(t2)
                    t2.add_neighbour(t1)

                if t1.is_special and t2.is_special and t2.has_special_common_side(t1):
                    t1.add_neighbour(t2)
                    t2.add_neighbour(t1)


    def find_triangle_by_position(self, point:Point) -> Triangle|None:
        for t in self.triangles:
            if t.contains_point(point):
                return t
        return None


    def move(self, position:Point) -> None:
        triangle_to_move = self.find_triangle_by_position(position)
        if triangle_to_move:
            self.moves_cnt += 1
            triangle_to_move.update()
            for neighbour in triangle_to_move.neighbours:
                neighbour.update()


    def shuffle(self, moves_num:int) -> None:
        for _ in range(moves_num):
            triangle_to_move = self.triangles[randint(0, len(self.triangles)-1)]
            triangle_to_move.update()
            for neighbour in triangle_to_move.neighbours:
                neighbour.update()


    def count_green_triangles(self):
        return len([t for t in self.triangles if t.colour == Colors.GREEN])


    def _show_statistic(self, statistic_name:str, cnt:int|Callable, stats_pos:tuple[int, int, int, int]) -> None:
        stats_cnt_font = pygame.freetype.SysFont('Cambria Math', int(36*self.window.get_height()/800))
        stats_label_font =pygame.freetype.SysFont('Cambria Math', int(24*self.window.get_height()/800))

        stats_cnt_text_surf, stats_cnt_text_rect = stats_cnt_font.render(f"{cnt}", Colors.WHITE.value)
        stats_label_text_surf, stats_label_text_rect = stats_label_font.render(f"{statistic_name}:", Colors.WHITE.value)

        stats_cnt_rect = pygame.Rect(stats_pos)
        pygame.draw.rect(self.window, (0, 0, 0),stats_cnt_rect)

        stats_cnt_text_rect.center = stats_cnt_rect.center
        self.window.blit(stats_cnt_text_surf, stats_cnt_text_rect)

        stats_label_text_rect.midbottom = (stats_cnt_text_rect.centerx, stats_cnt_rect.top - 5)
        self.window.blit(stats_label_text_surf, stats_label_text_rect)


    def show_number_of_moves(self) -> None:
        self._show_statistic(
            "Number of moves",
            self.moves_cnt,
            (
                int(self.window.get_width()*0.78),
                int(self.window.get_width()*0.0375),
                int(self.window.get_width()*0.15),
                int(self.window.get_width()*0.0375)
            )
        )


    def show_number_of_green_triangles(self) -> None:
        self._show_statistic(
            "Number of green triangles",
            self.count_green_triangles(),
            (
                int(self.window.get_width()*0.1),
                int(self.window.get_width()*0.0425),
                int(self.window.get_width()*0.15),
                int(self.window.get_width()*0.0375)
            )
        )
