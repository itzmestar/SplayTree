import tkinter
from tkinter import *


class node:
    def __init__(self, key, data):
        self.key = key
        self.right = None
        self.left = None
        self.p = None
        self.data = data
        self.h = 0
        self.pot = 0

    # find the height of the node
    # returns the height
    def height(self):
        r = self.right.height() if self.right else -1
        l = self.left.height() if self.left else -1

        self.h = max(l, r) + 1
        return self.h

    # find the potential of the node
    # returns the potential
    def potential(self):
        pot = 1
        if self.left:
            pot += self.left.potential()
        if self.right:
            pot += self.right.potential()

        self.pot = pot
        #print("key:{} pot:{}".format(self.key, pot))
        return pot

    def __str__(self):
        return "("+str(self.key)+", '"+str(self.data)+"')"

class SplayTree():
    def __init__(self, key, data):
        self.root = node(key, data)
        self.rotations = 0
        self.print = True
        self.n = 1
        pass

    #search a key in the Tree.
    # returns the node if found else returns None
    def search(self, key):

        ptr = self.root
        ptr1 = ptr
        while ptr:
            ptr1 = ptr
            if ptr.key > key:
                ptr = ptr.left
            elif ptr.key < key:
                ptr = ptr.right
            else:
                self.splay(ptr)
                #if self.print:
                #    self.print_info()
                #print(ptr.key)
                return ptr
        self.splay(ptr1)
        return None

    # insert the key-data into the tree as BST insertion then splay the tree
    def insert(self, key, data):

        new_node = node(key, data)

        #if root is None:
        if self.root is None:
            self.root = new_node
            self.splay(new_node)
            return
        #insert at the right position as BST
        ptr = self.root
        ptr1 = None
        while ptr is not None:
            if ptr.key > key:
                ptr1 = ptr
                #ptr.size += 1
                ptr = ptr.left
            elif ptr.key < key:
                ptr1 = ptr
                #ptr.size += 1
                ptr = ptr.right
            else:
                ptr1 = ptr
                break

        if ptr1.key == key:
            # key already exists: DO NOT INSERT
            pass
        elif ptr1.key < key:
            ptr1.right = new_node
            new_node.p = ptr1
        else:
            ptr1.left = new_node
            new_node.p = ptr1

        self.splay(new_node)
        #self.print_info()
        #self.root = new_node

    # calculate the total potential of the tree
    def tree_potential(self, ptr):
                
        if ptr.left:
            self.tree_potential(ptr.left)
        if ptr.right:
            self.tree_potential(ptr.right)
        #print("n={} key={} pot={}".format(n,ptr.key,ptr.potential()))
        self.n *= ptr.potential()
        return self.n

    # replace u node with v
    def _replace(self, u, v):
        if not u.p:
            self.root = v
        elif u == u.p.left:
            u.p.left = v
        else:
            u.p.right = v

        if v:
            v.p = u.p

    # find the minimum key node in the left subtree
    def _subtreeMinimum(self, ptr):
        while ptr.left:
            ptr = ptr.left
        return ptr

    # delete the node with key
    def delete(self, key):
        #self.print = False
        ptr = self.search(key)
        #self.print = True

        if not ptr:
            return

        #self.splay(ptr)

        if not ptr.left:
            self._replace(ptr, ptr.right)
        elif not ptr.right:
            self._replace(ptr, ptr.left)
        else:
            y = self._subtreeMinimum(ptr.right)
            if y.p != ptr:
                self._replace(y, y.right)
                y.right = ptr.right
                y.right.p = y
            self._replace(ptr, y)
            y.left = ptr.left
            y.left.p = y

        #print(self.root.key)
        #self.print_info()

    # perform a left rotation
    def _left_rotate(self, x):
        self.rotations += 1
        y = x.right
        if y:
            x.right = y.left
            if y.left:
                y.left.p = x
            y.p = x.p

        if not x.p:
            self.root = y
        elif x == x.p.left:
            x.p.left = y
        else:
            x.p.right = y

        if y:
            y.left = x
        x.p = y

    # perform a right rotation
    def _right_rotate(self, x):
        self.rotations += 1
        y = x.left
        if y:
            x.left = y.right
            if y.right:
                y.right.p = x
            y.p = x.p

        if not x.p:
            self.root = y
        elif x == x.p.left:
            x.p.left = y
        else:
            x.p.right = y

        if y:
            y.right = x
        x.p = y

    # perform the splay operation
    def splay(self, x):
        self.rotations = 0
        self.potential_before = 0
        self.potential_after = 0
        
        print("Splay on key : {}".format(x.key), flush=True)

        #potential before splay
        obere_root = self.root.potential()
        self.obere_root = (obere_root ** 3)*2
        #print("potential before")
        obere_x = x.potential()
        self.obere_x = obere_x ** 3
        self.n = 1
        self.potential_before = self.tree_potential(self.root)
        #print("potential before done")
        while x.p:
            #print(x.p.key)
            self.splayingStep(x)
        self.print_info()

    # print splay info
    def print_info(self):
        # potential after splay
        self.root.potential()
        self.n = 1
        self.potential_after = self.tree_potential(self.root)
        #print("potential after")
        rotations = 2**self.rotations
        print("2^ Rotations : {}".format(rotations), flush=True)
        print("2^ Potential before : {}".format(self.potential_before), flush=True)
        print("2^ Potential after : {}".format(self.potential_after), flush=True)


    # splaying step function
    def splayingStep(self, x):
        if x.p is None:
            return
        elif x.p.p is None and x == x.p.left:
            self._right_rotate(x.p)
        elif x.p.p is None and x == x.p.right:
            self._left_rotate(x.p)
        elif x == x.p.left and x.p == x.p.p.left:
            self._right_rotate(x.p.p)
            self._right_rotate(x.p)
        elif x == x.p.right and x.p == x.p.p.right:
            self._left_rotate(x.p.p)
            self._left_rotate(x.p)
        elif x == x.p.left and x.p == x.p.p.right:
            self._right_rotate(x.p)
            self._left_rotate(x.p)
        else:
            self._left_rotate(x.p)
            self._right_rotate(x.p)

    # draw the tree on the canvas
    def draw(self, canvas):
        if self.root is None:
            return
        self.root.height()
        self._preOrderDrawEdge(canvas, self.root, 500, 100)
        self._preOrderDrawNode(canvas, self.root, 500, 100)

    # draw the edge of the tree on canvas
    def _preOrderDrawEdge(self, canvas, ptr, x, y):

        if ptr is not None:
            #canvas.create_line(x, y, x+30, y+30)
            #print(ptr.key)
            if ptr.right is not None:
                canvas.create_line(x+15, y+30, x+(ptr.h*30)+15, y+50)
                self._preOrderDrawEdge(canvas, ptr.right, x + (ptr.h * 30), y + 50)
            if ptr.left is not None:
                canvas.create_line(x+15, y+15, x-(ptr.h*30)+15, y+50)
                self._preOrderDrawEdge(canvas, ptr.left, x-(ptr.h*30), y+50)

    # draw the node of the tree on canvas
    def _preOrderDrawNode(self, canvas, ptr, x, y):

        if ptr is not None:
            canvas.create_rectangle(x, y, x+30, y+30, fill="white")
            canvas.create_text(x+15, y+15, text=str(ptr.key))
            #print(ptr.key)
            self._preOrderDrawNode(canvas, ptr.left, x-(ptr.h*30), y+50)
            self._preOrderDrawNode(canvas, ptr.right, x+(ptr.h*30), y+50)




