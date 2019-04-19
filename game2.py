# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 19:17:21 2019

@author: Aviii
"""

import pygame


            
pygame.init()

win = pygame.display.set_mode()

pygame.display.set_caption("First Game")
x = 50
y = 250  
width = 10
height = 50
vel = 10

isJump = False
jumpCount = 10

run = True
#======================================

from pynput import keyboard    
#x=0
def on_press(key):
    global x,y
    global vel
    global isJump
    global jumpCount
    try: k = key.char # single-char keys
    except: k = key.name # other keys
    if key == keyboard.Key.esc: return False # stop listener  1
    if k in ['1', 'q', 'space', 'right']: # keys interested
        # self.keys.append(k) # store it in global-like variable
        if k=='q':
            x += vel
        if k=='space':
            isJump = True
        print('Key pressed: ' + k)
    

lis = keyboard.Listener(on_press=on_press) 
lis.start()      
#======================================
while run:
    pygame.time.delay(30)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
    pygame.display.update()
    print(x)   
#    keys = pygame.key.get_pressed()
#    
#    
#    if keys[pygame.K_a]:
#        x += vel
#    
##    if keyboard.is_pressed('a'):  # if key 'q' is pressed 
##            x += vel
#        
    if not(isJump):
        pass
#        if keys[pygame.K_SPACE]:
#            isJump = True
    else:           
        if jumpCount >= -10:
            neg = 1
            if jumpCount < 0:
                neg = -1 
            y -= (jumpCount ** 2) * 0.5 * neg
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10
                
    win.fill((0,0,0))
pygame.quit ()