import math
from typing import Dict, List, Optional, Iterable, Tuple
from collections import deque


class Grafo:
    def __init__(self, nomes: Optional[Iterable[str]] = None,
                 quantidade: Optional[int] = None, prefixo: str = "v"):
        self._idx: Dict[str, int] = {}
        self._nomes: List[str] = []
        self._mat: List[List[float]] = []

        if nomes is not None:
            for nome in nomes:
                self.adicionar_vertice(str(nome))
        elif quantidade is not None:
            for i in range(int(quantidade)):
                self.adicionar_vertice(f"{prefixo}{i}")

    def vertices(self) -> List[str]:
        return list(self._nomes)

    def adicionar_vertice(self, nome: str) -> None:
        if nome in self._idx:
            return
        i = len(self._nomes)
        self._idx[nome] = i
        self._nomes.append(nome)

        for linha in self._mat:
            linha.append(math.inf)

        nova = [math.inf] * (i + 1)
        nova[i] = 0.0
        self._mat.append(nova)

    def _garantir_vertice(self, nome: str) -> int:
        if nome not in self._idx:
            self.adicionar_vertice(nome)
        return self._idx[nome]

    def adicionar_aresta(self, u: str, v: str, peso: float) -> None:
        """
        Adiciona/atualiza aresta dirigida u -> v.
        (Permitimos peso negativo para Bellman-Ford)
        """
        ui = self._garantir_vertice(u)
        vi = self._garantir_vertice(v)
        self._mat[ui][vi] = float(peso)

    def adicionar_aresta_dupla(self, a: str, b: str,
                               peso_ida: float,
                               peso_volta: Optional[float] = None) -> None:
        if peso_volta is None:
            peso_volta = peso_ida
        self.adicionar_aresta(a, b, peso_ida)
        self.adicionar_aresta(b, a, peso_volta)

    def remover_aresta(self, u: str, v: str) -> None:
        if u in self._idx and v in self._idx:
            self._mat[self._idx[u]][self._idx[v]] = math.inf

    def obter_peso(self, u: str, v: str) -> float:
        if u not in self._idx or v not in self._idx:
            return math.inf
        return self._mat[self._idx[u]][self._idx[v]]

    # -----------------------------------------------------------
    #                         DIJKSTRA
    # -----------------------------------------------------------
    def dijkstra(self, origem: str, destino: Optional[str] = None):
        if origem not in self._idx:
            return ({} if destino is None else (math.inf, []))

        INF = math.inf
        n = len(self._nomes)
        s = self._idx[origem]
        t = self._idx[destino] if destino is not None and destino in self._idx else None

        dist = [INF] * n
        ant = [-1] * n
        vis = [False] * n
        dist[s] = 0.0

        for _ in range(n):
            u, melhor = -1, INF
            for i in range(n):
                if not vis[i] and dist[i] < melhor:
                    melhor, u = dist[i], i
            if u == -1:
                break

            vis[u] = True
            if t is not None and u == t:
                break

            for v in range(n):
                w = self._mat[u][v]
                if w == INF:
                    continue
                nd = dist[u] + w
                if nd < dist[v]:
                    dist[v] = nd
                    ant[v] = u

        if destino is None:
            dist_map = {self._nomes[i]: dist[i] for i in range(n) if dist[i] < INF}
            ant_map = {self._nomes[i]: (self._nomes[ant[i]] if ant[i] != -1 else None)
                       for i in range(n)}
            return dist_map, ant_map

        if destino not in self._idx or dist[self._idx[destino]] == INF:
            return INF, []

        caminho_idx = []
        v = self._idx[destino]
        while v != -1:
            caminho_idx.append(v)
            if v == s:
                break
            v = ant[v]
        caminho_idx.reverse()
        caminho = [self._nomes[i] for i in caminho_idx]
        return dist[self._idx[destino]], caminho

    def printar(self, origem: str, destino: Optional[str] = None):
        if destino is None:
            print(f"\nSaindo de: {origem}")
            distn, _ = self.dijkstra(origem)
            for i, local in enumerate(distn):
                print(f"Destino {i}: {local}")
                print("Distância:", round(distn[local], 2))
                print("---------------------------------")
        else:
            dist, caminho = self.dijkstra(origem, destino)
            if dist == math.inf:
                print(f"Não existe caminho de {origem} até {destino}.")
                return
            print(f"Distância: {round(dist, 2)}")
            for i, c in enumerate(caminho):
                print(f"Conexão {i}: {c}")

    # -----------------------------------------------------------
    #                        BELLMAN-FORD
    # -----------------------------------------------------------
    def bellman_ford(self, origem: str, destino: Optional[str] = None):

        if origem not in self._idx:
            return ({} if destino is None else (math.inf, []))

        INF = math.inf
        n = len(self._nomes)
        s = self._idx[origem]

        dist = [INF] * n
        ant = [-1] * n
        dist[s] = 0.0

        # lista de arestas
        arestas = []
        for u in range(n):
            for v in range(n):
                w = self._mat[u][v]
                if w != INF:
                    arestas.append((u, v, w))

        # V-1 relaxamentos
        for _ in range(n - 1):
            mudou = False
            for u, v, w in arestas:
                if dist[u] != INF and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    ant[v] = u
                    mudou = True
            if not mudou:
                break

        # Detectar ciclo negativo
        for u, v, w in arestas:
            if dist[u] != INF and dist[u] + w < dist[v]:
                raise ValueError(
                    "Ciclo de peso negativo alcançável detectado!"
                )

        if destino is None:
            dist_map = {self._nomes[i]: dist[i] for i in range(n) if dist[i] < INF}
            ant_map = {self._nomes[i]: (self._nomes[ant[i]] if ant[i] != -1 else None)
                       for i in range(n)}
            return dist_map, ant_map

        if destino not in self._idx or dist[self._idx[destino]] == INF:
            return INF, []

        # reconstruir caminho
        caminho_idx = []
        v = self._idx[destino]
        while v != -1:
            caminho_idx.append(v)
            if v == s:
                break
            v = ant[v]

        caminho_idx.reverse()
        caminho = [self._nomes[i] for i in caminho_idx]
        return dist[self._idx[destino]], caminho

    # -----------------------------------------------------------
    #                           BFS
    # -----------------------------------------------------------
    def bfs(self, origem: str, destino: Optional[str] = None):
        if origem not in self._idx:
            return ({}, {}) if destino is None else (-1, [])

        n = len(self._nomes)
        s = self._idx[origem]

        dist = [-1] * n
        ant = [-1] * n

        fila = deque([s])
        dist[s] = 0

        while fila:
            u = fila.popleft()
            for v in range(n):
                if self._mat[u][v] != math.inf and dist[v] == -1:
                    dist[v] = dist[u] + 1
                    ant[v] = u
                    fila.append(v)

        if destino is None:
            dist_map = {self._nomes[i]: dist[i] for i in range(n) if dist[i] != -1}
            ant_map = {self._nomes[i]: (self._nomes[ant[i]] if ant[i] != -1 else None)
                       for i in range(n)}
            return dist_map, ant_map

        if destino not in self._idx:
            return -1, []

        t = self._idx[destino]
        if dist[t] == -1:
            return -1, []

        caminho_idx = []
        v = t
        while v != -1:
            caminho_idx.append(v)
            if v == s:
                break
            v = ant[v]

        caminho_idx.reverse()
        caminho = [self._nomes[i] for i in caminho_idx]
        return dist[t], caminho

    # -----------------------------------------------------------
    #                           DFS
    # -----------------------------------------------------------
    def dfs(self, origem: str) -> List[str]:
        if origem not in self._idx:
            return []

        n = len(self._nomes)
        vis = [False] * n
        ordem = []

        def _dfs(u: int):
            vis[u] = True
            ordem.append(self._nomes[u])
            for v in range(n):
                if self._mat[u][v] != math.inf and not vis[v]:
                    _dfs(v)

        _dfs(self._idx[origem])
        return ordem


