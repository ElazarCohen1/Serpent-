from fltk import *
from time import sleep
from random import randint
from pathlib import Path 

#############
# fonctions #
#############

# truc technique

def case_vers_pixel(case):
    """
	Reçoit les coordonnées d'une case du plateau sous la forme d'un couple
	d'entiers (colonne, ligne) et renvoie les coordonnées du centre de cette
	case sous la forme d'un couple de flottants (abscisse, ordonnée). 
    
    Ce calcul prend en compte la taille de chaque case, donnée par la variable
	globale `taille_case`.

    >>> taille_case = 10
    >>> case_vers_pixel((4, 6))
    (45.0, 65.0)
    """
    i, j = case
    return (i + .5) * taille_case, (j + .5) * taille_case

def taille_jeu():
    x,y = case_vers_pixel((1,2))
    x1,y1 = case_vers_pixel((38,27))
    rectangle(x-taille_case/2,y-taille_case/2,
              x1+taille_case/2,y1-taille_case/2,
              couleur = "black",epaisseur = 2,remplissage = "#47BEAE")

def jouer():
    """toute les conditions pour arreter le jeu """
    if serpent_sort() or serpent_sort_2() or toucher_corp(serpent) or toucher_corp(serpent_2) or toucher_mur(mur,serpent) or toucher_mur(mur,serpent_2)  == True:
        return False
    else:
        return True

def actualiser_affichage():
    """si on recommence on actualise l'affichage depuis le debut """
    x1,y1 = case_vers_pixel((40,30))
    x2,y2 = case_vers_pixel((1,26))
    x3,y3 = case_vers_pixel((5,29))
    x4,y4 = case_vers_pixel((1,27))
    x5,y5 = case_vers_pixel((2,0))
    x6,y6 = case_vers_pixel((33,0))
    x7,y7 = case_vers_pixel((20,15))
    x8,y8 = case_vers_pixel((13,0))
    efface_tout()
    rectangle(0,0,x1+taille_case/2,y1-taille_case/2,
              remplissage = "#3F7A72")
    taille_jeu()
    image(x7,y7,fichier = "img.png")
    affiche_pommes(pommes)  
    affiche_serpent(serpent,serpent_2)
    affiche_mur(mur)
    texte(x5,y5,f"score-1 : {score}",taille = taille_case)
    texte(x8,y8,f"score-2 : {score_2}",taille = taille_case)
    texte (x6,y6,f"record : {record_b(lst_scores)}" ,taille = taille_case) 
    rectangle(x2-taille_case/2,y2+taille_case/2,
              x3+taille_case/2,y3-taille_case/2,remplissage ="black")
    texte(x4,y4,"QUITTER", couleur = "red",taille = 15)
    mise_a_jour()

def actualiser_etat_jeu():
    """si on recommence on actualise les données du joueur depuis le debut """
    framerate = 5   
    direction = (0,0)
    direction_2 = (0,0)  
    serpent = [[1,26]]  
    serpent_2 = [[38,2]]
    mur = coordonnée_mur()
    pommes= coordonee_pommes(serpent[0],mur)
    score = 0
    score_2 = 0
    
    return framerate,direction,direction_2,serpent,serpent_2,pommes,score,score_2,mur
      
def record_b(score):
    """determine le record et le stock dans un fichier record.txt """
    mon_fichier = Path("record.txt")
    with mon_fichier.open("r") as r:
        record = r.read()
    for i in score:
        if i > int(record):
            record = str(i)
    with mon_fichier.open("w") as w:
        r = w.write(record)
    return record

# pommes

def coordonee_pommes(serpent,mur):
    """renvoie la liste des coordonne de pommes """
    pommes = []
    for i in range(randint(3,6)):
        apple = [randint(2,37),randint(3,26)]
        while apple == serpent or apple in mur :
            apple =  [randint(1,38),randint(2,26)]
        pommes.append(apple)

    return pommes

def affiche_pommes(pommes):
    """
	Dessine une pomme dans chaque case désignée par la liste de couples
	d'entiers `pommes`. Pas de valeur de retour.
    """        
    i = 0
    while i < len(pommes):
        pomme = pommes[i]
        x, y = case_vers_pixel(pomme)
        cercle(x, y, taille_case/2,
               couleur='darkred', remplissage='red',tag = 'pommes')
        rectangle(x-2, y-taille_case*.4, x+2, y-taille_case*.7,
                  couleur='darkgreen', remplissage='darkgreen',tag = 'pommes')
        i += 1    

def superposition(pommes,serpent):
    """renvoie vrai si le serpent touche une pommes et sinon false"""
    if serpent[0] in pommes: 
        return True
    else:
        return False
    
