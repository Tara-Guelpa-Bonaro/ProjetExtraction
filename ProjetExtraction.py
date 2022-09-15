#!/usr/bin/env python3

"""
Nom du fichier : ProjetExtraction.py
Auteur : Tara Guelpa-Bonaro
Date : Avril 2022
Contenu du fichier : programme qui extrait les liens d’une page et indexe le texte de ces pages dans un dictionnaire.
le dictionnaire "index" a pour clé l'URL de la page cible et comme valeur le contenu de la page nettoyée.
La page nettoyée étant souvent très longue, je choisis de limiter le nombre de clé et de valeur à 1.
"""

import requests  # on importe le package "requests" pour faire une requête vers une page web
import sys  # on importe le package "sys" dont le but est de récupérer l'URL donnée par l'utilisateur

index = {}

# Fonction dont le but est d'ouvrir une requête sur l'URL spécifiée et d'extraire le texte de la page pour le traiter
def pilote(adresse, idx):
    # ouvre une requête sur l'URL spécifiée
    r = requests.get(adresse)
    if r.ok:
        # récupère le texte de la page
        text = r.text
    else:
        # affiche l'erreur (facultatif)
        print('erreur', r.reason)
        text = []
    liens = extraire_liens(text)
    indexe(idx, liens)
    return idx

# fonction dont le but est de parcourir les liens et de récupérer le texte de ces nouvelles pages
def indexe(idx, liens):
    # on itère sur les liens pour extraire le contenu nettoyé
    for url in liens:
        # ouvre une requête sur l'URL spécifiée
        r = requests.get(url)
        if r.ok:
            # récupère le texte de la page
            text = r.text
        else:
            # affiche l'erreur (facultatif)
            print('erreur', r.reason)
            text = []
        # nettoyage de la page, voir ci-après
        page_nette = nettoie_page(text)
        # on verifie si on veut vraiment indexer cette url
        if url not in idx:
            ajoute(idx, page_nette, url)

# fonction dont le but est d'ajouter l'URL au dictionnaire seulement si elle n'a pas encore été ajoutée
def ajoute(idx, page_nette, url):
    # si l'URL ne se trouve pas encore dans l'index,
    # on ajoute l'url en clé et son texte nettoyé en valeur
    if url not in idx:
        idx[url] = []
        idx[url] = page_nette
    return idx

# fonction dont le but est de nettoyer la page des balises HTML et de renvoyer le texte nettoyé
def nettoie_page(page):
    longueur_page = len(page)
    caractere = 0
    new_liste = []
    # On parcourt le texte sur la page
    while caractere <= longueur_page - 1:
        # Si on rencontre un début de balise en parcourant le texte, on continue de parcourir le texte
        # sans ajouter le caractere à la liste des caractères conservés
        if page[caractere] == "<":
            caractere += 1
            while page[caractere] != ">":
                caractere += 1
        # Si le caractère est en dehors d'une balise HTML, on l'ajoute à la liste des caractères à conserver
        else:
            new_liste.append(page[caractere])
        caractere += 1
    # On transforme la liste des caractères conservés en chaine de caractéres
    new_text = "".join(new_liste)
    return new_text

# fonction dont le but est d'extraire les URL de la page
def extraire_liens(page):
    longueur_page = len(page)
    caractere = 0
    new_liste = []
    liens = []
    # On parcourt le texte sur la page. Je choisis de limiter le nombre de clés et de valeur à 1.
    while caractere <= longueur_page - 1 and len(liens) < 1:
        # Si on rencontre un début de balise en parcourant le texte, on vérifie si c'est un lien HTML
        if page[caractere] == "<":
            caractere += 1
            test = page[caractere:caractere+12]
            if test == "a href=\"http":
                caractere += 8
                while page[caractere] != "\"":
                    new_liste.append(page[caractere])
                    caractere += 1
                # On transforme la liste des caractères conservés en chaine de caractéres
                new_text = "".join(new_liste)
                # On ajoute le lien à la liste des liens
                liens.append(new_text)
                new_text = ""
                new_liste = []
        # Si le caractère est en dehors d'une balise HTML, on ne l'ajoute pas à la liste
        else:
            caractere += 1
    return liens


# traite l'information à partir de l'URL fournie par l'utilisateur
url = sys.argv[1]
print(pilote(url, index))
