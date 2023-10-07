import pygame,numpy,sys,math
pygame.init()

WIDTH = 1300
HEIGHT = 650


screen = pygame.display.set_mode((WIDTH,HEIGHT))

class Board():
    def __init__(self,screen):
        self.x = 25
        self.y = 50
        self.start = None
        self.end = None
        self.screen = screen
        self.board = self.new_board()
        self.sqrsize = HEIGHT / self.x
        self.text = "Click on where to start"
    
    def new_board(self):
        return numpy.zeros((self.x,self.y),dtype=int)

    def draw_board(self):
        SQRSIZE = self.sqrsize
        for i in range(self.x):
            for j in range(self.y):
                rect = pygame.Rect(j * SQRSIZE + 4 , i * SQRSIZE + 4, SQRSIZE - 5, SQRSIZE - 5)
                pygame.draw.rect(self.screen,"#efefef", rect)
        pygame.display.set_caption(f"Visualizer ({self.text})")
        pygame.display.update()

    def get_start(self,x,y):
        SQRSIZE = self.sqrsize
        self.board[x,y] = 1
        rect = pygame.Rect(y * SQRSIZE + 4 , x * SQRSIZE + 4, SQRSIZE - 5, SQRSIZE - 5)
        pygame.draw.rect(self.screen,"#fe1122",rect)
        self.text = "Click on where to end"
        pygame.display.set_caption(f"Visualizer ({self.text})")
        pygame.display.update()
        self.start = x,y
    
    def get_end(self,x,y):
        SQRSIZE = self.sqrsize
        self.board[x,y] = 2
        rect = pygame.Rect(y * SQRSIZE + 4 , x * SQRSIZE + 4, SQRSIZE - 5, SQRSIZE - 5)
        pygame.draw.rect(self.screen,"#15ff22",rect)
        self.text = "Left click and drag to Draw walls,right click and drag to remove walls and press spacebar"
        pygame.display.set_caption(f"Visualizer ({self.text})")
        pygame.display.update()
        self.end = x,y
    
    def draw_walls(self,x,y):
        SQRSIZE = self.sqrsize
        self.board[x,y] = 3
        rect = pygame.Rect(y * SQRSIZE + 4 , x * SQRSIZE + 4, SQRSIZE - 5, SQRSIZE - 5)
        pygame.draw.rect(self.screen,"#1e1e1e",rect)
        pygame.display.update()
        return (x,y)
    
    def delete_wall(self,x,y):
        SQRSIZE = self.sqrsize
        self.board[x,y] = 0
        rect = pygame.Rect(y * SQRSIZE + 4 , x * SQRSIZE + 4, SQRSIZE - 5, SQRSIZE - 5)
        pygame.draw.rect(self.screen,"#efefef",rect)
        pygame.display.update()
    
    def get_neighbors(self,x,y):
        #top,topri,right,botri,bottom,botlef,left,tople 
        neighbors = [(0,-1),(1,0),(0,1),(-1,0)]
        temp = []
        for i,j in neighbors:
            if (x+i)>=0 and (x+i)<self.x and (y+j)>=0 and (y+j)<self.y:
                if (self.board[x+i][y+j] != 3):
                    temp.append((x+i,y+j)) 
        return temp


    def search(self,num):
        #end is labelled as 2 and walls as 3
        x,y = self.start
        # search = {"1":Board.bfs,"2":Board.dfs,"3":Board.GBFS,"4":Board.A_star}

        #uninformed search
        # self.bfs(x,y)
        # self.dfs(x,y)

        # #informed search
        # self.A_star(x,y)
        # self.GBFS(x,y) 

        if num == 0:
            self.bfs(x,y)
        elif num == 1:
            self.dfs(x,y)
        elif num == 2:
            self.GBFS(x,y)
        elif num == 3:
            self.A_star(x,y)

    def draw_rect(self,x,y,color):
        SQRSIZE = self.sqrsize
        if not self.start == (x,y) and not self.end == (x,y) :
            rect = pygame.Rect(y * SQRSIZE + 4 , x * SQRSIZE + 4, SQRSIZE - 5, SQRSIZE - 5)
            pygame.draw.rect(self.screen,color,rect)
            pygame.display.update()

    def bfs(self,x,y):
        queue = []
        visited = dict()
        parents = dict()

        while (x,y) != self.end:
            if (x,y) == self.start:
                parents[x,y] = self.start

            visited[(x,y)] = parents[(x,y)]
            self.draw_rect(x,y,"#2156ff")

            neighbors = self.get_neighbors(x,y)

            for neighbor in neighbors:
                if not neighbor in visited and not neighbor in parents:
                    self.draw_rect(neighbor[0],neighbor[1],"#214653")
                    queue.append(neighbor)
                    parents[neighbor] = (x,y)

            if len(queue) > 0:
                a,b = queue[0]
                queue = queue[1:]
                x,y = a,b
            else:
                print("No solution")
                self.text = "No solution"
                pygame.display.set_caption(self.text)
                return 0

        self.text = "Found using BFS search algorithm !"
        pygame.display.set_caption(self.text)
        self.draw_path(parents[x,y],visited)
        return 1

    
    def dfs(self,x,y):
        stack = []
        visited = dict()
        parents = dict()
        while (x,y) != self.end:
            if (x,y) == self.start:
                parents[x,y] = self.start

            self.draw_rect(x,y,"#ff06aa")
            visited[(x,y)] = parents[(x,y)]

            neighbors = self.get_neighbors(x,y)
            for neighbor in neighbors:
                if not neighbor in visited and not neighbor in stack:
                    self.draw_rect(neighbor[0],neighbor[1],"#660045")
                    stack.append(neighbor)
                    parents[neighbor] = (x,y)

            if len(stack) > 0:
                a,b = stack.pop()
                x,y=a,b
            else:
                print("No solution")
                self.text = "No solution"
                pygame.display.set_caption(self.text)
                return 0
        
        self.text = "Found using DFS search algorithm !"
        pygame.display.set_caption(self.text) 
        self.draw_path(parents[x,y],visited)
        return 1
            
    
    def h(self,m,n):
        i,j = self.end
        return math.sqrt((m-i)**2 + (n-j)**2)

    def GBFS(self,x,y):
        parent=()
        visited={}
        stack=dict()

        while (x,y) != self.end:
            if (x,y) == self.start:
                parent = (x,y)
            
            self.draw_rect(x,y,"#563336")        
            visited[(x,y)] = parent

            neighbors = self.get_neighbors(x,y)

            for (m,n) in neighbors:
                if (m,n) not in visited:
                    # stack[(m,n)] = self.h(m,n)
                    stack[(m,n)] = {"value":self.h(m,n),"parent":(x,y)}
                    self.draw_rect(m,n,"#203114")
            
            if len(stack) > 0:
                sorted_stack = sorted(stack.items(),key=lambda x: x[1]["value"],reverse=True)[-1]
                a,b = sorted_stack[0]
                parent = stack[(a,b)]["parent"]
                stack.pop(sorted_stack[0])
                x,y = a,b
            else:
                print("No solution")
                self.text = "No solution"
                pygame.display.set_caption(self.text)
                return 0
        self.text = "Found using GBFS search algorithm !"
        pygame.display.set_caption(self.text)
        self.draw_path(parent,visited)
        return 1
    
    def A_star(self,x,y):
        parent=()
        visited={}
        stack=dict()
        cost={}
        while (x,y) != self.end:
            if (x,y) == self.start:
                parent = (x,y)
                cost[(x,y)] = -1

            self.draw_rect(x,y,"#ee33aa")
            visited[(x,y)] = parent

            neighbors = self.get_neighbors(x,y)

            cost[(x,y)] = cost[parent] + 1
            
            for (m,n) in neighbors:
                if (m,n) not in visited and not (m,n) in stack.keys():
                    # stack[(m,n)] = {"value":self.h(m,n) + self.cost(m,n),"parent":(x,y)}
                    stack[(m,n)] = {"value":self.h(m,n) + cost[(x,y)]  ,"parent":(x,y) }
                    self.draw_rect(m,n,"#880055")

            if len(stack) > 0:
                sorted_stack = sorted(stack.items(),key=lambda x: x[1]["value"],reverse=True)[-1]
                a,b = sorted_stack[0]
                parent = stack[(a,b)]["parent"]
                stack.pop(sorted_stack[0])
                x,y = a,b

            else:
                print("No solution")
                self.text = "No solution"
                pygame.display.set_caption(self.text)
                return
        self.text = "Found using A_star search algorithm !"
        pygame.display.set_caption(self.text) 
        self.draw_path(parent,visited)
        return 1

    
    def draw_path(self,parent,stack):
        while not parent == self.start:
            x,y = parent[0],parent[1]
            self.board[x][y] = 5
            self.draw_rect(x,y,"#ffff00")
            parent = stack[parent]
        return

