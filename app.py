import tkinter as tk
import sqlite3
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv

windows = tk.Tk()
windows.geometry("545x700")
windows.title("My E-Bibliothèque")

##############################################################################
#fonction de style, ligne inférieur
##############################################################################
def switch_content(line, page):                                                      #fonction qui permet de switch entre les frame, et d'afficher la ligne inférieur sous chaque catégorie
    for next in menu_frame.winfo_children():
        if isinstance(next, tk.Label):
            next['bg'] = 'SystemButtonFace'                                          #SystemButtonFace, met une couleur automatiquement adaptée au background, fonctionnalité tkinter par défaut (donc c'est invisible)           
        else:
            pass

    line["bg"] = '#138D75'

    for frame in main_frame.winfo_children():
        frame.destroy()
        windows.update()

    page()

##############################################################################
#OPERATION SUR LA BASE 
##############################################################################
def create_books_database():
    conn = sqlite3.connect('books_database.db')
    c = conn.cursor()

    # Création de la table books dans la nouvelle base de données
    c.execute('''
        CREATE TABLE IF NOT EXISTS books (
            book_number INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            theme TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def add_book(book_number, title, author, theme):
    conn = sqlite3.connect('books_database.db')  # Mettez le nom de votre base de données
    c = conn.cursor()
    c.execute("INSERT INTO books (title, author, theme, status) VALUES (?, ?, ?, ?)", (title, author, theme, 'Disponible'))
    conn.commit()
    conn.close()


def create_emprunt_table():
    conn = sqlite3.connect('books_database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS Emprunt (
            id_emprunt INTEGER PRIMARY KEY AUTOINCREMENT,
            id_utilisateur INTEGER,
            id_livre INTEGER,
            date_emprunt DATE,
            FOREIGN KEY (id_utilisateur) REFERENCES users(id),
            FOREIGN KEY (id_livre) REFERENCES books(book_number)
        )
    ''')
    conn.commit()
    conn.close()

# Assurez-vous d'appeler cette fonction pour créer la table
create_emprunt_table()


##############################################################################
#premiere frame pour les boutons, personnalisation de la frame et des boutons
##############################################################################
def app():                                                                                              #visuel de l'application entière, les onglets, les titres par onglets, chaque fonction est développé ensuite pour remplir la page 
    global main_frame, menu_frame  # Declare menu_frame as a global variable 
    menu_frame = tk.Frame(windows)

    manage_book = tk.Button(menu_frame, text="Gestion des livres", font=('Montserrat',13), bd=0, fg="#138D75", activeforeground="#138D75", command=lambda: switch_content(line=manage_book_L, page=manage_book_content))  #commande lambda pour effectuer les actions au clic (ligne inferieur et fonction managebook)
    manage_book.place(x=0,y=0,width=150)
    manage_book_L = tk.Label(menu_frame, background="#138D75")
    manage_book_L.place(x=30,y=30,width=90,height=3)

    manage_user = tk.Button(menu_frame, text="Utilisateur", font=('Montserrat',13), bd=0, fg="#138D75", activeforeground="#138D75", command=lambda: switch_content(line=manage_user_L, page=manage_user_content))
    manage_user.place(x=140,y=0,width=110)
    manage_user_L = tk.Label(menu_frame)
    manage_user_L.place(x=165,y=30,width=60,height=3)

    book_status = tk.Button(menu_frame, text="Prêt et retour", font=('Montserrat',13), bd=0, fg="#138D75", activeforeground="#138D75", command=lambda: switch_content(line=book_status_L,page=manage_status_content))
    book_status.place(x=250,y=0,width=110)
    book_status_L = tk.Label(menu_frame)
    book_status_L.place(x=272,y=30,width=70,height=3)

    stats_and_report = tk.Button(menu_frame, text="Rapport et statistiques", font=('Montserrat',13), bd=0, fg="#138D75", activeforeground="#138D75", command=lambda: switch_content(line=stats_and_report_L, page=manage_stats_content))
    stats_and_report.place(x=360,y=0,width=190)
    stats_and_report_L = tk.Label(menu_frame)
    stats_and_report_L.place(x=397,y=30,width=120,height=3)

    menu_frame.pack(pady=5)
    menu_frame.pack_propagate(False)                      #permet ne pas s'aggrandir en fonction du contenu de la page 
    menu_frame.config(width=700, height=35)

    main_frame = tk.Frame(windows)
    main_frame.pack(fill=tk.BOTH, expand=True)
    manage_book_content()

