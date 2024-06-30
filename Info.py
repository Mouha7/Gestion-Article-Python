import json
import os
from tinydb import TinyDB
from pprint import pprint

class Info:
    def __init__(self, file_path:str="DB/data.txt", file_path_tiny_db:str="DB/tiny_DB.json",file_path_json:str = "DB/DB.json")->None:
        self.file_path = file_path
        self.file_path_json = file_path_json
        self.file_path_tiny_db = file_path_tiny_db
    
    def split_text(self, text:str)->tuple|None:
        if not text[0].isdigit():
            return None, text        
        for i, char in enumerate(text):
            if not char.isdigit():
                break
        return text[:i], text[i:]
    
    def create_articles(self, header:list, data_list:list)->list:
        articles = []
        for i in range(0, len(data_list), len(header)):
            article_data = data_list[i:i+len(header)]
            if len(article_data) == len(header):
                article_dict = {header[j]: article_data[j] for j in range(len(header))}
                articles.append(article_dict)
        return articles
    
    def read_data(self)->dict:
        with open(self.file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        result = ''
        for line in lines[2:]:
            for l in line:
                if l != '\n':
                    result += l
                if l == '\n':
                    result += ''
        data = result.split(';')
        datas = []
        for value in data:
            if len(value) != 0:
                datas.append(value)
        L = []
        for value in datas:
            if 'Article' in value:
                v1, v2 = self.split_text(value)
                if v1 is not None:
                    L.append(v1)
                    L.append(v2)
                else:
                    L.append(v2)
            else:
                L.append(value)
        headers = lines[0].strip().split(';')
        final = self.create_articles(headers, L)
        return {"headers": headers, "data": final}
    
    def add_to_txt_json(self, new_data:list)->None:
        if os.path.exists(self.file_path_json):
            with open(self.file_path_json, 'r', encoding='utf-8') as file:
                data = json.load(file)
            if not isinstance(data, list):
                data = [data]
        else:
            data = []
        existing_articles = {json.dumps(article, sort_keys=True) for article in data}
        if isinstance(new_data, list):
            new_data_list = new_data
        else:
            new_data_list = [new_data]
        for article in new_data_list:
            article_str = json.dumps(article, sort_keys=True)
            if article_str not in existing_articles:
                data.append(article)
                existing_articles.add(article_str)
        with open(self.file_path_json, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        
        print(f"Données ajoutées avec succès au fichier {self.file_path_json}")
    
    def add_to_json_tiny_db(self)->None:
        with open(self.file_path_json, 'r', encoding='utf-8') as json_file:
            articles_data = json.load(json_file)
        db = TinyDB(self.file_path_tiny_db)
        articles_table = db.table('articles')
        articles_table.truncate()
        headers = self.read_data()["headers"]
        for article in articles_data:
            if isinstance(article, dict):
                articles_table.insert(article)
            elif isinstance(article, list):
                article_dict = {}
                for i, value in enumerate(article):
                    if i < len(headers):
                        article_dict[headers[i]] = value
                    else:
                        break
                articles_table.insert(article_dict)
        print(f"Base de données créée avec succès. {len(articles_data)} articles insérés.")
        db.close()
    
    def list_article(self, article:dict)->None:
        print('Article   : ', article.get("Article"))
        print('Catégorie : ', article.get("Categorie"))
        print('Titre     : ', article.get("Titre"))
        print('Auteur    : ', article.get("auteur"))
        print('Tags      : ', article.get("tags"))
        print('Date      : ', article.get("date"))
        print('Etat      : ', article.get("etat"))
        print('Vue       : ', article.get("vue"))
        print('Like      : ', article.get("like"))
        print('Dislike   : ', article.get("dislike"))
        print('Contenu   : ', article.get("Contenu"))
        print('---------------------------------------------------------------------------')
    
    def list_articles(self)->None:
        db = TinyDB(self.file_path_tiny_db)
        articles_table = db.table('articles').all()
        print(f"Listes des Articles({len(articles_table)})")
        for article in articles_table:
            self.list_article(article)
    
    def add_tags(self)->str:
        tag = ''
        while(True):
            tag += input("Entrez un tag               : ")
            response = input("Voulez-vous ajouter un autre tag(O/N)? ")
            if response == 'o' or response == 'O':
                tag += ', '
            elif response == 'n' or response == 'N':
                break
            else:
                print("Erreur de saisie.")
        return tag
    
    def add_article(self)->dict:
        print("-----------Add-Article-----------")
        nom = input("Entrez le nom               : ")
        categorie = input("Entrez la catégorie         : ")
        titre = input("Entrez le titre             : ")
        auteur = input("Entrez l'auteur             : ")
        tags = self.add_tags()
        date = input("Entrez la date              : ")
        etat = input("Entrez l'état               : ")
        vue = input("Entrez le nombre de vue     : ")
        like = input("Entrez le nombre de like    : ")
        dislike = input("Entrez le nombre de dislike : ")
        contenu = input("Entrez le contenu           : ")
        return {
            "Article": nom,
            "Categorie": categorie,
            "Titre": titre,
            "Contenu": contenu,
            "tags": tags,
            "auteur": auteur,
            "date": date,
            "etat": etat,
            "vue": vue,
            "like": like,
            "dislike": dislike
        }

    def read_json(self)->None|dict:
        try:
            with open(self.file_path_json, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print(f"Le fichier {self.file_path_json} n'a pas été trouvé.")
            return None

    def add_article_tiny_db(self, new_article:list)->None:
        db = TinyDB(self.file_path_tiny_db)
        articles_table = db.table('articles')
        articles_table.insert(new_article)
        db.close()
        print("Article ajouté avec succès à la base de données TinyDB.")
    
    def highest_rated(self)->tuple:
        data = self.read_json()
        if(data is not None):
            max_vue = max_like = max_dislike = pos_vue = pos_like = pos_dislike = 0
            for pos_field, field in enumerate(data):
                vue = int(field.get('vue'))
                like = int(field.get('like'))
                dislike = int(field.get('dislike'))
                if max_vue < vue:
                    pos_vue = pos_field
                    max_vue = vue
                if max_like < like:
                    pos_like = pos_field
                    max_like = vue
                if max_dislike < dislike:
                    pos_dislike = pos_field
                    max_dislike = dislike
        return data[pos_vue], data[pos_like], data[pos_dislike]
    
    def list_most_rated(self)->None:
        vue, like, dislike = self.highest_rated()
        print(f"L'article avec plus de vue({vue.get("vue")})")
        self.list_article(vue)
        print(f"L'article avec plus de like({like.get("like")})")
        self.list_article(like)
        print(f"L'article avec plus de dislike({like.get("dislike")})")
        self.list_article(dislike)
    
    def list_article_by_tag(self)->None:
        data = self.read_json()
        tags = set()
        if data is not None:
            for field in data:
                for r in field.get('tags').split(','):
                    tags.add(r.strip())
            print(f"Liste des articles par tag({len(tags)})")                    
            for tag in sorted(list(tags)):
                print(f">>{tag}<<")
                for field in data:
                    if tag in field.get('tags'):
                        self.list_article(field)
    
    def list_article_by_auteur(self)->None:
        data = self.read_json()
        auteurs = set()
        if data is not None:
            for field in data:
                    auteurs.add(field.get('auteur').strip())
            print(f"Liste des articles par auteur({len(auteurs)})")
            for value in sorted(list(auteurs)):
                print(f">>{value}<<")
                for field in data:
                    if value in field.get('auteur'):
                        self.list_article(field)
    
    def list_article_by_etat(self)->None:
        data = self.read_json()
        etat = set()
        if data is not None:
            for field in data:
                    etat.add(field.get('etat').strip())
            print(f"Liste des articles par auteur({len(etat)})")
            for value in sorted(list(etat)):
                print(f">>{value}<<")
                for field in data:
                    if value in field.get('etat'):
                        self.list_article(field)