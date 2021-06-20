import pygame as pg
import math

from pygame import event

pg.init()
wind=[500,500]
f=pg.display.set_mode((500,500),pg.RESIZABLE)
render=pg.display.set_mode((500,500),pg.RESIZABLE)
fps=pg.time.Clock()
B=1
carte=[[1 for i in range(10)]]+[[1]+[0 for i in range(8)]+[1] for j in range(8)]+[[1 for i in range(10)]]
pos=[5,5]
moving=False
decal=0
ouverture=math.tau
torticoli=0
def scale(truc):
    return truc[0]*coef,truc[1]*coef
while B:
    fps.tick(60)
    pg.display.flip()
    f.fill(0)
    coef=int(min(wind)/10)
    indx,indy=0,0
    for y in carte:
        for x in y:
            if x:
                pg.draw.rect(f,0xffffff,(indx*coef,indy*coef,coef,coef))
            indx+=1
        indy+=1
        indx=0
    pg.draw.circle(f,0xff00ff,(pos[0]*coef,pos[1]*coef),coef/2)
    rays=[]
    precision=10
    decal=pg.mouse.get_pos()
    pg.draw.circle(f,0xff0000,decal,5)
    decal=math.atan2(decal[1]/coef-pos[1],decal[0]/coef-pos[0])*4
    for i in range(precision):
        ray=decal+(i/precision)*ouverture
        rpos=pos[:]
        test=[math.cos(ray/10)/10,math.sin(ray/10)/10]
        while (not carte[int(rpos[1])][int(rpos[0])]) and rpos[0]<wind[0] and rpos[1]<wind[1]:
            rpos[0]+=test[0]
            rpos[1]+=test[1]
        rpos[0]-=test[0]
        rpos[1]-=test[1]
        rays.append(rpos)
    for ray in rays:
        pg.draw.line(f,0xff0000,scale(pos),scale(ray))
        
    if moving:
        pos[0]+=moving[0]/10
        pos[1]+=moving[1]/10

    for event in pg.event.get():
        if event.type==pg.QUIT:
            pg.quit()
            B=0
        
        elif event.type==pg.KEYDOWN:
            if event.key==pg.K_z:moving=[0,-1]
            elif event.key==pg.K_q:moving=[-1,0]
            elif event.key==pg.K_s:moving=[0,1]
            elif event.key==pg.K_d:moving=[1,0]

        elif event.type==pg.KEYUP:
            moving=False
            torticoli=0
        elif event.type==pg.MOUSEBUTTONUP:
            npos=pg.mouse.get_pos()

            carte[int(npos[1]/coef)][int(npos[0]/coef)]=int(event.button==1)
        elif event.type==pg.VIDEORESIZE:
            wind=[event.w,event.h]