def supprimer_pommes(pommes,serpent):
    """renvoie l'index pour supprimer la pommes une fois passer dessus"""
    if superposition(pommes,serpent)  == True:
        return pommes.index(serpent[0])
 
# mur 
def change_x(n,x,y):
    """fais des mur en changant l'abscice """
    wall = []
    for i in range(n):
        brique = [x,y]
        x+=1
        wall.append(brique)
    return wall
       
def change_y(n,x,y):
    """fais des mur en changant l'ordonnée """
    wall = []
    for i in range(n):
        brique = [x,y]
        y+=1
        wall.append(brique)
    return wall

def coordonnée_mur():
    """renvoir toute les coordonnées des murs a afficher"""
    mur = [] 
    wall = change_x(9,2,3)
    mur.extend(wall)
    
    wall_1 = change_y(8,15,5)
    mur.extend(wall_1)

    wall_2 = change_x(8,2,20)
    mur.extend(wall_2)

    wall_3 = change_x(8,22,10)
    mur.extend(wall_3)

    wall_4 = change_y(5,20,20)
    mur.extend(wall_4)

    wall_5 = change_x(6,24,24)
    mur.extend(wall_5)

    wall_6 = change_y(4,35,4)
    mur.extend(wall_6)

    wall_7 = change_y(4,2,8)
    mur.extend(wall_7)

    """ wall_8 = change_x(3,12,5)
    mur.extend(wall_8)"""

    wall_9  = change_y(6,29,11)
    mur.extend(wall_9)

    wall_10 = change_x(4,31,4)
    mur.extend(wall_10)
    return mur

def affiche_mur(mur):
    """prend la coordonnée du mur aleatoirement et affiche a la case corespondante"""
    i= 0
    while i < len(mur):
        m = mur[i]
        x,y = case_vers_pixel(m)
        rectangle(x-taille_case/2, y+taille_case/2, x+taille_case/2, y-taille_case/2,
                  remplissage = "#144DE6", tag = "m")
        i+=1 

def toucher_mur(mur,serpent):
    """si le serpent touche un mur il renvoit vrai sinon Faux """
    if serpent[0] in mur:
        return True
    else:
        return False
    
# serpent 1
 
def affiche_serpent(serpent,serpent_2): 
    """affiche les deux serpent"""
    i = 0
    while i < len(serpent):
        s = serpent[i]
        x, y = case_vers_pixel(s)
        cercle(x, y, taille_case/2 + 1,
            couleur='darkgreen', remplissage='yellow')
        i +=1
    i = 0
    while i < len(serpent_2):
        e = serpent_2[i]
        x, y = case_vers_pixel(e)
        cercle(x, y, taille_case/2 + 1,
            couleur='darkgreen', remplissage='orange')
        i +=1

def bouger_serpent(serpent,direction):
    """renvoie les coordonnée du serpent pour le bouger """
    x = serpent[0][0] + direction[0]
    y = serpent[0][1] + direction[1]
    serpent = [x,y]
    return serpent

def change_direction(direction, touche):
    """
    Renvoie le vecteur unitaire indiquant la direction correspondant à la touche
    pressée par l'utilisateur. Les valeurs de retour possibles sont `(0, 1)`,
    `(1, 0)`, `(0, -1)` et `(-1, 0)`.
    """
    if jouer() == False:
        return (0,0)
    if touche == 'Up':
        if direction == (0,1):
            return (0,1)
        return (0, -1)
    elif touche == 'Down':
        if direction == (0,-1):
            return (0,-1)
        return (0,1)
    elif touche == 'Left':
        if direction == (1,0):
            return (1,0)
        return (-1,0)
    elif touche == 'Right':
        if direction == (-1,0):
            return (-1,0)
        return (1,0)
    else:      
        return direction

def serpent_sort():
    """si le serpent sort du jeu on renvoie Vrai"""
    x,y = bouger_serpent(serpent,direction)
    if  x < 0 or x > 39 or y < 1 or y > 27:
        return True
    else:
        return False

def toucher_corp(serpent):
    """renvoie un bool si la tete touche le corp"""
    se = []
    se.extend(serpent)
    del(se[0])
    if serpent[0] in se:
        return True
    else:
        return False    
     
def suivre_serpent(serpent):
    """ajoute la nouvelle tete du serpent et supprime la derniere queue 
       si on mange une pommes il supprime pas la derniere queue (ca rajoute un cercle)
       renvoie le serpent """
    Tserpent = bouger_serpent(serpent,direction)
    serpent.insert(0,Tserpent)
    if superposition(pommes,serpent) == False:
        serpent.pop()
    return serpent

#serpent 2

