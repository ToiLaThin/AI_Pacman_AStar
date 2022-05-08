class Map():
    def __init__(self) -> None:
        self.grid = []
        row = [0, 0, 0, 0, 0, 0, 0, -1, 0, -1]
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
        

    
    
    