# -*- coding: utf-8 -*-
"""
Autor: Xabier Gabiña Barañano
Script para la implementación del algoritmo kNN
Recoge los datos de un fichero csv y los clasifica en función de los k vecinos más cercanos
"""

import sys
import sklearn as sk
import numpy as np
import pandas as pd
import pickle

def load_data(file):
    """
    Función para cargar los datos de un fichero csv
    :param file: Fichero csv
    :return: Datos del fichero
    """
    data = pd.read_csv(file)
    return data

def calculate_precision(y_test, y_pred):
    """
    Función para calcular la precision
    :param y_test: Valores reales
    :param y_pred: Valores predichos
    :return: Precision
    """
    from sklearn.metrics import precision_score
    precision = precision_score(y_test, y_pred, average='macro')    
    return precision
    
def calculate_recall(y_test, y_pred):
    """
    Función para calcular el recall
    :param y_test: Valores reales
    :param y_pred: Valores predichos
    :return: recall
    """

    from sklearn.metrics import recall_score
    recall = recall_score(y_test, y_pred, average='macro')
    return recall
    
def calculate_fscore(y_test, y_pred):
    """
    Función para calcular el F-score
    :param y_test: Valores reales
    :param y_pred: Valores predichos
    :return: F-score (micro), F-score (macro), F-score (weighted)
    """
    from sklearn.metrics import f1_score
    import numpy as np
    num_classes = len(np.unique(y_test))	#mira si es clasificación binaria o multiclase
    
 # Clasificación binaria
    if num_classes == 2:
        f1 = f1_score(y_test, y_pred, average=None)
        f1_mean = np.mean(f1) 
        return f1_mean, None, None

    # Clasificación multiclase
    else:
        f1_macro = f1_score(y_test, y_pred, average='macro')
        f1_micro = f1_score(y_test, y_pred, average='micro')
        f1_weighted = f1_score(y_test, y_pred, average='weighted')

        return f1_macro, f1_micro, f1_weighted

def calculate_confusion_matrix(y_test, y_pred):
    """
    Función para calcular la matriz de confusión
    :param y_test: Valores reales
    :param y_pred: Valores predichos
    :return: Matriz de confusión
    """
    from sklearn.metrics import confusion_matrix
    cm = confusion_matrix(y_test, y_pred)
    return cm

def kNN(data, k, weights, p):
    """
    Función para implementar el algoritmo kNN
    
    :param data: Datos a clasificar
    :type data: pandas.DataFrame
    :param k: Número de vecinos más cercanos
    :type k: int
    :param weights: Pesos utilizados en la predicción ('uniform' o 'distance')
    :type weights: str
    :param p: Parámetro para la distancia métrica (1 para Manhattan, 2 para Euclídea)
    :type p: int
    :return: Clasificación de los datos
    :rtype: tuple
    """
    # Seleccionamos las características y la clase
    X = data.iloc[:, :-1].values # Todas las columnas menos la última
    y = data.iloc[:, -1].values # Última columna
    
    # Dividimos los datos en entrenamiento y test
    from sklearn.model_selection import train_test_split
    np.random.seed(42)  # Set a random seed for reproducibility
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
    
    # Escalamos los datos
    from sklearn.preprocessing import StandardScaler
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)
    
    # Entrenamos el modelo
    from sklearn.neighbors import KNeighborsClassifier
    classifier = KNeighborsClassifier(n_neighbors = k, weights = weights, p = p)
    classifier.fit(X_train, y_train)
    
    # Predecimos los resultados
    y_pred = classifier.predict(X_test)
    
    return y_test, y_pred, classifier

if __name__ == "__main__":
    # Comprobamos que se han introducido los parámetros correctos
    if len(sys.argv) < 2:
        print("Error en los parámetros de entrada")
        print("Uso: kNN.py <fichero*> ")
        sys.exit(1)
    
    # Cargamos los datos
    data = load_data(sys.argv[1])
    
    #Definimos una lista con los valores que nos interesa probar para cada hiperparámetro
    k_values = [1, 3, 5]
    p_values = [1, 2]
    weights_values = ['uniform', 'distance']
    resultados = []
    best_f1 = 0
    best_model = None
    best_params = None
    
    #Bucle principal, itera sobre cada combinación y entrena el modelo con cada una de ellas
    for k in k_values:
    	for p in p_values:
    		for w in weights_values:
    			y_test, y_pred, model = kNN(data, k, w, p)
    			
    			#Calcula el rendimiento del modelo
    			recall = calculate_recall(y_test, y_pred)
    			f_macro, f_micro, f_weighted = calculate_fscore(y_test, y_pred)
    			precision = calculate_precision(y_test, y_pred)
    			print("\nHiperparámetros del modelo entrenado:")
    			print(k,w,p)
    			print("F1 M, F1 m, F1 w, precision, recall:")
    			print(f_macro, f_micro, f_weighted, precision, recall)
    			
    			#Guarda los resultados de este modelo en una lista temporal
    			resultados.append([k, p, w, precision, recall, f_macro, f_micro, f_weighted])
    			
    			#Compara el fscore del modelo que acaba de entrenar con el mejor hasta el momento y guarda el
    			#que haya tenido mejor rendimiento
    			if f_macro > best_f1:
    				best_f1 = f_macro
    				best_model = model
    				best_params = (k, w, p)
    print("\nMEJORES RESULTADOS")
    print("Mejor fscore")
    print(best_f1)
    print("Mejor modelo")				
    print(best_f1, best_model, best_params)
    
    #Guarda los datos que habia almacenado temporalmente en una lista en un .csv  
    results_df = pd.DataFrame(resultados,columns=["K","P","W","PRECISION","RECALL","F1 MACRO","F1 MICRO","F1 WEIGHTED"])
    results_df.to_csv("resultados_knn.csv", index=False)
    print("\nResultados guardados en resultados_knn.csv")
    
    #Regenera el mejor modelo 
    k_best, w_best, p_best = best_params
    y_test, y_pred, best_model = kNN(data, k_best, w_best, p_best)
    
    #Guarda el mejor modelo
    pickle.dump(best_model, open("best_knn_model.sav", "wb"))
    print("\nMejor modelo guardado en best_knn_model.sav")
    
    #Carga el modelo guardado
    loaded_model = pickle.load(open("best_knn_model.sav", "rb"))
    print("\nModelo cargado correctamente")
    			
    			
    		
