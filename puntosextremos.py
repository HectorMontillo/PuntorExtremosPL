from math import factorial
from tabulate import tabulate
import numpy as np

def potencia(c):
	if len(c) == 0:
			return [[]]
	r = potencia(c[:-1])
	return r + [s + [c[-1]] for s in r]

def combinaciones(c, n):
	return [s for s in potencia(c) if len(s) == n]

def numero_combinaciones(m, n):
    return factorial(m) // (factorial(n) * factorial(m - n))

def evaluarPunto(p,m,b,bs):

	for x in p:
		if x == None:
			return "(Error Matriz singular)"
		elif x < 0:
			return "(SB) No es punto extremo"
	for i,r in enumerate(m):
		val = np.sum(list(map(lambda t : t[0]*t[1], zip(r,p))))
		if (val <= b[i] and bs[i] == "<=") or (val >= b[i] and bs[i] == ">=") or (val == b[i] and bs[i] == "=="):
			evaluacion = "(SBF) Punto Extremo Factible"
			
		else:
			evaluacion = "(SB) Punto Extremo"
			break
	
		
	return evaluacion
	
def puntosExtremos(m,b, bs,z, filtro=''):
	n = len(m[0]) #Número de variables
	nc = numero_combinaciones(len(m),n)
	c = combinaciones(range(len(m)),n)
	print("Numero de variables: {}".format(n))
	print("Numero de restricciones: {}".format(len(m)))
	print("Numero de puntos: {}".format(nc))

	puntos = list()
	for i in c:
		ecu = np.array([m[e] for e in i])
		res = np.array([b[e] for e in i])
		try:
			sol = np.linalg.solve(ecu,res)
		except np.linalg.LinAlgError:
			sol = [None] * n

		eva = evaluarPunto(sol,m,b,bs)
		if eva == "(SBF) Punto Extremo Factible":
			fo = np.sum(list(map(lambda t : t[0]*t[1], zip(z,sol))))
		else:
			fo = 'N/A'
		if filtro == '':
			puntos.append([i,sol,eva,fo])
		elif filtro == eva:
			puntos.append([i,sol,eva,fo])

	return puntos

def imprimirPuntosExtremos(puntos):
	print(tabulate(puntos, showindex=True,headers=["Hiperplanos", "Resultado", "Evaluacion", "Funcion objetivo"]))

if __name__ == "__main__":
	m = np.array(
		[
			[1,1,1,1,1,1],
			[-2,-1,-1,1,0,0],
			[0,0,1,1,2,1],
			[1,0,0,0,0,0],
			[0,1,0,0,0,0],
			[0,0,1,0,0,0],
			[0,0,0,1,0,0],
			[0,0,0,0,1,0],
			[0,0,0,0,0,1],
		]
	)

	b = np.array(
		[6,4,4,0,0,0,0,0,0]
	)
	bs = ["<=","<=","<=",">=",">=",">=",">=",">=",">="]
	z = [-1, -2,1,-1,-4,2]
	imprimirPuntosExtremos(puntosExtremos(m,b,bs,z))
