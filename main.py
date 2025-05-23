import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
pygame.init()

pygame.display.set_caption("JeuDePlateforme")

debut_chrono = pygame.time.get_ticks()
tchrono_actuel = 0
police = pygame.font.SysFont("Arial", 30)

WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 3.5
GRAVITE = 1
charge_max = 750  # en ms ; 
charge_force_ratio = 0.02 
vitesse_x = 0
vitesse_y = 0
vitessetonneaux_x = [-2]
vitessetonneaux_y = [0]
statutAir = False
statutCharge = False
statutSaute = False
direction = 'droite'
compteurcharge = 0
temps_charge_debut = 0
clock = pygame.time.Clock()
fenetre = pygame.display.set_mode( (WIDTH,HEIGHT) ) # Création d'une fenêtre graphique de taille 600x600 pixels
bg = pygame.image.load("sprites/ForetBackground/g/2304x1296.png") #l'image de fond
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT)) # Taille de l'image derriere
positionsurface = [0, 0] # Position de l'image de fond
#sol = pygame.Rect(0, 650, 1000, 150) #Création d'un rectangle pour la plateforme


bord_d, bord_g = pygame.Rect(-25,0,20, HEIGHT), pygame.Rect(1000,0,20,HEIGHT)


#Gestion des sols
soldebut = 650
sol_y = soldebut
plateforme_w = 825
plateforme_h = 32
positionplateforme1 = [0,530]
positionplateforme2 = [175,400]
positionplateforme3 = [0,270]
positionplateforme4 = [175,140]
plateforme1 = pygame.Rect(positionplateforme1[0],positionplateforme1[1],plateforme_w,plateforme_h)
plateforme2 = pygame.Rect(positionplateforme2[0],positionplateforme2[1],plateforme_w,plateforme_h)
plateforme3 = pygame.Rect(positionplateforme3[0],positionplateforme3[1],plateforme_w,plateforme_h)
plateforme4 = pygame.Rect(positionplateforme4[0],positionplateforme4[1],plateforme_w,plateforme_h)


#Gestion des tiles
tile_surface = pygame.image.load("sprites/plateformer/2 Locations/Tiles/Tile_03.png")
tile_terre = pygame.image.load("sprites/plateformer/2 Locations/Tiles/Tile_04.png")
tile_platforme = pygame.image.load("sprites/plateformer/2 Locations/Tiles/Tile_47.png")
tile_plateformer_width, tile_plateformer_height = 16, 16
tile_boite = pygame.image.load("sprites/plateformer/3 Objects/Boxes/1_Idle.png")


#Gestion joueur
positionjoueur = [15,620]
joueur_w, joueur_h = 22, 30
joueur = pygame.Rect(positionjoueur[0],positionjoueur[1],joueur_w, joueur_h)

#Gestion affichage joueur
joueursimple_sheet = pygame.image.load("sprites/plateformer/1 Main Characters/2/Idle.png").convert_alpha()
joueurcourt_sheet = pygame.image.load("sprites/plateformer/1 Main Characters/2/Run.png").convert_alpha()

def get_image(sheet, frame, width, height, scale_w, scale_h):
    image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
    image.fill((0, 0, 0, 0))
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image, (scale_w, scale_h))
    return image


joueursimple0 = get_image(joueursimple_sheet,0,32,32,joueur_w, joueur_h)
joueursimple1 = get_image(joueursimple_sheet,3,32,32,joueur_w, joueur_h)
joueursimple2 = get_image(joueursimple_sheet,5,32,32,joueur_w, joueur_h)
joueursimple3 = get_image(joueursimple_sheet,7,32,32,joueur_w, joueur_h)
joueursimple5 = get_image(joueursimple_sheet,9,32,32,joueur_w, joueur_h)
l_joueursimple = [joueursimple0, joueursimple1, joueursimple2, joueursimple3, joueursimple5]
i_simple = 0 #l'index pour chercher l'image dans l_joueursimple et caractéristique d'elle
c_simple = pygame.time.get_ticks() #temps initial 