##############################################################################
#FONCTIONs GESTION DES LIVRES ----> MANAGE_BOOK_CONTENT
##############################################################################
def manage_book_content():
    def add_book_to_database():                                                #fonction d'ajout de livre à la base 
        try:
            book_number = int(entry_book_number.get())
            title = entry_title.get()
            author = entry_author.get()
            theme = entry_theme.get()

            add_book(book_number, title, author, theme)
            messagebox.showinfo("Succès", "Livre ajouté avec succès!")
            update_book_table()  
        except ValueError:                                                     #condition non remplie, on envoie une pop up d'erreur, messagebox de tkinter
            messagebox.showerror("Erreur", "Veuillez entrer un numéro de livre valide.")

    def update_book_table():
        for row in book_tree.get_children():
            book_tree.delete(row)

        conn = sqlite3.connect('books_database.db')                            #à réutiliser dans la page emprunt pour la liste déroulante 
        c = conn.cursor()
        c.execute("SELECT * FROM books")                                       #recup toute les lignes de la table books (titre, auteur, numero, theme)
        books = c.fetchall()                                                   #books prend en argument la dernière requete du curseur, donc toute les lignes sur tableau. 
        conn.close()

        for book in books:                                                     #boucle qui insert dans la treeview, les lignes de la table books
            book_tree.insert('', 'end', values=book)

    def edit_book(selected_item):                                                           #fonction d'édition du tableau
        if selected_item:
            book_info = book_tree.item(selected_item)['values']
            book_number, title, author, theme = book_info[:4]

            edit_window = tk.Toplevel(windows)
            edit_window.title("Modifier le livre")
            edit_window.geometry("300x200")

            entry_new_title = tk.Entry(edit_window, width=30, font=('Montserrat', 12))
            entry_new_title.insert(0, title)
            entry_new_title.pack(pady=10)

            entry_new_author = tk.Entry(edit_window, width=30, font=('Montserrat', 12))
            entry_new_author.insert(0, author)
            entry_new_author.pack(pady=10)

            entry_new_theme = tk.Entry(edit_window, width=30, font=('Montserrat', 12))
            entry_new_theme.insert(0, theme)
            entry_new_theme.pack(pady=10)

            def apply_edit():                                                                                 #fonction qui apply les edition, prend en argument les éléments rentré dans les champs de la fenetre toplvl
                new_title = entry_new_title.get()
                new_author = entry_new_author.get()
                new_theme = entry_new_theme.get()

                conn = sqlite3.connect('books_database.db')
                c = conn.cursor()
                c.execute("UPDATE books SET title=?, author=?, theme=? WHERE book_number=?", (new_title, new_author, new_theme, book_number))   #les insert dans la table books
                conn.commit()
                conn.close()

                update_book_table()                                                                                                             #update du tableau pour avoir les dernières modifications

                edit_window.destroy()                                                                                                           #ferme la fenetre toplvl de modification

            apply_button = tk.Button(edit_window, text="Appliquer", font=('Montserrat', 12), fg="#138D75", command=apply_edit)                  #bouton qui execute la fonction apply
            apply_button.pack(pady=10)

    def delete_book(selected_item):                                                                                                             #fonction qui delete une ligne du tableau, la requete est directement dans la fonciton
        if selected_item:                                                                                                                       
            confirmation = messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer ce livre?")                                      #messagebox de confirmation, evite les suppression trop rapide
            if confirmation:
                book_number = book_tree.item(selected_item)['values'][0]

                conn = sqlite3.connect('books_database.db')
                c = conn.cursor()
                c.execute("DELETE FROM books WHERE book_number=?", (book_number,))                                                              #supprime le livre de la base 
                conn.commit()
                conn.close()

                book_tree.delete(selected_item)

    def on_book_tree_select(event):
        selected_item = book_tree.selection()
        if selected_item:
            edit_button.config(state=tk.NORMAL)
            delete_button.config(state=tk.NORMAL)
        else:
            edit_button.config(state=tk.DISABLED)
            delete_button.config(state=tk.DISABLED)

    frame_book = tk.Frame(main_frame)                                                                                                           #Personnalisation de la page gestion des livres 
    frame_book_lb = tk.Label(frame_book, text='Gestion des livres', font=('Montserrat', 25), fg="#138D75")
    frame_book_lb.pack(pady=20)

    entry_book_number = tk.Entry(frame_book, width=30, font=('Montserrat', 12))                                                                 #Exemple d'entrée pour le numéro du livre 
    entry_book_number.insert(0, "Numéro de livre")
    entry_book_number.pack(pady=10)

    entry_title = tk.Entry(frame_book, width=30, font=('Montserrat', 12))
    entry_title.insert(0, "Titre")
    entry_title.pack(pady=10)

    entry_author = tk.Entry(frame_book, width=30, font=('Montserrat', 12))
    entry_author.insert(0, "Auteur")
    entry_author.pack(pady=10)

    entry_theme = tk.Entry(frame_book, width=30, font=('Montserrat', 12))
    entry_theme.insert(0, "Thème")
    entry_theme.pack(pady=10)

    add_book_button = tk.Button(frame_book, text="Ajouter Livre", font=('Montserrat', 12), fg="#138D75",                                        #Exemple de bouton lié aux fonctions ci-dessus, ici on ajoute un livre 
                                command=add_book_to_database)
    add_book_button.pack(pady=10)

    edit_button = tk.Button(frame_book, text="Modifier le livre", font=('Montserrat', 12), fg="#138D75",
                            command=lambda: edit_book(book_tree.selection()))
    edit_button.pack(pady=10)
    edit_button.config(state=tk.DISABLED)

    delete_button = tk.Button(frame_book, text="Supprimer le livre", font=('Montserrat', 12), fg="#138D75",
                              activeforeground="#FF5733", command=lambda: delete_book(book_tree.selection()))
    delete_button.pack(pady=10)
    delete_button.config(state=tk.DISABLED)

    book_tree = ttk.Treeview(frame_book, columns=("Numéro", "Titre", "Auteur", "Thème"),                                                        #Affichage dans la treeview avec les colonnes correspondant à la base 
                             show="headings", height=10)
    book_tree.heading("Numéro", text="Numéro")
    book_tree.heading("Titre", text="Titre")
    book_tree.heading("Auteur", text="Auteur")
    book_tree.heading("Thème", text="Thème")
    book_tree.pack(pady=10)

    book_tree.column('Numéro', width=130)
    book_tree.column('Titre', width=130)
    book_tree.column('Auteur', width=130)
    book_tree.column('Thème', width=130)



    book_tree.bind("<ButtonRelease-1>", on_book_tree_select)                                                                                    #Designe l'action au clic (clic gauche pour -1)

    frame_book.pack(fill=tk.BOTH, expand=True)
    update_book_table()


