import pygame as pg
import math
import random 
from colorsys import hsv_to_rgb


# Constantes :
FPS = 60  # les fps tabernak
WIND = 750 # dimentions de la fentere
size=10 # la taille de la map
shadow=10 # l'assombirssemnt à distance
main_coul=random.random() # la couleur principale (hue) de 0 à 1
agl=90 #L'ouverture de l'oeil
speed=0.1 # La vitesse de déplacement

def sgt(x1,y1,yp1,couleure=0xffffff):
    """tracer un segment vertical"""
    pg.draw.line(f,couleure,
                 (x1*WIND,(up+0.5-y1)*WIND),
                 (x1*WIND,(up+0.5-yp1)*WIND),
                 5)
#--- Génération de la map
carte:list=[]
for y in range(size):
    carte.append([])
    for x in range(size):
        carte[y].append(2)
posx,posy=1,1
while posx in range(size-1) and posy in range(size-1):
    carte[posy][posx]=0
    xp,yp=posx,posy
    while xp in range(size-1) and yp in range(size-1):
        carte[yp][xp]=0
        if random.randint(0,1):
            xp+=1
        else:
            yp+=1
    if random.randint(0,1):
        posx+=1
    else:
        posy+=1
nouv=[list([1 for i in range(size)])]
for y in range(1,len(carte)-3):
    nouv.append([2])
    for x in range(1,len(carte[y])-3):
        if carte[y][x]==1:
            total=carte[y-1][x-1]+\
                    carte[y-1][x]+\
                    carte[y-1][x+1]+\
                    carte[y][x-1]+\
                    carte[y][x+1]+\
                    carte[y+1][x-1]+\
                    carte[y+1][x]+\
                    carte[y+1][x+1]
            if total==8:
                nouv[y].append(0)
            else:
                nouv[y].append(1)
        else:
            nouv[y].append(0)
    nouv[y].append(1)
nouv.append(list([1 for i in range(size)])) 
for i in range(len(carte)):
    for j in range(len(carte[i])):
        if carte[i][j]==1:
            carte[i][j]=random.random()
        elif carte[i][j]==2:
            carte[i][j]=main_coul
#----- Fin de la génération de la carte
            
            
            
posx,posy=1.5,1.5 #Position initiale du joueur
pg.init()
f=pg.display.set_mode((WIND*2, WIND),pg.RESIZABLE)
pg.display.set_caption("3D maze mdrs")
horloge = pg.time.Clock() #Pour gérer les FPS
font = pg.font.SysFont('consolas',30) # Charger la police d'écriture
look=math.pi/4 # Le regard horizontal

viz=WIND/size # Zoom sur l'apreçu de map
accro=True # Accrocher la souris dans le jeu

