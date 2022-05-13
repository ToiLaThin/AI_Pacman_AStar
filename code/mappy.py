from matplotlib.pyplot import grid


class Map():
    def __init__(self) -> None:
        self.grid = []
        row = [0, 0, 0, 1, 0, 0, 0, -1, 0, -1]
        self.grid.append(row)
        row = [0, -1, -1, -1, 0, -1, 0, 0, 0, 0]
        self.grid.append(row)
        row = [0, -1, 0, 0, 0, -1, -1, 0, -1, 0]
        self.grid.append(row)
        row = [0, -1, 0, -1, 0, 0, 0, 0, -1, -0]
        self.grid.append(row)
        row = [0, -1, 0, -1, -1, -1, 0, -1, -1, 0]
        self.grid.append(row)
        row = [0, 0, 0, 0, 0, -1, 0, -1, 0, 0]
        self.grid.append(row)
        row = [0, -1, 0, -1, 0, 0, 0, -1, 0, 0]
        self.grid.append(row)
    
    def remaining_diem(self) -> int:
        remaining_dots = 0
        for row in range(len(self.grid)):
            for col in range(0,len(self.grid[len(self.grid)-1])):
                if self.grid[row][col] == 1:
                    remaining_dots += 1
        return remaining_dots

        

    
    
    