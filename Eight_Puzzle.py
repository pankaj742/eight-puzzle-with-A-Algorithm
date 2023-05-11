import pygame,sys,time,random
from pygame.locals import *
pygame.init()
windowSurface=pygame.display.set_mode((900,650),0,32)
pygame.display.set_caption("Eight Puzzle")
WHITE=(255,255,255)
black=(0,0,0)
green=(57, 198, 182)
thoda_green=(48, 282, 188)
sunehra=(255, 176, 7)
thoda_sunehra=(255, 189, 7)
nila=(178, 255, 244)
textBack=(54, 118, 180)
strt_color=(180, 255, 119)
succ_color=(201, 18, 184)
goal_color=(81, 205, 289)
#clock
clock=pygame.time.Clock()
#data structure for storing blocks
side=[]
states={}
frontier=[]
explored=[]
def mainloop():
    #(pygame.font.get_fonts())
    #main loop
    while(True):
        for event in pygame.event.get():
            if event.type== QUIT:
                pygame.quit()
                sys.exit()
        windowSurface.fill(WHITE)
        #nameplate()
        button("Start",100,550,100,60,green,strt_color,"start")
        button("Randomize",600,550,100,60,sunehra,thoda_sunehra,"randomize")
        drawSide()
        #first_indicator()
        pygame.display.update()
        #time.sleep(0.01)
        clock.tick(64)

def drawSide():
    #draw one side
    for i in range(8):
        colum=side[i]
        for j in range(8):
            box=colum[j]
            pygame.draw.rect(windowSurface,box["color"],box["rect"],2)
            drawText(box["tag"],box["centerx"],box["centery"])

    
def button(msg,x,y,w,h,ic,ac,action=None):
    #find button
    mouse=pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    #(click)
    #(mouse)
    if(x+w>mouse[0]>x and y+h > mouse[1] >y):
        pygame.draw.rect(windowSurface,ac,(x,y,w,h))
        if click[0]==1 and action !=None:
            if action == "start":
                start()
                ("start")
            elif action == "randomize":
                randomize()
    else:
        pygame.draw.rect(windowSurface,ic,(x,y,w,h))
    smallText=pygame.font.SysFont(None,20)
    textSurf=smallText.render(msg,True,black,ic)
    textRect=textSurf.get_rect()
    textRect.centerx= x+(w/2)
    textRect.centery= y+(h/2)
    windowSurface.blit(textSurf,textRect)
