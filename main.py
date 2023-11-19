import tkinter as tk 

root = tk.Tk()
root.title("My E-bibliothèque")
# root.geometry("500x500")
root.config(bg="#D4EFDF")


#permet de faire apparaître la page d'accueil au centre au début de l'execution
window_width = 500
window_height = 500
screen_width = root.winfo_screenwidth()                                                            #argument tkinter winfo.screenwidth, screen_width prend en paramètre la largeur en pxl de la page
screen_height = root.winfo_screenheight()                                                          #argument tkinter winfo.screenheight, screen_width prend en paramètre la hauteur en pxl de la page
x_coordinate = (screen_width/2) - (window_width/2)                                                 #trouve le point central sur la ligne horizontal de l'écran 
y_coordinate = (screen_height/2) - (window_height/2)                                               #trouve le point central sur la ligne vertical de l'écran
root.geometry(f"{window_width}x{window_height}+{int(x_coordinate)}+{int(y_coordinate)}")


#fonction d'ouverture du script login 
def open_admin_page():
        import login


#boucle qui configure une grille sur ma page, je place ensuite les éléments en lignes et colonnes (6 est un peu trop)
for i in range(6):
    root.grid_rowconfigure(i, weight=1)                                             
    root.grid_columnconfigure(i, weight=1)


#Message d'accueil sur la page, style classique (placé en responsive sur la grille)
message = tk.Label(root,text="Bienvenue sur My E-bibliothèque", font=('Montserrat',20), fg="#138D75", activeforeground="#138D75",background="#EAFAF1")
message.grid(row=1,column=3)   


while True :                                                                                                                                                                       #pour éviter que le script se termine après le clic

    login_button = tk.Button(root,text="Entrer",font=('Montserrat',14), fg="#138D75", activeforeground="#138D75", command=open_admin_page)                                         #Button qui permet d'accèder à la page login, command --> ma fonction qui ouvre login
    login_button.grid(row=3,column=3)                                                                                                                                              #Placement du bouton en responsive

    exit_button = tk.Button(root,text="Quitter l'application", font=('Montserrat',10), fg="#138D75", activeforeground="#138D75",command=root.destroy)                              #Button qui destroy la page d'accueil (et donc empêche la suite du script)
    exit_button.place(x=370,y=460)                                                                                                                                                 #Placement du bouton en fixe, parce que ça bug sinon (jai essayé)                                                                                                                             
    
    root.mainloop()