def find_path(num):
    pygame.display.set_caption("Visualizer")
    board = Board(screen)
    board.draw_board()
    running = True
    searching = False
    pygame.display.update()

    # algo = None
    # search = {"1":Board.bfs,"2":Board.dfs,"3":Board.GBFS,"4":Board.A_star}

    while running == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                x,y = pygame.mouse.get_pos()
                clickedX,clickedY = int(y//board.sqrsize) , int(x//board.sqrsize)
                if board.start == None:
                    board.get_start(clickedX,clickedY)

                elif board.start != None and board.end == None:
                    if not (clickedX,clickedY) == board.start:
                        board.get_end(clickedX,clickedY)

            if event.type == pygame.MOUSEMOTION and board.end != None and searching == False:
                x,y = pygame.mouse.get_pos()
                clickedX,clickedY = int(y//board.sqrsize) , int(x//board.sqrsize)
                left,_,right = pygame.mouse.get_pressed()
                if clickedX>=0 and clickedX<board.x and clickedY>=0 and clickedY<board.y:
                    if (clickedX,clickedY) != board.start and (clickedX,clickedY) != board.end: 
                        if left:
                            board.draw_walls(clickedX,clickedY)
                        if right:
                            board.delete_wall(clickedX,clickedY)

            if event.type == pygame.KEYDOWN:
                if board.end != None:
                    if event.key == pygame.K_SPACE and searching == False:
                        searching = True
                        # print(board.board)
                        pygame.display.set_caption("Searching...")
                        board.search(num)
                if event.key == pygame.K_RSHIFT:
                    screen.fill("#000000")
                    main()

def main():
    algo = None
    text = ["Breadth First Search","Depth First Search","Greedy BFS","A* search"]
    s_Rect = []
    font = pygame.font.SysFont('arial',60,True)
    for num,i in enumerate(text):
        text = font.render(f"{num+1}. {i}",True,"#ffffff")
        text_rect = pygame.Rect(WIDTH/3, num*60 +text.get_height()*(num+1) + 40 ,text.get_width() , text.get_height())
        screen.blit(text,text_rect)
        s_Rect.append(text_rect)
    
    while algo == None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                for num,j in enumerate(s_Rect):
                    if j.collidepoint(pygame.mouse.get_pos()):
                        algo = num
        pygame.display.update()
    screen.fill("#000000")
    find_path(algo)

if __name__ == "__main__":
    main()