joueurcourt0 = get_image(joueurcourt_sheet,0,32,32,joueur_w, joueur_h)
joueurcourt1 = get_image(joueurcourt_sheet,4,32,32,joueur_w, joueur_h)
l_joueurcourt = [joueurcourt0, joueurcourt1]
i_court = 0
c_court = 0

joueurcharge = get_image(joueurcourt_sheet,5,32,32,joueur_w, joueur_h)
joueursaute = pygame.image.load("sprites/plateformer/1 Main Characters/2/Jump.png")
joueurtombe= pygame.image.load("sprites/plateformer/1 Main Characters/2/Fall.png")

joueur_a = joueursimple0

#Gestion DonkeyKong
def get_image2(sheet, frame, frame2, width, height, scale_w, scale_h):
    image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
    image.fill((0, 0, 0, 0))
    image.blit(sheet, (0, 0), ((frame * width), (frame2 * height) , width, height))
    image = pygame.transform.scale(image, (scale_w, scale_h))
    return image

donkey_sheet = pygame.image.load("sprites/DonkeyKong.png")

donkey_w, donkey_h = 115,135
positionDonkey = [810,positionplateforme4[1]-donkey_h]
donkey = pygame.Rect(positionDonkey[0],positionDonkey[1],donkey_w, donkey_h) 

donkeysimple = get_image2(donkey_sheet,2,1,47,43,donkey_w,donkey_h)
donkeytonneau_gauche = get_image2(donkey_sheet,0,1,47,43,donkey_w,donkey_h)
donkeytonneau_droite = get_image2(donkey_sheet,4,1,51,43,donkey_w,donkey_h)
donkey_a = donkeysimple

l_donkeytonneau = [donkeytonneau_gauche, donkeysimple, donkeytonneau_droite]
i_donkeytonneau = 0
c_donkeytonneau = 0

#Gestion Tonneaux
tonneau_w, tonneau_h = 30,30
tonneausimple = get_image2(donkey_sheet,1,0,20,17,tonneau_w,tonneau_h)

positionTonneaux = [[785,positionplateforme4[1]-tonneau_h]]
Tonneau = pygame.Rect(positionTonneaux[0][0],positionTonneaux[0][1], tonneau_w, tonneau_h)
l_tonneaux = [Tonneau]

tonneaux_detruits = 0

def dessiner(): 
    global fenetre, bg, tchrono_actuel
    fenetre.blit(bg, (0, 0)) # Dessine l'image de fond
    fenetre.blit(joueur_a, joueur)
    fenetre.blit(donkey_a, donkey)

    #Afficher sol
    for i in range(0, WIDTH, tile_plateformer_width):
        fenetre.blit(tile_surface, (i, soldebut))
    for j in range(0, WIDTH, tile_plateformer_width):
        for k in range(soldebut+tile_plateformer_height, 800, tile_plateformer_height):
            fenetre.blit(tile_terre, (j, k))
    
    #Afficher les tonneaux
    for i in range(len(l_tonneaux)):
        fenetre.blit(tonneausimple, l_tonneaux[i])

    #Afficher plateformes
    for j in range(0, plateforme_w, tile_plateformer_width):
        for k in range(plateforme1[1], plateforme1[1]+plateforme_h, tile_plateformer_height):
            fenetre.blit(tile_platforme, (j, k))
    for j in range(175, plateforme_w+175, tile_plateformer_width):
        for k in range(plateforme2[1], plateforme2[1]+plateforme_h, tile_plateformer_height):
            fenetre.blit(tile_platforme, (j, k))
    for j in range(0, plateforme_w, tile_plateformer_width):
        for k in range(plateforme3[1], plateforme3[1]+plateforme_h, tile_plateformer_height):
            fenetre.blit(tile_platforme, (j, k))
    for j in range(175, plateforme_w+175, tile_plateformer_width):
        for k in range(plateforme4[1], plateforme4[1]+plateforme_h, tile_plateformer_height):
            fenetre.blit(tile_platforme, (j, k))

    tchrono_actuel = pygame.time.get_ticks()
    temps_ecoule = (tchrono_actuel - debut_chrono) // 1000
    texte_chrono = police.render(str(temps_ecoule), True, (255,255,255))
    fenetre.blit(texte_chrono, (10,10))
    pygame.display.flip()

    
