#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

naive_bayes.py
---------------

Archivo general para realizar las pruebas del uso del método de bayes inocente.

Se prueba en un conjunto de prueba de dimensión fija sobre cadenas de ADN.
Para mayor información sobre la base de datos, se puede consultar en

http://archive.ics.uci.edu/ml/datasets/Molecular+Biology+(Splice-junction+Gene+Sequences)

La base ya se trato, y se convirtieron los valores de genes a numeros enteros
con el fin de poder utilizar la base para varios métodos de clasificación (como
redes neuronales).

La base de datos ya se repartió en una base de entrenamiento (dna.data) y otra
base de prueba(dna.test). Con el fin de probar la robustez de los algoritmos de
aprendizaje ante ruido, se agregó a la base otros atributos extra con valores
asignados al azar (como si tuvieramos atributos extra con información no
significativa). Estos datos se encuentran en dna_noise.data y dna_noise.test
respectivamente.

Para estar seguro que el algoritmo funciona, tanto sin ruido como con
ruido el error de clasificación con los datos originales debe estar
por debajo del 5%, mientras que el error en el conjunto de prueba debe
de andar un poco por arriba del 5% pero claramente menor al 7%

"""

import nb

def carga_archivo(archivo):
    """
    Cargar el archivo de datos a clasificar, devuelve

    - datos = [dato1, dato2, ..., datoE], la lista de E datos a clasificar
      donde dato1 = [dato1(1), ..., dato1(n)] son los n valores de los
      atributos de dato1.

    - clases = [clase1, clase2, ..., claseE] la clase a la que pertenece
      cada dato

    """
    datos, clases = [], []

    enlistado = open(archivo, 'rU').readlines()
    for linea in enlistado:
        renglon = [int(d.strip().strip('\n')) for d in linea.split(',')]
        datos.append(renglon[0: -1])
        clases.append(renglon[-1])
    return datos, clases


def error_clasif(c1, c2):
    """
    Encuentra el porcentaje de valores diferentes entre la lista c1 y la c2

    """
    acc = len([1 for i in range(len(c1)) if c1[i] != c2[i]])
    return 1.0 * acc / len(c1)


def main():
    
    print("\nPrueba con la base de datos de DNA sin ruido")
    print("----------------------------------------------")

    datos, clases = carga_archivo("dna.data")
    clasificador = nb.NaiveBayes()

    clasificador.aprende(datos, clases)
    clases_estimadas = clasificador.reconoce(datos)
    error = error_clasif(clases, clases_estimadas)
    print("Error de estimación en los mismos datos: " +
        str(error*100)+" %")

    datos_test, clases_test = carga_archivo("dna.test")
    clases_estimadas_test = clasificador.reconoce(datos_test)
    error_test = error_clasif(clases_test, clases_estimadas_test)
    print("Error de estimación en los datos de prueba: " +
        str(error_test*100)+" %\n")

    print("\nPrueba con la base de datos de DNA con ruido")
    print("----------------------------------------------")

    datos, clases = carga_archivo("dna_noise.data")
    clasificador_ruido = nb.NaiveBayes()

    clasificador_ruido.aprende(datos, clases)
    clases_estimadas = clasificador_ruido.reconoce(datos)
    error = error_clasif(clases, clases_estimadas)
    print("Error de estimación en los mismos datos: "+str(error*100)+"%")

    datos_test, clases_test = carga_archivo("dna_noise.test")
    clases_estimadas_test = clasificador_ruido.reconoce(datos_test)
    error_test = error_clasif(clases_test, clases_estimadas_test)
    print("Error de estimación en los datos de prueba: "+str(error_test*100)+"%\n")


if __name__ == "__main__":
    main()

"""
Resultados:

    Prueba con la base de datos de DNA sin ruido
    ----------------------------------------------
    Error de estimación en los mismos datos: 4.05 %
    Error de estimación en los datos de prueba: 5.649241146711636 %

    Prueba con la base de datos de DNA con ruido
    ----------------------------------------------
    Error de estimación en los mismos datos: 3.85%
    Error de estimación en los datos de prueba: 5.480607082630692%

Conclusion:

    Los resultados obtenidos son similares, pero los porcentajes
    son mejores con los datos con ruido. Esto se debe a que
    a la hora de calcular las probabilidades siguen estando los datos
    sin ruido y estos siguen teniendo gran valor en el calculo y los datos
    con ruido no influyen tanto debido a que deben ser pocos comparado
    con los datos sin ruido.

"""
