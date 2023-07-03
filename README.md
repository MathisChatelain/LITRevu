# Création et activation d'un environnement de développement Python avec venv

Ce guide vous expliquera comment créer et activer un environnement de développement Python en utilisant l'outil `venv`. Un environnement virtuel vous permet d'isoler les dépendances de votre projet Python, ce qui facilite la gestion des bibliothèques et des versions spécifiques requises pour votre application.

## Étapes

### 1. Vérifiez la version de Python

Assurez-vous d'avoir Python installé sur votre système. Ouvrez un terminal et exécutez la commande suivante :

```bash
python --version
```

Si Python est installé, vous verrez s'afficher la version correspondante (par exemple, `Python 3.9.2`). Si Python n'est pas installé, téléchargez et installez la dernière version depuis le site officiel de Python.

### 2. Créez un nouvel environnement virtuel

Ouvrez un terminal et placez-vous dans le répertoire de votre projet. Pour créer un nouvel environnement virtuel, exécutez la commande suivante :

```bash
python -m venv env
```

Cela créera un répertoire appelé `env` qui contiendra tous les fichiers de votre environnement virtuel.

### 3. Activez l'environnement virtuel

Selon votre système d'exploitation, la commande pour activer l'environnement virtuel peut varier :

#### Sous Windows

```bash
.\env\Scripts\activate
```

#### Sous macOS et Linux

```bash
source env/bin/activate
```

Après avoir exécuté la commande appropriée, vous verrez le nom de votre environnement virtuel s'afficher dans votre invite de commandes, indiquant que l'environnement a été activé avec succès.

### 4. Utilisez l'environnement virtuel

Maintenant que votre environnement virtuel est activé, vous pouvez installer les bibliothèques Python spécifiques à votre projet sans affecter les autres installations Python sur votre système.

Pour installer une bibliothèque, utilisez la commande `pip` (le gestionnaire de paquets Python) suivi du nom de la bibliothèque. Par exemple :

```bash
pip install numpy
```

Vous pouvez installer autant de bibliothèques que nécessaire pour votre projet.

### 5. Désactivation de l'environnement virtuel

Lorsque vous avez terminé de travailler dans votre environnement virtuel, vous pouvez le désactiver en exécutant la commande suivante :

```bash
deactivate
```

Cela vous ramènera à l'environnement Python global de votre système.

## Conclusion

Félicitations ! Vous savez maintenant comment créer et activer un environnement de développement Python en utilisant `venv`. L'utilisation d'environnements virtuels est une pratique recommandée pour développer des applications Python afin de maintenir la cohérence des dépendances et d'isoler votre projet des autres installations Python sur votre système.