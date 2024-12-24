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

### Quick One File Testing:
An all-in-one file (`main.py`) is available to quickly test all functionalities, including adding a single node, adding a list of nodes, retrieving the root hash, obtaining the audit path, getting the consistency proof path, and performing `is_member` verification. (Line 161)

The input logs are provided in the `example.txt` file and can be modified manually as needed.

### Distributed Deployment:
The RPC system is located in the `RPC` folder and contains `merkle_server.py` and `merkle_client.py`. These files can be executed in the terminal to test the solution.

### Change the Hash Method:
To make it easier to check the implemented method, the hash function can be changed to `"h(value)"`. Simply uncomment the following code lines:
- Line 25 in `main.py`
- Line 15 in `RPC/merkle_tree.py`

---

## Désactiver l`environnement virtuel

Une fois que vous avez terminé, vous pouvez désactiver l`environnement virtuel avec la commande :

```bash
deactivate
```

