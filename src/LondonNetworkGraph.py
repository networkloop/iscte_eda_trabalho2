from Graph import Vertex, Edge, Graph
import csv
import haversine as hs
import matplotlib.pyplot as plt
import networkx as nx
    
class Station(Vertex):

    def __init__(self, station, position):
        super().__init__(station, position)

    def get_station(self):
        return self.get_key()

class EdgeLine(Edge):
    def __init__(self, start_station, end_station, line):
        super().__init__(start_station, end_station, line)

    def get_stations(self):
        return self.get_vs()

    def get_line(self):
        return self.get_info()

    def other_station(self):
        return self.get_vs()
    
def distance_weight(p1, p2):
    return hs.haversine(p1, p2, unit=hs.Unit.KILOMETERS)

def time_weight(p1, p2, speed = 30, sinuous_factor = 1.2):
    distance = distance_weight(p1, p2)
    average_speed = speed
    return distance / average_speed * sinuous_factor


class LondonNetworkGraph(Graph):
    def __init__(self):
        super().__init__()

    def stations(self, file_path = "include/stations.csv"):
        stations_informations = []
        with open(file_path, newline='', encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if row:
                    stations_informations.append(row)
        return stations_informations

    def connections(self, file_path = "include/connections.csv"):
        connections_informations = []
        with open(file_path, newline='', encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if row:
                    connections_informations.append(row)
        return connections_informations

    def n_stations(self):
        return len(self.stations())

    def n_edges(self):
        return len(self.connections())

    def n_edges_line(self):
        connections_line = {}
        for row in self.connections():
            if row[2] in connections_line:
                connections_line[row[2]] += 1
            else:
                connections_line[row[2]] = 1

        return connections_line

    def mean_degree(self):
        return (self.n_edges()/self.n_stations())
    
    def mean_weight(self, weight_type):
        stations = self.stations()
        distance = 0
        total_weight = 0
        for row in stations:
            if row in stations:
                p1, p2 = float(row[1]), float(row[2])
                if weight_type == "distance":
                    distance = distance_weight(p1, p2)
                elif weight_type == "time":
                    distance = time_weight(p1, p2)
                total_weight += distance
        avg_weight = total_weight / self.n_edges()
        return avg_weight
    
    def visualize(self, metro):
        graph = nx.Graph()
        for stations in metro.stations():
            graph.add_node(stations[0:3])
            for connections in metro.connections():
                graph.add_edge(*connections, line=connections[2])
        nx.draw(graph, with_labels=True)
        plt.title("London Metro Network")
        plt.show()

metro = LondonNetworkGraph()
metro.visualize(metro)