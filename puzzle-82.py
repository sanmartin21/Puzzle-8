import random
import time
from queue import PriorityQueue

# Classe para representar o quebra-cabeça


class Puzzle:
    def __init__(self, estado_inicial=None):
        # Inicializa o quebra-cabeça com o estado inicial fornecido ou o embaralha se nenhum estado inicial for fornecido
        self.estado_inicial = estado_inicial if estado_inicial else self.embaralhar()
        # Define o estado objetivo do quebra-cabeça
        self.estado_objetivo = [[1, 2, 3], [4, 5, 6], [7, 8, None]]

    def embaralhar(self):
        # Embaralha as peças do quebra-cabeça
        pecas = list(range(1, 9)) + [None]
        random.shuffle(pecas)
        return [pecas[i*3:(i+1)*3] for i in range(3)]

# Classe para representar um nó no espaço de estados


class No:
    def __init__(self, estado, pai=None, acao=None, custo=0):
        # Inicializa um nó com um estado, nó pai, ação e custo
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo

    def __lt__(self, outro):
        # Sobrecarga do operador "<" para comparar nós com base no custo
        return self.custo < outro.custo

# Função para realizar a busca A* com uma heurística


def busca_a_estrela(quebra_cabeca, heuristica):
    no_inicial = No(quebra_cabeca.estado_inicial)
    fronteira = PriorityQueue()
    fronteira.put((0, no_inicial))
    explorados = set()
    while not fronteira.empty():
        no_atual = fronteira.get()[1]
        if no_atual.estado == quebra_cabeca.estado_objetivo:
            return no_atual, len(explorados)
        explorados.add(tuple(map(tuple, no_atual.estado)))
        for acao in ["CIMA", "BAIXO", "ESQUERDA", "DIREITA"]:
            no_filho = mover_peca_vazia(no_atual, acao)
            if no_filho and tuple(map(tuple, no_filho.estado)) not in explorados:
                if heuristica == 1:
                    # Heurística de peças fora do lugar
                    h = pecas_fora_do_lugar(
                        no_filho.estado, quebra_cabeca.estado_objetivo)
                else:
                    # Heurística da Distância de Manhattan
                    h = distancia_manhattan(
                        no_filho.estado, quebra_cabeca.estado_objetivo)
                # Calcula o custo total (custo do caminho percorrido + heurística)
                f = no_filho.custo + h
                fronteira.put((f, no_filho))
    return None, len(explorados)

# Função para calcular o número de peças fora do lugar


def pecas_fora_do_lugar(estado, estado_objetivo):
    return sum(s != g for s, g in zip(estado, estado_objetivo) if s is not None and g is not None)

# Função para calcular a Distância de Manhattan


def distancia_manhattan(estado, estado_objetivo):
    distancia = 0
    for i in range(3):
        for j in range(3):
            if estado[i][j] is not None:
                objetivo_i, objetivo_j = next((x, y) for x, linha in enumerate(
                    estado_objetivo) for y, val in enumerate(linha) if val == estado[i][j])
                distancia += abs(objetivo_i - i) + abs(objetivo_j - j)
    return distancia

# Função para realizar a busca em largura (BFS)


def busca_largura(quebra_cabeca):
    no_inicial = No(quebra_cabeca.estado_inicial)
    if no_inicial.estado == quebra_cabeca.estado_objetivo:
        return no_inicial, 0
    fronteira = [no_inicial]
    explorados = set()
    while fronteira:
        no_atual = fronteira.pop(0)
        explorados.add(tuple(map(tuple, no_atual.estado)))
        for acao in ["CIMA", "BAIXO", "ESQUERDA", "DIREITA"]:
            no_filho = mover_peca_vazia(no_atual, acao)
            if no_filho and tuple(map(tuple, no_filho.estado)) not in explorados:
                if no_filho.estado == quebra_cabeca.estado_objetivo:
                    return no_filho, len(explorados)
                fronteira.append(no_filho)
    return None, len(explorados)

# Função para mover a peça vazia


def mover_peca_vazia(no, acao):
    estado = [linha[:] for linha in no.estado]
    i, j = next((i, j) for i, linha in enumerate(estado)
                for j, val in enumerate(linha) if val is None)
    if acao == "CIMA" and i > 0:
        estado[i][j], estado[i-1][j] = estado[i-1][j], estado[i][j]
    elif acao == "BAIXO" and i < 2:
        estado[i][j], estado[i+1][j] = estado[i+1][j], estado[i][j]
    elif acao == "ESQUERDA" and j > 0:
        estado[i][j], estado[i][j-1] = estado[i][j-1], estado[i][j]
    elif acao == "DIREITA" and j < 2:
        estado[i][j], estado[i][j+1] = estado[i][j+1], estado[i][j]
    else:
        return None
    return No(estado, no, acao, no.custo + 1)

# Função para escolher o método de busca


def busca(quebra_cabeca, metodo):
    if metodo == 1:
        return busca_largura(quebra_cabeca)
    elif metodo == 2:
        return busca_a_estrela(quebra_cabeca, heuristica=1)
    elif metodo == 3:
        return busca_a_estrela(quebra_cabeca, heuristica=2)
    else:
        print("Método não reconhecido")
        return None, 0

# Função para retroceder e obter as ações tomadas


def retroceder(no):
    acoes = []
    while no.pai is not None:
        acoes.append(no.acao)
        no = no.pai
    return acoes[::-1]


# Função principal
if __name__ == "__main__":
    puzzle = Puzzle()
    print("Estado inicial do quebra-cabeça:")
    for linha in puzzle.estado_inicial:
        print(linha)
    metodo = int(input(
        "Escolha o método de busca (1 para BFS, 2 para A* com g(x), 3 para A* com g(x) + h(x)): "))
    inicio = time.time()
    resultado, nodos_explorados = busca(puzzle, metodo)
    tempo_decorrido = time.time() - inicio
    print(f"Tempo de busca: {tempo_decorrido} segundos")
    print(f"Número de nodos explorados: {nodos_explorados}")

    if resultado is None:
        print("Não foi possível resolver o quebra-cabeça.")
    else:
        acoes = retroceder(resultado)
        estado = puzzle.estado_inicial
        for acao in acoes:
            no = mover_peca_vazia(No(estado), acao)
            estado = no.estado
        print("Estado final do quebra-cabeça:")
        for linha in estado:
            print(linha)
