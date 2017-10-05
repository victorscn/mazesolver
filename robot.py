import math
import random
import sys
class Robot(object):

    def __init__(self, maze_dim):

        sys.setrecursionlimit(1700)
        '''
        Use the initialization function to set up attributes that your robot
        will use to learn and navigate the maze. Some initial attributes are
        provided based on common information, including the size of the maze
        the robot is placed in.
        '''
        self.x = 0
        self.y = 0
        self.heading = 'up'
        self.angle = 0
        self.maze_dim = maze_dim
        self.goal = [(self.maze_dim / 2) - 1, self.maze_dim / 2]
        # TO-DO grid: Estado [up,right,down,left,]. Necessario atualizar checkmap
        self.grid = [[[1, 1, 1, 1,0] for col in range(maze_dim)]
                     for row in range(maze_dim)]
        self.dist = [[0 for col in range(maze_dim)] for row in range(maze_dim)]
        self.initializeDistMaze()
        self.run = 0        
        self.step =1
        self.epsilon = math.exp(-0.01*self.step) 

    def reset(self):
        # Reseta a posicao e angulo interno do robo
        self.x = 0
        self.y = 0
        self.angle = 0
        self.heading='up'
        return

    def hit_goal(self, sensors):
        # Checa se o micromouse esta na chegada
        if self.x == self.goal[0] and self.y == self.goal[1]:
            return True
        return False

    def initializeDistMaze(self):
        # Inicializa a matriz de valores com a funcao heuristica escolhida
        for y in range(self.maze_dim):
            for x in range(self.maze_dim):
                self.dist[y][x] = self.heuristic(x, y)

    def heuristic(self, x, y):
        # Utiliza Manhattan distance para encontrar custo
        return abs(x - self.goal[0]) + abs(y - self.goal[1])

    def updateMap(self, sensors):
        # Atualiza a matriz de mapa.
        #Input: informacao dos sensores
        way = [-90, 0, 90]
        # 1. Reconhecer lado que sensores estao detectando (norte, leste, sul, oeste)
        # 2. Marcar celula correta
        self.grid[self.y][self.x][4] = 1
        for i in range(len(sensors)):
            # Calcular direcao do sensor
            direction = (self.angle + way[i]) % 360
            distance = [sensors[i] * d for d in self.convertAngle(direction)]

            self.grid[self.y + distance[1]][self.x +
                                            distance[0]][self.gridConvert(direction)] = 0

    def compass(self, angle):
        if angle == 0:
            return 'up'
        elif angle == 90:
            return 'right'
        elif angle == 180:
            return 'down'
        elif angle == 270:
            return 'left'

    def convertAngle(self, angle):
        if angle == 0:  # Up
            return [0, 1]
        elif angle == 90:  # Right
            return [1, 0]
        elif angle == 270:  # Left
            return [-1, 0]
        elif angle == 180:  # Down
            return [0, -1]
        else:
            return [0, 0]

    def convertMove(self, move):
        if move == [0, 1]:  # UP
            return 0
        elif move == [1, 0]:  # Right
            return 90
        elif move == [-1, 0]:  # Left
            return 270
        elif move == [0, -1]:  # Down
            return 180
        else:
            return 'Not a move'

    def gridConvert(self, move):
        if move == 0:  # Up
            return 0
        elif move == 90:  # Right
            return 1
        elif move == 180:  # Down
            return 2
        elif move == 270:  # Left
            return 3

    def checkMoves(self, sensors):
        # Checa movimentos. Devolve angulos e distancias possiveis
        moves = []
        possible = []
        way = [-90, 0, 90]

        for i in range(len(way)):
            for d in range(1,4):
                if d <= sensors[i]: #TO-DO corrigir distancia
                    possible. append([(self.angle + way[i]) % 360,d])

        for move in possible:
            if self.grid[self.y][self.x][self.gridConvert(move[0])] == 1:
                if move[1] == 1 :
                    moves.append(move)
                elif move[1] == 2:
                    nxny = self.convertAngle(move[0])
                    if self.grid[self.y + nxny[1]][self.x +
                    nxny[0]][self.gridConvert(move[0])] == 1:
                        moves.append(move)
                elif move[1] == 3:
                    nxny = self.convertAngle(move[0])
                    if self.grid[self.y + nxny[1]*2][self.x +
                    nxny[0] * 2][self.gridConvert(move[0])] == 1:
                        moves.append(move)
        
        return moves

    def checkBest(self, moves):
        # Recebe lista de movimentos possiveis e escolhe o menor valor de distancia
        # na matriz dist
        best = []
        dist_value = self.dist[self.y][self.x]        
        for move in moves:
            nxny = [move[1] * d for d in self.convertAngle(move[0])]
            if self.dist[self.y + nxny[1]][self.x + nxny[0]] < dist_value:
                if self.run < 2 or self.grid[self.y + nxny[1]][self.x + nxny[0]][4] ==1:                
                    dist_value = self.dist[self.y + nxny[1]][self.x + nxny[0]]
                    best = move
        #Checa o movimento contrario, caso as distancias tenham sido atualizadas
        if best == []:
            back = (self.angle+180)%360
            nxny = self.convertAngle(back)
            if self.grid[self.y][self.x][self.gridConvert(back)] == 1:
                if self.dist[self.y + nxny[1]][self.x + nxny[0]] < dist_value:
                    best = [self.angle,-1]   

        # Caso nao encontrar um bom movimento, atualiza valores
        if best == []:
            self.updateDist(self.x, self.y)            
            best = self.checkBest(moves)
        return best

    def exclusive(self, listed):
        checked = []
        for l in listed:
            if l not in checked:
                checked.append(l)
        return checked

    def updateDist(self, x, y):
        
        stack = [[x, y]]
        ways = [[0,1], [1,0], [0,-1], [-1,0]]               
        while stack != []:
            mim = stack.pop()
            minDist = self.dist[mim[1]][mim[0]]
            newDist = []            
            check = 0
            for i in range(len(ways)):
                if self.grid[mim[1]][mim[0]][i] == 1:                    
                    if mim[1] + ways[i][1] in range(self.maze_dim) and mim[0] + ways[i][0] in range(self.maze_dim):
                        
                        value = self.dist[mim[1] + ways[i][1]][mim[0] + ways[i][0]]
                        
                        if value < minDist:
                            check = 1                            
                            break
                        else:                            
                            newDist.append(value+1)
                    else:
                        check = 1
            if check == 0:
                for i in range(len(ways)):
                    if self.grid[mim[1]][mim[0]][i] == 1:                                         
                        stack.append([mim[0] + ways[i][0], mim[1] + ways[i][1]])
                stack = self.exclusive(stack)
                
                self.dist[mim[1]][mim[0]] = min(newDist)

    def steer(self, new_angle):
        # Define quantos graus e a direcao do mouse        
        mod = 1
        # Para casos sem rotacao:
        if self.angle == new_angle:
            return 0

        # Definindo modificacao para rotacao no caso de sul e leste
        if self.angle >= 180:
            mod = -1
        # Casos para mouse indo para o norte ou sul
        if self.angle == 0 or self.angle == 180:
            if new_angle == 90:
                return 90 * mod
            if new_angle == 270:
                return -90 * mod

        # Casos para mouse indo oeste e leste
        if self.angle == 90 or self.angle == 270:
            if new_angle == 180:
                return 90 * mod
            if new_angle == 0:
                return -90 * mod

    def acc(self, rotation):
        new_angle = (self.angle+rotation)%360
        # Define a quantidade de passos que o mouse andara
        if self.grid[self.y][self.x][self.gridConvert(new_angle)] == 1:
            return 1
        else:
            return 0

    def not_visited(self,move):
        check = self.convertAngle((move[0])%360)        
        check = [move[1] * d for d in check]        
        if self.grid[self.y + check[1]][self.x + check[0]][4] ==0:
            return True
        else:
            return False
               
    def next_move(self, sensors):
        go = 1
        '''
        Use this function to determine the next move the robot should make,
        based on the input from the sensors after its previous move. Sensor
        inputs are a list of three distances from the robot's left, front, and
        right-facing sensors, in that order.

        Outputs should be a tuple of two values. The first value indicates
        robot rotation (if any), as a number: 0 for no rotation, +90 for a
        90-degree rotation clockwise, and -90 for a 90-degree rotation
        counterclockwise. Other values will result in no rotation. The second
        value indicates robot movement, and the robot will attempt to move the
        number of indicated squares: a positive number indicates forwards
        movement, while a negative number indicates backwards movement. The
        robot may move a maximum of three units per turn. Any excess movement
        is ignored.

        If the robot wants to end a run (e.g. during the first training run in
        the maze) then returing the tuple ('Reset', 'Reset') will indicate to
        the tester to end the run and return the robot to the start.
        '''
        # First run: construct map using fill flood. When the goal is found, use A* to
        # come back to the start and try to find a better route. When the start
        # is found, end the search run.

        if self.hit_goal(sensors):   
                self.run +=1
                self.reset()
                return ('Reset', 'Reset')            
        

        self.updateMap(sensors)

        

        # Escolha do proximo movimento
        # Inicia checando movimentos possiveis a partir da posicao e
        # procura pelo melhor valor
        possible_moves = self.checkMoves(sensors) 
#        if self.run == 0:
#            self.step+=1.0   
#            self.epsilon = math.exp(-0.01*self.step)
#            if self.epsilon < random.random():
#                best = self.checkBest(possible_moves)
#            else:
#                if possible_moves == []:
#                    possible_moves.append([self.angle,-1])
#                a = False                
#                while not a:
#                    random.shuffle(possible_moves)
#                    move = possible_moves.pop()
#                    a = self.not_visited(move)
#                    if possible_moves == []:
#                        best = move
#                        break
#                    else:
#                        best = move
#                
#        else:
        best = self.checkBest(possible_moves)

               
        # A partir da informacao do melhor movimento possivel,
        # calcula como sera feita a movimentacao
        best[0] = self.steer(best[0])        
#        go = self.acc(rotation) * best[1]
        move = self.convertAngle((self.angle+best[0])%360)        
        move = [best[1] * d for d in move]        
        self.x = self.x + move[0]
        self.y = self.y + move[1]      
        self.angle = (self.angle + best[0]) % 360
        self.heading = self.compass(self.angle)
        return best[0], best[1]

# Debugging Functions
    def showDist(self):
        for i in range(len(self.dist)):
            print self.dist[i]

    def showGridPosition(self, x, y):
        return self.grid[y][x]
