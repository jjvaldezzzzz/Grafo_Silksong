# Grafo_Silksong
Mapa de 'Hollow Knight: Silksong' modelado em Grafos. Algoritmo de dijkstra aplicado para encontrar o menor caminho de uma área para outra
--- 
## Contexto
- Jogador que já completou o jogo (ou seja, tem tudo desbloqueado) e quer se aventurar nas terras de fiarlongo sem utilizar nenhum fast-travel
---
# Modelagem
- Escolhemos um banco (local onde o você salva o progresso do jogo) principal de cada área do mapa para representá-los como vértices no nosso modelo
- A partir disso colocamos o mapa em um grid e traçamos as arestas entre bancos que possuem conexão direta
- O peso foi calculado com base na distância entre os vértices passando por áreas passáveis do mapa(considerando o jogador que tem tudo desbloqueado)


---

## 🚀 Funcionalidades

- Estrutura de grafo usando **lista de adjacência** (vértices representados por `str`).
- Adição de vértices e arestas (incluindo arestas nos dois sentidos).
- Impressão da **matriz de adjacência** com formatação ajustável.
- Implementação do algoritmo de **Dijkstra**:
  - Retorna distância mínima de um vértice origem para todos os outros.
  - Ou retorna o custo e caminho completo até um vértice destino específico.
- Tratamento de casos de aresta inexistente (`math.inf`).

