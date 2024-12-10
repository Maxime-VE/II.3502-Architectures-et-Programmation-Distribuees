# Guide pour récupérer et exécuter le code Python

Ce dépôt contient du code écrit en Python. Un environnement virtuel (**venv**) est fourni pour vous faciliter l`utilisation de notre solution.

---

## Récupérer le code depuis GitHub

Pour cloner ce dépôt et récupérer le code sur votre machine, suivez les étapes ci-dessous :

### 1. Cloner le dépôt

Utilisez la commande suivante pour cloner le dépôt sur votre machine locale :

```bash
git clone https://github.com/Maxime-VE/II.3502-Architectures-et-Programmation-Distribuees
```

### 2. Accéder au répertoire du TP

Une fois le clonage effectué, changez la branche du répertoire pour accéder au bon TP avec la commande :

```bash
git checkout Lab5
```
---

## Activer l`environnement virtuel

Le projet utilise un environnement virtuel Python afin de gérer les dépendances. Cet environnement est situé dans le dossier `venv`.

### 1. Activer le venv sous Windows

Si vous utilisez Windows, activez l`environnement virtuel avec la commande suivante :

```bash
venv\Scripts\activate
```

### 2. Activer le venv sous MacOS/Linux

Si vous êtes sur MacOS ou Linux, utilisez cette commande pour activer l`environnement virtuel :

```bash
source venv/bin/activate
```

---

## Lancer le programme

Dans un environnement munis de spark et dans le dossier Python du projet, Lancer le serveur Spark avec la commande: 
```bash
spark-submit main_spark.py
```
Après son lancement, vous pouvez visualiser son état d'avancement directement depuis la page de gestion Spark disponible à l'adresse: 
```bash
localhost:4040
```
---
## Fichier de sortie

Les fichiers générés par le serveur sont disponible dans le dossier  `SparkOutput`au format .csv. Une application externe
comme `Excel` peut rendre la lecture plus simple

---

## Désactiver l`environnement virtuel

Une fois que vous avez terminé, vous pouvez désactiver l`environnement virtuel avec la commande :

```bash
deactivate
```

