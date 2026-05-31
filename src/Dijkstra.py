import LondonNetworkGraph as lng

def dijkstra(graph, start_vertex):
    unvisited_vertices = {vertex: float('inf') for vertex in graph.vertices}
    unvisited_vertices[start_vertex] = 0
    visited_vertices = {}
    previous_vertices = {}

    while unvisited_vertices:
        current_vertex = min(unvisited_vertices, key=lambda vertex: unvisited_vertices[vertex])
        current_distance = unvisited_vertices[current_vertex]

        for edge in graph.edges:
            if edge.vertex1 == current_vertex:
                neighbor = edge.vertex2
            elif edge.vertex2 == current_vertex:
                neighbor = edge.vertex1
            else:
                continue

            if neighbor in visited_vertices:
                continue

            new_distance = current_distance + edge.weight
            if new_distance < unvisited_vertices[neighbor]:
                unvisited_vertices[neighbor] = new_distance
                previous_vertices[neighbor] = current_vertex

        visited_vertices[current_vertex] = current_distance
        del unvisited_vertices[current_vertex]

    return visited_vertices, previous_vertices