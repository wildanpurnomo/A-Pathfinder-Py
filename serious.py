from tkinter import *
import time

class Cell():
    def __init__(self, master, x, y, size):
        #attribute for drawing
        self.master = master
        self.abs = x
        self.ord = y
        self.size = size

        #attribute for A*
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

        #position
        self.position= (y,x)

        #color
        self.color = None

    def __eq__(self, other):
        return self.position == other.position
        

    def draw(self):
        if self.master is not None:
            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size
            
            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill = 'white')

    def _colorizeStartNode(self):
        if self.master is not None :
            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size

            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill = 'red')

    def _colorizeEndNode(self):
        if self.master is not None:
            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size

            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill = 'green')

    def _colorizePath(self):
        if self.master is not None:
            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size

            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill = 'blue')

    def _colorizeWall(self):
        if self.master is not None:
            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size

            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill = 'black')
            

class Maze(Canvas):
    def __init__(self, master, row_number, col_number, cell_size, *args, **kwargs):
        Canvas.__init__(self, master, width = cell_size * col_number, height = cell_size * row_number, *args, **kwargs)

        #row and col number
        self.row_number = row_number
        self.col_number = col_number

        self.start_cell = None
        self.start_cell_position = None
        self.end_cell = None
        self.end_cell_position = None
        
        self.cell_size = cell_size
        self.grid = []
        for row in range (row_number):
            line = []
            for column in range(col_number):
                line.append(Cell(self, column, row, cell_size))

            self.grid.append(line)

        self.bind("<Control-1>", self._createStartCell)
        self.bind("<Control-3>", self._createEndCell)
        self.bind("<B3-Motion>", self._createWallCell)
        
        self.draw()
        

    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw()

    def _eventCoords(self, event):
        row = int(event.y / self.cell_size)
        column = int(event.x / self.cell_size)
        return row, column

    def _createStartCell(self, event):
        row, column = self._eventCoords(event)
        temp = (row, column)

        if self.start_cell_position is not None:
            if temp != self.start_cell_position:
                old_cell = self.grid[self.start_cell_position[0]][self.start_cell_position[1]]
                old_cell.draw()
                
                self.start_cell_position = temp
                self.start_cell = self.grid[row][column]
                self.start_cell.parent = None
                self.start_cell._colorizeStartNode()
                
                self._printStartNode()
                
        else:
            self.start_cell_position = temp
            self.start_cell = self.grid[row][column]
            self.start_cell.parent = None
            self.start_cell._colorizeStartNode()
            
            self._printStartNode()


    def _createEndCell(self, event):
        row, column = self._eventCoords(event)
        temp = (row, column)

        if self.end_cell_position is not None:
            if temp != self.end_cell_position:
                old_cell= self.grid[self.end_cell_position[0]][self.end_cell_position[1]]
                old_cell.draw()

                self.end_cell_position = temp
                self.end_cell = self.grid[row][column]
                self.end_cell._colorizeEndNode()
                self._printEndNode()

        else:
            self.end_cell_position = temp
            self.end_cell = self.grid[row][column]
            self.end_cell._colorizeEndNode()
            self._printEndNode()

    def _createWallCell(self, event):
        row, column = self._eventCoords(event)
        self.grid[row][column]._colorizeWall()
        self.grid[row][column].color = 'black'
        
    
    def _printStartNode(self):
        print("Start Node is ", self.start_cell_position)

    def _printEndNode(self):
        print("End Node is ", self.end_cell_position)
        
def astar(maze):
    #create start and end node
    start_node = maze.start_cell
    end_node = maze.end_cell

    #initialize open and closed list
    open_list = []
    closed_list = []

    #add the start node
    open_list.append(start_node)

    print(start_node.position, end_node.position)

    #loop until find the end node
    while len(open_list) > 0:

        #get current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        #colorize current_node
##        if current_node != start_node and current_node is not end_node:
##            print("ayeaye")
##            maze.grid[current_node.position[0]][current_node.position[1]]._colorizePath()

        #print traversing info
        if current_node.parent is not None:
            print("current Node : ", current_node.position, " with parent node = ", current_node.parent.position, " end node = ", end_node.position)

        #pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        #found the goal!
        if current_node == end_node:
            print("PATH FOUND: ")
            path = []
            current = current_node
            while current is not None:
                if current.position is not end_node.position:
                    current._colorizePath()
                    
                path.append(current.position)
                
                if current.parent.position == start_node.position :
                    break
                
                current = current.parent
                
            return path[::-1]
            
            

        #generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:

            #get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            

            #make sure within range
            if node_position[0] > maze.row_number - 1 or node_position[0] < 0 or node_position[1] > maze.col_number - 1 or node_position[1] < 0:
                continue

            #make sure walkable
            if maze.grid[node_position[0]][node_position[1]].color is 'black':
                continue

            #dont go back
            if maze.grid[node_position[0]][node_position[1]].parent is not None:
                print(node_position)
                if node_position == current_node.parent.position :
                    continue

            #create new node
            row = node_position[0]
            column = node_position[1]
            new_node = maze.grid[row][column]
            new_node.parent = current_node

            #append to children
            children.append(new_node)

        #loop through the children
        for child in children:

            #child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            #compute f, g and h values
            child.g = current_node.g + 1
            child.h = ((child.abs - end_node.abs) ** 2) + ((child.ord - end_node.ord) ** 2)
            child.f = child.g + child.h
            print(child.position, " = ", child.f)

            #child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            #add child to open list
            open_list.append(child)


if __name__ == "__main__":         
    app = Tk()
##    app.geometry("500x500")
    maze = Maze(app, 20, 20, 100)
    maze.pack()
    
    app.bind("<Return>", lambda event, arg = maze: print(astar(arg)))

    app.mainloop()
