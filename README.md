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
git checkout Lab1
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

Après avoir activé le venv, vous pouvez exécuter les programme Python (veuillez vous assurer de lancer le server avant le client) :

```bash
python server.py
```
```bash
python client.py
```

---

## Désactiver l`environnement virtuel

Une fois que vous avez terminé, vous pouvez désactiver l`environnement virtuel avec la commande :

```bash
deactivate
```

