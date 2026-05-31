from src.LondonNetworkGraph import LondonNetworkGraph
from src.Kruskal import kruskal, visualize_mst
from src.LondonNetworkGraph import cost_uniform, cost_haversine

if __name__ == "__main__":
    graph = LondonNetworkGraph()

    print("=== Estatísticas da Rede ===")
    print(f"Número de estações: {graph.n_stations()}")
    print(f"Número de ligações: {graph.n_edges()}")
    print(f"Grau médio: {graph.mean_degree():.4f}")
    print(f"Peso médio (Uniforme): {graph.mean_weight(cost_uniform):.4f}")
    print(f"Peso médio (Haversine): {graph.mean_weight(cost_haversine):.4f}")
    print("Ligações por linha:")
    for line, count in graph.n_edges_line().items():
        print(f"  Linha {line}: {count}")
    graph.visualize()

    graph_kruskal_uniform = kruskal(cost_function=cost_uniform)
    graph_kruskal_haversine = kruskal(cost_function=cost_haversine)

    print("\n=== Kruskal Custo Uniforme ===")
    print(f"Arestas na rede original: {graph_kruskal_uniform['n_original_connections']}")
    print(f"Arestas na MST: {graph_kruskal_uniform['n_mst_connections']}")
    print(f"Custo total da rede: {graph_kruskal_uniform['total_original_cost']}")
    print(f"Custo total da MST: {graph_kruskal_uniform['total_cost']}")

    print("\n=== Kruskal Haversine ===")
    print(f"Arestas na rede original: {graph_kruskal_haversine['n_original_connections']}")
    print(f"Arestas na MST: {graph_kruskal_haversine['n_mst_connections']}")
    print(f"Custo total da rede: {graph_kruskal_haversine['total_original_cost']:.4f}")
    print(f"Custo total da MST: {graph_kruskal_haversine['total_cost']:.4f}")

    visualize_mst(graph_kruskal_uniform['mst_connections'], output_path='map_kruskal_uniform.html')
    visualize_mst(graph_kruskal_haversine['mst_connections'], output_path='map_kruskal_haversine.html', color='#1a6e3c')