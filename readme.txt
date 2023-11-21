#############################
Application My E-Bibliothèque
#############################


Cette application à pour but de simplifier les emprunts de livre dans une bibliothèque. Avec cette application
vous pouvez gérer les utilisateurs de la bibliothèques, repertorier les livres. Et générer des statistiques sur les emprunts
des derniers jours. Un ficher csv est aussi exportable pour des traitement xlsx. 


##############################################################
BIBLIOTHEQUES ET CLASS 
##############################################################

!!! Installer matplolib !!!
--> commande : pip install matlotlib

Toutes les bibliothèques utilisées sont : 
- Tkinter, avec les class ttk, messagebox,
- SQLite3
- Datetime, timedelta
- Matplotlib et sa class FigureCanvasTkAgg
- CSV 

Tkinter : 
- TTK : pour le style des boutons et des labels (certains)
- Messagebox : pour les popup d'alerte et les message suivant les actions (ajout, suppression)

SQlite3 : 
- Gestion de la base de données, création et modification
- Requête python sur la base, pour remplir un tableau ou rechercher une information. 

Datetime : 
- datetime pour avoir une temporalité des actions, ajout de livre etc
- timedelta pour gérer un interval de temps (fonctionnalité pas encore developpe), utile pour gérer les retard de rendu de livre

Matplotlib : 
- Matplotlib, permet de générer des graph, des stats à partir des données d'une base 
- FigureCanvasTkAgg qui sert à implémenter des graph sur Tkinter 

CSV : 
- Pour l'export du fichier de stat, le format csv doit être appelé en tant que bibliothèque
##############################################################

##############################################################
ORGANISATION DU CODE : 
##############################################################
Sens des appel : 
main.py --> login.py --> app.py



Organisation du main : 
#######################
1/ Initialisation d'une fenetre principale
2/ Style avec titre, background 
3/ Un bouton qui appel le fichier login.py 



Organisation de login : 
#######################
1/ Initialisation d'une fenetre graphique
2/ 2 entrées pour un mot de passe et un nom d'utilisateur 
3/ Création d'une base utilisateur pour y stocker les login
4/ Création de la fonctions pour récupérer les champs d'entrée 
5/ Création des fonctions d'authentification, comparé logins avec la bases, une fonction en appel une autre qui compare la base aux champs
6/ Création du style de la page, mise en place des entrées, des labels et des boutons



Organisation de app : 
#######################
1/ Développement du style classique de la page de l'app (ex : switch de frame avec les titres de pages souligné)
2/ Création des bases de données utilisées, une table books et une tables emprunt (les deux dans la meme base sqlite)
3/ Chaque page est associé à une fonction du menu_frame, au clic (command = lambda:)
4/ Développement de chaque fonction/page (Gestion livres, Gestion user, Pret et retour, Stats et Rapport)


##############################################################
ORGANISATION DU PAGES  : 
##############################################################

Gestion des livres : 
1/ Mise en place de 4 champs d'entrée : Numéro, Titre, Auteur, Thème
2/ Mise en place de la récupération en base de ces champs
3/ Création des boutons qui intéragissent avec ces données
4/ Implémentation du clic sur les données et de l'action (clic sur la ligne + bouton delete, add ou edit)
5/ Ajouter --> fait un insert de l'information récupérée
6/ Modifier --> Update, ouvre un formulaire, qui appel une fonction apply_edit (fonction qui modifie la base)
7/ Supprimer --> Delete de la base
8/ Fonction qui update à chaque action le tableau sur l'interface. 


Gestion des users : 
1/ Création du tableau qui affiche tous les utilisateurs de la base 
2/ Création des fonctions de suppressions, et de modifications (admin ou user)
3/ Supplément de style pour les boutons avec les states, disable ou normal (si on séléctionne un item, le states passe au normal sinon il est disable)
4/ Utilisation des treeview pour l'edition des cellule (rollback sur la gestion des livres pour mettre aussi la fonctionnalité)


Gestion des pret et des retour : 
1/ Plusieurs éléments à développer 
    --> Deux tableau, un sur les emprunt et un sur les retour 
    --> Un champ de recherche + bouton de recherche 
    --> Deux boutons à action rendre et emprunter
    --> Un label d'aide pour l'utilisation de cette page 

2/ Fonctionalité de recherche (une fonction qui recherche et une qui met dans le tableau, la deuxième appelle la premiere)
3/ Mise en place des deux Treeview 
4/ Création de la fonctionnalité d'emprunt, passe le status du livre (par défaut à Disponible) à Indisponible
5/ Ajout des livres emprunté dans le tableau des retour
6/ Ajout de la fonctionnalité Rendre, qui change le status dans le sens inverse. 
7/ Ajustement du style en fonction du nombre d'élément. 


Rapport et Statistiques :
1/ Découverte de Matplotlib avec tkinter
2/ Deux boutons, un pour le graph, un pour le csv 
    --> Graph : 
        Une fonction A qui récupère les échange de livre sur 5 jours 
        Une fonction B qui récupère ces variables et les génère sous forme de graph (graph à barre sur chaque jours)

    --> CSV : 
        Recupère les variables de la fonction A et les écris jours par jours (ligne par ligne) dans un csv




##############################################################
PROBLEME RENCONTRE 
##############################################################
Debug compliqué avec tkinter, print dans la console
Changement de frame, fenetre toplevel (au début après ez)
Utilisation des bases de données, user et book en conflit (pour rien...)
Utilisation des class, tkinter et class j'était super lent donc j'ai speed en normal, programme bcp plus lourd et moins rapide. 
Découverte des fonction prédéfinie et des class tkinter : display grid pour du responsive. 
Class ttk qui empeche la personnalisation classique (font, bg, fg, activeforeground etc)


##############################################################
POINT D'AMELIORATION
##############################################################
- systeme d'authentification user - admin 
- système d'emprunt pour implémenter un système de retard
    -->plusieurs echelle de rendu (1 sem, 2sem ou 3) et faire une opération datetime timedelta pour calculer l'interval de rendu
- sécurité, hashage des mdp et login, grâce à la bibliothèque bcrypt
- optimisation bdd, regrouper les tables en une base plus conséquente
- migration de l'architecture du code actuel vers du code en class pour gagner en mémoire. 