antesx,antesy=0,0
val=0 # Pour l'effet de slection smooth
up=0.1 # Le regard horizontal
midx,midy=0,0
b = True #la boucle du jeu
try:
    pg.mouse.set_pos((WIND/2,WIND/2))
    while b:
        
        # Actualiser:
        pg.display.flip()
        val+=0.1
        val=val%(4*math.pi)
        fac=up+1
        if fac>1:fac=1

        # Appliquer les images de fond sur la fenetre
        s = pg.Surface((WIND*2, WIND))  
        s.fill((0, 0, 0))
        f.blit(s, (0, 0))
        #Le ciel et la Terre
        horiz=int((up+0.5)*WIND)
        for i in range(horiz):
            pg.draw.line(f,(0,0,255-i/horiz*255),(0,horiz-i),(WIND,horiz-i))
        for j in range(horiz,WIND):
            t=(j-horiz)/(WIND-horiz)*255
            pg.draw.line(f,(t,t,t),(0,j),(WIND,j))

        rays=[] # Les rayons de vue
        for i in range(0,(agl+1)*2,2):
            i=i/2
            balyeur=look+math.radians(i-agl/4)
            x,y=posx,posy
            sin,cos=math.sin(balyeur)/10,math.cos(balyeur)/10
            n=0
            while int(x)<len(carte) and int(y)<len(carte[0]) and carte[int(x)][int(y)]==0:
                x+=cos
                y+=sin
                n+=1
            if n==0:
                posx-=math.cos(look)*speed
                posy-=math.sin(look)*speed
                break
            elif i==int((agl+1)/2):
                midx=x
                midy=y
            d=math.sqrt((posx-midx)**2+(posy-midy)**2)
            rays.append((x,y,d))
            h=1/(n*math.cos(balyeur-look))

            if int(x)<len(carte) and int(y)<len(carte[0]) and carte[int(x)][int(y)]!=0:
                hue=carte[int(x)][int(y)]
                if int(x)==round(x,1) and int(y)==round(y,1):
                    sgt(i/agl,h,-h,(255,255,255))
                else:
                    if hue==1-main_coul:
                        sgt(i/agl,h,-h,hsv_to_rgb(hue,(math.cos(val)+1)/2,255-d*shadow))
                        print('hallah')
                    else:
                        if i==int((agl+1)/2):
                            sgt(i/agl,h,-h,hsv_to_rgb(1-hue,1,255-d*shadow))
                            
                        else:
                            sgt(i/agl,h,-h,hsv_to_rgb(hue,1,255-d*shadow))
                coul=255-d*20
        
        vizx=posx+math.cos(look)*d*fac
        vizy=posy+math.sin(look)*d*fac
        p = pg.key.get_pressed()  # SI la touche est appuyée
        for indx in range(len(carte)):
            for indy in range(len(carte[indx])):
                
                hue=carte[indx][indy]
                if hue==1:
                    pg.draw.rect(f,(255,255,255),pg.Rect(WIND+indx*viz,indy*viz,viz,viz))
                elif hue!=0:
                    if hue==1-main_coul:
                        pg.draw.rect(f,hsv_to_rgb(hue,(math.cos(val)+1)/2,255),pg.Rect(WIND+indx*viz,indy*viz,viz,viz))
                    else:
                        pg.draw.rect(f,hsv_to_rgb(1-hue,1,255),pg.Rect(WIND+indx*viz,indy*viz,viz,viz))
                else:
                    pg.draw.circle(f,(255,255,255),(WIND+indx*viz,indy*viz),2)
            pg.draw.circle(f,(255,255,255),(WIND+posx*viz,posy*viz),5)
            """for ray in rays:
                pg.draw.line(f,hsv_to_rgb(main_coul,0.5,200),(WIND+posx*viz,posy*viz),(WIND+ray[0]*viz,ray[1]*viz))"""
            pg.draw.line(f,hsv_to_rgb(1-hue,0.5,255),(WIND+vizx*viz,vizy*viz),(WIND+posx*viz,posy*viz))
        if carte[int(midx)][int(midy)]==0:
            
            antesx,antesy=int(midx),int(midy)
            
        if p[pg.K_d]:look+=math.pi/128
        if p[pg.K_q]:look-=math.pi/128
        if p[pg.K_a]:up+=1/500
        if p[pg.K_w]:up-=1/500
        if p[pg.K_z]:
            posx+=math.cos(look)*speed
            posy+=math.sin(look)*speed
        elif p[pg.K_s]:
            posx-=math.cos(look)*speed
            posy-=math.sin(look)*speed
        
        if accro:
            pg.mouse.set_visible(False)
            mouvx,mouvy=(pg.mouse.get_pos()[0]-WIND/2),(pg.mouse.get_pos()[1]-WIND/2)
            up-=mouvy*10/WIND
            up=((up+1)%2)-1
            look+=mouvx*10/WIND
            pg.mouse.set_pos((WIND/2,WIND/2))
                
        for event in pg.event.get():  # QUAND la touche est appuyée
            if event.type == pg.QUIT:
                b = False
                print("Fin du jeu  babe")
                
            elif event.type == pg.KEYUP:
                if event.key==pg.K_ESCAPE:
                    accro=False
                    pg.mouse.set_visible(True)   
            elif event.type==pg.MOUSEBUTTONUP:
                if event.button==1:
                    if int(event.pos[0]) in range(WIND) and int(event.pos[1]) in range(WIND):
                        accro=True
                if event.button==1: #click gauche
                    if up+1<=1:
                        carte[int(vizx)][int(vizy)]=main_coul
                elif event.button==3: #click droit
                    if up+1<=1:
                        carte[int(vizx)][int(vizy)]=0
                elif event.button==4: #scroller vers le haut
                    posx+=math.cos(look)*speed*5
                    posy+=math.sin(look)*speed*5
                elif event.button==5: #scroller vers le bas
                    posx-=math.cos(look)*speed*5
                    posy-=math.sin(look)*speed*5
                    
        text=font.render(str(int(horloge.get_fps())),False,(255,255,255))
        f.blit(text, (WIND/2-text.get_rect().width/2,WIND/2-10-text.get_rect().height))
        pg.draw.line(f,(255,255,255),(WIND/2-10,WIND/2),(WIND/2+10,WIND/2))
        pg.draw.line(f,(255,255,255),(WIND/2,WIND/2-10),(WIND/2,WIND/2+10))
        horloge.tick(FPS)
except :
    pg.quit()
    raise
finally:
    pg.quit()
