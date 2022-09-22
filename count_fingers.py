import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

tipIds = [4, 8, 12, 16, 20]

# Definir una función para contar dedos
def countFingers(image, hand_landmarks, handNo=0):
    if hand_landmarks:
        hand1 = hand_landmarks[handNo].landmark
        print(hand1)
        dedos = []
        for id in tipIds:
            dedoIncial_y = hand1[id].y
            dedoAbajo_y = hand1[id-2].y
            if id != 4:
                if dedoIncial_y < dedoAbajo_y:
                    dedos.append(1)
                    print("El dedo está abierto")
                if dedoAbajo_y > dedoIncial_y:
                    dedos.append(0)
                    print("El dedo está cerrado") 
        dedosCount = dedos.count(1)
        text = f"Dedos: {dedosCount}"
        cv2.putText(image, text, (50,50) , cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)               
                        

# Definir una función para
def drawHandLanmarks(image, hand_landmarks):

    # Dibujar conexiones entre los puntos de referencia
    if hand_landmarks:

      for landmarks in hand_landmarks:
               
        mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)


while True:
    success, image = cap.read()

    image = cv2.flip(image, 1)
    
    # Detectar los puntos de referencia de las manos
    results = hands.process(image)

    # Obtener la posición de los puntos de referencia del resultado procesado
    hand_landmarks = results.multi_hand_landmarks

    # Dibujar puntos de referencia
    drawHandLanmarks(image, hand_landmarks)

    # Obtener la posición de los dedos de la mano
    countFingers(image, hand_landmarks)

    cv2.imshow("Controlador de medios", image)

    # Cerrar la ventana al presionar la barra espaciadora
    key = cv2.waitKey(1)
    if key == 32:
        break

cv2.destroyAllWindows()