def dessinerperdu():
    global fenetre, debut_chrono, police, WIDTH, HEIGHT
    texte = 'Perdu'
    texte_surface = police.render(texte, True,(255,255,255))
    fenetre.blit(texte_surface,(WIDTH//2, HEIGHT//2))
    #Chrono
    tempsfinal = (pygame.time.get_ticks() - debut_chrono)//1000
    texte2 = 'Temps avant défaite:' + str(tempsfinal)
    texte_chrono = police.render(texte2, True, (255,255,255))
    fenetre.blit(texte_chrono,(WIDTH//2, HEIGHT//2+50))

def dessinervictoire():
    global fenetre, debut_chrono, police, WIDTH, HEIGHT
    texte = 'Gagné !'
    texte_surface = police.render(texte, True,(255,255,255))
    fenetre.blit(texte_surface,(WIDTH//2, HEIGHT//2))
    #Chrono
    tempsfinal = (pygame.time.get_ticks() - debut_chrono)//1000
    texte2 = 'Temps avant vicoire:' + str(tempsfinal)
    texte_chrono = police.render(texte2, True, (255,255,255))
    fenetre.blit(texte_chrono,(WIDTH//2, HEIGHT//2+50))

def gererclavier():
    global joueur, positionjoueur, vitesse_y, statutAir, sol_y, vitesse_x, direction, c_simple, i_simple, joueur_a, l_joueursimple, i_court, c_court, l_joueurcourt, joueursaute, joueurtombe, statutCharge, statutSaute, donkey_a, c_donkeytonneau, i_donkeytonneau, l_donkeytonneau, positionTonneaux, l_tonneaux, Tonneau, vitessetonneaux_y, tonneaux_detruits
    touchesPressees = pygame.key.get_pressed()

    #Animation Donkey + Gestion Tonneau
    t_actuel = pygame.time.get_ticks()
    if t_actuel - c_donkeytonneau > 1000:
        i_donkeytonneau = (i_donkeytonneau + 1) % len(l_donkeytonneau) #le reste devient l'indice
        if i_donkeytonneau == 0:
            positionTonneau_nouveau = ([785,positionplateforme4[1]-tonneau_h])
            nouveauTonneau = pygame.Rect(positionTonneau_nouveau[0],positionTonneau_nouveau[1], tonneau_w, tonneau_h)
            positionTonneaux.append(positionTonneau_nouveau)
            l_tonneaux.append(nouveauTonneau)
            vitessetonneaux_y.append(0)
            vitessetonneaux_x.append(-2)
        donkey_a = l_donkeytonneau[i_donkeytonneau]
        c_donkeytonneau = t_actuel

    for i in range(len(l_tonneaux)):
        positionTonneaux[i][0] = positionTonneaux[i][0] + vitessetonneaux_x[i]
        l_tonneaux[i] = pygame.Rect(positionTonneaux[i][0],positionTonneaux[i][1], tonneau_w, tonneau_h) #maj du rectangle associé 

    #Gestion gravité tonneau + collisions + surface
    for i in range(len(l_tonneaux)):
        vitessetonneaux_y[i] += GRAVITE
        positionTonneaux[i][1] += vitessetonneaux_y[i]

        tonneau_rect_test = pygame.Rect(positionTonneaux[i][0], positionTonneaux[i][1], tonneau_w, tonneau_h)

        if tonneau_rect_test.colliderect(plateforme1):
            if positionTonneaux[i][1] + tonneau_h <= positionplateforme1[1] + 10 and positionTonneaux[i][0] < positionplateforme1[0] + plateforme_w:
                positionTonneaux[i][1] = positionplateforme1[1] - tonneau_h
                vitessetonneaux_y[i] = 0
        elif tonneau_rect_test.colliderect(plateforme2):
            if positionTonneaux[i][1] + tonneau_h <= positionplateforme2[1] + 10 and positionTonneaux[i][0] < positionplateforme2[0] + plateforme_w:
                positionTonneaux[i][1] = positionplateforme2[1] - tonneau_h
                vitessetonneaux_y[i] = 0
        elif tonneau_rect_test.colliderect(plateforme3):
            if positionTonneaux[i][1] + tonneau_h <= positionplateforme3[1] + 10 and positionTonneaux[i][0] < positionplateforme3[0] + plateforme_w:
                positionTonneaux[i][1] = positionplateforme3[1] - tonneau_h
                vitessetonneaux_y[i] = 0
        elif tonneau_rect_test.colliderect(plateforme4):
            if positionTonneaux[i][1] + tonneau_h <= positionplateforme4[1] + 10 and positionTonneaux[i][0] < positionplateforme4[0] + plateforme_w:
                positionTonneaux[i][1] = positionplateforme4[1] - tonneau_h
                vitessetonneaux_y[i] = 0
        elif positionTonneaux[i][1] + tonneau_h >= soldebut:
            positionTonneaux[i][1] = soldebut - tonneau_h
            vitessetonneaux_y[i] = 0
        
        if tonneau_rect_test.colliderect(bord_g):
            vitessetonneaux_x[i] = -vitessetonneaux_x[i]
        if tonneau_rect_test.colliderect(bord_d):
            vitessetonneaux_x[i] = -vitessetonneaux_x[i]
        
        if joueur.colliderect(l_tonneaux[i]):
            del l_tonneaux[i]
            del positionTonneaux[i]
            del vitessetonneaux_y[i]
            tonneaux_detruits += 1
            if tonneaux_detruits >= 3:
                dessinerperdu()
                pygame.display.flip()
                pygame.time.delay(3000)
                pygame.quit()
                exit()
            break        

    #Animation simple
    if touchesPressees[pygame.K_LEFT] == False and touchesPressees[pygame.K_RIGHT] == False and touchesPressees[pygame.K_SPACE] == False and statutAir == False:
        t_actuel = pygame.time.get_ticks()
        if t_actuel - c_simple > 150:
            i_simple = (i_simple + 1) % len(l_joueursimple) #le reste devient l'indice
            if direction == 'droite' or direction == 'neutre':
                joueur_a = l_joueursimple[i_simple]
            else:
                joueur_a = pygame.transform.flip(l_joueursimple[i_simple], True, False)
            c_simple = t_actuel #recommence ze process

    #Gauche/droite
    if touchesPressees[pygame.K_RIGHT] == True and positionjoueur[0]<978 and statutAir==False:
        if statutCharge == False:
            positionjoueur[0] += PLAYER_VEL
            #Animation
            t_actuel = pygame.time.get_ticks()
            if t_actuel - c_court > 100:
                i_court = (i_court + 1) % len(l_joueurcourt) #le reste devient l'indice
                joueur_a = l_joueurcourt[i_court]
                c_court = t_actuel
        direction = 'droite'
    if touchesPressees[pygame.K_LEFT] == True and positionjoueur[0]>0 and statutAir==False:
        if statutCharge == False:
            positionjoueur[0] -= PLAYER_VEL
            #Animation
            t_actuel = pygame.time.get_ticks()
            if t_actuel - c_court > 100:
                i_court = (i_court + 1) % len(l_joueurcourt) #le reste devient l'indice
                joueur_a = pygame.transform.flip(l_joueurcourt[i_court], True, False)
                c_court = t_actuel
        direction = 'gauche'
    if touchesPressees[pygame.K_UP] == True and positionjoueur[0]<978 and statutAir==False:
        direction = 'neutre'
    joueur = pygame.Rect(positionjoueur[0],positionjoueur[1],joueur_w, joueur_h) #Met à jour avec nouvelles positions
    
    #Saut directionnel + Collision avec les bords
    if statutAir == True:
        if vitesse_y < 0:
            statutSaute = True
        else:
            statutSaute = False
        if joueur.colliderect(bord_d) or joueur.colliderect(bord_g):
            vitesse_x = -vitesse_x * 0.75
        positionjoueur[0] += vitesse_x 
    
    #Gravite
    positionjoueur[1] += vitesse_y
    vitesse_y += GRAVITE
    if statutAir == True and vitesse_y > 0:
        if direction == 'droite' or direction == 'neutre':
            joueur_a = joueursaute
        else:
            joueur_a = pygame.transform.flip(joueursaute, True, False)
    if statutAir == True and vitesse_y < 0:
        if direction == 'droite' or direction == 'neutre':
            joueur_a = joueurtombe
        else:
            joueur_a = pygame.transform.flip(joueurtombe, True, False)
    
    #Choix du sol
    if joueur.colliderect(plateforme1):
        if positionjoueur[1] < positionplateforme1[1] and positionjoueur[0] < positionplateforme1[0] + plateforme_w:
            sol_y = round(plateforme1[1]+1)
        elif positionjoueur[1] <= positionplateforme1[1] + plateforme_h and positionjoueur[0] < positionplateforme1[0] + plateforme_w:
            positionjoueur[1] = positionplateforme1[1] + plateforme_h
            vitesse_y = 0
            vitesse_x = vitesse_x*0.5
    elif joueur.colliderect(plateforme2):
        if positionjoueur[1] < positionplateforme2[1] and positionjoueur[0] < positionplateforme2[0] + plateforme_w:
            sol_y = round(plateforme2[1]+1)
        elif positionjoueur[1] <= positionplateforme2[1] + plateforme_h and positionjoueur[0] < positionplateforme2[0] + plateforme_w:
            positionjoueur[1] = positionplateforme2[1] + plateforme_h
            vitesse_y = 0
            vitesse_x = vitesse_x*0.5
    elif joueur.colliderect(plateforme3):
        if positionjoueur[1] < positionplateforme3[1] and positionjoueur[0] < positionplateforme3[0] + plateforme_w:
            sol_y = round(plateforme3[1]+1)
        elif positionjoueur[1] <= positionplateforme3[1] + plateforme_h and positionjoueur[0] < positionplateforme3[0] + plateforme_w:
            positionjoueur[1] = positionplateforme3[1] + plateforme_h
            vitesse_y = 0
            vitesse_x = vitesse_x*0.5
    elif joueur.colliderect(plateforme4):
        if positionjoueur[1] < positionplateforme4[1] and positionjoueur[0] < positionplateforme4[0] + plateforme_w:
            sol_y = round(plateforme4[1]+1)
        elif positionjoueur[1] <= positionplateforme4[1] + plateforme_h and positionjoueur[0] < positionplateforme4[0] + plateforme_w:
            positionjoueur[1] = positionplateforme4[1] + plateforme_h
            vitesse_y = 0
            vitesse_x = vitesse_x*0.5
    else:
        sol_y = soldebut
    
    
     #Collision avec le sol
    if positionjoueur[1]+30 >= sol_y:
        positionjoueur[1] = sol_y-30
        vitesse_y = 0
        statutAir = False
    
    #Win condition: collision donkeykong/joueur
    if joueur.colliderect(donkey):
        dessinervictoire()
        pygame.display.flip()
        pygame.time.delay(3000)
        pygame.quit()
        exit()

    


def main(window):
    global statutCharge, compteurcharge, temps_charge_debut, vitesse_y, statutAir, vitesse_x, direction, joueur_a
    jouer = True
    while jouer:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type ==  pygame.QUIT:
                jouer = False
                break
            
            #Commencer la charge du saut 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and statutAir == False:
                    statutCharge = True
                    temps_charge_debut = pygame.time.get_ticks() # Temps de début de la charge
                    if direction == 'droite' or direction == 'neutre':
                        joueur_a = joueurcharge
                    else:
                        joueur_a = pygame.transform.flip(joueurcharge, True, False)
        
            #Relache la charge du saut 
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE and statutAir == False and statutCharge == True:
                temps_charge = pygame.time.get_ticks() - temps_charge_debut #Temps actuel - temps de début
                temps_charge = min(temps_charge, charge_max) #valeur minimale comme ça si on dépasse max charge c'est elle qui est prise
                force_saut = temps_charge * charge_force_ratio * 1.1
                vitesse_y = -force_saut
                if direction == 'droite':
                    vitesse_x = temps_charge * charge_force_ratio * 0.4
                elif direction == 'gauche':
                    vitesse_x = -temps_charge * charge_force_ratio * 0.4
                else:
                    vitesse_x = 0
                statutAir = True
                statutCharge = False

                
            
        dessiner()
        gererclavier()
    pygame.quit()
    quit()
    
if __name__ == "__main__":
    main(fenetre)