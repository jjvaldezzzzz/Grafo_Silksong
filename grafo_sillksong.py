import math
from typing import Dict, List, Optional, Iterable, Tuple

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
        """Adiciona/atualiza aresta dirigida u -> v com peso >= 0."""
        if peso < 0:
            raise ValueError("Dijkstra requer pesos nAo negativos.")
        ui = self._garantir_vertice(u)
        vi = self._garantir_vertice(v)
        self._mat[ui][vi] = float(peso)

    def remover_aresta(self, u: str, v: str) -> None:
        """Remove a aresta u -> v (define como math.inf)."""
        if u in self._idx and v in self._idx:
            self._mat[self._idx[u]][self._idx[v]] = math.inf

    def obter_peso(self, u: str, v: str) -> float:
        """Retorna o peso de u -> v (math.inf se nAo existir)."""
        if u not in self._idx or v not in self._idx:
            return math.inf
        return self._mat[self._idx[u]][self._idx[v]]
    
    def adicionar_aresta_dupla(self, a: str, b: str, peso_ida: float, peso_volta: Optional[float] = None) -> None:
        """Atalho para adicionar arestas nos dois sentidos entre a e b."""
        if peso_volta is None:
            peso_volta = peso_ida
        self.adicionar_aresta(a, b, peso_ida)
        self.adicionar_aresta(b, a, peso_volta)


    # ---------- dijkstra ----------
    def dijkstra(self, origem: str, destino: Optional[str] = None):
        """
        Calcula menores caminhos a partir de 'origem' usando Dijkstra O(V^2).

        Retorna:
          - Se destino is None:
              (dist, anterior)
                dist: dict[vértice] -> custo mInimo desde 'origem'
                anterior: dict[vértice] -> predecessor no caminho mInimo (ou None)
          - Caso contrArio:
              (custo_origem_destino, caminho_lista)
                custo_origem_destino: float (math.inf se inalcançAvel)
                caminho_lista: [origem, ..., destino] (lista vazia se inalcançAvel)
        """
        if origem not in self._idx:
            return ({} if destino is None else (math.inf, []))

        INF = math.inf
        n = len(self._nomes)
        s = self._idx[origem]
        t = self._idx[destino] if (destino is not None and destino in self._idx) else None

        dist = [INF] * n
        ant = [-1] * n
        vis = [False] * n
        dist[s] = 0.0

        for _ in range(n):
            # escolhe o nAo visitado com menor distAncia
            u, melhor = -1, INF
            for i in range(n):
                if not vis[i] and dist[i] < melhor:
                    melhor, u = dist[i], i
            if u == -1:
                break

            vis[u] = True
            if t is not None and u == t:
                break

            # relaxamento
            du = dist[u]
            linha = self._mat[u]
            for v in range(n):
                w = linha[v]
                if w == INF:
                    continue
                nd = du + w
                if nd < dist[v]:
                    dist[v] = nd
                    ant[v] = u

        # saIda por destino ou mapas completos
        if destino is None:
            dist_map = {self._nomes[i]: dist[i] for i in range(n) if dist[i] < INF}
            ant_map = {self._nomes[i]: (self._nomes[ant[i]] if ant[i] != -1 else None)
                       for i in range(n)}
            return dist_map, ant_map

        if destino not in self._idx or dist[self._idx[destino]] == INF:
            return INF, []

        # reconstrói caminho s -> t
        caminho_idx: List[int] = []
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
        if(destino is None):
            print(f'Saindo de: {origem}')
            cont = 0
            distn = self.dijkstra(origem)[0]
            print("DEBUG nomes:", self._nomes)
            print("DEBUG dist_map:", distn)

            for local in distn:
                print(f'Destino {cont}: {local} \nDistância:', round(distn[local], 2))
                print('---------------------------------')
                cont += 1
            
        else:
            dist, caminho = self.dijkstra(origem, destino)
        print(f'Distância:', round(dist, 2))
        cont = 0
        for i in caminho:
            print(f'Conexão {cont}: {i}')
            cont += 1
arestas = ['O ABISMO', 'NINHO DE TECELA ATLA','DOCAS PROFUNDAS', 'A MEDULA', 'GRUTA MUSGOSA', 
             'COVIL DOS VERMES', 'TRILHA DE SKARR', 'CAMPOS LONGINQUOS', 
             'VERDANIA', 'PANTANO CINZENTO', 'CAMPANULA', 'CASCOMADEIRA', 'CAMINHO DOS PECADORES',
             'DEGRAUS DEVASTADOS', 'AREIAS DE KARAK', 'CLAUSTROFORJAS',
             'SPA DA CIDADELA', 'ESTAÇAO VIA CAMPANARIA', 'ALA BRANCA','BOSQUE DOS LUMES', 
             'CAMARAS SUSSURRANTES', 'BILEBREJO', 'O ROCHEDO', 'MONTE PLUMIDIO',
             'SALOES SUPREMOS', 'MEMORIUM', 'CANAIS PESTILENTOS', 'O BERÇO']   
arestas.sort()
mapa = Grafo(arestas)

