import tkinter as tk
import requests
import json
from generator import GeneratorWindow

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Connexion")
        self.geometry("400x200")

        # Champ pour l'email
        email_label = tk.Label(self, text="Email:")
        email_label.pack()
        self.email_entry = tk.Entry(self)
        self.email_entry.pack()

        # Champ pour le mot de passe
        password_label = tk.Label(self, text="Mot de passe:")
        password_label.pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        # Bouton de connexion
        login_button = tk.Button(self, text="Connexion", command=self.login)
        login_button.pack()

        # Étiquette pour afficher les messages d'erreur
        self.error_label = tk.Label(self, fg="red")
        self.error_label.pack()

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        url = "http://127.0.0.1:8000/api/login_check"
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        payload = {"email": email, "password": password}
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        if response.status_code == 200:
            # Authentification réussie, passer à la fenêtre de génération d'article
            token = response.json().get('token')
            self.destroy()
            self.generator_window = GeneratorWindow(token)
        else:
            # Authentification échouée, afficher un message d'erreur
            self.error_label.config(text="Identifiants incorrects")
