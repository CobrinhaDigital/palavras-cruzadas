import pandas as pd
import numpy as np
from numpy import random
import unicodedata
from enum import Enum

class Espaco: 
    def __init__(self, coluna_inicial, linha_inicial, direcao, tamanho, restricoes={}):
        self.coluna_inicial = coluna_inicial
        self.linha_inicial = linha_inicial
        self.direcao = direcao
        self.tamanho = tamanho
        self.restricoes = restricoes 
        
    def __str__(self):
        return f"Espaco: coluna {self.coluna_inicial}, linha {self.linha_inicial}, {self.direcao}, {self.tamanho} letras"

class Direcao(Enum): 
    horizontal = 'horizontal'
    vertical = 'vertical'
    
def gerar_matriz(dimensao):
    matriz = np.full((dimensao, dimensao), ' ')
    x_min = int((dimensao**2) * 0.2)
    x_max = int((dimensao**2) * 0.25)
    x = random.randint(x_min, x_max)
    print("numero de X: ", x)
    for x in range(x): 
        coluna = random.randint(0, dimensao - 1)
        linha = random.randint(0, dimensao - 1)
        matriz[linha, coluna] = 'X'
    return matriz

def mapear_matriz(matriz, dimensao) -> list[Espaco]: 
    espacos = [] 
    
    # Percorrendo horizontal 
    for linha in range(dimensao):
        inicio_coluna = 0 
        for coluna in range(dimensao):
            if matriz[linha, coluna] == 'X':
                tamanho = coluna - inicio_coluna 
                if tamanho > 1: 
                    espacos.append(Espaco(inicio_coluna, linha, Direcao.horizontal, tamanho))
                inicio_coluna = coluna + 1
                
    # Percorrendo vertical 
    for coluna in range(dimensao):
        inicio_linha = 0
        for linha in range(dimensao): 
            if matriz[coluna, linha] == 'X': 
                tamanho = linha - inicio_linha
                if tamanho > 1: 
                    espacos.append(Espaco(coluna, inicio_linha, Direcao.vertical, tamanho))
                inicio_linha = linha + 1 

    return espacos
    