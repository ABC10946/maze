import sys


class Solver:
    # maze 0 -> wall, 1 -> road, 2 -> marked road
    def __init__(self):
        self.maze = []
        self.prevDirMap = []  # 該当セルに前のセルデータを登録するマップ

    def setMaze(self, maze):
        self.maze = maze
        self.height = len(maze)
        self.width = len(maze[0])
        self.prevDirMap = [
            [-1 for _ in range(self.width)] for _ in range(self.height)]

    def getCell(self, x, y):
        if 1 <= x and x < self.width and 1 <= y and y < self.height:
            return self.maze[y][x]
        else:
            return -1

    def isForwardable(self, x, y, dir):
        # right 0
        # up 1
        # left 2
        # down 3
        if dir == 0:
            return self.getCell(x+1, y) == 1 and self.getCell(x+2, y) == 1
        elif dir == 1:
            return self.getCell(x, y-1) == 1 and self.getCell(x, y-2) == 1
        elif dir == 2:
            return self.getCell(x-1, y) == 1 and self.getCell(x-2, y) == 1
        elif dir == 3:
            return self.getCell(x, y+1) == 1 and self.getCell(x, y+2) == 1

    def mark(self, x, y, dir):
        if dir == 0:
            self.maze[y][x+1] = 2
            self.maze[y][x+2] = 2
            self.prevDirMap[y][x+1] = dir
            self.prevDirMap[y][x+2] = dir
        elif dir == 1:
            self.maze[y-1][x] = 2
            self.maze[y-2][x] = 2
            self.prevDirMap[y-1][x] = dir
            self.prevDirMap[y-2][x] = dir
        elif dir == 2:
            self.maze[y][x-1] = 2
            self.maze[y][x-2] = 2
            self.prevDirMap[y][x-1] = dir
            self.prevDirMap[y][x-2] = dir
        elif dir == 3:
            self.maze[y+1][x] = 2
            self.maze[y+2][x] = 2
            self.prevDirMap[y+1][x] = dir
            self.prevDirMap[y+2][x] = dir

    def solve(self, startX, startY, goalX, goalY):
        self.startX = startX
        self.startY = startY
        self.goalX = goalX
        self.goalY = goalY

        posStack = []
        tempX = startX
        tempY = startY

        while True:
            if tempX == goalX and tempY == goalY:
                # 終了条件
                break

            isAllDirStacked = True
            for dir in range(4):
                isAllDirStacked &= not self.isForwardable(tempX, tempY, dir)

            if isAllDirStacked and len(posStack) != 0:
                tempX, tempY = posStack.pop()

            for dir in range(4):
                if self.isForwardable(tempX, tempY, dir):
                    posStack.append((tempX, tempY))
                    self.mark(tempX, tempY, dir)
                    if dir == 0:
                        tempX += 2
                    elif dir == 1:
                        tempY -= 2
                    elif dir == 2:
                        tempX -= 2
                    elif dir == 3:
                        tempY += 2

    def getRoute(self):
        tempX = self.goalX
        tempY = self.goalY
        route = []
        prevDir = -1

        while True:
            if tempX == self.startX and tempY == self.startY:
                break

            dirToPrevCell = self.prevDirMap[tempY][tempX]
            if prevDir != dirToPrevCell:
                route.append((tempX, tempY))

            if dirToPrevCell == 0:
                tempX -= 2
            elif dirToPrevCell == 1:
                tempY += 2
            elif dirToPrevCell == 2:
                tempX += 2
            elif dirToPrevCell == 3:
                tempY -= 2

            prevDir = dirToPrevCell

        return list(reversed(route))


if __name__ == "__main__":
    w, h = map(int, input().split())
    maze = []
    for _ in range(h):
        line = input()
        maze.append(list(map(int, line)))

    if len(sys.argv) != 3:
        print('python3 solver.py <goalX> <goalY>')
        sys.exit(1)

    goalXStr = sys.argv[1]
    goalYStr = sys.argv[2]

    if (not goalXStr.isnumeric()) and (not goalYStr.isnumeric()):
        print('ゴール座標は整数で指定してください。')
        sys.exit(1)

    goalX = int(goalXStr)
    goalY = int(goalYStr)

    if not (0 < goalX and goalX <= w - 2 and 0 < goalY and goalY <= h - 2):
        print('ゴール座標は迷路の範囲内で指定してください。')
        sys.exit(1)

    if goalX % 2 == 0 or goalY % 2 == 0:
        print('ゴール座標は奇数で指定してください。')
        sys.exit(1)

    solver = Solver()
    solver.setMaze(maze)

    solver.solve(1, 1, goalX, goalY)

    print(solver.getRoute())
