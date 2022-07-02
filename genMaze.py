import random
import sys

class Maze:
    """
    dir -> 0 右, 1 上, 2 左, 3 下
    field cell 0 -> 壁, 1 -> 道
    """
    def __init__(self, mazeWidth, mazeHeight):
        self.mazeWidth = mazeWidth
        self.mazeHeight = mazeHeight
        self.field = [[0 for _ in range(self.mazeWidth)] for _ in range(self.mazeHeight)]


    def getStrField(self):
        """
        fieldを文字列として出力
        """
        lines = []
        for line in self.field:
            lines.append("".join(list(map(str, line))))

        return "\n".join(lines)


    def isForwardable(self, x, y, dir):
        """
        座標(x,y)においてdir方向に2マス進めるか確認する
        """
        if dir == 0:
            return self.getCell(x+2, y) == 0
        elif dir == 1:
            return self.getCell(x, y-2) == 0
        elif dir == 2:
            return self.getCell(x-2, y) == 0
        elif dir == 3:
            return self.getCell(x, y+2) == 0


    def getCell(self, x, y):
        """
        座標(x,y)がfieldの範囲内であればマスの情報を取得
        範囲外であれば-1を返す
        """
        if 1 <= x and x < self.mazeWidth and 1 <= y and y < self.mazeHeight:
            return self.field[y][x]
        else:
            return -1


    def dig(self, x, y, dir):
        """
        指定したセルからdir方向側に2マス通路を掘る
        """
        if dir == 0:
            self.field[y][x+1] = 1
            self.field[y][x+2] = 1
        elif dir == 1:
            self.field[y-1][x] = 1
            self.field[y-2][x] = 1
        elif dir == 2:
            self.field[y][x-1] = 1
            self.field[y][x-2] = 1
        elif dir == 3:
            self.field[y+1][x] = 1
            self.field[y+2][x] = 1
        


    def genMaze(self, startX, startY):
        """
        迷路生成
        """
        tempX = startX
        tempY = startY

        # スタート地点を掘る
        self.field[tempY][tempX] = 1

        # 分岐管理スタック
        pos_stack = []

        while True:
            isAllDirStacked = True
            for i in range(4):
                isAllDirStacked &= not self.isForwardable(tempX, tempY, i)
            
            if isAllDirStacked and len(pos_stack) == 0:
                # 経路生成終了
                break
            
            if isAllDirStacked and len(pos_stack) != 0:
                tempX, tempY = pos_stack.pop()
            
            randomDir = random.randint(0, 3)
            if self.isForwardable(tempX, tempY, randomDir):
                pos_stack.append((tempX, tempY))
                self.dig(tempX, tempY, randomDir)
                if randomDir == 0:
                    tempX += 2
                elif randomDir == 1:
                    tempY -= 2
                elif randomDir == 2:
                    tempX -= 2
                elif randomDir == 3:
                    tempY += 2
                continue
            else:
                continue


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('python3 main.py <width> <height>')
        sys.exit(1)

    mazeWidthStr = sys.argv[1]
    mazeHeightStr = sys.argv[2]

    if (not mazeWidthStr.isnumeric()) or (not mazeHeightStr.isnumeric()):
        print('迷路のサイズは縦横ともに整数で指定してください。')
        sys.exit(1)

    mazeWidth = int(mazeWidthStr)
    mazeHeight = int(mazeHeightStr)

    if mazeWidth % 2 == 0 or mazeHeight % 2 == 0:
        print('迷路のサイズは縦横ともに奇数に設定してください。')
        sys.exit(1)

    maze = Maze(mazeWidth, mazeHeight)
    maze.genMaze(1, 1)

    print(mazeWidth, mazeHeight)
    print(maze.getStrField())
