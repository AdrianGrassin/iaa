############ UNIVERSIDAD DE LA LAGUNA ############
#
# Asignatura: Inteligencia Artificial Avanzada
# Curso: 2022-2023
# Alumno: Adrián Grassin Luis
# Fecha: 4/18/2023
# Email: alu0101349480@ull.edu.es    
#    
# Requerimientos del programa: 
#  - A continuación se listan los paquetes necesarios para ejecutar el programa y su instalación.
#  - Se recomienda utilizar un entorno virtual para instalar los paquetes.
#
#                              Python 3.9.7 o superior
#                              nltk 3.6.2           | pip install nltk
#                              emoji 1.6.1          | pip install emoji
#                              argparse 1.1 
#                   (opcional) spellchecker 0.6.3   | pip install pyspellchecker
#
#
# Descripción: Programa que genera el vocabulario a partir de un archivo.
#              He decidido prescindir de la librería spellchecker ya que se toma demasiado tiempo en ejecutar.
#
# Uso: python vocabulary.py --train <ruta al archivo a procesar>
#     - por defecto se procesa el archivo "F75_train.csv" suministrado por el profesor
#     - el vocabulario se genera en el archivo "vocabulario.txt"
# # #


import nltk
import emoji
import argparse

# import spellchecker
# #

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
# from spellchecker import SpellChecker
# #

#
# Definición de funciones
#
def tokenize(texto):
  return nltk.word_tokenize(texto.lower())

def eliminarRepeticiones(tokens):
  return list(set(tokens))

def eliminarStopwords(tokens):
  stop_words = set(stopwords.words('english'))
  return [palabra for palabra in tokens if not palabra in stop_words]

def eliminarPuntuacion(tokens):
  return [palabra for palabra in tokens if palabra.isalpha()]

def eliminarNumbers(tokens):
  return [palabra for palabra in tokens if not palabra.isdigit()]

def eliminarEmojis(tokens):
  return [palabra for palabra in tokens if not emoji.is_emoji(palabra)]

def eliminarURLS(tokens):
  return [palabra for palabra in tokens if not palabra.startswith('http')]

def eliminarHashtags(tokens):
  return [palabra for palabra in tokens if not palabra.startswith('#')]

def truncar(tokens):
  stemmer = PorterStemmer()
  return [stemmer.stem(tokens) for tokens in tokens]

def lematizar(tokens):
  lemmatizer = nltk.stem.WordNetLemmatizer()
  return [lemmatizer.lemmatize(tokens) for tokens in tokens]

def preprocessTokens(tokens):
  tokens = tokenize(tokens)
  tokens = eliminarRepeticiones(tokens)
  tokens = eliminarEmojis(tokens)
  tokens = eliminarNumbers(tokens)
  tokens = eliminarPuntuacion(tokens)
  tokens = eliminarURLS(tokens)
  tokens = eliminarHashtags(tokens)
  tokens = lematizar(tokens)
  # tokens = truncar(tokens)
  # tokens = correctorOrtografico(tokens) # se toma mucho tiempo
  tokens = eliminarRepeticiones(tokens)
  tokens.sort()
  return tokens

def preprocessArticle(articles):
  tokens = tokenize(articles)
  tokens = eliminarRepeticiones(tokens)
  tokens = eliminarEmojis(tokens)
  tokens = eliminarNumbers(tokens)
  tokens = eliminarPuntuacion(tokens)
  tokens = eliminarURLS(tokens)
  tokens = eliminarHashtags(tokens)
  tokens = lematizar(tokens)
  # tokens = truncar(tokens)
  tokens = ' '.join(tokens)
  return tokens

# def correctorOrtografico(tokens):
#   spell = SpellChecker()
#   return [spell.correction(palabra) for palabra in tokens]
# #

# #
# Codigo principal del programa

def main(args):
  trainfile = './datafiles/F75_train.csv'
  if(args.train):
    print("Procesando el archivo de entrenamiento: \"" + args.train[0] + "\"")
    trainfile = args.train[0]
    
# abrimos el archivo csv y lo leemos
  with open(trainfile, newline='', encoding='utf-8') as csvfile:
    contenido = csvfile.read()

  # procesamos el contenido
  tokens = preprocessTokens(contenido)

  # escribimos los tokens en el archivo vocabulario.txt
  with open('vocabulario.txt', 'w', encoding='utf-8') as archivo:
    archivo.write("Numero de palabras: " + str(len(tokens)) + '\n')
    for palabra in tokens:
      archivo.write(palabra + '\n')


# punto de entrada al programa principal donde se parsean los argumentos
if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Programa que genera el vocabulario a partir de un archivo")
  parser.add_argument('--train', nargs=1, help='Indicas la ruta al archivo a procesar')
  args = parser.parse_args()
  main(args)