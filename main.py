from Info import Info
from pprint import pprint

ERROR_MSG = "Erreur, veuillez bien choisir"

def menu():
    print("-----------Look-Article-----------")
    print("1- Créer un fichier Json d'articles.")
    print("2- Créer une base de donnée SQLite.")
    print("3- Ajouter un article.")
    print("4- Afficher les articles.")
    print("5- Article le plus noté.")
    print("6- Afficher les articles par tags.")
    print("7- Afficher les articles par auteurs.")
    print("8- Afficher les articles par état.")
    print("0- Quitter.")
    return input("Faites votre choix : ")

def sub_menu():
    print("-----------Type-Ajout-----------")
    print("1- Ajouter dans la base donnée.")
    print("2- Ajouter dans le fichier Json.")
    print("0- Quitter")
    return input("Faites votre choix : ")

def handle_sub_choice(info, choice):
    article = info.add_article()
    if choice == '1':
        info.add_article_tiny_db(article)
    elif choice == '2':
        info.add_to_txt_json(article)
    else:
        print(ERROR_MSG)

if __name__ == "__main__":
    info = Info()
    while(True):
        choix = menu()
        if choix == '1':
            info.add_to_txt_json(info.read_data()["data"])
        elif choix == '2':
            info.add_to_json_tiny_db()
        elif choix == '3':
            while(True):
                choix2 = sub_menu()
                if choix2 in ['1', '2']:
                    handle_sub_choice(info, choix2)
                    break
                elif choix2 == '0':
                    print("Retour au menu principal")
                    break
                else:
                    print("Erreur, veuillez bien choisir")
        elif choix == '4':
            info.list_articles()
        elif choix == '5':
            info.list_most_rated()
        elif choix == '6':
            info.list_article_by_tag()
        elif choix == '7':
            info.list_article_by_auteur()
        elif choix == '8':
            info.list_article_by_etat()
        elif choix == '0':
            print("Bye-bye")
            break
        else:
            print(ERROR_MSG)