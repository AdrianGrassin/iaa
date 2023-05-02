# Universidad de La Laguna
# Escuela Superior de Ingeniería y Tecnología
# Grado en Ingeniería Informática
# Asignatura: Inteligencia Artificial Avanzada
# Curso: 2022-2023
# Alumno: Adrián Grassin Luis
# Fecha: 4/18/2023
# Email: alu0101349480@ull.edu.es
#
# Programa: Generador de lenguajes de modelos
# Descripción: Programa que genera los lenguajes de modelos a partir de un csv.

import math
import argparse
from vocabulary import preprocessArticle

def filter_feeling(file_data):
    pos_model = []
    neg_model = []
    neut_model = []
    # filtramos los modelos
    for line in file_data.splitlines():
        if line.endswith('negative'):
            neg_model.append(line)
        elif line.endswith('positive'):
            pos_model.append(line)
        elif line.endswith('neutral'):
            neut_model.append(line)
    # prerprocesamos los articulos
    pos_model = [preprocessArticle(line) for line in pos_model]
    neg_model = [preprocessArticle(line) for line in neg_model]
    neut_model = [preprocessArticle(line) for line in neut_model]
    return pos_model, neg_model, neut_model

def getFrecuenciaSuavizadoLaplaciano(frecuencia, total_palabras, total_vocabulario):
  return math.log((frecuencia + 1) / ((total_palabras + total_vocabulario) + 1))

def write_corpus_to_file(model, filename):
    for line in model:
        filename.write(line + '\n')

def get_word_info(word, model, vocabulario_length):
    frecuencia = 0
    numero_palabras = 0
    for line in model:
        numero_palabras += len(line.split())
        if word in line.split():
            frecuencia += 1
    
    return "Palabra: " + word + " Frecuencia: " + str(frecuencia) + " LogProb: " + str(getFrecuenciaSuavizadoLaplaciano(frecuencia, numero_palabras, vocabulario_length)) + "\n"

def write_model_to_file(model, filename, vocabulario_length, word):
    filename.write(get_word_info(word, model, vocabulario_length))

def write_header_to_file(model, filename):
    with open(filename, 'a') as file:
        file.write("Numero de documentos (noticias) del corpus: " + str(len(model)) + "\n")
        file.write("Numero de palabras del corpus: " + str(sum(len(line.split()) for line in model)) + "\n")

def clear_output_files():
    open('./corpus/Corpus_P.txt', 'w').close()
    open('./corpus/Corpus_N.txt', 'w').close()
    open('./corpus/Corpus_T.txt', 'w').close()
    open('./langmod/modelo_lenguaje_P.txt', 'w').close()
    open('./langmod/modelo_lenguaje_N.txt', 'w').close()
    open('./langmod/modelo_lenguaje_T.txt', 'w').close()


####

def main(training_file):

    # limpiamos los archivos de salida si existen
    clear_output_files()

    # abrimos el archivo csv y lo leemos
    if(training_file == None):
        training_file = 'F75_train.csv'
    
    corpusP = open('./corpus/Corpus_P.txt', 'w')
    corpusN = open('./corpus/Corpus_N.txt', 'w')
    corpusT = open('./corpus/Corpus_T.txt', 'w')

    with open('./datafiles/F75_train.csv', 'r', encoding='utf8') as file:
        file_data = file.read()
        pos_model, neg_model, neut_model = filter_feeling(file_data)
    
    write_corpus_to_file(pos_model, corpusP)
    write_corpus_to_file(neg_model, corpusN)
    write_corpus_to_file(neut_model, corpusT)

    corpusP.close()
    corpusN.close()
    corpusT.close()

    # obtenemos el tamaño del vocabulario
    with open('vocabulario.txt', 'r', encoding='utf8') as vocabulario:
        next(vocabulario)
        vocabulario_length = sum(1 for _ in vocabulario)

    # escribimos los headers
    write_header_to_file(pos_model, './langmod/modelo_lenguaje_P.txt')
    write_header_to_file(neg_model, './langmod/modelo_lenguaje_N.txt')
    write_header_to_file(neut_model, './langmod/modelo_lenguaje_T.txt')

    # escribimos los modelos

    modelLenP = open('./langmod/modelo_lenguaje_P.txt', 'w')
    modelLenN = open('./langmod/modelo_lenguaje_N.txt', 'w')
    modelLenT = open('./langmod/modelo_lenguaje_T.txt', 'w')

    with open('vocabulario.txt', 'r', encoding='utf8') as vocabulario:
        next(vocabulario)
        for word in vocabulario:
            word = word.strip()
            write_model_to_file(pos_model, modelLenP, vocabulario_length, word)
            write_model_to_file(neg_model, modelLenN, vocabulario_length, word)
            write_model_to_file(neut_model, modelLenT, vocabulario_length, word)

    modelLenP.close()
    modelLenN.close()
    modelLenT.close()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Programa que genera los modelos de lenguaje a partir de un archivo y el vocabulario")
    parser.add_argument('--data', nargs=1, help='Indicas la ruta al archivo a procesar')
    args = parser.parse_args()
    main(args)



