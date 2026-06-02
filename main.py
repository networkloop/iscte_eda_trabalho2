from src.LondonNetworkGraph import LondonNetworkGraph
from src.Kruskal import kruskal, visualize_mst
from src.LondonNetworkGraph import uniform_weight, distance_weight, time_weight

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

    visualize_mst(graph_kruskal_uniform['kruskal_connections'], output_path='map_kruskal_uniform.html')
    visualize_mst(graph_kruskal_distance['kruskal_connections'], output_path='map_kruskal_distance.html', color='#1a6e3c')
    visualize_mst(graph_kruskal_time['kruskal_connections'], output_path='map_kruskal_time.html', color='#4B0082')