import tkinter as tk
import constants as cst
import time 


class GUI :
    def __init__(self):
        self.world = None
        self.win = None
        self.canvas = None
        self.color_offset = None 
        self.link_Tab = []

    def open_GUI(self):
        self.win = tk.Tk()
        
    def loop(self):
        self.win.mainloop()

    def set_World(self, world):
        
        self.world = world
       
        w = world.size_X*cst.SIZE_MULTIPLICATOR + cst.MARGE
        h = world.size_Y*cst.SIZE_MULTIPLICATOR + cst.MARGE
        self.canvas = tk.Canvas(self.win, width= w, height= h)
        ### Visual asspect of the canvas
        self.canvas.create_rectangle(cst.FRAME_PADDING, cst.FRAME_PADDING, w-cst.FRAME_PADDING, h-cst.FRAME_PADDING)
        

    def set_Nodes(self, nodes):
        for n in nodes:
            xMin = n.pos_X*cst.SIZE_MULTIPLICATOR - cst.NODE_SIZE + 2*cst.MARGE
            xMax = n.pos_X*cst.SIZE_MULTIPLICATOR + cst.NODE_SIZE + 2*cst.MARGE
            yMin = n.pos_Y*cst.SIZE_MULTIPLICATOR - cst.NODE_SIZE + 2*cst.MARGE
            yMax = n.pos_Y*cst.SIZE_MULTIPLICATOR + cst.NODE_SIZE + 2*cst.MARGE
            self.canvas.create_oval(xMin, yMin, xMax, yMax)

            self.display()
        
        for n in nodes:
            self.canvas.create_text(n.pos_X*cst.SIZE_MULTIPLICATOR+2*cst.MARGE, n.pos_Y*cst.SIZE_MULTIPLICATOR+2*cst.MARGE, text=n.id)
            self.display
        self.color_offset = 2*len(nodes)
            

    def display(self):
        self.canvas.pack()

    def refresh(self, nodes):
        
        n=0
        for n in nodes:
            
            xMin = n.pos_X*cst.SIZE_MULTIPLICATOR - cst.NODE_SIZE + 2*cst.MARGE
            xMax = n.pos_X*cst.SIZE_MULTIPLICATOR + cst.NODE_SIZE + 2*cst.MARGE
            yMin = n.pos_Y*cst.SIZE_MULTIPLICATOR - cst.NODE_SIZE + 2*cst.MARGE
            yMax = n.pos_Y*cst.SIZE_MULTIPLICATOR + cst.NODE_SIZE + 2*cst.MARGE
            self.canvas.coords(n.id+2,xMin, yMin, xMax, yMax)

            self.canvas.coords(n.id+len(nodes)+2,n.pos_X*cst.SIZE_MULTIPLICATOR+2*cst.MARGE, n.pos_Y*cst.SIZE_MULTIPLICATOR+2*cst.MARGE)


 
        self.canvas.update()

    def color_refresh(self, node_list):
        for l in self.link_Tab:
            self.canvas.delete(l)
        for n in node_list :
            for color in list(n.coloring.keys()):
                #print(n.coloring.get(color))
                if (n.coloring.get(color)== None):
                    continue
                line = self.canvas.create_line(node_list[color[0]].pos_X*cst.SIZE_MULTIPLICATOR+2*cst.MARGE, node_list[color[0]].pos_Y*cst.SIZE_MULTIPLICATOR+2*cst.MARGE, node_list[color[1]].pos_X*cst.SIZE_MULTIPLICATOR+2*cst.MARGE, node_list[color[1]].pos_Y*cst.SIZE_MULTIPLICATOR+2*cst.MARGE, fill=cst.COLOR[n.coloring.get(color)])
                self.link_Tab.append(line)

    def color_node (self, node, node_list):
        for l in self.link_Tab:
            self.canvas.delete(l)
        
        for color in list(node.coloring.keys()):
            
            line = self.canvas.create_line(node_list[color[0]].pos_X*cst.SIZE_MULTIPLICATOR+2*cst.MARGE, node_list[color[0]].pos_Y*cst.SIZE_MULTIPLICATOR+2*cst.MARGE, node_list[color[1]].pos_X*cst.SIZE_MULTIPLICATOR+2*cst.MARGE, node_list[color[1]].pos_Y*cst.SIZE_MULTIPLICATOR+2*cst.MARGE, fill=cst.COLOR[node.coloring.get(color)])
            self.link_Tab.append(line)

        
            
            