class TreeVisualizer():
    def __init__(self, tk):
        self.tk = tk
        self.master = tk
        Label(self.master, text="Key").grid(row=0)
        Label(self.master, text="Data").grid(row=1)

        self.entry1 = Entry(self.master)
        self.entry2 = Entry(self.master)

        self.entry1.grid(row=0, column=1)
        self.entry2.grid(row=1, column=1)

        construct_button = Button(self.master, text='construct', command=self.create).grid(row=3, column=1, sticky=W, pady=4)
        #construct_button.pack()
        self.master.mainloop()

    # create the new window with 3 buttons & draw root node
    def create(self):
        key = self.entry1.get()
        data = self.entry2.get()
        #print(key)
        #print(data)
        self.T = SplayTree(int(key), data)
        self.master.destroy()

        self.master = Tk()

        self.draw()
        self.master.mainloop()

    # perform this function when insert button is clicked
    def insert(self):
        key = self.key_entry.get()
        data = self.data_entry.get()

        if key == "":
            return
        #print("inserting")

        self.T.insert(int(key), data)

        #print("inserted")
        self.canvas.destroy()
        #print("destroyed")
        self.draw()
        #print("")

    # perform this function when search button is clicked
    def search(self):
        key = self.key_entry.get()

        if key == "":
            return

        node = self.T.search(int(key))
        if node:
            print(node)
        self.canvas.destroy()
        self.draw()

    # perform this function when delete button is clicked
    def delete(self):
        key = self.key_entry.get()

        if key == "":
            return

        self.T.delete(int(key))
        self.canvas.destroy()
        self.draw()

    # draw buttons & tree nodes on the canvas
    def draw(self):
        canvas_width = 1200
        canvas_height = 600
        self.canvas = tkinter.Canvas(self.master, width=canvas_width, height=canvas_height)
        self.canvas.pack()
        self.canvas.create_text(300, 15, text="Key")
        self.canvas.create_text(300, 55, text="Data")

        self.key_entry = Entry(self.canvas)
        self.data_entry = Entry(self.canvas)

        self.key_entry.configure(width=60)
        self.canvas.create_window(350, 5, anchor=NW, window=self.key_entry)
        self.data_entry.configure(width=60)
        self.canvas.create_window(350, 45, anchor=NW, window=self.data_entry)
        #self.canvas.create_rectangle(50, 20, 150, 80, fill="#476042")
        #self.canvas.create_rectangle(65, 35, 135, 65, fill="yellow")

        self.search_button = Button(self.canvas, text='search', width=10, command=self.search)
        self.insert_button = Button(self.canvas, text='insert', width=10, command=self.insert)
        self.delete_button = Button(self.canvas, text='delete', width=10, command=self.delete)

        self.canvas.create_window(290, 70, anchor=NW, window=self.search_button)
        self.canvas.create_window(470, 70, anchor=NW, window=self.insert_button)
        self.canvas.create_window(630, 70, anchor=NW, window=self.delete_button)

        self.T.draw(self.canvas)

        pass




tk = tkinter.Tk()
app = TreeVisualizer(tk)
'''
#print (result)

T = SplayTree(10,10)
for i in range (9,4, -1):
    T.insert(i,i)
    #T.root.height()
    #T._inOrder(T.root, 0)

T.search(10).key
T.search ( 10 ).data
T.delete ( 8 )

'''