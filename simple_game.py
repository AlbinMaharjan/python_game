import pygame
import random       #to get the random values
import math
import sys
from pygame import mixer

mixer.init()
pygame.init()


# print('''
#       Press 1 for Level One
#       Press 2 for Level Two
#       ''')

# choice=int(input("Enter your choice:"))

# if choice=='1':
#     lvl1()
# elif choice=='2':
#     lvl2()
# else:
#     print('Invalid Input')     






mixer.music.load('background.wav')
mixer.music.play(-1)                                    #music in loop
screen=pygame.display.set_mode((800,600))
pygame.display.set_caption('Welcome To The Space Shooter Game')
icon=pygame.image.load('icon.png')
pygame.display.set_icon(icon)

background=pygame.image.load('background.png')

player_img=pygame.image.load('khiladi.png')
enemy_img=[]
enemyX=[]
enemyY=[]
enemyspeedX=[]
enemyspeedY=[]


no_of_enemy=6

for i in range(no_of_enemy):                                    #adding 6 enemy
    enemy_img.append(pygame.image.load('dushman.png'))

    enemyX.append(random.randint(0,736))                        #alien ko value randomly auxa between those range
    enemyY.append(random.randint(30,150)) 
    enemyspeedX.append(-1)                      
    enemyspeedY.append(40)


spaceshipX=370
spaceshipY=470
changeX=0  
score=0 
def player():
    screen.blit(player_img,(370,600))
 
 

   
   
bullet_img=pygame.image.load('goli.png')   
check=False
bulletX=386
bulletY=490

running=True

font=pygame.font.SysFont('Arial',32,'bold')       #creating a font object

def score_text():
    img=font.render(f'Score:{score}',True,'red')      #to show the score
    screen.blit(img,(10,10))

    
font_gameover=pygame.font.SysFont('Arial',64,'bold') 
def game_over():
    img_go=font_gameover.render('Game Over',True,'red')      
    screen.blit(img_go,(200,250))   
while running:
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
         
        if event.type==pygame.KEYDOWN:    
            if event.key==pygame.K_LEFT:            #left arrow press xaki xaina check
               changeX=-5                           #speed badaunu parye yo badauni
               
            if event.key==pygame.K_RIGHT:               #right arrow press xaki xaina check
                changeX=5 
            
            
            if event.key==pygame.K_SPACE:                #space press xaki xaina check
               if check is False:                           #bullet end ma pugesi balla next bullet will fire
                   bulletSound= mixer.Sound('laser.wav')        #sound overwrite huna nadina
                   bulletSound.play()
                   check=True
                   bulletX=spaceshipX+16 
               
               
        if event.type==pygame.KEYUP:
           changeX=0            
           
            
    spaceshipX+=changeX    
    if spaceshipX<=0:           #left ma arcade rokna
        spaceshipX=0      
    elif spaceshipX>=736:      #windowsize-arcade size
        spaceshipX=736          #stop arcade at right
        
    for i in range(no_of_enemy):   
        if enemyY[i]>=420:              #destroying alien
           for j in range(no_of_enemy):
                enemyY[j]=2000
                game_over(50)
                break
        enemyX[i]+=enemyspeedX[i]  
        if enemyX[i]<=0:
            enemyspeedX[i]=1
            enemyY[i]+=enemyspeedY[i]
        if enemyX[i]>=736:
            enemyspeedX[i]=-1
            enemyY[i]+=enemyspeedY[i]
            

        distance=math.sqrt(math.pow(bulletX-enemyX[i],2)+math.pow(bulletY-enemyY[i],2))        #distance formula
        if distance<27:
           explosionSound= mixer.Sound('explosion.wav')        #sound overwrite huna nadina
           explosionSound.play()
           bulletY=480             #move back to the original position
           check=False
           enemyX[i]=random.randint(0,736)        #after collision move alien to the value                
           enemyY[i]=random.randint(30,150)
           score+=5
        screen.blit(enemy_img[i], (enemyX[i],enemyY[i]))  #1st run ma 1st image blit and so on
    
    if bulletY<=0:
        bulletY=490
        check=False          #stop the continious bullet 
        bulletX=spaceshipX+16       #so that bullet comes out fro tip (difference of 16)
        
    if check is True:                                   #true bhaye matra bullet niskinxa
        screen.blit(bullet_img,(bulletX,bulletY)) 
        bulletY-=5                                     #bullet mathi pathauna
    
   
    
    
    
    screen.blit(player_img, (spaceshipX,spaceshipY))        #load image
    
    player()      
    score_text()  
    pygame.display.update()       
    
    
    
    
 