from src.LondonNetworkGraph import LondonNetworkGraph, uniform_weight, distance_weight, time_weight
from src.Dijkstra import dijkstra, dijkstra_nx, visualize
from src.Kruskal import kruskal, visualize_mst

if __name__ == "__main__":
    graph = LondonNetworkGraph()

    print("=== Estatísticas da Rede ===")
    print(f"Número de estações: {graph.n_stations()}")
    print(f"Número de ligações: {graph.n_edges()}")
    print(f"Grau médio: {graph.mean_degree():.4f}")
    print(f"Peso médio (Uniforme): {graph.mean_weight(uniform_weight):.4f}")
    print(f"Peso médio (Distância): {graph.mean_weight(distance_weight):.4f} km")
    print(f"Peso médio (Tempo): {graph.mean_weight(time_weight):.4f} h")
    print("Ligações por linha:")
    for line, count in graph.n_edges_line().items():
        print(f"  Linha {line}: {count}")

    graph.visualize()

    print("\n=== Cenários Dijkstra ===")
    cenarios = [
        {"nome": "Trajeto Curto", "origem": "74", "destino": "247"},
        {"nome": "Trajeto Longo", "origem": "271", "destino": "267"}
    ]
    testes = [
        {"nome": "Custo Uniforme", "weight_function": uniform_weight, "penalty_factor": 0},
        {"nome": "Distância (Sem Penalização)", "weight_function": distance_weight, "penalty_factor": 0},
        {"nome": "Distância (Com Penalização)", "weight_function": distance_weight, "penalty_factor": 5},
        {"nome": "Tempo (Sem Penalização)", "weight_function": time_weight, "penalty_factor": 0},
        {"nome": "Tempo (Com Penalização)", "weight_function": time_weight, "penalty_factor": 5}
    ]
    station_data = {}
    for row in graph.stations():
        station_data[row[0]] = row

    penalty_factor = 5
    for cenario in cenarios:
        print(f"\n--------------------------------------------------")
        print(f"CENÁRIO: {cenario['nome']} ({cenario['origem']} -> {cenario['destino']})")
        print(f"--------------------------------------------------")

        file_name = cenario['nome'].lower().replace(' ', '_')
        custo_para_validar = 0

        for teste in testes:
            path, custo, mudancas = dijkstra(graph, cenario['origem'], cenario['destino'], teste['weight_function'], penalty_factor=teste['penalty_factor'])
            distancia_real = 0
            tempo_real = 0
            if path:
                for i in range(len(path)-1):
                    station_one_id = path[i]
                    station_two_id = path[i+1]
                    station_one = station_data[station_one_id]
                    station_two = station_data[station_two_id]
                    current_line = None
                    for line in graph._graph[station_one_id]:
                        if line.opposite(station_one_id) == station_two_id:
                            current_line = line.get_info()
                            break
                    distancia_real += distance_weight(station_one, station_two, current_line) 
                    tempo_real += time_weight(station_one, station_two, current_line) 
            if teste['nome'] == "Distância (Sem Penalização)":
                custo_para_validar = custo
            print(f"=== {teste['nome']} ===")
            print(f"Estações      : {len(path)}")
            print(f"Transbordos   : {mudancas}")
            print(f"Custo na rede : {custo:.4f} (com penalizações aplicadas)")
            print(f"Estatísticas  : {distancia_real:.4f} km | {tempo_real:.4f} h\n")
            nome_ficheiro = f"mapa_dijkstra_{file_name}_{teste['nome'].lower()}.html"
            visualize(path, output_path=nome_ficheiro)
            

        print("\n=== Comparação com NetworkX (Distância Sem Penalização) ===")
        path_nx, custo_nx = dijkstra_nx(graph, cenario['origem'], cenario['destino'], distance_weight)
        
        print(f"[NetworkX Nativo]   Estações: {len(path_nx):<3} | Custo: {custo_nx:<8.4f}")
        if round(custo_nx, 4) == round(custo_para_validar, 4):
            print(">> O resultado do Dijkstra implementado é consistente com o NetworkX.")

    graph_kruskal_uniform = kruskal(weight_function=uniform_weight)
    graph_kruskal_distance = kruskal(weight_function=distance_weight)
    graph_kruskal_time = kruskal(weight_function=time_weight)

    print("\n=== Kruskal Custo Uniforme ===")
    print(f"Arestas na rede original: {graph_kruskal_uniform['n_original_connections']}")
    print(f"Arestas na MST: {graph_kruskal_uniform['n_kruskal_connections']}")
    print(f"Custo total da rede: {graph_kruskal_uniform['total_original_cost']}")
    print(f"Custo total da MST: {graph_kruskal_uniform['total_cost']}")

    print("\n=== Kruskal Distance ===")
    print(f"Arestas na rede original: {graph_kruskal_distance['n_original_connections']}")
    print(f"Arestas na MST: {graph_kruskal_distance['n_kruskal_connections']}")
    print(f"Custo total da rede: {graph_kruskal_distance['total_original_cost']:.4f} km")
    print(f"Custo total da MST: {graph_kruskal_distance['total_cost']:.4f} km")

    print("\n=== Kruskal Time ===")
    print(f"Arestas na rede original: {graph_kruskal_time['n_original_connections']}")
    print(f"Arestas na MST: {graph_kruskal_time['n_kruskal_connections']}")
    print(f"Custo total da rede: {graph_kruskal_time['total_original_cost']:.4f} h")
    print(f"Custo total da MST: {graph_kruskal_time['total_cost']:.4f} h")

    visualize_mst(graph_kruskal_uniform['kruskal_connections'], output_path='map_kruskal_uniform.html')
    visualize_mst(graph_kruskal_distance['kruskal_connections'], output_path='map_kruskal_distance.html', color='#1a6e3c')
    visualize_mst(graph_kruskal_time['kruskal_connections'], output_path='map_kruskal_time.html', color='#4B0082')

