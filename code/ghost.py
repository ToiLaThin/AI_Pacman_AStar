class Ghost():
    def __init__(self) -> None:
        self.cord_x = 0
        self.cord_y = 0

    def move(self, action:str):
        '''Con ma di chuyển = thuật toán nên input sẽ khác'''

        # THỬ thay đổi tọa độ
        if action == "UP":
            self.cord_y -= 1
        elif action == "DOWN":
            self.cord_y += 1
        elif action == "LEFT":
            self.cord_x -= 1
        elif action == "RIGHT":
            self.cord_x += 1


