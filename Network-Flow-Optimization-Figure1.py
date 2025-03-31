from collections import deque
import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self, vertices):
        self.V = vertices  # Numri i nyjeve (vertices)
        self.graph = [[0] * vertices for _ in range(vertices)]  # Matrica e kapaciteteve
        self.original_graph = [[0] * vertices for _ in range(vertices)]  # Kopje e grafit origjinal për vizualizim

    def add_edge(self, u, v, capacity):
        self.graph[u][v] = capacity  # Shto një lidhje me kapacitet të caktuar
        self.original_graph[u][v] = capacity  # Ruaj lidhjet origjinale për vizualizim

    def bfs(self, source, sink, parent):
        """ Algoritmi BFS për të gjetur një rrugë me rrjedhë të mundshme """
        visited = [False] * self.V
        queue = deque([source])
        visited[source] = True

        while queue:
            u = queue.popleft()
            for v in range(self.V):
                if not visited[v] and self.graph[u][v] > 0:  # Nëse ka kapacitet të mbetur
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u
                    if v == sink:
                        return True  # Arriti destinacionin
        return False

    def ford_fulkerson(self, source, sink):
        """ Implementimi i algoritmit Ford-Fulkerson për të gjetur rrjedhën maksimale """
        parent = [-1] * self.V
        max_flow = 0  # Rrjedha maksimale

        while self.bfs(source, sink, parent):
            # Gjej rrjedhën maksimale të mundshme në rrugën e gjetur nga BFS
            path_flow = float('Inf')
            s = sink
            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]
            
            # Përditëso rrjedhën në graf
            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow  # Përditëso rrjedhën e mbetur
                self.graph[v][u] += path_flow  # Shto rrjedhën në rrjedhën e kthyer
                v = parent[v]
            
            max_flow += path_flow  # Shto rrjedhën aktuale

        return max_flow

    def print_flow(self):
        """ Shfaq rrjedhën për secilën lidhje """
        print("Rrjedha për secilën lidhje:")
        for u in range(self.V):
            for v in range(self.V):
                if self.original_graph[u][v] > 0:
                    print(f"Lidhja {u} -> {v}: {self.original_graph[u][v] - self.graph[u][v]}")  # Rrjedha aktuale

    def draw_graph(self):
        """ Vizualizon grafikun me rrjedhat e gjetura """
        G = nx.DiGraph()
        for u in range(self.V):
            for v in range(self.V):
                if self.original_graph[u][v] > 0:
                    G.add_edge(u, v, capacity=self.original_graph[u][v], flow=self.original_graph[u][v] - self.graph[u][v])
        
        pos = nx.spring_layout(G)
        edge_labels = {(u, v): f"{d['flow']}/{d['capacity']}" for u, v, d in G.edges(data=True)}
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=12)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, font_color='red')
        plt.show()

# Shembull përdorimi
graph = Graph(6)
graph.add_edge(0, 1, 16)
graph.add_edge(0, 2, 13)
graph.add_edge(1, 2, 10)
graph.add_edge(1, 3, 12)
graph.add_edge(2, 1, 4)
graph.add_edge(2, 4, 14)
graph.add_edge(3, 2, 9)
graph.add_edge(3, 5, 20)
graph.add_edge(4, 3, 7)
graph.add_edge(4, 5, 4)

source, sink = 0, 5
print("Rrjedha maksimale është:", graph.ford_fulkerson(source, sink))

# Shfaq rrjedhën për secilën lidhje
graph.print_flow()

# Vizualizo grafikun
graph.draw_graph()
