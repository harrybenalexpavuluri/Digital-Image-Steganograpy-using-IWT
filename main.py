import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image, ImageOps
import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


canvas_width = 400
canvas_height =400

root = tk.Tk()
frame = tk.Frame(root)
frame.pack()

def fun1():
    global img, file_path
    
    file_path = filedialog.askopenfilename()
    canvas = Canvas(root, width = 300, height = 300)  
    canvas.pack()  
    img = ImageTk.PhotoImage(Image.open(file_path))  
    canvas.create_image(20, 20, anchor=NW, image=img)
def fun2():
    global img1, file_path1
    
    file_path1 = filedialog.askopenfilename()
    canvas = Canvas(root, width = 300, height = 300)  
    canvas.pack()  
    img1 = ImageTk.PhotoImage(Image.open(file_path1))  
    canvas.create_image(20, 20, anchor=NW, image=img1)

def embed():
    imgg1 = img
    imgg2 = img1

    c_img = cv2.imread(file_path, 0)
    c_img = cv2.resize(c_img, (256, 256))

    m_img = cv2.imread(file_path1, 0)
    m_img = cv2.resize(m_img, (256, 256))
    m_img[m_img>0] = 1

    
    c_flatten = c_img.flatten()
    m_flatten = m_img.flatten()

    print(c_flatten.shape)
    print(m_flatten.shape)

    out = []
    for a, b in zip(c_flatten, m_flatten):
        a = np.binary_repr(a, width=8)
        xor_a = int(a[1]) ^ int(a[2])
        xor_b = int(a[0]) ^ xor_a
        xor_c = int(b) ^ xor_b 
        save = a[:-1] + str(xor_c)
        out.append(int(save, 2))

    stego_img = np.array(out)
    stego_img = np.reshape(stego_img, (256, 256))
    os.remove(file_path1)
    cv2.imwrite('stego.png',stego_img)

    canvas = Canvas(root, width = 300, height = 300)  
    canvas.pack()  
    img3 = ImageTk.PhotoImage(Image.open('stego.png'))  
    canvas.create_image(20, 20, anchor=NW, image=img3)

def encode():

    file_path = filedialog.askopenfilename()
    img4 = ImageTk.PhotoImage(Image.open(file_path))

    stego_img = img4 #cv2.imread("stego.png", 0)
    stego_flatten = stego_img.flatten()

    out = []
    for x in stego_flatten:
        # step 2: change pixel value to binary
        x = np.binary_repr(x, width=8)

        # step 3: perform XOR on 7th and 6th bits
        xor_a = int(x[1]) ^ int(x[2])
        
        # step 4: perform XOR operation on 8th bit with xor_a
        xor_b = int(x[0]) ^ xor_a
        
        # step 5: perform XOR operations on message bits with 3 MSB
        xor_c = int(x[-1]) ^ xor_b
        
        out.append(int(xor_c))

    recover_img = np.reshape(np.array(out), (256,256))
    recover_img[recover_img==1] = 255

    cv2.imwrite('git.png',recover_img)
     
    


button1 = tk.Button(frame, 
                   text="Select Display Image",
                   command=fun1)
button1.pack(side=tk.LEFT)

button2 = tk.Button(frame, 
                   text="Select Hidden Image",
                   command=fun2)
button2.pack(side=tk.LEFT)
button2 = tk.Button(frame, 
                   text="Embed Image",
                   command=embed)
button2.pack(side=tk.LEFT)
button2 = tk.Button(frame, 
                   text="Extract Image",
                   command=encode)
button2.pack(side=tk.LEFT)

root.mainloop()


