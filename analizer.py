#Analizes texts and returns writes two output files:
# - clasificacion_alu0101349480.txt
#   + <primeros 10 caracteres de la noticia>,<lp en P>,<lp en N>,<lp en T>,<P/N/T>
#   (siendo lp el logaritmo neperiano de la probabilidad de la noticia en el modelo correspondiente con 2 decimales)
# - resumen_alu0101349480.txt
#   + <P/N/T>

import argparse
from vocabulary import preprocessArticle

def getmodel(filename):
    model = {}
    with open(filename, 'r') as file:
        for line in file:
            word = line.split()[1]
            logprob = line.split()[5]
            model[word] = logprob
    return model


# reads the data file that will be analized and preprocesed and returns the output data with the classification
def getoutputdata(filename, posModel, negModel, neutModel):
   outputdata = ''
   with open(filename, 'r') as inputfile:
    filedata = inputfile.read()
    for line in filedata.splitlines():
        if line == ',':
            continue
        
        line = preprocessArticle(line)
        logprobP = 0
        logprobN = 0
        logprobT = 0
        for word in line.split():
            if word in posModel:
                logprobP += float(posModel[word])
            if word in negModel:
                logprobN += float(negModel[word])
            if word in neutModel:
                logprobT += float(neutModel[word])
        
        if logprobP > logprobN and logprobP > logprobT:
            classification = 'P'
        elif logprobN > logprobP and logprobN > logprobT:
            classification = 'N'
        else:
            classification = 'T'

        outputdata += line[:10] + ',' + str(round(logprobP, 2)) + ',' + str(round(logprobN, 2)) + ','+ str(round(logprobT, 2)) + ',' + classification + '\n'
    return outputdata
   
# reads the already classified data file and writes the output file 
def writeResume(filename):
    trainingfile = open(filename, 'r')
    trainingdata = trainingfile.read()
    with open('./results/resumen_train.txt', 'w') as outputfile:
        for line in trainingdata.splitlines():
            if(line[-8:] == 'positive'):
                 outputfile.write('P\n')
            elif(line[-8:] == 'negative'):
                 outputfile.write('N\n')
            else:
                outputfile.write('T\n')
        trainingfile.close()
   
# compares the output file with the already classified data file and prints the accuracy
def printAccuracy():
    with open('./results/resumen_alu0101349480.txt', 'r') as outputfile:
        with open('./results/resumen_train.txt', 'r') as trainingfile:
            outputdata = outputfile.read()
            trainingdata = trainingfile.read()
            correct = 0
            total = 0
            for line in outputdata.splitlines():
                if(line == trainingdata.splitlines()[total]):
                    correct += 1
                total += 1

    print('Accuracy: {:0.2f}'.format((correct/total) * 100) + '%')


def main(args):
    posModel = getmodel('./langmod/modelo_lenguaje_P.txt')
    negModel = getmodel('./langmod/modelo_lenguaje_N.txt')
    neutModel = getmodel('./langmod/modelo_lenguaje_T.txt')

    # reads the data file that will be analized and returns the output data

    if args.files.__len__() == 2:
        archivo_analizar, archivo_test = args.files
    else:
        archivo_analizar = None
        archivo_test = None
        
    if(archivo_analizar):
        filename = archivo_analizar
    else:
        filename = './datafiles/eval_first.csv'

    outputdata = getoutputdata(filename, posModel, negModel, neutModel)
     
    # write the output data to the output file
    with open('./results/clasificacion_alu0101349480.txt', 'w') as outputfile:
        outputfile.write(outputdata)

    # write the resume file
    with open('./results/resumen_alu0101349480.txt', 'w') as outputfile:
        for line in outputdata.splitlines():
            outputfile.write(line[-1] + '\n')   

    # if a test file is given, print the accuracy
    if(archivo_test):
        filename = archivo_test
        writeResume(filename)  
        printAccuracy()
    



if __name__ == '__main__':
    args = argparse.ArgumentParser(description="Analiza un texto y si se le pasa un fichero de comparación, devuelve la precisión del modelo")
    args.add_argument('-f', '--files', nargs="+", help='Ficheros de entrenamiento y de testeo')
    args = args.parse_args()
    main(args)

      
      

          