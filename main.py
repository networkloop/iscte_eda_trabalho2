from src.LondonNetworkGraph import LondonNetworkGraph
from src.Kruskal import kruskal, visualize_mst
from src.LondonNetworkGraph import uniform_weight, distance_weight, time_weight
from src.Dijkstra import dijkstra, visualize

if __name__ == "__main__":
    graph = LondonNetworkGraph()

    print("=== Estatísticas da Rede ===")
    print(f"Número de estações: {graph.n_stations()}")
    print(f"Número de ligações: {graph.n_edges()}")
    print(f"Grau médio: {graph.mean_degree():.4f}")
    print(f"Peso médio (Uniforme): {graph.mean_weight(uniform_weight):.4f}")
    print(f"Peso médio (Haversine): {graph.mean_weight(distance_weight):.4f}")
    print("Ligações por linha:")
    for line, count in graph.n_edges_line().items():
        print(f"  Linha {line}: {count}")
    graph.visualize()

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
    print(f"Custo total da rede: {graph_kruskal_distance['total_original_cost']:.4f}")
    print(f"Custo total da MST: {graph_kruskal_distance['total_cost']:.4f}")

    print("\n=== Kruskal Time ===")
    print(f"Arestas na rede original: {graph_kruskal_time['n_original_connections']}")
    print(f"Arestas na MST: {graph_kruskal_time['n_kruskal_connections']}")
    print(f"Custo total da rede: {graph_kruskal_time['total_original_cost']:.4f}")
    print(f"Custo total da MST: {graph_kruskal_time['total_cost']:.4f}")

    visualize_mst(graph_kruskal_uniform['mst_connections'], output_path='map_kruskal_uniform.html')
    visualize_mst(graph_kruskal_distance['mst_connections'], output_path='map_kruskal_distance.html', color='#1a6e3c')
    visualize_mst(graph_kruskal_time['mst_connections'], output_path='map_kruskal_time.html', color='#4B0082')

    print("\n=== Cenários Dijkstra ===")
    cenarios = [
        {"nome": "Trajeto Curto", "origem": "1", "destino": "73"},
        {"nome": "Trajeto Longo", "origem": "271", "destino": "267"},
        {"nome": "Transbordos", "origem": "11", "destino": "273"}
    ]
    testes = [
        {"nome": "Custo Uniforme", "weight_function": uniform_weight, "penalty_factor": 0},
        {"nome": "Distância (Sem Penalização)", "weight_function": distance_weight, "penalty_factor": 0},
        {"nome": "Distância (Com Penalização)", "weight_function": distance_weight, "penalty_factor": 5}
    ]
    penalty_factor = 5
    for cenario in cenarios:
        print(f"\n--------------------------------------------------")
        print(f"CENÁRIO: {cenario['nome']} ({cenario['origem']} -> {cenario['destino']})")
        print(f"--------------------------------------------------")

        file_name = cenario['nome'].lower().replace(' ', '_')

        for teste in testes:
            path, custo, mudancas = dijkstra(graph, cenario['origem'], cenario['destino'], teste['weight_function'], penalty_factor=teste['penalty_factor'])
            print(f"[{teste['nome']:<12}] Estações: {len(path):<3} | Custo: {custo:<8.2f} | Mudanças: {mudancas}")
            nome_ficheiro = f"mapa_dijkstra_{file_name}_{teste['nome'].lower()}.html"
            visualize(path, output_path=nome_ficheiro)

        

    visualize_mst(graph_kruskal_uniform['kruskal_connections'], output_path='map_kruskal_uniform.html')
    visualize_mst(graph_kruskal_distance['kruskal_connections'], output_path='map_kruskal_distance.html', color='#1a6e3c')
    visualize_mst(graph_kruskal_time['kruskal_connections'], output_path='map_kruskal_time.html', color='#4B0082')