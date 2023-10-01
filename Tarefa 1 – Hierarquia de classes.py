# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 12:22:53 2023

@author: dnery
"""
#%% Bibliotecas
import numpy as np
from array import array

#%% Classe Pai
class EDL:
    def __init__(self, matrix):
        self.matrix = matrix
    
    def __str__(self):
        matrix_str = ""
        for linha in self.matrix:
            matrix_str += "|"
            for j in linha:
                matrix_str += f" {j:^5}"
            matrix_str += " |\n"
        return matrix_str
    
    def traco(self):
        if len(self.matrix) != len(self.matrix[0]):
            raise ValueError("O traço só pode ser calculado para matrizes quadradas.")
        
        traco = sum(self.matrix[i][i] for i in range(len(self.matrix)))
        return traco
    
#%% Quadrada
class Quadrada(EDL):
    def __init__(self, matrix):
        super().__init__(matrix)
    
    def __sub__(self,other):
        M1 = len(self.matrix) ; M2 = len(other.matrix)
        N1 = len(self.matrix[0]) ; N2 = len(other.matrix[0])
        
        if M1 != M2 or N1 != N2:
            raise ValueError("As matrizes devem ter as mesmas dimensões para a soma.")
        
        resultado = np.zeros((M1,N1))
        
        for i,_ in enumerate(self.matrix):
            for j,_ in enumerate(self.matrix[i]):
                soma_elemento = self.matrix[i][j] - other.matrix[i][j] 
                resultado[i][j] = soma_elemento
        
        return EDL(resultado)
    
    def __add__(self,other):
        M1 = len(self.matrix) ; M2 = len(other.matrix)
        N1 = len(self.matrix[0]) ; N2 = len(other.matrix[0])
        
        if M1 != M2 or N1 != N2:
            raise ValueError("As matrizes devem ter as mesmas dimensões para a soma.")
        
        resultado = np.zeros((M1,N1))
        
        for i,_ in enumerate(self.matrix):
            for j,_ in enumerate(self.matrix[i]):
                soma_elemento = self.matrix[i][j] + other.matrix[i][j] 
                resultado[i][j] = soma_elemento
        
        return EDL(resultado)
    
    def __mul__(self,other):
        if isinstance(other, (int, float)):
            # Se o segundo operando for um número, multiplica todos os elementos da matriz pelo número
            resultado = [[elemento * other for elemento in linha] for linha in self.matrix]
            return Quadrada(resultado)
        
        M1 = len(self.matrix) ; M2 = len(other.matrix)
        N1 = len(self.matrix[0]) ; N2 = len(other.matrix[0])
        
        if M1 != M2 or N1 != N2:
            raise ValueError("As matrizes devem ter as mesmas dimensões para a soma.")
        
        resultado = []
        for i in range(len(self.matrix)):
            linha = []
            for j in range(len(other.matrix[0])):
                produto = 0
                for k in range(len(self.matrix[0])):
                    produto += self.matrix[i][k] * other.matrix[k][j]
                linha.append(produto)
            resultado.append(linha)
        
        return Quadrada(resultado)
    
    def __rmul__(self,other): #Just have the scalar multiplication because if "other" are a matrix, the __mul__ method is goin to be used
        if isinstance(other, (int, float)):
            resultado = [[elemento * other for elemento in linha] for linha in self.matrix]
            return Quadrada(resultado)
    
    def transposta(self):
        num_linhas = len(self.matrix)
        num_colunas = len(self.matrix[0])
        
        # Cria uma nova matriz para a transposta
        transposta_matrix = [[0.0] * num_linhas for _ in range(num_colunas)]
        
        for i in range(num_linhas):
            for j in range(num_colunas):
                transposta_matrix[j][i] = self.matrix[i][j]
        
        return Quadrada([array('d', linha) for linha in transposta_matrix])

        
    
    def determinante(self):
        if len(self.matrix) == 1:
            return self.matrix[0][0]

        if len(self.matrix) == 2:
            # Caso base para matrizes 2x2
            return self.matrix[0][0] * self.matrix[1][1] - self.matrix[0][1] * self.matrix[1][0]

        det = 0
        for coluna in range(len(self.matrix)):
            cofator = self.calcular_cofator(0, coluna)
            det += self.matrix[0][coluna] * cofator

        return det

    def calcular_cofator(self, linha, coluna):
        submatriz = [linha[0:coluna] + linha[coluna + 1:] for linha in self.matrix[1:]]
        submatriz_quadrada = Quadrada(submatriz)
        return (-1) ** (linha + coluna) * submatriz_quadrada.calcular_determinante()
                
#%% Triangular Sup
class TriangularSuperior(EDL):
    def __init__(self, matrix):
        super().__init__(matrix)

    def calcular_determinante(self):
        pass

    def calcular_inversa(self):
        pass
#%% Triagular Inf
class TriangularInferior(EDL):
    def __init__(self, matrix):
        super().__init__(matrix)

    def calcular_determinante(self):
        pass

    def calcular_inversa(self):
        pass

    

    
    
#%% Testes
matriz_quadrada = np.array([array('d', [2, 1]), array('d', [5, 3])])
matrix2 = np.array([array('d', [3, 0]), array('d', [7, 5])])


matriz_triang_superior = np.array([array('d', [2, 1, 4]), array('d', [0, 3, 2]), array('d', [0, 0, 1])])

calc_quadrada = Quadrada(matriz_quadrada)
t_calc_quadrada = calc_quadrada.transposta()

calc_matrix2 = Quadrada(matrix2)
t_calc_matrix2 = calc_matrix2.transposta()


calc_triang_superior = TriangularSuperior(matriz_triang_superior)

print("Matriz Quadrada:")
print("Matrix 1:\n")
print(calc_quadrada)
print(f"Traço da matrix 1:{calc_quadrada.traco()}\n")
print(f"Determinante da matrix 1:{calc_quadrada.determinante()}\n")
print("Matrix 1 Transposta:\n")
print(t_calc_quadrada)


print("Matrix 2:\n")
print(calc_matrix2)
print(f"Traço da matrix 2:{calc_matrix2.traco()}\n")
print(f"Determinante da matrix 2:{calc_matrix2.determinante()}\n")
print("Matrix 2 Transposta:\n")
print(t_calc_matrix2)



Soma = calc_quadrada + calc_matrix2
Sub1 = calc_quadrada - calc_matrix2
Sub2 = calc_matrix2 - calc_quadrada
prod1 = calc_matrix2*calc_quadrada
prod2 = calc_quadrada*calc_matrix2 
prod_esc2 = 2*calc_matrix2
prod_esc1 = 3*calc_quadrada
det_1 = calc_quadrada.determinante()
det_2 = calc_matrix2.determinante()

print("\nSoma das matrizes: M1 + M2")
print(Soma)
print("\nDiferença das matrizes: M1 - M2 ")
print(Sub1)
print("\nDiferença das matrizes: M2 - M1 ")
print(Sub2)
print("\nProduto das matrizes: M2*M1 ")
print(prod1)
print("\nProduto das matrizes: M1*M2 ")
print(prod2)
print("\nProduto por escalar: 2*M2")
print(prod_esc2)
print("\nProduto por escalar: 3*M1")
print(prod_esc1)


print("\nMatriz Triangular Superior:")
print(calc_triang_superior)


#%%



    