import pandas as pd
import numpy as np
from numpy import random
import unicodedata
from enum import Enum

df = pd.read_csv("palavras_normalizadas.csv", header=None, names=['palavra'])

class Espaco: 
    def __init__(self, coluna_inicial, linha_inicial, direcao, tamanho, restricoes={}, cruzamentos={}):
        self.coluna_inicial = coluna_inicial
        self.linha_inicial = linha_inicial
        self.direcao = direcao
        self.tamanho = tamanho
        self.restricoes = restricoes 
        self.cruzamentos = cruzamentos
        self.coordenadas = self.obter_coordenadas()
        self.dominio = []
        
    def __str__(self):
        return f"coluna {self.coluna_inicial}, linha {self.linha_inicial}, {self.direcao.value}, {self.tamanho} letras, coordenadas: {self.coordenadas}, cruzamentos: {self.cruzamentos}, dominio: {self.dominio}"
    
    def obter_coordenadas(self): 
        coordenadas = [] 
        for i in range(self.tamanho):
            if self.direcao == Direcao.horizontal:
                coordenadas.append((self.coluna_inicial + i, self.linha_inicial))
            else:
                coordenadas.append((self.coluna_inicial, self.linha_inicial + i))
        return coordenadas
    
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

def mapear_matriz(matriz, dimensao): 
    espacos = [] 
    
    # Percorrendo horizontal 
    for linha in range(dimensao):
        inicio_coluna = 0 
        for coluna in range(dimensao + 1):
            if coluna == dimensao or matriz[linha, coluna] == 'X':
                tamanho = coluna - inicio_coluna 
                if tamanho > 1: 
                    espacos.append(Espaco(inicio_coluna, linha, Direcao.horizontal, tamanho))
                inicio_coluna = coluna + 1
                
    # Percorrendo vertical 
    for coluna in range(dimensao):
        inicio_linha = 0
        for linha in range(dimensao + 1): 
            if linha == dimensao or matriz[linha, coluna] == 'X': 
                tamanho = linha - inicio_linha
                if tamanho > 1: 
                    espacos.append(Espaco(coluna, inicio_linha, Direcao.vertical, tamanho))
                inicio_linha = linha + 1 

    return espacos
    
def obter_cruzamentos(espacos):
    for i in range(len(espacos)): 
        for j in range(i + 1, len(espacos)):
            espaco1 = espacos[i]
            espaco2 = espacos[j]
            
            cruzamentos = set(espaco1.coordenadas) & set(espaco2.coordenadas)
            
            if cruzamentos:
                espaco1.cruzamentos[j] = cruzamentos
                espaco2.cruzamentos[i] = cruzamentos
                
def obter_dominio(espacos, df):
    for espaco in espacos: 
        valores = df[df['palavra'].str.len() == espaco.tamanho]
        espaco.dominio = valores['palavra'].tolist()