##############################################################################
#FONCTIONs GESTION DES USERS ----> MANAGE_USER_CONTENT
##############################################################################

def manage_user_content():
    def delete_user():                                                                                                                          #Exemple de fonction sur la table user, ici on supprime un user
        selected_item = user_tree.selection()
        if selected_item:
            user_id = user_tree.item(selected_item)['values'][0]
            conn = sqlite3.connect('user_database.db')
            c = conn.cursor()
            c.execute("DELETE FROM users WHERE username=?", (user_id,))
            conn.commit()
            conn.close()
            user_tree.delete(selected_item)
        else:
            messagebox.showwarning("Problème de sélection", "Veuillez sélectionner un utilisateur à supprimer.")                                 #Cas de la non sélection d'un utilisateur à supprimer 

    def edit_user(selected_item):
        if selected_item:
            user_info = user_tree.item(selected_item)['values']
            user_id, username, password, role = user_info[:4]

            edit_window = tk.Toplevel(windows)
            edit_window.title("Modifier l'utilisateur")
            help_message = tk.Label(edit_window, text="Le changement de rôle ne peut être que 'user' ou 'admin'",font=('Montserrat',10), fg="#138D75")
            help_message.place(x=0,y=200)
            edit_window.geometry("330x300")

            entry_new_username = tk.Entry(edit_window, width=30, font=('Montserrat', 12))
            entry_new_username.insert(0, username)
            entry_new_username.pack(pady=10)

            entry_new_password = tk.Entry(edit_window, width=30, font=('Montserrat', 12), show="*")
            entry_new_password.insert(0, password)
            entry_new_password.pack(pady=10)

            entry_new_role = tk.Entry(edit_window, width=30, font=('Montserrat', 12))
            entry_new_role.insert(0, role)
            entry_new_role.pack(pady=10)

            def apply_edit():
                new_username = entry_new_username.get()
                new_password = entry_new_password.get()
                new_role = entry_new_role.get()

                conn = sqlite3.connect('user_database.db')
                c = conn.cursor()
                c.execute("UPDATE users SET username=?, password=?, role=? WHERE id=?", (new_username, new_password, new_role, user_id))
                conn.commit()
                conn.close()

                update_user_table()

                edit_window.destroy()

            apply_button = tk.Button(edit_window, text="Appliquer", font=('Montserrat', 12), fg="#138D75", command=apply_edit)
            apply_button.pack(pady=10)

    def update_user_table():                
        for row in user_tree.get_children():
            user_tree.delete(row)

        conn = sqlite3.connect('user_database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        users = c.fetchall()
        conn.close()

        for user in users:
            user_tree.insert('', 'end', values=user)

    def on_user_tree_select(event):                                                                                                                         #States du bouton, niveau style, le bouton est vert quand on clic sur un user, et desactiver quand on clic pas 
        selected_item = user_tree.selection()
        if selected_item:
            delete_button.config(state=tk.NORMAL)                                                                                                           #States normal (vert) s'il y a un élement selectionner
            edit_button.config(state=tk.NORMAL)
        else:
            delete_button.config(state=tk.DISABLED)                                                                                                         #States disable, desactiver donc gris, si aucun user est sélectionner
            edit_button.config(state=tk.DISABLED)

    frame_user = tk.Frame(main_frame)
    frame_user_lb = tk.Label(frame_user, text='Gestion des utilisateurs', font=('Montserrat', 25), fg="#138D75")
    frame_user_lb.pack(pady=20)
    frame_user.pack(fill=tk.BOTH, expand=True)

    user_tree = ttk.Treeview(frame_user, columns=("ID", "Nom d'utilisateur", "Mot de Passe", "Role"), show="headings",
                             height=10)
    user_tree.heading("ID", text="ID")
    user_tree.heading("Nom d'utilisateur", text="Nom d'utilisateur")
    user_tree.heading("Mot de Passe", text="Mot de Passe")
    user_tree.heading("Role", text="Role")
    user_tree.pack(pady=10)

    user_tree.column('ID', width=100)
    user_tree.column('Nom d\'utilisateur', width=150)
    user_tree.column('Mot de Passe', width=100)
    user_tree.column('Role', width=150)

    user_tree.bind("<ButtonRelease-1>", on_user_tree_select)

    delete_button = tk.Button(frame_user, text="Supprimer l'utilisateur", font=('Montserrat', 12), fg="#138D75",
                              activeforeground="#FF5733", command=delete_user)
    delete_button.pack(pady=10)
    delete_button.config(state=tk.DISABLED)

    edit_button = tk.Button(frame_user, text="Modifier l'utilisateur" , font=('Montserrat', 12), fg="#138D75",
                            command=lambda: edit_user(user_tree.selection()))
    edit_button.pack(pady=10)
    edit_button.config(state=tk.DISABLED)

    frame_user.pack(fill=tk.BOTH, expand=True)
    update_user_table()



##############################################################################
#FONCTIONs GESTION DES PRET ET RETOUR ----> MANAGE_STATUS_CONTENT
##############################################################################

def manage_status_content():
    global main_frame
    def update_book_table(books):
        for row in book_tree.get_children():
            book_tree.delete(row)

        for book in books:
            book_tree.insert('', 'end', values=book)

    def on_search():                                                                                                                            #permet de rechercher un livre dans la base 
        search_query = search_entry.get()
        books = get_book_from_db(search_query)                                                                                                  #appel donc une fonction qui peut sortir un livre de la bdd

        if books:
            update_book_table(books)
            status_label.config(text="")
        else:
            update_book_table([])                                                                                                               #cas ou le livre n'existe pas en base
            status_label.config(text="Aucun livre trouvé.")

    def on_emprunter():                                                                                                                         #fonction d'emprunt d'un livre
        selected_book = book_tree.selection()

        if selected_book:
            book_info = book_tree.item(selected_book)['values']
            book_id, title, author, theme, status = book_info

            if status == 'Disponible':                                                                                                          #ne peut etre emprunté que s'il est disponible 
                user_id = get_user_id(current_user)                                                                                             #récupère la variable globale user_id qui designe l'utilisateur actuel
                date_emprunt = datetime.today().strftime('%Y-%m-%d')                                                                            #récupère grace à datetime la date d'aujourd'hui, qui est la date d'emprunt

                conn = sqlite3.connect('books_database.db')
                c = conn.cursor()
                c.execute("UPDATE books SET status = 'Indisponible' WHERE book_number = ?", (book_id,))                                         #change le status du livre en base à indisponible 
                c.execute("INSERT INTO Emprunt (id_utilisateur, id_livre, date_emprunt) VALUES (?, ?, ?)", (user_id, book_id, date_emprunt))    #insert dans la table emprunt, l'id user, l'id du livre, et la date de l'emprunt
                conn.commit()
                conn.close()
                update_book_table(get_book_from_db())
                update_emprunt_table()
                status_label.config(text="Livre emprunté avec succès.", fg="green")                                                             #résultat de la manipulation
            else:
                status_label.config(text="Le livre n'est pas disponible.", fg="red")
        else:
            status_label.config(text="Veuillez sélectionner un livre.", fg="red")

    
    def on_rendre():                                                                                                                            #fonction de rendu du livre 
        selected_emprunt = emprunt_tree.selection()                                                                                             #la selection par le clic 

        if selected_emprunt:
            emprunt_info = emprunt_tree.item(selected_emprunt)['values']
            emprunt_id, user_id, book_id, date_emprunt = emprunt_info

            conn_books = sqlite3.connect('books_database.db')                               
            c_books = conn_books.cursor()
            c_books.execute("UPDATE books SET status = 'Disponible' WHERE book_number = ?", (book_id,))                                         #fait la manipulation inverse, change le status du livre de indisponible --> disponible
            conn_books.commit()
            conn_books.close()

            conn_emprunt = sqlite3.connect('books_database.db')
            c_emprunt = conn_emprunt.cursor()
            c_emprunt.execute("DELETE FROM Emprunt WHERE id_emprunt = ?", (emprunt_id,))                                                        #on delete de la table emprunt car le livre n'est plus emprunte (pourrai etre save pour les statistiques)
            conn_emprunt.commit()
            conn_emprunt.close()

            update_emprunt_table()
            update_book_table(get_book_from_db())
            status_label.config(text="Livre rendu avec succès.", fg="green")                                                                    #résultats de la manipulation 
        else:
            status_label.config(text="Veuillez sélectionner un emprunt à rendre.", fg="red")


    def get_user_id(username):
        conn = sqlite3.connect('user_database.db')
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username=?", (username,))
        result = c.fetchone()
        conn.close()

        if result:
            user_id = result[0]
            return user_id
        else:
            return None

    def get_book_from_db(search_query=None):                                                                                                        #fonction de recherche dans la base de donnée, search query est le l'entrée de la search entry,
        conn = sqlite3.connect('books_database.db')
        c = conn.cursor()

        if search_query:
            c.execute("SELECT * FROM books WHERE title LIKE ? AND status='Disponible'", ('%' + search_query + '%',))                                #selectionne tous les livres disponible, et renvoie celui qui se rapproche du titre recherché en search entry
        else:
            c.execute("SELECT * FROM books WHERE status='Disponible'")                      

        books = c.fetchall()
        conn.close()
        return books

    def update_emprunt_table():                                                                                                                     #permet de mettre à jour la table d'emprunt en permanence (on appel la fonction un peu partout)
        for row in emprunt_tree.get_children():
            emprunt_tree.delete(row)
        conn_books = sqlite3.connect('books_database.db')
        c_books = conn_books.cursor()
        c_books.execute("SELECT Emprunt.id_emprunt, Emprunt.id_utilisateur, Emprunt.id_livre, Emprunt.date_emprunt, books.title FROM Emprunt JOIN books ON Emprunt.id_livre = books.book_number")               #jointure entre book et emprunt pour avoir le titre du livre
        emprunts = c_books.fetchall()                                                                                                               #récupère les éléments de la dernières requete
        conn_books.close()
        for emprunt in emprunts:
            emprunt_tree.insert('', 'end', values=(emprunt[0], emprunt[1], emprunt[4], emprunt[3]))                                                 #insert les éléments récupéré de la dernière requete dans le tableau (id, user qui emprunte, livre emprunté, date)
                    
    current_user = "username" 

    frame_status_title = tk.Label(main_frame, text='Prêt et retour de livres', font=('Montserrat', 25), fg="#138D75")                               #style de la page pret et retour 
    frame_status_title.pack(pady=20)

    frame_status = tk.Frame(main_frame)
    frame_status.pack(fill=tk.BOTH, expand=True)


    search_entry = tk.Entry(frame_status, font=('Montserrat', 12), width=30)
    search_entry.insert(0,'Titre du livre')
    search_entry.grid(row=0, column=0, padx=10, pady=10)


    search_button = tk.Button(frame_status, text="Rechercher", font=('Montserrat', 12),fg="#138D75", command=on_search)                             #bouton qui effectuent les actions (ici rechercher un livre)
    search_button.grid(row=0, column=1, pady=10)


    emprunter_button = tk.Button(frame_status, text="Emprunter", font=('Montserrat', 12), fg="#138D75", command=on_emprunter)
    emprunter_button.grid(row=2, column=0, pady=30, columnspan=2)

    rendre_button = tk.Button(frame_status, text="Rendre", font=('Montserrat', 12),fg="#138D75", command=on_rendre)
    rendre_button.grid(row=2, column=1, pady=10, columnspan=2)

    status_label = tk.Label(frame_status, text="Cliquer sur un livre ci-dessous pour le rendre", font=('Montserrat', 12), fg="#FF5733")
    status_label.grid(row=3, column=0, pady=20, columnspan=2)

 
    book_tree = ttk.Treeview(frame_status, columns=("ID", "Titre", "Auteur", "Thème", "Status"), show="headings", height=5)                         #affichage dans le tableau des livres pouvant etre emprunté 
    book_tree.heading("ID", text="ID")
    book_tree.heading("Titre", text="Titre")
    book_tree.heading("Auteur", text="Auteur")
    book_tree.heading("Thème", text="Thème")
    book_tree.heading("Status", text="Status")
    book_tree.grid(row=1, column=0, pady=10, padx=20, columnspan=2)

    book_tree.column('ID', width=50)
    book_tree.column('Titre', width=110)
    book_tree.column('Auteur', width=110)
    book_tree.column('Thème', width=110)
    book_tree.column('Status', width=110)


    emprunt_tree = ttk.Treeview(frame_status, columns=("ID", "Utilisateur de l'emprunt", "Livre emprunté", "Date de l'emprunt"), show="headings", height=5)            #affichage des livres empruntés
    emprunt_tree.heading("ID", text="ID")
    emprunt_tree.heading("Utilisateur de l'emprunt", text="Utilisateur de l'emprunt")
    emprunt_tree.heading("Livre emprunté", text="Livre emprunté")
    emprunt_tree.heading("Date de l'emprunt", text="Date de l'emprunt")
    emprunt_tree.grid(row=4, column=0, pady=10, padx=20, columnspan=2)

    emprunt_tree.column('ID', width=50)
    emprunt_tree.column('Utilisateur de l\'emprunt', width=120)
    emprunt_tree.column('Livre emprunté', width=120)
    emprunt_tree.column('Date de l\'emprunt', width=120)
    update_emprunt_table()
    book_tree.column

##############################################################################
#FONCTIONS RAPPORT ET STATISTIQUES ----> MANAGE_STATS_CONTENT
##############################################################################

def manage_stats_content():
    global status_label
    def generate_csv():                                                                                         #fonction qui export un csv 

        end_date = datetime.today()
        start_date = end_date - timedelta(days=4) 

        emprunts_par_jour = get_emprunts_par_jour(start_date, end_date)


        conn = sqlite3.connect('books_database.db')
        c = conn.cursor()

        with open('livres_empruntes_par_jour.csv', 'w', newline='', encoding='utf-8') as csvfile:               #ouvre un fichier csv ou le crée
            csv_writer = csv.writer(csvfile)                                                                    #initialisation d'un writer
            csv_writer.writerow(['Date', 'Nombre de livres empruntés', 'Titres des livres empruntés'])          #defintion des colonnes 

            for i in range(5):                                                                                  #boucle pour des stats sur les 5 jours
                current_date = start_date + timedelta(days=i)
                next_date = start_date + timedelta(days=i + 1)
                c.execute("SELECT COUNT(*), GROUP_CONCAT(books.title) FROM Emprunt JOIN books ON Emprunt.id_livre = books.book_number WHERE date_emprunt >= ? AND date_emprunt < ? GROUP BY date_emprunt", (current_date, next_date))    #titre du livre, nombre d'emprunt, jour
                result = c.fetchone()

                if result:
                    num_emprunts, titres_livres = result
                else:
                    num_emprunts, titres_livres = 0, ""

                csv_writer.writerow([current_date.strftime('%Y-%m-%d'), num_emprunts, titres_livres])           #ecriture dans le csv des informations sur les emprunts dans les 5 jours passé

        conn.close()
        status_label.config(text="Fichier CSV généré avec succès.", fg="green")

    def generate_stats():                                                                                       #fonction de génération de stats

        end_date = datetime.today()                                                                             #dernière date du graph, aujourd'hui
        start_date = end_date - timedelta(days=4)                                                               #sur les 5 derniers jours 
        dates = [start_date + timedelta(days=x) for x in range(5)]

        emprunts_par_jour = get_emprunts_par_jour(start_date, end_date)


        fig, ax = plt.subplots()
        ax.bar(dates, emprunts_par_jour, color='green')                                                         #création du graphique à barre
        ax.set_xlabel('Date')                                                                                   #axe x avec les dates   
        ax.set_ylabel('Nombre de livres empruntés')                                                             #axe y avec le nombre de livre emprunté
        ax.set_title('Nombre de livres empruntés par jour (5 derniers jours)')                                  #titre du graph


        canvas = FigureCanvasTkAgg(fig, master=frame_stats)                                                     #crée une toile tkinter
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

    def get_emprunts_par_jour(start_date, end_date):                                                            #fonction pour avoir le nombre d'emprunt par jour 
        conn = sqlite3.connect('books_database.db')
        c = conn.cursor()

        emprunts_par_jour = []
        for i in range(5):                                                                                      
            current_date = start_date + timedelta(days=i)                                                       #opération avec une paire de date 
            next_date = start_date + timedelta(days=i + 1)                                                      
            c.execute("SELECT COUNT(*) FROM Emprunt WHERE date_emprunt >= ? AND date_emprunt < ?", (current_date, next_date))      #récupère le nombre de livre emprunté à current date et exclu ceux de next date, itere jusqu'a arriver 5 jours
            emprunts_par_jour.append(c.fetchone()[0])

        conn.close()
        return emprunts_par_jour
    
    
    frame_stats = tk.Frame(main_frame)
    frame_stats_lb = tk.Label(frame_stats, text='Rapport et statistiques', font=('Montserrat', 25), fg="#138D75")
    frame_stats_lb.pack(pady=20)
    generate_button = tk.Button(frame_stats, text="Générer les statistiques", font=('Montserrat', 12), fg="#138D75", command=generate_stats)
    generate_button.pack(pady=10)
    generate_csv_button = tk.Button(frame_stats, text="Générer CSV", font=('Montserrat', 12), fg="#138D75", command=generate_csv)
    generate_csv_button.pack(pady=10)
    frame_stats.pack(fill=tk.BOTH, expand=True)
    status_label = tk.Label(frame_stats, text="", font=('Montserrat', 12), fg="#138D75")
    status_label.pack(pady=20)

create_books_database()
app()

windows.mainloop() 
