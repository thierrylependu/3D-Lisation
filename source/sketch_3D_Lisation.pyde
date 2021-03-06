'''
Sans paquets UDP
Rotation d'une figure en utilisant la souris et les fleches haut et bas
Zoom sur la figure avec la roulette de la souris
Avec paquets UDP
Rotation de la figure avec le gyroscope du téléphone
Zoom sur la figure avec l'écran tactile
'''

import socket
from struct import *
import os
from subprocess import check_output

#Recupere l'adresse IP de la machine
UDP_IP = check_output(['hostname', '--all-ip-addresses'])
UDP_PORT = 50000  
sock = socket.socket(socket.AF_INET, # Internet
socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))


#Initialisation des variables globales
z = 0
zoom = 0
zPlus = False
zMoins = False

 
def setup():
    size(800, 800, P3D)
    
#Creer les cylindres de la figure   
def cylinder(bottom, top, h, sides):
    pushMatrix()
    translate(0,h/2,0)
    angle = 0
    x = [0]*(sides+1)
    z = [0]*(sides+1)
    x2 = [0]*(sides+1)
    z2 = [0]*(sides+1)
    #get the x and z position on a circle for all the sides
    for i in range(len(x)):
        angle = TWO_PI/(sides)*i
        x[i] = sin(angle) * bottom
        z[i] = cos(angle) * bottom
    for i in range(len(x)):
        angle = TWO_PI/(sides) * i
        x2[i] = sin(angle)*top
        z2[i]= cos(angle)*top
    #draw the bottom of the cylinder
    beginShape(TRIANGLE_FAN)
    vertex(0, -h/2, 0)
    for i in range(len(x)):
        vertex(x[i], -h/2, z[i])
    endShape()
    #draw the center of the cylinder
    beginShape(QUAD_STRIP)
    for i in range(len(x)):
        vertex(x[i], -h/2, z[i])
        vertex(x2[i], h/2, z2[i])
    endShape()
    #draw the top of the cylinder
    beginShape(TRIANGLE_FAN)   
    vertex(0, h/2, 0)
    for i in range(len(x)):
        vertex(x2[i], h/2, z2[i])
    endShape()
    popMatrix()
   

#Sans l'utilisation du telephone
'''
def mouseWheel(event):
    e = event.getCount()
    global zoom
    if e < 0 :
        zoom += 10
    else :
        zoom -= 10
    
    
def keyPressed():
    if key == CODED:
        if keyCode == UP :
            global zPlus 
            zPlus = False
        if keyCode == DOWN:
            global zMoins 
            zMoins = False
def keyReleased():
    if key == CODED:
        if keyCode == UP :
            global zPlus 
            zPlus = False
        if keyCode == DOWN:
            global zMoins 
            zMoins = False
'''
    
#Permet de quitter le programme avec la touche echap
def keyPressed():
    if key == CODED:
        if keyCode == ESC :
            exit()
#Permet de zoomer
def Zoomer():
    data, addr = sock.recvfrom(1024)
    global zoom
    xS = "%1.4f" %unpack_from ('!f', data, 8)
    x = float(xS)
    if x < 0:
        zoom -= 10
    else:
        zoom += 10
    

    
def draw():
    background(50)
    lights()
    fill(255)
    translate(width/2, height/2, zoom)    
    #recoit les paquets UDP
    data, addr = sock.recvfrom(1024)
    
    #Sans le telephone
    '''
    y = mouseX
    x = mouseY
    if zPlus == True:
        global z
        z += 200
    if zMoins == True:
        global z
        z -= 200'''
    
    #transforme les donnees du paquet en float
    yS = "%1.4f" %unpack_from ('!f', data, 36)
    xS = "%1.4f" %unpack_from ('!f', data, 44)
    zS = "%1.4f" %unpack_from ('!f', data, 40)
    y = float(yS)
    x = float(xS)
    z = float(zS)
    
    
    listeTouche = [64, 68, 72, 76, 80, 84, 88, 92]
    for i in listeTouche:
        touche = "%1.4f" %unpack_from ('!f', data, i)
        #verifie si une touche est appuye
        if float(touche) != 0:
            Zoomer()
        else:
            round(x,1)
            round(y,1)
            round(z,1)
            rotateX(radians(x/2))
            rotateY(radians(y/2)) 
            rotateZ(radians(z/2))
    
    #Construit la figure
    largeurmin = 100
    longueurmin = 140
    hauteur = 10
    cote = 50
    box(largeurmin+(3*hauteur), hauteur, longueurmin+(3*hauteur))
    translate(0, hauteur, 0)
    box(largeurmin+(2*hauteur), hauteur, longueurmin+(2*hauteur))
    translate(0, hauteur, 0)
    box(largeurmin+hauteur, hauteur, longueurmin+hauteur)
    translate(0, hauteur, 0)
    box(largeurmin, hauteur, longueurmin)
    translate(0, 105, 0)
    beginShape()
    vertex(-50, 0, -70)
    vertex( 50, 0, -70)
    vertex( 0, 20, -70)
    endShape()
    beginShape()
    vertex( 0, 20, 70)
    vertex( 50, 0, 70)
    vertex(-50, 0, 70)
    endShape()
    beginShape()
    vertex( 50, 0, -70)
    vertex( 0, 20, -70)
    vertex( 0, 20, 70)
    vertex( 50, 0, 70)
    endShape()
    beginShape()
    vertex(-50, 0, -70)
    vertex( 0, 20, -70)
    vertex( 0, 20, 70)
    vertex(-50, 0, 70)
    endShape()
    beginShape()
    vertex(-50, 0, -70)
    vertex( 50, 0, -70)
    vertex( 50, 0, 70)
    vertex(-50, 0, 70)
    endShape()
    translate(0, -105, 0)
    translate(30, 5, 50)
    cylinder(6,6,100,cote)
    translate(0, 0, -20)
    cylinder(6,6,100,cote)
    translate(0, 0, -20)
    cylinder(6,6,100,cote)
    translate(0, 0, -20)
    cylinder(6,6,100,cote)
    translate(0, 0, -20)
    cylinder(6,6,100,cote)
    translate(0, 0, -20)
    cylinder(6,6,100,cote)
    translate(-60, 0, 0)
    cylinder(6,6,100,cote)
    translate(0, 0, 20)
    cylinder(6,6,100,cote)
    translate(0, 0, 20)
    cylinder(6,6,100,cote)
    translate(0, 0, 20)
    cylinder(6,6,100,cote)
    translate(0, 0, 20)
    cylinder(6,6,100,cote)
    translate(0, 0, 20)
    cylinder(6,6,100,cote)
