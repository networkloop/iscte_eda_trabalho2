import csv
import folium
import webbrowser
from .LondonNetworkGraph import uniform_weight, distance_weight, time_weight

class UnionFind:
    def __init__(self, elements):
        self._parent = {}
        for element in elements:
            self._parent[element] = element

    def find_root(self, node):
        while self._parent[node] != node:
            node = self._parent[node]
        return node

    def union(self, node_x, node_y):
        root_x = self.find_root(node_x)
        root_y = self.find_root(node_y)

        if root_x == root_y:
            return False

        self._parent[root_x] = root_y
        return True

def kruskal(stations_path='include/stations.csv',
            connections_path='include/connections.csv',
            weight_function=uniform_weight):

    stations = {}
    with open(stations_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row:
                stations[row[0]] = row

    weighted_connections = []
    total_original_cost = 0
    with open(connections_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row:
                id_one = row[0]
                id_two = row[1]
                line = row[2]
                station_one = stations[id_one]
                station_two = stations[id_two]
                weight = weight_function(station_one, station_two, line)
                weighted_connections.append((id_one, id_two, line, weight))
                total_original_cost += weight

    weighted_connections.sort(key=lambda e: e[3])
    union_find = UnionFind(stations.keys())
    kruskal_connections = []
    total_cost = 0
    n_stations = len(stations)

    for id_one, id_two, line, weight in weighted_connections:
        if union_find.union(id_one, id_two):
            kruskal_connections.append((id_one, id_two, line, weight))
            total_cost += weight
            if len(kruskal_connections) == n_stations - 1:
                break

    return {
        'kruskal_connections': kruskal_connections,
        'total_cost': total_cost,
        'n_kruskal_connections': len(kruskal_connections),
        'n_original_connections': len(weighted_connections),
        'total_original_cost': total_original_cost,
    }

def visualize_mst(mst_connections,
                  stations_path='include/stations.csv',
                  connections_path='include/connections.csv',
                  output_path='map_kruskal.html',
                  color = '#1a3a8f' ):

    stations = {}
    with open(stations_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row:
                stations[row[0]] = row

    all_connections = []
    with open(connections_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row:
                all_connections.append(row)

    m = folium.Map(location=[51.5074, -0.1278], zoom_start=12, tiles='CartoDB positron')

    for connection in all_connections:
        station_one = stations[connection[0]]
        station_two = stations[connection[1]]
        folium.PolyLine(
            locations=[[float(station_one[1]), float(station_one[2])],
                       [float(station_two[1]), float(station_two[2])]],
            color='#555555',
            weight=2.5,
            opacity=0.8
        ).add_to(m)

    for id_one, id_two, line, weight in mst_connections:
        station_one = stations[id_one]
        station_two = stations[id_two]
        folium.PolyLine(
            locations=[[float(station_one[1]), float(station_one[2])],
                       [float(station_two[1]), float(station_two[2])]],
            color= color,
            weight=3.5
        ).add_to(m)

    for station_id in stations:
        station = stations[station_id]
        folium.CircleMarker(
            location=[float(station[1]), float(station[2])],
            radius=4,
            color='#333333',
            fill=True,
            fill_color='white',
            fill_opacity=1,
            tooltip=station[3],
            popup=station[3],
        ).add_to(m)

    m.save(output_path)
    webbrowser.open(output_path)
    return m
