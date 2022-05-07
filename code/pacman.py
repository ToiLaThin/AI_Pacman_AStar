from tkinter import LEFT
from mappy import Map


class PacMan():
    def __init__(self) -> None:
        self.score = 0
        self.cord_x = 2
        self.cord_y = 2

    def move(self, direction: str, map: Map):
        '''Thực hiện di chuyển thử thay đổi tọa độ. 
        Nếu tọa độ hợp lệ thì thay đổi bản đồ.
        Nều không thì vẫn đứng yên.'''
        # lưu lại tọa độ cũ
        old_x = self.cord_x
        old_y = self.cord_y

        # THỬ thay đổi tọa độ
        if direction == "UP":
            self.cord_y -= 1
        elif direction == "DOWN":
            self.cord_y += 1
        elif direction == "LEFT":
            self.cord_x -= 1
        elif direction == "RIGHT":
            self.cord_x += 1

        # kiểm tra hợp lệ -> quyết định thay đổi lại tọa độ không
        if not self.cord_is_valid(map):
            self.cord_x = old_x
            self.cord_y = old_y
            return

        # thay đổi bản đồ và tăng điểm nếu tại ô đó có điểm
        if map.grid[self.cord_y][self.cord_x] != 0:
            self.score += map.grid[self.cord_y][self.cord_x]
            map.grid[self.cord_y][self.cord_x] = 0

    def cord_is_valid(self, map: Map) -> bool:
        '''Kiểm tra xem tọa độ của pacman hiện tai hợp lệ hay không'''
        if 0 <= self.cord_x <= 9 and 0 <= self.cord_y <= 6:
            if map.grid[self.cord_y][self.cord_x] != -1:
                return True
        return False
