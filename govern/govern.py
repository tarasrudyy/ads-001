def main():
    input_file = "govern.in"
    output_file = "govern.out"

    graph = read_file(input_file)

    order = get_topological_order(graph)

    write_file(output_file, "\n".join(order))


def read_file(filename):
    vertices = list()
    edges = list()
    documents = dict()

    with open(filename, 'r') as f:
        for line in f:
            docs = line.split()
            first_doc = docs[0]
            for doc in docs:
                # add vertices
                if doc not in documents:
                    vertex = Vertex(doc)
                    vertices.append(vertex)
                    documents[doc] = vertex
                # add edges
                if doc != first_doc:
                    edge = Edge(documents[first_doc], documents[doc])
                    documents[first_doc].outbound_edges.append(edge)
                    edges.append(edge)

    return Graph(vertices, edges)

def write_file(filename, value):
    with open(filename, 'w') as f:
        f.write(value)

def get_topological_order(graph):
    # Find all vertices that don't have inbound edges, then run
    # the (almost) usual DFS with those vertices initially in the stack.
    return dfs(graph, get_vertices_without_inbound_edges(graph))


def get_vertices_without_inbound_edges(graph):
    have_inbounds = {vertex: False for vertex in graph.vertices}
    for edge in graph.edges:
        have_inbounds[edge.end_vertex] = True
    return [vertex for vertex in have_inbounds.keys() if not have_inbounds[vertex]]


def dfs(graph, start_vertices):
    result = []

    stack = []
    stack.extend(start_vertices)
    visited = {vertex: False for vertex in graph.vertices}

    while len(stack) > 0:
        # Read the last vertex from the stack, but don't remove it.
        current_vertex = stack[-1]

        visited[current_vertex] = True
        neighbors = [edge.end_vertex
                     for edge in current_vertex.outbound_edges
                     if not visited[edge.end_vertex]]

        # If all neighbors have already been discovered (or don't exist at all),
        # push the current vertex to the results of the topological sorting.
        if len(neighbors) == 0:
            result.append(current_vertex.label)
            stack.pop()

        stack.extend(neighbors)

    return result


class Vertex:
    def __init__(self, label):
        self.label = label
        self.outbound_edges = []

    def __str__(self):
        return "Label: %s    Edges: %s" % (self.label, ', '.join([str(edge) for edge in self.outbound_edges]))


class Edge:
    def __init__(self, start_vertex, end_vertex):
        self.start_vertex = start_vertex
        self.end_vertex = end_vertex

    def __str__(self):
        return "%s -> %s" % (self.start_vertex.label, self.end_vertex.label)


class Graph:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges


if __name__ == "__main__":
    main()