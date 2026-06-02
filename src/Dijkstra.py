from .LondonNetworkGraph import uniform_weight, distance_weight, time_weight, line_color
import csv
import folium
import webbrowser 

def dijkstra(graph, start_station, end_station, weight_function, penalty_factor=0):
    stations = {}
    for row in graph.stations():
        stations[row[0]] = row

    best_value = {}
    best_previous_station = {}
    best_line = {}
    unvisited_stations = {}

    for station in graph._iter_vertex():
        best_value[station] = float('inf')
        best_previous_station[station] = None
        best_line[station] = None
        unvisited_stations[station] = True
    best_value[start_station] = 0

    while unvisited_stations:
        current_station = min(unvisited_stations, key=lambda s: best_value[s])
        if best_value[current_station] == float('inf') or current_station == end_station:
            break
        del unvisited_stations[current_station]

        for line in graph._graph[current_station]:
            adjacent_station = line.opposite(current_station)

            if adjacent_station in unvisited_stations:
                edge_line = line.get_info()
                station_one_info = stations[current_station]
                station_two_info = stations[adjacent_station]
                base_cost = weight_function(station_one_info, station_two_info, edge_line)
                arrival_line = best_line[current_station]
                line_change_penalty = 0
                if arrival_line is not None and arrival_line != edge_line:
                    line_change_penalty = penalty_factor
                new_distance = best_value[current_station] + base_cost + line_change_penalty
                if new_distance < best_value[adjacent_station]:
                    best_value[adjacent_station] = new_distance
                    best_previous_station[adjacent_station] = current_station
                    best_line[adjacent_station] = edge_line
    path = []
    current_station = end_station
    line_changes = 0
    last_line = None

    if best_value[current_station] != float('inf'):
        while current_station is not None:
            path.append(current_station)
            edge_line = best_line[current_station]
            if last_line is not None and edge_line is not None and edge_line != last_line:
                line_changes += 1
            if edge_line is not None:
                last_line = edge_line

            current_station = best_previous_station[current_station]
        path.reverse()
    return path, best_value[end_station], line_changes

def visualize(path,
                stations_path='include/stations.csv',
                connections_path='include/connections.csv',
                output_path='map_dijkstra.html',
                color = "#9f5ddd" ):
    stations = {}
    with open(stations_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row:
                stations[row[0]] = row

    if not path:
        print("No path found.")
        return None
    
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

    for i in range(len(path) - 1):
        station_one_id = path[i]
        station_two_id = path[i + 1]
        station_one = stations[station_one_id]
        station_two = stations[station_two_id]
        
        current_color = '#000000'
        for connection in all_connections:
            if (connection[0] == station_one_id and connection[1] == station_two_id) or (connection[0] == station_two_id and connection[1] == station_one_id):
                color_hex = line_color(connection)
                if color_hex:
                    current_color = '#' + color_hex
                break
        folium.PolyLine(
            locations=[[float(station_one[1]), float(station_one[2])],
                       [float(station_two[1]), float(station_two[2])]],
            color=current_color,
            weight=3.5,
        ).add_to(m)

    for station_id in stations:
        station = stations[station_id]
        lat, lon, name = float(station[1]), float(station[2]), station[3]
        if station_id == path[0]:
            folium.Marker(
                location=[lat, lon],
                icon=folium.Icon(color='green', icon='play'),
                tooltip=f"Start: {name}",
                popup=f"<b>ORIGIN:</b> {name}"
            ).add_to(m)
        elif station_id == path[-1]:
            folium.Marker(
                location=[lat, lon],
                icon=folium.Icon(color='red', icon='stop'),
                tooltip=f"End: {name}",
                popup=f"<b>DESTINATION:</b> {name}"
            ).add_to(m)
        elif station_id in path:
            folium.CircleMarker(
                location=[lat, lon],
                radius=4,
                color='#000000',
                fill=True,
                fill_color='white',
                fill_opacity=1,
                tooltip=name,
                popup=f"<b>STATION:</b> {name}"
            ).add_to(m)
        else:    
            folium.CircleMarker(
                location=[lat, lon],
                radius=2.5,
                color='#888888',
                fill=True,
                fill_color='white',
                fill_opacity=1,
                tooltip=name
            ).add_to(m)

    m.save(output_path)
    webbrowser.open(output_path)
    return m