mapa.adicionar_aresta_dupla('O ABISMO', 'DOCAS PROFUNDAS', 8.1, 8.1)
mapa.adicionar_aresta_dupla('NINHO DE TECELA ATLA', 'GRUTA MUSGOSA', 2.8, 2.8)
mapa.adicionar_aresta_dupla('A MEDULA', 'GRUTA MUSGOSA', 4.2, 4.2)
mapa.adicionar_aresta_dupla('A MEDULA', 'DOCAS PROFUNDAS', 6.5, 6.5)
mapa.adicionar_aresta_dupla('DOCAS PROFUNDAS', 'TRILHA DE SKARR', 6.6, 6.6)
mapa.adicionar_aresta_dupla('COVIL DOS VERMES', 'GRUTA MUSGOSA', 2.8, 2.8)
mapa.adicionar_aresta_dupla('CASCOMADEIRA', 'COVIL DOS VERMES', 5.5, 5.5)
mapa.adicionar_aresta_dupla('CASCOMADEIRA','CAMPANULA', 1.6, 1.6)
mapa.adicionar_aresta_dupla('CAMPANULA', 'PANTANO CINZENTO', 4.0, 4.0)
mapa.adicionar_aresta_dupla('PANTANO CINZENTO', 'CAMPOS LONGINQUOS', 4.6, 4.6)
mapa.adicionar_aresta_dupla('CAMPOS LONGINQUOS', 'DOCAS PROFUNDAS', 4.0, 4.0)
mapa.adicionar_aresta_dupla('CAMPOS LONGINQUOS', 'TRILHA DE SKARR', 3.0, 3.0)
mapa.adicionar_aresta_dupla('CAMPOS LONGINQUOS', 'VERDANIA', 5.8, 5.8)
mapa.adicionar_aresta_dupla('VERDANIA', 'PANTANO CINZENTO', 5.5, 5.5)
mapa.adicionar_aresta_dupla('PANTANO CINZENTO', 'BOSQUE DOS LUMES', 2.1, 2.1)
mapa.adicionar_aresta_dupla('PANTANO CINZENTO', 'CAMINHO DOS PECADORES', 3.4, 3.4)
mapa.adicionar_aresta_dupla('CAMINHO DOS PECADORES', 'BILEBREJO', 6.3, 6.3)
mapa.adicionar_aresta_dupla('DEGRAUS DEVASTADOS','CASCOMADEIRA', 6.4, 6.4)
mapa.adicionar_aresta('DEGRAUS DEVASTADOS','COVIL DOS VERMES', 3.8)
mapa.adicionar_aresta('DEGRAUS DEVASTADOS', 'GRUTA MUSGOSA', 4.8)
mapa.adicionar_aresta_dupla('O BERÇO', 'MEMORIUM', 3.0, 3.0)
mapa.adicionar_aresta_dupla('O BERÇO', 'SALOES SUPREMOS', 3.8, 3.8)
mapa.adicionar_aresta_dupla('SPA DA CIDADELA', 'O ROCHEDO', 2.2, 2.2)
mapa.adicionar_aresta_dupla('SPA DA CIDADELA', 'ALA BRANCA', 4.9, 4.9)
mapa.adicionar_aresta_dupla('SALOES SUPREMOS', 'MEMORIUM', 2.5, 2.5)
mapa.adicionar_aresta_dupla('CAMARAS SUSSURRANTES', 'MEMORIUM', 2.0, 2.0)
mapa.adicionar_aresta_dupla('MONTE PLUMIDIO', 'O ROCHEDO',  4.6, 4.6)
mapa.adicionar_aresta_dupla('DEGRAUS DEVASTADOS','AREIAS DE KARAK', 3.3, 3.3)
mapa.adicionar_aresta_dupla('DEGRAUS DEVASTADOS', 'SPA DA CIDADELA', 5.1, 5.1)
mapa.adicionar_aresta_dupla('CANAIS PESTILENTOS', 'MEMORIUM', 4.0, 4.0)
mapa.adicionar_aresta_dupla('CANAIS PESTILENTOS', 'BILEBREJO', 2.1, 2.1)
mapa.adicionar_aresta_dupla('ALA BRANCA', 'CLAUSTROFORJAS', 3.0, 3.3)
mapa.adicionar_aresta_dupla('ESTAÇAO VIA CAMPANARIA', 'ALA BRANCA', 3.5, 3.5)
mapa.adicionar_aresta_dupla('ESTAÇAO VIA CAMPANARIA', 'CAMARAS SUSSURRANTES', 3.8, 3.8)
mapa.adicionar_aresta_dupla('ESTAÇAO VIA CAMPANARIA', 'CLAUSTROFORJAS', 4.4, 4.4)
mapa.adicionar_aresta_dupla('ESTAÇAO VIA CAMPANARIA', 'CAMINHO DOS PECADORES', 5.5, 5.5)
mapa.adicionar_aresta_dupla('BILEBREJO', 'CAMARAS SUSSURRANTES', 9.2, 9.2)
mapa.adicionar_aresta_dupla('DEGRAUS DEVASTADOS', 'CLAUSTROFORJAS', 7.9, 7.9)
mapa.adicionar_aresta_dupla('CLAUSTROFORJAS', 'BOSQUE DOS LUMES', 4.0, 4.0)
mapa.adicionar_aresta_dupla('CAMPANULA', 'A MEDULA', 3.0, 3.0)

mapa.printar('GRUTA MUSGOSA', 'CAMINHO DOS PECADORES')