def change_direction_2(direction,touche):
    """
    Renvoie le vecteur unitaire indiquant la direction correspondant à la touche
    pressée par l'utilisateur. Les valeurs de retour possibles sont `(0, 1)`,
    `(1, 0)`, `(0, -1)` et `(-1, 0)`.
    """
    if jouer() == False:
        return (0,0)
    if touche == 'z':
        if direction == (0,1):
            return (0,1)
        return (0, -1)
    elif touche == 's':
        if direction == (0,-1):
            return (0,-1)
        return (0,1)
    elif touche == 'q':
        if direction == (1,0):
            return (1,0)
        return (-1,0)
    elif touche == 'd':
        if direction == (-1,0):
            return (-1,0)
        return (1,0)
    else:      
        return direction

def bouger_serpent_2(serpent_2,direction_2):
    """renvoie les coordonnée du serpent pour le bouger """
    x = serpent_2[0][0] + direction_2[0]
    y = serpent_2[0][1] + direction_2[1]
    serpent = [x,y]
    return serpent

def suivre_serpent_2(serpent_2):
    """ajoute la nouvelle tete du serpent et supprime la derniere queue 
       si on mange une pommes il supprime pas la derniere queue (ca rajoute un cercle)
       renvoie le serpent """
    Tserpent = bouger_serpent_2(serpent_2,direction_2)
    serpent_2.insert(0,Tserpent)
    if superposition(pommes,serpent_2) == False:
        serpent_2.pop()
    return serpent_2

def serpent_sort_2():
    """si le serpent sort du jeu on renvoie Vrai"""
    x,y = bouger_serpent_2(serpent_2,direction_2)
    if  x < 0 or x > 39 or y < 1 or y > 27:
        return True
    else:
        return False


#######################
# programme principal #
#######################

if __name__ == "__main__":
    taille_case = 20
    largeur_plateau = 40  # en nombre de cases
    hauteur_plateau = 30  # en nombre de cases    
    rejouer = True
    lst_scores = [] 
    framerate,direction,direction_2,serpent,serpent_2,pommes,score,score_2,mur = actualiser_etat_jeu()
    cree_fenetre(taille_case * largeur_plateau,
                 taille_case * hauteur_plateau)
   # boucle principale
    while  rejouer :
        if jouer() == True:
            actualiser_affichage() # affichage des objets 
        ev = donne_ev()  
        ty = type_ev(ev)
        if ty == 'Quitte':
            rejouer = False
        elif ty == 'Touche':
            direction = change_direction(direction, touche(ev))
            direction_2 = change_direction_2(direction_2,touche(ev))
        elif ty == "ClicGauche" or ty == "ClicDroit":
            x = abscisse(ev)
            y = ordonnee(ev)
            i = (x / taille_case) - 0.5
            j = (y / taille_case) - 0.5
            if 1 <= i<= 5 and 26 <= j<= 29 :
                rejouer =  False
        serpent = suivre_serpent(serpent) 
        serpent_2 = suivre_serpent_2(serpent_2)
        if pommes == []: # rajoute des pommes au hasard quand il y'en a plus
            pommes = coordonee_pommes(serpent,mur)
        if superposition(pommes,serpent)  == True: # verifie si serpent 1 mange une pomme 
            framerate +=1
            idx = supprimer_pommes(pommes,serpent)
            pommes.pop(idx) 
            score+=1
        elif superposition(pommes,serpent_2) == True:  # verifie si serpent_2 mange une pomme 
            framerate +=1
            idx_2 = supprimer_pommes(pommes,serpent_2)
            pommes.pop(idx_2)
            score_2 +=1 
        # si on a perdu
        if jouer() == False:
            if toucher_mur(mur,serpent) or toucher_mur(mur,serpent_2) or toucher_corp(serpent) or toucher_corp(serpent_2)  == True :
                direction = (0,0)
                direction_2 = (0,0)
            lst_scores.append(score) # ajoute le score a une liste pour calculer le max 
            lst_scores.append(score_2)
            serpent = suivre_serpent(serpent)
            serpent_2 = suivre_serpent(serpent_2)
            x1,y1 = case_vers_pixel((8,13))
            efface("m") #efface les murs 
            efface("pommes") #efface les pommes 
            texte(x1,y1,"Veux-tu relancer ? (oui: Entrée), (non : échap)",couleur ="red",taille = taille_case)
            mise_a_jour()
            if ty == 'Quitte': # si on appuie sur la croix on quitte 
                rejouer = False
            elif ty == 'Touche':
                touch = touche(ev)
                if touch == 'Return':  # si on appuie sur entrée on relance la partie en mettant tout a 0 
                    actualiser_affichage()
                    framerate,direction,direction_2,serpent,serpent_2,pommes,score,score_2,mur = actualiser_etat_jeu()
                elif touch == 'Escape': # sinon on quitte le jeu 
                    rejouer = False
        sleep(1/framerate)

    #fermeture et sortie
    ferme_fenetre() 
            
