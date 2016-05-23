import pygame
from pygame.locals import *
from PositionalList import PositionalList

pygame.init()

SCREEN_HEIGHT=600
SCREEN_WIDTH=800
SCREEN_SIZE=(SCREEN_WIDTH,SCREEN_HEIGHT)
myfont=pygame.font.SysFont("arial", 20)

pygame.display.set_caption('Polygon')
screen=pygame.display.set_mode(SCREEN_SIZE,pygame.RESIZABLE)
background=pygame.Surface(screen.get_size())
background=background.convert()
background.fill((255,255,255))

def main():
    global screen,SCREEN_WIDTH,SCREEN_SIZE,deltaX,deltaY
    vertex=PositionalList()
    running=True
    done=False
    clickTrue=False
    getPrev=False
    deltaX=0
    deltaY=0
    x=0
    y=0
    screen.fill((255,255,255))
    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            elif event.type==pygame.MOUSEBUTTONDOWN:
                (posx,posy)=pygame.mouse.get_pos()
                if done==False and len(vertex)>=0:
                    if (x-posx)**2+(y-posy)**2<=25:
                        vertex.add_last(vertex.first().element())
                    else:
                        vertex.add_last((posx,posy))
                    if len(vertex)>1:
                        (x,y)=vertex.first().element()
                        if (x-posx)**2+(y-posy)**2<=25:
                            done=True
                            (posx,posy)=vertex.first().element()
                        p=vertex.before(vertex.last())
                        pygame.draw.line(screen,(0,0,0),p.element(),(posx,posy))
                    pygame.draw.circle(screen,(0,0,0),(posx,posy),5)
                else:
                    p=click(vertex,(posx,posy))
                    if click(vertex,(posx,posy))!=None:
                        clickTrue=not clickTrue
                    # if not clickTrue:
                    #     p=click(vertex,(posx,posy))
                    #     if p!=None:
                    #         clickTrue=True
                    # else:
                    #     (posx,posy)=pygame.mouse.get_pos()
                    #     vertex.add_after(p,(posx,posy))
                    #     screen.fill((255,255,255))
                    #     drawPolygon(vertex)
                    #     p=None
                    #     clickTrue=False
                    #     getPrev=False

            elif event.type==pygame.MOUSEMOTION and clickTrue:
                    if done==True:
                        (posx,posy)=pygame.mouse.get_pos()
                        screen.fill((255,255,255))
                        vertex.add_after(p,(posx,posy))
                        # if getPrev:
                        #     deltaX=(posx-pPosx)
                        #     deltaY=(posy-pPosy)
                        # updateVertex(vertex,deltaX,deltaY)
                        drawPolygon(vertex)
                        
                        vertex.delete(vertex.after(p))
                        # getPrev=True
                        # (pPosx, pPosy) = (posx,posy)
            elif event.type==pygame.MOUSEBUTTONUP:
                if clickTrue and done:
                    vertex.add_after(p,(posx,posy))
                clickTrue=False
        pygame.display.flip()

# def updateVertex(L,deltaX,deltaY):
#     p=L.first()
#     (x,y)=p.element()
#     for i in range(len(L)-1):
#         if 

def drawPolygon(L):
    p=L.first()
    (x,y)=p.element()
    pygame.draw.circle(screen,(0,0,0),(int(x),int(y)),5)
    for i in range (len(L)-1):
        (preX,preY)=p.element()
        p=L.after(p)
        (x,y)=p.element()
        pygame.draw.circle(screen,(0,0,0),(int(x),int(y)),5)
        pygame.draw.line(screen,(0,0,0),(int(preX),int(preY)),(int(x),int(y)))

def click(L,a):
    p=L.first()
    for i in range(len(L)-1):
        (x,y)=p.element()
        if (x-a[0])**2+(y-a[1])**2<=25:
            return p
        p=L.after(p)
    return None
main()
