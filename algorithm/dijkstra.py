from collections import defaultdict
import heapdict

def create_graph(values : list, volumes : list, L : float) -> defaultdict:
    """
    Creates a graph as a dictionary, it represents a decision tree of whether to add a specific item or not.
    Each vertex given as a key returns edges from it to different vertices
    eg. graph[vertex1]=[(vertex2,weight2),(vertex3,weight3)]
    vertices are defined as tuples (free space left, item id)
    with the exception of first and last vertex defined as:
    (free space, -1) and (0, number of items) respectively
    in order to use Dijkstra algorythm later on, weights of edges is defined as such:
    highest volume of all items, for all edges where an item was not added,
    highest volume of all items - weight of item added, for edges where item was added
    :param values: takes in values of items. Determines the weight of edges. Solution optimise for maximum value.
    :param volumes: takes in volumes of items. Determines space taken in the knapsack.
    :param L: capacity of the knapsack
    :return: returns a graph as a dictionary
    """
    N=len(values)

    graph = defaultdict(list)

    values_inv = []
    max_value = max(values)
    for value in values:
        values_inv.append(max_value-value)

    nodes = [(L, -1)]

    for i in range(N):
        nodes_new = []
        for node in nodes:
            graph[node].append(((node[0],i),max_value))
            if (node[0],i) not in nodes_new:
                nodes_new.append((node[0],i))
            if node[0]-volumes[i]>=0:
                graph[node].append(((node[0]-volumes[i], i), values_inv[i]))
                if (node[0]-volumes[i], i) not in nodes_new:
                    nodes_new.append((node[0]-volumes[i], i))
        nodes = nodes_new

    for node in nodes:
        graph[node].append(((0,N),0))

    return graph


def dijkstra(G : dict) -> tuple:
    """
    Runs Dijkstra algorithm to find the shortest path in a graph,
    where the graph is represented as a dictionary
    dist - storing distances from starting vertex to any other vertex
    prev - storing the previous vertex in the shortest path from starting vertex to any other vertex
    :param G: takes in a graph as a dictionary
    :return: returns two dictionaries, one with distances and the other with previous vertices
    """
    Q = list(G.keys())

    end = Q[0]
    while G[end]:
        end = G[end][0][0]
    Q.append(end)

    dist = {}
    prev = {}
    for vertex in Q:
        dist[vertex] = float('inf')
        prev[vertex] = None

    dist[Q[0]]=0
    
    heap = heapdict.heapdict()
    for vertex in Q:
        heap[vertex] = dist[vertex]

    while heap:
        u, temp = heap.popitem()
        for v in G[u]:
            if dist[v[0]]>dist[u]+v[1]:
                dist[v[0]] = dist[u]+v[1]
                prev[v[0]] = u
                heap[v[0]] = dist[u]+v[1]

    return dist, prev


def get_path(G : defaultdict,prev : dict) -> list:
    """
    Returns the shortes path between staring and ending vertex
    takes in the graph and dictionary prev from dijkstra algorythm
    :param G: takes in a graph as a dictionary
    :param prev: takes in a dictionary with previous vertices from dijkstra algorythm
    :return: returns the shortest path as a list of vertices
    """
    Q = list(G.keys())

    end = Q[0]
    while G[end]:
        end = G[end][0][0]

    best_path = []

    while prev[end] is not None:
        best_path.append(end)
        end = prev[end]

    best_path.append(end)
    best_path.reverse()

    return best_path


def get_items(path : list) -> list:
    """
    Takes in the best path and returns the items being the solution to the knapsack problem
    :param path: takes in the best path as a list of vertices
    :return: returns a list of items being the solution to the knapsack problem
    """
    selected = []
    for i in range(1, len(path) - 1):
        previous, current = path[i - 1], path[i]
        if current[0] < previous[0]:
            selected.append(current[1])
    return selected

if __name__ == '__main__':
    #two examples:
    capacity = 5
    values = [60.0, 100.0, 120.0]
    volumes = [1.0, 2.0, 3.0]

    G = create_graph(values,volumes,capacity)
    dist, prev = dijkstra(G)
    best_path = get_path(G,prev)
    items = get_items(best_path)
    print(best_path)
    print(items)

    capacity = 6
    values = [20.0, 17.0, 18.0, 15.0, 7.0]
    volumes = [4.0, 3.0, 2.0, 2.0, 1.0]

    G = create_graph(values,volumes,capacity)
    dist, prev = dijkstra(G)
    best_path = get_path(G,prev)
    items = get_items(best_path)
    print(best_path)
    print(items)