def randomize():
    initialize_blocks()
    pos=list(range(0,64))
    newpos=[]
    lettors=list(range(64))
    for i in range(64):
        rand1=random.randint(0,len(pos)-1)
        newpos.append(pos[rand1])
        pos.remove(pos[rand1])
    (newpos)
    for j in range(64):
        if(lettors[j]==0):
            side[newpos[j]//8][newpos[j]%8]["tag"]=None
            continue
        side[newpos[j]//8][newpos[j]%8]["tag"]=str(lettors[j])

def getcost(state):
    h1=0 #misplaced blocks
    h2=0 #sum of distance of blocks
    pos=state["pos"]
    nonpos=state["nonpos"]
    for i in range(64):
        if((i != nonpos) and (pos[i]-1 != i)):
            h1 += 1
        if(i != nonpos):
            h2 += max(pos[i]-1,i)-min(pos[i]-1,i)
    return(h1+h2)

def max(i,j):
    if(i>j):
        return i
    else:
        return j
def min(i,j):
    if(i<j):
        return i
    else:
        return j

def getposition(state):
    p=[]
    for i in range(64):
        if(side[i//8][i%8]["tag"] == None):
            state["nonpos"]=i
            p.append(side[i//8][i%8]["tag"])
            continue
        else:
            p.append(int(side[i//8][i%8]["tag"]))
    state["pos"]=p #may be erronious
    state["actions"]=side[state["nonpos"]//8][state["nonpos"]%8]["actions"]

def addfrontier(v):
    #v is dictionary
    frontier.append(v)
    if(len(frontier) == 1):
        return
    current=len(frontier)-1
    parant=(current-1)//2
    while(True):
        #print("in while loop in addfrontier")
        if(current == 0):
            break
        elif(frontier[parant]["cost"] >= frontier[current]["cost"]):
            (frontier[parant],frontier[current])=(frontier[current],frontier[parant])
            current=parant
            if(current != 0):
                parant=(current-1)//2
                continue
        else:
            break

def getfrontier():
    if(len(frontier)== 0):
        return False
    top=frontier[0]
    frontier.remove(frontier[0])
    if(len(frontier)== 0 or len(frontier)== 1):
        return top
    frontier.insert(0,frontier.pop())
    current=0
    while(True):
        #print("while loop in getfrontier")
        if(current > (len(frontier)-2)//2):
            break
        
        if(frontier[current]["cost"] >= frontier[minchildren(current)]["cost"]):
            (frontier[minchildren(current)],frontier[current])=(frontier[current],frontier[minchildren(current)])
            current=minchildren(current)
            continue
        else:
            break
    return top
def minchildren(i):
    children1=2*i+1
    children2=2*i+2
    if(children2 <=len(frontier)-1):
        if(frontier[children1]["cost"] < frontier[children2]["cost"]):
            return children1
        else:
            return children2
    else:
        return children1

def checkvisited(state):
    for i in range(len(explored)):
        stateno=explored[i]["stateno"]
        tstate=states[stateno]
        if(state["pos"]==tstate["pos"]):
            return True
    for i in range(len(frontier)):
        stateno=frontier[i]["stateno"]
        tstate=states[stateno]
        if(state["pos"]==tstate["pos"]):
            return True
    else:
        return False

def applyactions(state):
    #frontier cost will be different than state cost
    #print(state)
    stateno=state["no"]
    actions=state["actions"]
    for action in actions:
        pos=state["pos"][:]
        nonpos=state["nonpos"]
        cost=state["cost"]
        
        path=[]
        path=state["path"][:]
        newstate={}
        frontiernode={}
        if action == "up":
            #print(str(nonpos)+"up")
            (pos[nonpos],pos[nonpos-1])=(pos[nonpos-1],pos[nonpos])
            newstate["no"]= stateno+1
            stateno += 1
            newstate["pos"]=pos
            newstate["nonpos"]=nonpos-1
            newstate["actions"]=side[(nonpos-1)//8][(nonpos-1)%8]["actions"]
            newstate["cost"] = cost+0
            path.append(str(nonpos)+"up")
            newstate["path"]=path[:]
            if(checkvisited(newstate) == False):
                frontiernode["stateno"]=stateno
                frontiernode["cost"]=newstate["cost"]+getcost(newstate)
                addfrontier(frontiernode)
                states[stateno]=newstate
            
            
        elif action == "down":
            #print(str(nonpos)+"down")
            (pos[nonpos],pos[nonpos+1])=(pos[nonpos+1],pos[nonpos])
            newstate["no"]= stateno+1
            stateno += 1
            newstate["pos"]=pos
            newstate["nonpos"]=nonpos+1
            newstate["actions"]=side[(nonpos+1)//8][(nonpos+1)%8]["actions"]
            newstate["cost"] = cost+0
            path.append(str(nonpos)+"down")
            newstate["path"]=path[:]
            
            if(checkvisited(newstate) == False):
                frontiernode["stateno"]=stateno
                frontiernode["cost"]=newstate["cost"]+getcost(newstate)
                addfrontier(frontiernode)
                states[stateno]=newstate

        elif action == "left":
            #print(str(nonpos)+"left")
            (pos[nonpos],pos[nonpos-8])=(pos[nonpos-8],pos[nonpos])
            newstate["no"]= stateno+1
            stateno += 1
            newstate["pos"]=pos
            newstate["nonpos"]=nonpos-8
            newstate["actions"]=side[(nonpos-8)//8][(nonpos-8)%8]["actions"]
            newstate["cost"] = cost+0
            path.append(str(nonpos)+"left")
            newstate["path"]=path[:]
            if(checkvisited(newstate) == False):
                frontiernode["stateno"]=stateno
                frontiernode["cost"]=newstate["cost"]+getcost(newstate)
                addfrontier(frontiernode)
                states[stateno]=newstate

        elif action == "right":
            #print(str(nonpos)+"right")
            (pos[nonpos],pos[nonpos+8])=(pos[nonpos+8],pos[nonpos])
            newstate["no"]= stateno+1
            stateno += 1
            newstate["pos"]=pos
            newstate["nonpos"]=nonpos+8
            newstate["actions"]=side[(nonpos+8)//8][(nonpos+8)%8]["actions"]
            newstate["cost"] = cost+0
            path.append(str(nonpos)+"right")
            newstate["path"]=path[:]
            if(checkvisited(newstate) == False):
                frontiernode["stateno"]=stateno
                frontiernode["cost"]=newstate["cost"]+getcost(newstate)
                addfrontier(frontiernode)
                states[stateno]=newstate
    
    

#start function
def start():
    state={}
    fnode={}
    state["path"]=[]
    state["no"]=1
    getposition(state)
    state["cost"]=0
    #print(state)
    states[1]=state
    fnode["stateno"]=1
    fnode["cost"]=getcost(state)
    explored.append(fnode)
    applyactions(state)
    print(getcost(state))
    print("********states********")
    print(states)
    #start searching
    while(True):
        if len(frontier) == 0:
            print("fail")
            break
        node=getfrontier()
        print(node)
        #print(frontier)
        explored.append(node)
        if(getcost(states[node["stateno"]]) == 0):
            print(states[node["stateno"]])
            print("success")
            break
        else:
            applyactions(states[node["stateno"]])
            

    
def find_id(tag):
    for i in range(8):
        for j in range(8):
            if(side[i][j]["tag"] == tag):
                return(side[i][j]["pos"])
def initialize_blocks():
    for i in range(64):
        side[i//8][i%8]["tag"]=None
        

def createBlocks(side):
    #create blocks
    for i in range(8):
        side.append([])
        for j in range(8):
            box={}
            box["pos"]=(i*8+j)
            box["rect"]=pygame.Rect(0,0,50,50)
            box["centerx"]=i*50+50+200
            box["centery"]=j*50+50
            box["rect"].centerx=box["centerx"]
            box["rect"].centery=box["centery"]
            box["tag"]=str(box["pos"]+1)
            box["color"]=nila

            if(box["pos"]==63):
                box["tag"]=None
            if(box["pos"] in (1,2,3,4,5,6)):
                box["actions"]=("up","down","right")
            elif(box["pos"] in (15,23,31,39,47,55)):
                box["actions"]=("up","left","right")
            elif(box["pos"] in (57,58,59,60,61,62)):
                box["actions"]=("up","down","left")
            elif(box["pos"] in (8,16,24,32,40,48)):
                box["actions"]=("down","left","right")
            elif(box["pos"] == 0):
                box["actions"]=("down","right")
            elif(box["pos"] == 7):
                box["actions"]=("up","right")
            elif(box["pos"] == 63):
                box["actions"]=("up","left")
            elif(box["pos"] == 56):
                box["actions"]=("down","left")
            else:
                box["actions"]=("up","down","left","right")
            side[i].append(box)
            
def drawText(msg,x,y):
    basicFont=pygame.font.SysFont(None,48)
    text=basicFont.render(msg,True,WHITE,textBack)
    textRect=text.get_rect()
    textRect.centerx=x
    textRect.centery=y
    windowSurface.blit(text,textRect)


#very important function find
def find(x,y=None):
    xpos=None
    ypos=None
    if(y == None):
        for i in range(64):
            tag=side[i//8][i%8]["tag"]
            if(tag == x):
                return (i,None)
    else:
        for i in range(64):
            tag=side[i//8][i%8]["tag"]
            if(tag == x):
                xpos=i
            elif(tag == y):
                ypos=i
            if((xpos != None) and (ypos != None)):
                break
        return((xpos,ypos))

def nameplate():
    rect1=pygame.Rect((860,5,170,50))
    basicFont=pygame.font.SysFont("comicsansms",14)
    text1=basicFont.render("developed by pankaj shah",True,black,strt_color)
    text1Rect=text1.get_rect()
    text1Rect.centerx=rect1.centerx
    text1Rect.centery=rect1.centery
    pygame.draw.rect(windowSurface,strt_color,rect1)
    windowSurface.blit(text1,text1Rect)
def first_indicator():
    ("in first_indicator and case:"+str(case))
    if(state == 1):
        indicators("Start Position","Goal Position",strt_color)
    elif(state == 2):
        indicators("Goal Achived","Goal Position",succ_color)
def indicators(msg1,msg2,fcolor):
    rect1=pygame.Rect((75,400,250,100))
    basicFont=pygame.font.SysFont(None,48)
    text1=basicFont.render(msg1,True,black,fcolor)
    text1Rect=text1.get_rect()
    text1Rect.centerx=rect1.centerx
    text1Rect.centery=rect1.centery

    rect2=pygame.Rect((575,400,250,100))
    text2=basicFont.render(msg2,True,WHITE,goal_color)
    text2Rect=text2.get_rect()
    text2Rect.centerx=rect2.centerx
    text2Rect.centery=rect2.centery

    pygame.draw.rect(windowSurface,fcolor,rect1)
    pygame.draw.rect(windowSurface,goal_color,rect2)
    windowSurface.blit(text1,text1Rect)
    windowSurface.blit(text2,text2Rect)
#main loop call
createBlocks(side)
mainloop()

       
