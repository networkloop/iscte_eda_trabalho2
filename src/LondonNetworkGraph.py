from src.Graph import Vertex, Edge, Graph
import csv
import networkx as nx
import folium
import webbrowser
import math

def cost_uniform(station_one, station_two, line=None):
    return 1

def cost_haversine(station_one, station_two, line=None):

    lat1, lon1 = math.radians(float(station_one[1])), math.radians(float(station_one[2]))
    lat2, lon2 = math.radians(float(station_two[1])), math.radians(float(station_two[2]))

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    angle = 2 * math.asin(math.sqrt(a))

    R = 6371
    return R * angle

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
    with open(lines, newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row and int(row[0]) == int(connection[2]):
                return row[2]
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
        return self.n_edges()/self.n_stations()

    def mean_weight(self, weight_type):
        stations_sorted = sorted(self.stations(), key=lambda s: int(s[0]))
        total_weight = 0
        for connection in self.connections():
            station_one = search_station(connection[0], stations_sorted)
            station_two = search_station(connection[1], stations_sorted)
            total_weight += weight_type(station_one, station_two,)
        return total_weight/self.n_edges()

    def visualize(self):
        m = folium.Map(location=[51.5074, -0.1278], zoom_start=12, tiles="CartoDB positron")
        stations_sorted = sorted(self.stations(), key=lambda s: int(s[0]))

        for connection in self.connections():
            station_one = search_station(connection[0], stations_sorted)
            station_two = search_station(connection[1], stations_sorted)
            folium.PolyLine(
                locations=[[float(station_one[1]), float(station_one[2])],
                           [float(station_two[1]), float(station_two[2])]],
                color= '#' + line_color(connection),
                weight=3
            ).add_to(m)

        for station in stations_sorted:
            folium.CircleMarker(
                location=[station[1], station[2]],
                radius=4,
                color="red",
                fill=True,
                fill_color="white",
                fill_opacity=1,
                popup = station[3],
                tooltip=station[3],
            ).add_to(m)

        m.save("map.html")
        webbrowser.open("map.html")
        return m