# -----------------------------------------------------------
#                     MAPA DE HOLLOW KNIGHT
# -----------------------------------------------------------

vértices = [
    'O ABISMO', 'NINHO DE TECELA ATLA', 'DOCAS PROFUNDAS', 'A MEDULA',
    'GRUTA MUSGOSA', 'COVIL DOS VERMES', 'TRILHA DE SKARR', 'CAMPOS LONGINQUOS',
    'VERDANIA', 'PANTANO CINZENTO', 'CAMPANULA', 'CASCOMADEIRA',
    'CAMINHO DOS PECADORES', 'DEGRAUS DEVASTADOS', 'AREIAS DE KARAK',
    'CLAUSTROFORJAS', 'SPA DA CIDADELA', 'ESTAÇAO VIA CAMPANARIA',
    'ALA BRANCA', 'BOSQUE DOS LUMES', 'CAMARAS SUSSURRANTES', 'BILEBREJO',
    'O ROCHEDO', 'MONTE PLUMIDIO', 'SALOES SUPREMOS', 'MEMORIUM',
    'CANAIS PESTILENTOS', 'O BERÇO'
]

vértices.sort()
mapa = Grafo(vértices)

# Caminhos (mesmos que você tinha)
mapa.adicionar_aresta_dupla('O ABISMO', 'DOCAS PROFUNDAS', 8.1)
mapa.adicionar_aresta_dupla('NINHO DE TECELA ATLA', 'GRUTA MUSGOSA', 2.8)
mapa.adicionar_aresta_dupla('A MEDULA', 'GRUTA MUSGOSA', 4.2)
mapa.adicionar_aresta_dupla('A MEDULA', 'DOCAS PROFUNDAS', 6.5)
mapa.adicionar_aresta_dupla('DOCAS PROFUNDAS', 'TRILHA DE SKARR', 6.6)
mapa.adicionar_aresta_dupla('COVIL DOS VERMES', 'GRUTA MUSGOSA', 2.8)
mapa.adicionar_aresta_dupla('CASCOMADEIRA', 'COVIL DOS VERMES', 5.5)
mapa.adicionar_aresta_dupla('CASCOMADEIRA', 'CAMPANULA', 1.6)
mapa.adicionar_aresta_dupla('CAMPANULA', 'PANTANO CINZENTO', 4.0)
mapa.adicionar_aresta_dupla('PANTANO CINZENTO', 'CAMPOS LONGINQUOS', 4.6)
mapa.adicionar_aresta_dupla('CAMPOS LONGINQUOS', 'DOCAS PROFUNDAS', 4.0)
mapa.adicionar_aresta_dupla('CAMPOS LONGINQUOS', 'TRILHA DE SKARR', 3.0)
mapa.adicionar_aresta_dupla('CAMPOS LONGINQUOS', 'VERDANIA', 5.8)
mapa.adicionar_aresta_dupla('VERDANIA', 'PANTANO CINZENTO', 5.5)
mapa.adicionar_aresta_dupla('PANTANO CINZENTO', 'BOSQUE DOS LUMES', 2.1)
mapa.adicionar_aresta_dupla('PANTANO CINZENTO', 'CAMINHO DOS PECADORES', 3.4)
mapa.adicionar_aresta_dupla('CAMINHO DOS PECADORES', 'BILEBREJO', 6.3)
mapa.adicionar_aresta_dupla('DEGRAUS DEVASTADOS', 'CASCOMADEIRA', 6.4)
mapa.adicionar_aresta('DEGRAUS DEVASTADOS', 'COVIL DOS VERMES', 3.8)
mapa.adicionar_aresta('DEGRAUS DEVASTADOS', 'GRUTA MUSGOSA', 4.8)
mapa.adicionar_aresta_dupla('O BERÇO', 'MEMORIUM', 3.0)
mapa.adicionar_aresta_dupla('O BERÇO', 'SALOES SUPREMOS', 3.8)
mapa.adicionar_aresta_dupla('SPA DA CIDADELA', 'O ROCHEDO', 2.2)
mapa.adicionar_aresta_dupla('SPA DA CIDADELA', 'ALA BRANCA', 4.9)
mapa.adicionar_aresta_dupla('SALOES SUPREMOS', 'MEMORIUM', 2.5)
mapa.adicionar_aresta_dupla('CAMARAS SUSSURRANTES', 'MEMORIUM', 2.0)
mapa.adicionar_aresta_dupla('MONTE PLUMIDIO', 'O ROCHEDO', 4.6)
mapa.adicionar_aresta_dupla('DEGRAUS DEVASTADOS', 'AREIAS DE KARAK', 3.3)
mapa.adicionar_aresta_dupla('DEGRAUS DEVASTADOS', 'SPA DA CIDADELA', 5.1)
mapa.adicionar_aresta_dupla('CANAIS PESTILENTOS', 'MEMORIUM', 4.0)
mapa.adicionar_aresta_dupla('CANAIS PESTILENTOS', 'BILEBREJO', 2.1)
mapa.adicionar_aresta_dupla('ALA BRANCA', 'CLAUSTROFORJAS', 3.0)
mapa.adicionar_aresta_dupla('ESTAÇAO VIA CAMPANARIA', 'ALA BRANCA', 3.5)
mapa.adicionar_aresta_dupla('ESTAÇAO VIA CAMPANARIA', 'CAMARAS SUSSURRANTES', 3.8)
mapa.adicionar_aresta_dupla('ESTAÇAO VIA CAMPANARIA', 'CLAUSTROFORJAS', 4.4)
mapa.adicionar_aresta_dupla('ESTAÇAO VIA CAMPANARIA', 'CAMINHO DOS PECADORES', 5.5)
mapa.adicionar_aresta_dupla('BILEBREJO', 'CAMARAS SUSSURRANTES', 9.2)
mapa.adicionar_aresta_dupla('DEGRAUS DEVASTADOS', 'CLAUSTROFORJAS', 7.9)
mapa.adicionar_aresta_dupla('CLAUSTROFORJAS', 'BOSQUE DOS LUMES', 4.0)
mapa.adicionar_aresta_dupla('CAMPANULA', 'A MEDULA', 3.0)

# Exemplo: aresta NEGATIVA para testar Bellman-Ford
mapa.adicionar_aresta('MEMORIUM', 'O ABISMO', -5.0)

# Exemplo de uso
if __name__ == "__main__":
    print("\n### DIJKSTRA ###")
    mapa.printar('GRUTA MUSGOSA', 'DOCAS PROFUNDAS')

    print("\n### BELLMAN-FORD ###")
    print(mapa.bellman_ford('GRUTA MUSGOSA', 'O ABISMO'))

    print("\n### BFS ###")
    print(mapa.bfs('GRUTA MUSGOSA', 'MEMORIUM'))

    print("\n### DFS ###")
    print(mapa.dfs('GRUTA MUSGOSA'))
