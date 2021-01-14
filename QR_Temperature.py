from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import numpy as np
import pandas as pd 
import cv2
import time
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import serial

global temperature 

def decode(im,password) :
  # Find barcodes and QR codes
  decodedObjects = pyzbar.decode(im)

  # Print results
  for obj in decodedObjects:
    #print('Type : ', obj.type)
    #print('Data : ', str(obj.data),'\n')
    password.append(str(obj.data.decode("utf-8")))   
  return decodedObjects


# Display barcode and QR code location
def display(im, decodedObjects):

  # Loop over all decoded objects
  for decodedObject in decodedObjects:
    points = decodedObject.polygon

    # If the points do not form a quad, find convex hull
    if len(points) > 4 :
      hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
      hull = list(map(tuple, np.squeeze(hull)))
    else :
      hull = points;
    # Number of points in the convex hull
    n = len(hull)
    # Draw the convext hull
    for j in range(0,n):
      cv2.line(im, hull[j], hull[ (j+1) % n], (255,0,0), 3)
  # Display results
  return im



def QR_access():
  # Read image
  cap = cv2.VideoCapture(0)
  password = []
  while(True):
    # Capture frame-by-frame
    ret, im = cap.read()
    decodedObjects = decode(im,password)
    im = display(im, decodedObjects)
    # Display the resulting frame
    if len(decodedObjects) == 0:
      im = cv2.putText(im,'Escanea tu codigo QR para ingresar', (40,40), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
      cv2.imshow('frame',im)
    elif len(decodedObjects) != 0:
      if len(password) and password[0] == '12345':
        im = cv2.putText(im,'Sea bienvenido QR correcto ', (100,60), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,255),2)
        cv2.imshow('frame',im)
        cv2.waitKey(2500)
        cv2.destroyAllWindows()
        password.clear()
        decodedObjects.clear()
        return True
      else:
        im = cv2.putText(im,'Acceso denegado QR incorrecto',(100,60), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,255),2)
        cv2.imshow('frame',im)
        cv2.waitKey(2500)
        cv2.destroyAllWindows()
        password.clear()
        decodedObjects.clear()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break      
  # When everything done, release the capture
  cap.release()
  cv2.destroyAllWindows()
  return False

class App():
  def __init__(self):
    self.data = ""
    self.gui = Tk() 
    self.gui.config(bg="white")
    self.gui.resizable(0,0)
    self.gui.title("Registro de temperatura") 
    self.myframe = Frame()
    self.myframe.pack(fill="both",expand="True")
    #change color de frame
    self.myframe.config(bg="white")
    self.myframe.config(width="650",height="500")
    self.myframe.config(bd=35)
    self.myframe.config(relief="groove")
    self.myframe.config(cursor="hand2")

    self.zero_frame = Frame(self.myframe, bg="white")
    self.zero_frame.grid(row=0, column=0)

    self.first_frame = Frame(self.myframe, bg="white")
    self.first_frame.grid(row=1, column=0)

    self.temperature = StringVar()

    self.labelSend = Label(self.first_frame, text="Ingrese su temperatura (ºC)")
    self.labelSend.grid(row=0,column=0,padx=10,pady=5)
    self.labelSend.config(fg="red",justify="left")
    self.labelSend.config(bd=10)

    self.labelTemperature = Entry(self.first_frame,textvariable = self.temperature, bg="white")
    self.labelTemperature.grid(row=1,column=0,padx=10,pady=5)
    self.labelTemperature.config(fg="red",justify="center")
    self.labelTemperature.config(bd=10)

    self.B1 = Button(self.first_frame,text="Enviar temperatura",fg="red",command = self.CallBackButton)  
    self.B1.grid(row=1,column=1,sticky="e",padx=30,pady=5)  

    self.gui.mainloop()
    
  def CallBackButton(self):
    text = str(self.temperature.get())
    if text.isdigit():
      if int(text) > 37:
        self.data = "enfermo"
        messagebox.showwarning(message="Ir a servicio medico.", title="Warnnig")
        arduino = serial.Serial('/dev/ttyUSB0', 9600)
        time.sleep(2)
        arduino.write(b'0')
        arduino.close()
        self.gui.destroy()
      elif int(text) < 0:
        messagebox.showinfo(message="La temperatura debe ser positiva.", title="Message")
      else:
        self.data = "sano"
        messagebox.showinfo(message="Puede accesar.", title="Message")
        arduino = serial.Serial('/dev/ttyUSB0', 9600)
        time.sleep(2)
        arduino.write(b'1')
        arduino.close()
        self.gui.destroy()
    else:
      messagebox.showinfo(message="Escribe la temperatura en numeros enteros por favor.", title="Alert")

  def Health(self):
    return self.data

# Main
if __name__ == '__main__':
  number = []
  health = []
  i = 0
  while True:
    if QR_access():
      Apk = App()
      i = i+1 
      number.append(i)
      health.append(Apk.Health())
      dict = {'Persona': number, 'Salud': health}  
      df = pd.DataFrame(dict) 
      df.to_csv('file_name.csv')



