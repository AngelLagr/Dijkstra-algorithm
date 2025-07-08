from copy import deepcopy
import math as mt
import os

gexo10 = {
        'A':{'duree':3,'precedent':set()},
        'B':{'duree':4,'precedent':{'A','I'}},
        'C':{'duree':1,'precedent':{'B'}},
        'D':{'duree':4,'precedent':set()},
        'E':{'duree':2,'precedent':{'H','D'}},
        'F':{'duree':5,'precedent':{'I','D','E'}},
        'G':{'duree':1,'precedent':set()},
        'H':{'duree':3,'precedent':{'G'}},
        'I':{'duree':5,'precedent':{'H'}},
        'J':{'duree':6,'precedent':set()},
        'K':{'duree':3,'precedent':{'J','I'}},
        'L':{'duree':14,'precedent':set()},
        'M':{'duree':2,'precedent':{'I'}},
        'N':{'duree':2,'precedent':{'M','L'}},
        'O':{'duree':3,'precedent':{'M','C','F'}},
        'P':{'duree':3,'precedent':{'N','O'}},
        'Q':{'duree':2,'precedent':{'P','S'}},
        'R':{'duree':1,'precedent':{'N','K','O'}},
        'S':{'duree':3, 'precedent':{'R'}}
         }
    
dic_prec = {
        'A':{'duree':3,'precedent':set()},
        'B':{'duree':9,'precedent':set()},
        'C':{'duree':5,'precedent':set()},
        'D':{'duree':8,'precedent':{'A'}},
        'E':{'duree':4,'precedent':{'B'}},
        'F':{'duree':7,'precedent':{'B'}},
        'G':{'duree':20,'precedent':{'B'}},
        'H':{'duree':6,'precedent':{'C','F'}},
        'I':{'duree':5,'precedent':{'D','E'}}
        }

##################################################################################################################################################################
def couleur_arc(dico_precedents:dict)->dict:
    graphe=deepcopy(dico_precedents)
    for sommet1 in graphe.keys():
        prec_color={}
        for sommet2 in graphe[sommet1]['precedent']:
            prec_color[sommet2]='black'
        graphe[sommet1]['precedent']=prec_color
    return graphe

def f_niveau(graph:dict)->list:
    """

    Parameters
    ----------
    graph : dict
        Graphe.

    Returns
    -------
    list
        Renvoie une liste des sommets du graphe rangés par niveau dans l'ordre croissant.

    """
    dic=deepcopy(graph)
    #Transformation du dictionnaire des suivants en un ensemble
    for sommet in dic.keys():
        dic[sommet]['precedent']=set(dic[sommet]['precedent'].keys())
    #==========================================================
    liste=[set(),] # L'ensemble Ci sera liste[i]
    T=set() # Ensemble des sommets traites, initialise a "vide"
    S=set(dic.keys()) # Ensemble de tous les sommets
    k = 0 # k represente le niveau "traite" dans l'algorithme
    #===== Initialisation =====
    for sommet in S:
        if not dic[sommet]['precedent']: # Les sommets sans precedents ...
            T.add(sommet) # sont traites et ...
            liste[k].add(sommet) # sont de niveau 0
    #===== Boucle while =====
    while T != S :
        for sommet in S-T: # Pour les sommets non traites
            # On raye les sommets de niveau k dans la liste des precedents :
            dic[sommet]['precedent']=dic[sommet]['precedent']-liste[k]
        k = k + 1
        # On cree un ensemble pour le sommets de niveau "k+1", initialise a vide :
        liste.append(set())
        for sommet in S-T: # Pour tous les sommets non traites
            if not dic[sommet]['precedent']: # Si le sommet n'a plus de precedent
                T.add(sommet) # il est traite et ...
                liste[k].add(sommet) # est de niveau "k+1"
    return liste

def dic2dot(dic:dict,fileName=None)->str:
    txt_f = 'digraph G2 {\nrankdir=LR;\nnode [shape = Mrecord, style=filled];'
    for sommet,dico in dic.items():        
        plustot=dico['tot']
        plustard=dico['tard']
        bordure=dico['couleur']
        txt_f += f'\n{sommet} :t [label="'+'{'+f' {plustot} | {plustard}'
        txt_f += ' }'+f'|<t> {sommet}",fillcolor={"white"},color={bordure}];'
    for sommet,dico in dic.items():
        for suivant in dico['suivant'].keys():
            cout=dico['duree']
            trait=dico['suivant'][suivant]
            txt_f += f'\n{sommet}->{suivant} [label={cout},color={trait}];'
    txt_f += '\n }'
    if fileName != None:
        with open(fileName,'w') as fd:
            fd.write(txt_f)
    return txt_f
##################################################################################################################################################################
def prec2complet(dico:dict)->dict:
    """

    Parameters
    ----------
    dico : dict
        Graphe.

    Returns
    -------
    dict
        Retourne le graphe donné en y ajoutant à ses sommet la clé 'suivant' et en lui affectant le graphe correspondant.

    """
    for dico_s in dico.values():
        dico_s['suivant']={}
    for sommet, dico_s in dico.items():
        for sommet_pre in dico_s['precedent'].keys():
            dico[sommet_pre]['suivant'][sommet]='black'
    return dico
