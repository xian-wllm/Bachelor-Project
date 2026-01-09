# Projet de Bachelor

Ce repository contient le code et les données associés à mon projet de bachelor.

## Structure du Repository

- `chsh_inequality/` : Contient tout le code lié au calcul à la limite de CHSH.
- `data_plot/` : Contient les données générées durant le projet.
- `main/` : Contient le code principal décrivant les inflations et le calcul de la visibilité pour les distributions GHZ et W.
- `plot/` : Contient le code permettant de générer les graphiques.

## Prérequis

Avant d'exécuter le code, assurez-vous d'avoir installé les prérequis suivants :

- [cvxpy](https://www.cvxpy.org/install/index.html) : Une bibliothèque Python pour la modélisation de problèmes d'optimisation convexes.
- [MOSEK](https://www.mosek.com/downloads/) : Un solveur d'optimisation. Vous aurez besoin d'une licence MOSEK pour utiliser cette bibliothèque.

Vous pouvez installer `cvxpy` via pip :

```bash
pip install cvxpy

