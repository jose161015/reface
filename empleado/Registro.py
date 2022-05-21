import cv2
import os
import numpy



def entrenar():
    dataPath = os.getcwd()
    dataPath = os.path.join(dataPath,"CoreDatos") #Cambia a la ruta donde hayas almacenado Data
    peopleList = os.listdir(dataPath)
    #print('Lista de personas: ', peopleList)
    print("PathCore: " + dataPath)


    labels = []
    facesData = []
    label = 0


    for nameDir in peopleList:
        #personPath = os.path.join(dataPath,nameDir)
        personPath = dataPath  + "/" + nameDir
        
        for fileName in os.listdir(personPath):
            #print('Rostros: ', nameDir + '/' + fileName)
            labels.append(label)
            facesData.append(cv2.imread(personPath+'/'+fileName,0))
            #image = cv2.imread(personPath+'/'+fileName,0)
            #cv2.imshow('image',image)
            #cv2.waitKey(10)
        label = label + 1

    print('labels= ',labels)
    #print('Numero de etiquetas 0: ',np.count_nonzero(np.array(labels)==0))
    #print('Numero de etiquetas 1: ',np.count_nonzero(np.array(labels)==1))

    # Métodos para entrenar el reconocedor
    #face_recognizer = cv2.face.EigenFaceRecognizer_create()
    #face_recognizer = cv2.face.FisherFaceRecognizer_create()
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Entrenando el reconocedor de rostros
    print("Aprendiendo rostros...")
    face_recognizer.train(facesData, numpy.array(labels))

    # Almacenando el modelo obtenido
    #face_recognizer.write('modeloEigenFace.xml')
    #face_recognizer.write('modeloFisherFace.xml')
    face_recognizer.write('modeloLBPHFace.xml')
    print("Modelo de rostros listo...")