##################################################################################################################################################################
def graph_fin(graph:dict)->dict:
    """

    Parameters
    ----------
    graph : dict
        Graphe.

    Returns
    -------
    dict
        Renvoie le graphe donné en y ajoutant un sommet 'fin' puis en y ajoutant à ses sommets la clé 'couleur' avec la valeur 'black'.

    """
    D=dict()
    for sommet, dico_s in graph.items():
        dico_s['couleur']='black'
        for _ in dico_s['precedent'].keys():
            if dico_s['suivant']=={}:
                D[sommet]='black'
        
    graph['fin']={'duree':0,'precedent':D,'suivant':{},'couleur':'black'}
    return prec2complet(graph) # on réactualise les clés "suivant" pour le sommet fin
##################################################################################################################################################################
def affecte_f_niveau(graph:dict)->dict:
    """

    Parameters
    ----------
    graph : dict
        Graphe.

    Returns
    -------
    dict
        Renvoie le graphe donné en y ajoutant une clé "niveau" à tout ses sommets avec la bonne valeur associée.

    """
    L=f_niveau(graph)
    for niveau in range(0,len(L)):
        for sommet, dico_s in graph.items():
            if sommet in L[niveau]:
                dico_s['niveau']=niveau
    return graph
##################################################################################################################################################################
def graphe2mpm(graph:dict)->dict:
    """

    Parameters
    ----------
    graph : dict
        Graphe.

    Returns
    -------
    dict
        Ajoute les clés "tot" et "tard" à tout les sommets avec la valeur "_".

    """
    for sommet,dico_s in graph.items():
      dico_s['tot']='_'
      dico_s['tard']='_'
    return graph
##################################################################################################################################################################
def sommetini(graph:dict)->list:
    """

    Parameters
    ----------
    graph : dict
        Graphe

    Returns
    -------
    list
        Retourne une liste contenant tout les sommets sans predecesseurs.

    """
    liste=[]
    for sommet in graph.keys():
        if graph[sommet]['precedent']=={}:
            liste.append(sommet)
    return(liste)
        

def sommetatteignable(graph:dict,s:str)->list:
    """
    
    Parameters
    ----------
    graph : dict
        Graphe
        
    s : str
        sommet initial   
    Returns
    -------
    list
        Retourne une liste contenant tout les sommets "atteignables" en partant du sommet s.

    """
    liste=[[s]] #on commence avec le sommet initial
    sommetetudie=s
    fait=set(s) #on initialise un ensemble des sommets étudiés
    while graph[sommetetudie]['suivant']!={}: #tant que les sommets étudiés ont des sommets suivants
        for lsommet in liste:#pour les listes contenues dans "liste"
            lsuiv=[] #on initialise une liste qui contiendras les sommets suivants du sommet étudié
            for sommet in lsommet:#pour chaque sommet présent dans la liste de sommets étudiés
                sommetetudie=sommet #on étudie un sommet à la fois
                for sommetsuiv in graph[sommetetudie]['suivant'] : #parmis tout les sommets suivants dans le sommet étudié
                    if sommetsuiv not in fait: #si l'un de ces sommets n'a pas encore été traités
                        lsuiv.append(sommetsuiv)  #on le rajoute dans la liste "lsuiv"
                        fait=fait.union({sommetsuiv})
    
                if lsuiv!=[] and lsuiv not in liste:#on évite les erreurs de listes vides ou que l'on retrouve une même liste plusieurs fois
                    liste.append(lsuiv)
    # ici on à problème c'est que l'on se retrouve avec une liste contenant d'autres liste. Afin d'éviter ce problème on créer une nouvelle liste dans laquelle on rajoute tout les sommets étudiés                
    nvlliste=[] #
    for lsommet in liste:
        for sommet in lsommet:
            nvlliste.append(sommet)
    return nvlliste
      

def ford(graph:dict,f:str)->int:
    """
    
    Parameters
    ----------
    graph : dict
        Graphe.
    f : str
        sommet.
    
    Returns
    -------
    int
        Retourne la valeur du chemin le plus élévé juqu'au sommet f en partant de n'importe quel sommet initial.
    
    """
    lniveau=f_niveau(graph)  #on récupère la liste des sommets qui permettent d'atteindre le point f
    maximum=[]
    for sommet0 in sommetini(graph): # on étudie tous les potentiels s0 pour arriver à f
       if f in sommetatteignable(graph,sommet0):
          P={list(graph.keys())[i] for i in range(len(graph))} #ensemble des sommets
          trace={sommet0:[0,None]} #initialisation coût s0
          for s in P-{sommet0}: #initialisation coûts associés aux sommets différents de s0
              trace[s]=[mt.inf,None]
          k=1
          while trace[f][0]==mt.inf:
            for y in lniveau[k]: #ensemble des sommets de niveau k          
              value=[trace[x][0]+graph[x]['duree'] for x in graph[y]['precedent'] if x in sommetatteignable(graph,sommet0)]
              if value!=[]: 
                trace[y][0]=max(value)
      
              for z in graph[y]['precedent']:       
                if trace[z][0]+graph[z]['duree']==trace[y][0] and z in sommetatteignable(graph,sommet0):
                  trace[y][1]=z 
            k+=1
          maximum.append(trace[f][0])    
             
    if maximum!=[]:
      maxi=max(maximum)  #on compare la durée des chemins menant à f suivant les sommets de départs choisis  
    else:
      maxi=0
    return maxi

  
