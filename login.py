import sqlite3
import tkinter as tk
from tkinter import ttk
import subprocess

import sqlite3

def create_books_table():                                                                                         
    conn = sqlite3.connect('books_database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_number INTEGER,
            title TEXT,
            author TEXT,
            theme TEXT
        )
    ''')
    conn.commit()
    conn.close()

def create_users_table():
    conn = sqlite3.connect('user_database.db') 
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            role TEXT
        )
    ''')
    conn.commit()
    conn.close()

def register_user(username, password, role):                                                                         #fonction d'enregistrement en base de notre profil 
    conn = sqlite3.connect('user_database.db')                                                                       #peut utiliser bcrypt pour ne pas stocker le mdp en clair dans la bdd
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))           #requete qui ajoute les login en base dans les colonnes adaptées
    conn.commit()                                                                                                    
    conn.close()                                                                                                     #ferme la connexion à la bdd 

def login_user(username, password):
    conn = sqlite3.connect('user_database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user

def register():
    username = entry_username.get()                                                                                                                 #récupère le nom entré dans les champs                                                                                                                          
    password = entry_password.get()                                                                                                                 #récupère le mdp entré dans les champs  
    role = var_role.get()                                                                                                                           #à développer, que user pr le moment 

    if username and password and role:
        register_user(username, password, role)
        register_result_label.config(text="Inscription réussie en tant qu'utilisateur!", fg="green")
    else:
        register_result_label.config(text="Veuillez remplir tous les champs et sélectionner le rôle d'utilisateur.", fg="red")

def login():                                                       
    global current_user                                                                                                                             #permet d'avoir le nom de l'utilisateur actuel (utilisé dans l'app)
    username = entry_username.get()
    password = entry_password.get()
    user = login_user(username, password)
    if user:
        
        role = user[3]                                                                                                                              #dans la table user, le role est la 3 colonnes 
        if role == "admin":                                                                                                                         #connexion autorisée en user et non en admin
            login_result_label.config(text="Échec de la connexion. Vous devez vous connecter en tant qu'utilisateur.", fg="red")
        else:
            current_user = username
            login_result_label.config(text=f"Connexion réussie! Rôle : {role}", fg="green")
            subprocess.run(["python", "app.py"])                                                                                                    #subprocess permet de lancer l'app si l'authentification est réussie 
            
    else:
        login_result_label.config(text="Échec de la connexion. Nom d'utilisateur ou mot de passe incorrect.", fg="red")

root = tk.Tk()
root.title("Login System")
root.config(bg="#D4EFDF")

# Centrer la fenêtre principale
window_width = 500
window_height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width/2) - (window_width/2)
y_coordinate = (screen_height/2) - (window_height/2)
root.geometry(f"{window_width}x{window_height}+{int(x_coordinate)}+{int(y_coordinate)}")


# Ajouter des espacements pour rendre le centrage plus clair
space_top = ttk.Label(root, text="", background="#D4EFDF")
space_top.pack(pady=20)

label_username = tk.Label(root, text="Nom d'utilisateur:",font=('Montserrat',10), fg="#138D75", activeforeground="#138D75",background="#EAFAF1")          #titre du champs, charte graphique, utilisée dans chaque titre ou bouton
label_username.pack(pady=10)

entry_username = tk.Entry(root)
entry_username.pack(pady=10)

label_password = tk.Label(root, text="Mot de passe",font=('Montserrat',10), fg="#138D75", activeforeground="#138D75",background="#EAFAF1")
label_password.pack(pady=10)

entry_password = ttk.Entry(root, show="*")
entry_password.pack(pady=10)

label_role = tk.Label(root, text="Rôle:",font=('Montserrat',10), fg="#138D75", activeforeground="#138D75",background="#EAFAF1")
label_role.pack(pady=10)

var_role = tk.StringVar()
var_role.set("user")

radio_user = ttk.Radiobutton(root, text="User", variable=var_role, value="user")
radio_user.pack()

label_admin = tk.Label(root, text="Pour avoir un accès administrateur, demandez à remi.cancel@epsi.fr", fg="#138D75")
label_admin.pack(pady=5)

register_button = tk.Button(root, text="S'inscrire", font=('Montserrat',12), fg="#138D75", activeforeground="#138D75", command=register)
register_button.pack(pady=20)

login_button = tk.Button(root, text="Se connecter",  font=('Montserrat',12), fg="#138D75", activeforeground="#138D75", command=login)
login_button.pack(pady=10)

register_result_label = tk.Label(root, text="", bg="#D4EFDF")
register_result_label.pack()

login_result_label = tk.Label(root, text="", bg="#D4EFDF")
login_result_label.pack()

create_books_table()
root.mainloop()
