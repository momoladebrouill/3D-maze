import pygame as pg
import math

from pygame import event

pg.init()
wind=[500,500]
f=pg.display.set_mode((500,500),pg.RESIZABLE)

fps=pg.time.Clock()
B=1
rays=[]
carte=[[1 for i in range(10)]]+[[1]+[0 for i in range(8)]+[1] for j in range(8)]+[[1 for i in range(10)]]
pos=[5,5]
fpos=pos[:]
moving=[0,0]
decal=0
fpsmode=False
ouverture=math.tau/8
precision=50 #-- précision pour trouver le point de contact au mur à 1/precision près mais aussi nombre de lignes
scale=lambda truc:(truc[0]*coef,truc[1]*coef)
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
    
   
    
    if not fpsmode:
        decal=pg.mouse.get_pos()
        decal=math.atan2(decal[1]/coef-pos[1],decal[0]/coef-pos[0])-ouverture/2
    rays=[]
    for i in range(precision):
        ray=decal+i*ouverture/precision
        rpos=pos[:]
        test=[math.cos(ray)/10,math.sin(ray)/10]
        while (not carte[int(rpos[1])][int(rpos[0])]) and rpos[0]<wind[0] and rpos[1]<wind[1]:
            rpos[0]+=test[0]
            rpos[1]+=test[1]
        rpos[0]-=test[0]
        rpos[1]-=test[1]
        rpos.append(math.dist(rpos,pos))
        rpos.append(ray)
        rays.append(rpos)
    ind=0
    for ray in rays:
        tt=[int((1-ray[2]/15)*0xff) for _ in range(3)]
        haut=ray[2]/30*wind[1] # longueur sur longuer maxi x hauteur maxi
        haut=ray[2]*math.sin(decal+math.atan2(pos[1]-ray[1],pos[0]-ray[0]))/wind[1]
        pg.draw.rect(f,tt,
                (min(wind)+ind/len(rays)*(max(wind)-min(wind)), # x
                haut, # y
                (max(wind)-min(wind))/len(rays), # largeur
                wind[1]-haut*2     # hauteur
                ))
        ind+=1
    pg.draw.polygon(f,0x555555,[scale(i) for i in rays+[pos]])
    if fpsmode:
        rayon=rays[len(rays)//2]
        pg.draw.rect(f,0xffff00,(int(rayon[0])*coef,int(rayon[1])*coef,coef,coef))
        pg.draw.rect(f,0xffff00,(int(rayon[0]+math.cos(rayon[3]))*coef,int(rayon[1]+math.sin(rayon[3]))*coef,coef,coef),5)
    pg.draw.circle(f,0xff0000,(pos[0]*coef,pos[1]*coef),coef/4)

    if moving:
        fpos[0]+=moving[0]/10
        if carte[int(fpos[1])][int(fpos[0])]:
            fpos[0]-=moving[0]
        fpos[1]+=moving[1]/10
        if carte[int(fpos[1])][int(fpos[0])]:
            fpos[1]-=moving[1]
    pos[0]+=(fpos[0]-pos[0])/7
    pos[1]+=(fpos[1]-pos[1])/7
    for event in pg.event.get():
        if event.type==pg.QUIT:
            pg.quit()
            B=0
        
        elif event.type==pg.KEYDOWN:
            if fpsmode:
                if event.key== pg.K_z:
                    moving=[math.cos(decal),math.sin(decal)]
                if event.key== pg.K_q:
                    moving=[math.cos(decal-math.pi/2),math.sin(decal-math.pi/2)]
                if event.key== pg.K_s:
                    moving=[-math.cos(decal),-math.sin(decal)]
                if event.key== pg.K_d:
                    moving=[math.cos(decal+math.pi/2),math.sin(decal+math.pi/2)]
            else:
                if event.key==pg.K_z:moving[1]=-1
                elif event.key==pg.K_q:moving[0]=-1
                elif event.key==pg.K_s:moving[1]=1
                elif event.key==pg.K_d:moving[0]=1

        elif event.type==pg.KEYUP:
            if fpsmode:moving=[0,0]
            if event.key==pg.K_z:moving[1]=0
            elif event.key==pg.K_q:moving[0]=0
            elif event.key==pg.K_s:moving[1]=0
            elif event.key==pg.K_d:moving[0]=0
            elif event.key==pg.K_a:
                fpsmode=not fpsmode
                if fpsmode:
                    pg.mouse.set_pos((min(wind)+(max(wind)-min(wind))/2,wind[1]/2))
                pg.mouse.set_visible( not fpsmode)
        elif event.type==pg.MOUSEMOTION and fpsmode:
            rel=list(pg.mouse.get_pos())
            rel[0]=rel[0]-min(wind)-(max(wind)-min(wind))/2
            rel[1]=rel[1]-wind[1]/2
            decal+=rel[0]/wind[1]
            pg.mouse.set_pos((min(wind)+(max(wind)-min(wind))/2,wind[1]/2))
        elif event.type==pg.MOUSEBUTTONUP:
            if fpsmode:
                rayon=rays[len(rays)//2]
                if event.button==1:
                    carte[int(rayon[1])][int(rayon[0])]=1
                else:
                    carte[int(rayon[1]+math.sin(rayon[3]))][int(rayon[0]+math.cos(rayon[3]))]=0
            else:
                npos=pg.mouse.get_pos()
                carte[int(npos[1]/coef)][int(npos[0]/coef)]=int(event.button==1)
        elif event.type==pg.VIDEORESIZE:
            wind=[event.w,event.h]