def plustot(graph:dict)->dict:
    """

    Parameters
    ----------
    graph : dict
        Graphe.

    Returns
    -------
    dict
        Renvoie le Graphe donné en paramêtre avec la clé 'tot' remplie par la valeur correspondante sur chacun de ses sommets.

    """
    for sommet in graph.keys(): # on ajoute la valeur associée aux sommets à la clé "tot"
      graph[sommet]['tot']=ford(graph,sommet)
    return graph
##################################################################################################################################################################
def plustard(graph:dict)->dict:
    """

    Parameters
    ----------
    graph : dict
        Graphe.

    Returns
    -------
    dict
        Renvoie le Graphe donné en paramêtre avec la clé 'tard' remplie par la valeur correspondante sur chacun de ses sommets.


    """
    n=f_niveau(graph)
    trace={'fin':ford(graph,'fin')}
    
    for ensemble in n[:-1]: 
      for sommet in ensemble:
        trace[sommet]=mt.inf
    k=graph['fin']['niveau']
    
    while max([trace[i] for i in n[0]])==mt.inf: 
      for u in n[k-1]:
        value=[trace[v]-graph[u]['duree'] for v in graph[u]['suivant']]
        if value!=[]:
            trace[u]=min(value) 
      k-=1
    
    for sommet in trace.keys():# on ajoute la valeur associée aux sommets à la clé "tard"
      graph[sommet]['tard']=trace[sommet]
    return graph
##################################################################################################################################################################
def margeT(graph:dict)->dict:
    """

    Parameters
    ----------
    graph : dict
        Graphe.

    Returns
    -------
    dict
        Renvoie le Graphe donné en paramêtre avec la clé 'MT' remplie par la valeur de la marge totale correspondante sur chacun de ses sommets.

    """
    for sommet in graph.keys():
      graph[sommet]['MT']=graph[sommet]['tard']-graph[sommet]['tot']
    return graph
##################################################################################################################################################################
def margeL(graph:dict)->dict:
    """

    Parameters
    ----------
    graph : dict
        Graphe.

    Returns
    -------
    dict
        Renvoie le Graphe donné en paramêtre avec la clé 'ML' remplie par la valeur de la marge libre correspondante sur chacun de ses sommets.

    """
    for sommet in graph.keys():
      listemarge=[graph[sommetsuiv]['tot'] - graph[sommet]['tot'] - graph[sommet]['duree'] for sommetsuiv in graph[sommet]['suivant']]
      if listemarge!=[]:
        graph[sommet]['ML']=min(listemarge)
      else:
        graph[sommet]['ML']=0
    return graph  
##################################################################################################################################################################
def affiche(graph:dict)->None:
    """

    Parameters
    ----------
    graph : dict
        Graphe.

    Returns
    -------
    None
        Ne retourne rien, affiche un tableau avec tout les sommets du graphe et la valeur du debut des taches au plus tard et au plus tot et la valeur des marges totales et libres correspondantes.

    """
    print("sommet +tot +tard MT ML")
    for sommet,dico in graph.items():
        i1=len(sommet)
        i2=len(str(dico['tot']))
        i3=len(str(dico['tard']))
        i4=len(str(dico['MT']))
        print(sommet+(7-i1)*" "+str(dico['tot'])+(5-i2)*" "+str(dico['tard'])+(6-i3)*" "+str(dico['MT'])+(3-i4)*" "+str(dico['ML']))
##################################################################################################################################################################
def critique(graph:dict)->dict:
    """

    Parameters
    ----------
    graph : dict
        Graphe.

    Returns
    -------
    dict
        Colorie les sommets critiques en rouge sur le Graphe donné en paramêtre.

    """
    for sommet in graph.keys():
      if graph[sommet]['tot']==graph[sommet]['tard']:
        graph[sommet]['couleur']='red'
    return graph

#Test Exo 4.9#################################################################################################################################################
print("Exo 4.9 :\n")
Gra=critique(margeL(margeT(plustot(plustard(graphe2mpm(affecte_f_niveau(graph_fin(prec2complet(couleur_arc(dic_prec))))))))))
dic2dot(Gra,'Exo4_9.dot')
os.system("dot -Tpng Exo4_9.dot -o Exo4_9.png")
affiche(Gra)
print("\n")

#Test Exo 4.10################################################################################################################################################
print("Exo 4.10 :\n")
Gra=critique(margeL(margeT(plustot(plustard(graphe2mpm(affecte_f_niveau(graph_fin(prec2complet(couleur_arc(gexo10))))))))))
dic2dot(Gra,'Exo4_10.dot')
os.system("dot -Tpng Exo4_10.dot -o Exo4_10.png")
affiche(Gra)

