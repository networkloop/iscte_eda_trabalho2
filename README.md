# Metro de Londres - Algoritmos de procura
v1.0

Este trabalho tem como objetivo representar, analisar e visualizar a rede do metro de Londres
utilizando grafos. Pretende-se que os estudantes desenvolvam uma solução em Python que
permita modelar a rede, calcular caminhos entre estações e analisar o impacto de diferentes
estratégias de modelação.´

O projeto está estruturado da seguinte forma:

```bash
.
├── main.py
├── README.md
├── requirements.txt
├── include
│   ├── connections.csv
│   ├── lines.csv
│   ├── speeds.csv
│   └── stations.csv
└── src
    ├── Dijkstra.py
    ├── Graph.py
    ├── Kruskal.py
    └── LondonNetworkGraph.py
```

Indicações de desenvolvimento
Antes de começar a desenvolver no projeto, devem ser instaladas as dependências listadas no arquivo requirements.txt (que deve incluir bibliotecas cruciais como networkx e folium) utilizando o seguinte comando no terminal:

```bash
pip install -r requirements.txt
```

Após o desenvolvimento das soluções (Algoritmo de Dijkstra e Algoritmo de Kruskal), é necessário executar o script principal para verificar as estatísticas na consola, validar os custos com a biblioteca NetworkX e gerar as visualizações dos mapas. No diretório do projeto, basta executar o seguinte comando no Command Prompt:

```bash
python main.py
```

Nota: A execução com sucesso do programa irá gerar ficheiros .html (ex: map_dijkstra.html e map_kruskal_time.html) na diretoria principal, que abrem automaticamente no navegador mostrando as rotas calculadas sobre o mapa real de Londres.
