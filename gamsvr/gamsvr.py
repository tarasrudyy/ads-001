import sys

def main():
    input_file = "gamsvr.in" if len(sys.argv) == 1 else sys.argv[1]
    output_file = "gamsvr.out" if len(sys.argv) == 1 else sys.argv[2]

    # read data
    lines = read_file(input_file)

    # init graph
    graph = init_graph(lines)

    N = lines[1][0]

    clients = lines[2]
    routers = list(set(_ for _ in range(1, N + 1)) - set(clients))

    less_clients = len(clients) < len(routers)
    if not less_clients:
        clients = routers
        routers = lines[2]

    min_max = [0] * N
    result = sys.maxint

    for client in clients:
        distances, shortest_path_predecessor = dijkstra(graph, graph.vertices[client - 1])

        if less_clients:
            for i in routers:
                # find maximum distance among distances from client to router
                if min_max[i - 1] < distances[i - 1]:
                    min_max[i - 1] = distances[i - 1]
        else:
            max_distance_to_client = max(distances)
            if result > max_distance_to_client:
                result = max_distance_to_client

    if less_clients:
        # find minimum among maximum distances
        for i in routers:
            if result > min_max[i - 1]:
                result = min_max[i - 1]

    # write data
    write_file(output_file, result)


def read_file(input_file):
    lines = []
    lines.append(input_file)
    with open(input_file) as f:
        for line in f:
            if ' ' in line:
                lines.append(map(int, line.split(' ')))
            else:
                lines.append(int(line))
    return lines

def write_file(output_file, value):
    with open(output_file, 'w') as f:
        f.write(str(value))


def init_graph(lines):
    vertex_count = lines[1][0]
    edge_count = lines[1][1]

    vertices = [Vertex(index) for index in range(0, vertex_count)]
    edges = []

    for i in range(3, edge_count + 3):
        # Adding the edge to the list of outbound edges for the start vertex.
        edge_params = lines[i]
        start_vertex_index = edge_params[0] - 1
        end_vertex_index = edge_params[1] - 1
        weight = edge_params[2]

        edge = Edge(vertices[start_vertex_index], vertices[end_vertex_index], weight)
        vertices[start_vertex_index].outbound_edges.append(edge)

        # For non-directed graphs, an outbound edge is also an inbound one (0 -> 1 == 1 -> 0).
        # Therefore, we reverse the edge and add it to the other vertex.
        reverse_edge = Edge(vertices[end_vertex_index], vertices[start_vertex_index], weight)
        vertices[end_vertex_index].outbound_edges.append(reverse_edge)

        edges.append(edge)
        edges.append(reverse_edge)

    return Graph(vertices, edges)

def dijkstra(graph, start_vertex):
    # Initialization: setting all known shortest distances to infinity,
    # and the start vertex will have the shortest distance to itself equal to 0.
    INFINITY = sys.maxint
    distances = [INFINITY for _ in graph.vertices]
    shortest_path_predecessor = [None for _ in graph.vertices]
    distances[start_vertex.label] = 0

    # Visiting every vertex in the graph...
    visit_list = [vertex for vertex in graph.vertices]

    while len(visit_list) > 0:
        # ...but selecting the vertex with the shortest known distance every time.
        #
        # We can avoid doing the linear-time lookup every time by using a Fibonacci Heap instead,
        # thus reducing the complexity to O(E log V).
        shortest_distance_vertex = visit_list[0]
        shortest_distance_index = 0

        for (index, vertex) in enumerate(visit_list):
            if distances[vertex.label] < distances[shortest_distance_index]:
                shortest_distance_vertex = vertex
                shortest_distance_index = index

        visit_list.pop(shortest_distance_index)

        # For each adjacent vertex v, check if the path from the current vertex would be more efficient
        # than the one we've known before. I.e., if distance[current] + weight(current->v) < distance[v].
        for edge in shortest_distance_vertex.outbound_edges:
            alternative_distance = distances[shortest_distance_vertex.label] + edge.weight
            if alternative_distance < distances[edge.end_vertex.label]:
                # If we have indeed found a better path, remembering the new distance and predecessor.
                distances[edge.end_vertex.label] = alternative_distance
                shortest_path_predecessor[edge.end_vertex.label] = shortest_distance_vertex.label

    # We can avoid the shortest_path_predecessor array completely, but we'll return it in case there's
    # a need to output the actual PATH instead of just the shortest distances.
    return distances, shortest_path_predecessor

class Vertex:
    def __init__(self, label):
        self.label = label
        self.outbound_edges = []

    def __str__(self):
        return "Label: %d    Edges: %s" % (self.label, ', '.join([str(edge) for edge in self.outbound_edges]))


class Edge:
    def __init__(self, start_vertex, end_vertex, weight):
        self.start_vertex = start_vertex
        self.end_vertex = end_vertex
        self.weight = weight

    def __str__(self):
        return "%d ---%d---> %d" % (self.start_vertex.label, self.weight, self.end_vertex.label)


class Graph:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges

if __name__ == "__main__":
    main()
