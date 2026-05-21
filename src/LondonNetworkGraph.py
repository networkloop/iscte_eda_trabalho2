from Graph import Vertex, Edge, Graph
import csv

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