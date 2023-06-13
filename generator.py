import tkinter as tk
import requests
import codecs
import re
import json

class GeneratorWindow(tk.Tk):
    def __init__(self, token):
        tk.Tk.__init__(self)
        self.title("Générateur d'articles")
        self.token = token

        self.title_label = tk.Label(self, text="Titre de l'article:")
        self.title_label.pack()
        self.title_entry = tk.Entry(self)
        self.title_entry.pack()

        self.content_label = tk.Label(self, text="Contenu de l'article:")
        self.content_label.pack()
        self.content_text = tk.Text(self, height=20, width=90)
        self.content_text.pack()
        self.content_text.configure(wrap=tk.WORD)

        self.loading_label = tk.Label(self, text="")
        self.loading_label.pack()

        self.generate_button = tk.Button(self, text="Générer le contenu", command=self.generate_content)
        self.generate_button.pack()

        self.post_button = tk.Button(self, text="Publier l'article", command=self.post_article)
        self.post_button.pack()

    def disable_widgets(self):
        self.title_entry.config(state="disabled")
        self.content_text.config(state="disabled")
        self.generate_button.config(state="disabled")
        self.post_button.config(state="disabled")

    def enable_widgets(self):
        self.title_entry.config(state="normal")
        self.content_text.config(state="normal")
        self.generate_button.config(state="normal")
        self.post_button.config(state="normal")
        

    def generate_content(self):
        title = self.title_entry.get()
        url = "http://127.0.0.1:8000/api/ai-generate"
        headers = {"Authorization": "Bearer " + self.token, "Content-Type": "application/json"}
        payload = {"title": title}

        self.disable_widgets()
        self.loading_label.config(text="Chargement en cours...")
        self.loading_label.update()

        response = requests.post(url, headers=headers, json=payload)
        

        if response.status_code == 200:
            self.enable_widgets()
            decoded_text = codecs.decode(response.text, 'unicode_escape')
            formatted_text = re.sub(r'\.', '.\n', decoded_text)
            formatted_text = formatted_text.strip('"')
            self.content_text.delete("1.0", tk.END)
            self.content_text.insert(tk.END, formatted_text)
            self.loading_label.config(text="yes ! Le contenue est généré")
        else:
            self.enable_widgets()
            self.content_text.delete("1.0", tk.END)
            self.content_text.insert(tk.END, "Erreur lors de la génération du contenu")

    def post_article(self):
        title = self.title_entry.get()
        content = self.content_text.get("1.0", tk.END)

        url = "http://127.0.0.1:8000/api/articlePost"
        headers = {"Authorization": "Bearer " + self.token, "Content-Type": "application/json"}
        payload = {"title": title, "content": content}


        response = requests.post(url, headers=headers, data=json.dumps(payload))
        

        if response.status_code == 201:
            self.enable_widgets()
            self.loading_label.config(text="yes ! L'article est publié")
        else:
            self.enable_widgets()
            self.content_text.delete("1.0", tk.END)
            self.content_text.insert(tk.END, "Erreur lors de la publication de l'article")

if __name__ == "__main__":
    generator_window = GeneratorWindow()
    generator_window.mainloop()
