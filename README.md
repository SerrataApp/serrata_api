# serrata_api

Création de la base de données et API pour les scores de https://github.com/CorentinAT/serrata

Développé en Python

## Outils utilisés

- SQLite3 pour la création de la base de données
- FastAPI pour l'API

## Fichiers

- **bdd.py** créé la base de données, et contient les fonctions qui communiquent directement avec elles
- **classes.py** contient le modèle des classes renvoyées par l'API, et les fonctions pour convertir les données renvoyés par bdd.py en objets
- **api.py** contient l'API FastAPI et ses fonctions

## Requetes disponibles

- **/scores_europe** récupère tous les scores envoyés dans le mode de jeu "Europe", dans l'ordre croissant des temps
- **/scores_afrique** idem pour le mode de jeu "Afrique"
- **/scores_monde** idem pour le mode de jeu "Monde"
- **/envoyer_score_europe** envoie et enregistre un score lié au mode de jeu "Europe"
- **/envoyer_score_afrique** idem pour le mode "Afrique"
- **/envoyer_score_monde** idem pour le mode "Monde"
