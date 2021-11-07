import tkinter as Tk
import matplotlib
import numpy as np
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import networkx as nx
import sys
from matplotlib.figure import Figure

#Se lee el archivo txt
f = sys.stdin # Por entrada estandar
data = f.read().strip()
f.close()


minist = Tk.Tk()
minist.wm_title("Minimum spanning tree")
fi = Figure(figsize=(12,7), dpi=100 )
a = fi.add_subplot(111)


#Se ingresa todo el contenido del txt a MI 
MI = [[int(num) for num in line.strip().split()] for line in data.split('\n')]

#Dimension de la matriz de adyacencia
dim = MI[0][0]

#Se crea MA
MA = []
for i in range(dim):
    MA.append([])
    for j in range(dim):
        MA[i].append(None)

#Se le dan los valores a MA
for i in range(dim):
    for j in range(dim):
    	MA[i][j] = MI[i+1][j]

print("Matriz entrante:")
#print(MA)

for i in range(dim):
    for j in range(dim):
         print(MA[i][j], end=" ")#end="& "
    print("\n")

#------------| Inicio NetworkX |--------------------
#Se crea el grafo
G=nx.Graph()

#Se crean los vertices
for i in range(dim):
    G.add_node(i)

#Se crean las aristas
for i in range(dim):
    for j in range(dim):
        if MA[i][j]>0:
            G.add_edge(i,j,weight=MA[i][j],key=0)
        
#Forma del grafo
pos=nx.circular_layout(G)


#----------------| Kruskal |-------------------------
nodos = dim
A=0
B=0
cantidadDistancias = 1
    
#Se crea PE y MAA
PE = np.arange(dim) # PE lista de vertices
MAA = np.zeros((dim,dim)) # MAA matriz con ceros
        
while cantidadDistancias != nodos:
    mini = 500
    actual = 0        
    for i in range(nodos):
        for j in range (nodos):
            if mini > MA[i][j] and MA[i][j] != 0 and MA[i][j] != -1 and PE[i] != PE[j]:
                mini = MA[i][j]
                A=i
                B=j  

    if PE[A] != PE[B]:
        MAA[A][B]= mini
        MAA[B][A]= mini            
        actual = PE[B]
        PE[B] = PE[A]        
        for k in range (nodos):
            if PE[k] == actual:
                PE[k]=PE[A]
    cantidadDistancias = cantidadDistancias+1
#-------------- Fin Kruskal --------------------------

#Se crea el grafo G1 (Arbol recubridor)
G1=nx.Graph()

#Se crean los vertices
for i in range(dim):
    G1.add_node(i)

#Se crean las aristas
for i in range(dim):
    for j in range(dim):
        if MAA[i][j]>0:
            G1.add_edge(i,j,weight=MAA[i][j],key=0)
        
#Forma del grafo
pos=nx.circular_layout(G1)
print("----------------------------------------------")
print("Matriz del arbol recubridor minimo")
#print(MAA)

for i in range(dim):
    for j in range(dim):
         print(MAA[i][j], end=" ") #end="& "
    print("\n")

"""
#Se crea G1 (Un grafo que es el arbol de espancion minima de G)
#Se pueden usar tres algoritmos: kruskal, prim o boruvka.
# G1 = nx.minimum_spanning_tree(G, algorithm='kruskal')
# G1 = nx.minimum_spanning_tree(G, algorithm='prim')
# G1 = nx.minimum_spanning_tree(G, algorithm='boruvka')

G1 = nx.minimum_spanning_tree(G)
#En este caso como no se le da un tipo de algoritmo, por defecto utiliza el de kruskal
"""

#LG1 contiene la informacion de las aristas de G1
LG1 = sorted(G1.edges(data=True))
#print(LG1)
#Se sobreescriben las aristas de G que estan contenidas en G1
#Pero se les cambia el key a 1
for i in range(len(LG1)):
    G.add_edge(LG1[i][0],LG1[i][1],weight=LG1[i][2]['weight'],key=1)

#Creo una lista con las aristas de G que tengan key=1
caminoA=[(u,v) for (u,v,d) in G.edges(data=True) if d['key'] == 1]


#--------------| Draw |---------------------------
# nodes
nx.draw_networkx_nodes(G,pos,ax=a)
# Node labels
labels={}
for i in range(dim):
    labels[i]=i+1
#Draw Node Labels
nx.draw_networkx_labels(G,pos,labels,font_size=10,ax=a)

# edges
nx.draw_networkx_edges(G,pos,width=2,ax=a)
#nx.draw_networkx_edges(G,pos,edgelist=caminoA,width=2,ax=a)
edge_labels = {i[0:2]:'{}'.format(i[2]['weight']) for i in G.edges(data=True)}

# labels
nx.draw_networkx_edge_labels(G,pos,font_size=6,font_family='sans-serif', edge_labels = edge_labels,ax=a)
#plt.axis('off')
#plt.savefig("minimum_spanning_tree.png") # save as png



def mostrar():
    #minist.withdraw()
    win=Tk.Toplevel()
    win.geometry('1200x740')
    fe = Figure(figsize=(12,7), dpi=100 )
    b = fe.add_subplot(111)

    #--------------| Draw 2|---------------------------
    # nodes
    nx.draw_networkx_nodes(G,pos,ax=b)
    # Node labels
    labels={}
    for i in range(dim):
        labels[i]=i+1
    #Draw Node Labels
    nx.draw_networkx_labels(G,pos,labels,font_size=10,ax=b)

    # edges
    nx.draw_networkx_edges(G,pos,width=2,alpha=0.1,ax=b)
    nx.draw_networkx_edges(G,pos,edgelist=caminoA,width=2,ax=b)
    edge_labels = {i[0:2]:'{}'.format(i[2]['weight']) for i in G.edges(data=True)}

    # labels
    nx.draw_networkx_edge_labels(G,pos,font_size=6,font_family='sans-serif', edge_labels = edge_labels,ax=b)
    canvas2 = FigureCanvasTkAgg(fe, win)
    canvas2.show()
    toolbar = NavigationToolbar2TkAgg( canvas2, win )
    toolbar.update()
    canvas2._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)


canvas = FigureCanvasTkAgg(fi, minist)
canvas.show()
#canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

toolbar = NavigationToolbar2TkAgg( canvas, minist )
toolbar.update()
canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

button = Tk.Button(minist, text='Mostrar arbol recubridor minimo', command=mostrar)
button.pack(side=Tk.BOTTOM)

Tk.mainloop()


