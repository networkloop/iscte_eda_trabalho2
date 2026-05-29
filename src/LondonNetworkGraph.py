from src.Graph import Vertex, Edge, Graph
import csv
import networkx as nx
import folium
import webbrowser

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

def search_station(station_id, stations=None):
    if stations is None:
        stations = LondonNetworkGraph.stations()
    stations = sorted(stations, key=lambda s: int(s[0]))
    upper_limit = len(stations) - 1
    lower_limit = 0

    while lower_limit <= upper_limit:
        pointer = (upper_limit + lower_limit) // 2
        if int(stations[pointer][0]) == int(station_id):
            return stations[pointer]
        elif int(stations[pointer][0]) > int(station_id):
            upper_limit = pointer - 1
        else:
            lower_limit = pointer + 1

    return None

def line_color(connection, lines="include/lines.csv"):
    lines_information = []
    with open(lines, newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row:
                lines_information.append(row)
    lines_information = sorted(lines_information, key=lambda s: int(s[0]))
    upper_limit = len(lines_information) - 1
    lower_limit = 0

    while lower_limit <= upper_limit:
        pointer = (upper_limit + lower_limit) // 2
        if int(lines_information[pointer][0]) == int(connection[2]):
            return lines_information[pointer][2]
        elif int(lines_information[pointer][0]) > int(connection[2]):
            upper_limit = pointer - 1
        else:
            lower_limit = pointer + 1

    return None

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

    def visualize(self):
        map = folium.Map(location=[51.5074, -0.1278], zoom_start=12, tiles="CartoDB positron")
        for station in self.stations():
            folium.CircleMarker(
                location=[station[1], station[2]],
                radius=5,
                color="red",
                fill=True,
                fill_color="white",
                fill_opacity=1,
                popup = station[3],
                tooltip=station[3],
            ).add_to(map)

        for connection in self.connections():
            station_one = search_station(connection[0], self.stations())
            station_two = search_station(connection[1], self.stations())
            folium.PolyLine(
                locations=[[float(station_one[1]), float(station_one[2])],
                           [float(station_two[1]), float(station_two[2])]],
                color= '#' + line_color(connection),
                weight=3
            ).add_to(map)

        map.save("map.html")
        webbrowser.open("map.html")
        return map