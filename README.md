# Grafo_Silksong
Modelagem do mapa de *Hollow Knight: Silksong* usando Grafos e algoritmos clássicos de caminhamento.

---

## Contexto
Projeto voltado para jogadores que já possuem acesso total ao mapa e desejam explorar rotas sem utilizar o fast-travel do jogo, analisando caminhos e conexões entre áreas usando algoritmos de grafos.

---

## Modelagem
- Cada área do mapa é um **vértice**.
- Conexões diretas entre áreas viram **arestas**, podendo ser unidirecionais ou bidirecionais.
- Pesos representam distâncias aproximadas no mapa.
- Matriz de adjacência usada como estrutura base.

---

## Aviso
O código contém **spoilers** dos nomes das áreas do jogo.

---

## 🚀 Funcionalidades

### Algoritmos Implementados
- **Dijkstra** (detecta pesos negativos e interrompe)
- **Bellman-Ford** (suporta pesos negativos)
- **BFS** – menor número de passos
- **DFS** – exploração profunda

### Operações do Grafo
- Adição automática de vértices
- Arestas simples e duplas
- Impressão de caminhos e distâncias

---

## ▶️ Como Executar

1. Baixe o projeto:
```bash
git clone https://github.com/jjvaldezzzzz/Grafo_Silksong.git
cd Grafo_Silksong
```
2. Execute o arquivo principal:
```bash
python3 grafo_silksong.py
```
