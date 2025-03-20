import argparse  # Importe argparse pour analyser les arguments de la ligne de commande
import csv  # Importe le module csv pour lire les fichiers CSV
import time  # Importe time pour mesurer le temps d'exécution
from itertools import (
    combinations,
)  # Importe combinations pour générer des combinaisons de données


def parse_args():
    parser = argparse.ArgumentParser(
        description="Optimize stock portfolio"
    )  # Crée un analyseur d'arguments
    parser.add_argument(
        "--file", type=str, required=True, help="Path to CSV file with stock data"
    )  # Ajoute un argument pour le chemin du fichier CSV
    parser.add_argument(
        "--budget", type=float, default=500, help="Investment budget (default: 500)"
    )  # Ajoute un argument pour le budget d'investissement
    return parser.parse_args()  # Analyse les arguments et les retourne


def read_csv(file_path):
    """
    Lit un fichier CSV et retourne une liste de tuples (action, coût, bénéfice).
    Chaque ligne du fichier doit contenir une action, un coût et un bénéfice en pourcentage.
    """
    data = []  # Initialise une liste vide pour stocker les données
    with open(file_path, "r") as file:  # Ouvre le fichier CSV en mode lecture
        reader = csv.reader(file)  # Crée un lecteur CSV pour lire le fichier
        next(reader)  # Saute la ligne d'en-tête

        for row in reader:  # Pour chaque ligne dans le fichier CSV
            action = row[0]  # Récupère le nom de l'action
            cost = int(row[1])  # Convertit le coût en entier
            benefit = int(
                row[2].rstrip("%")
            )  # Supprime le '%' et convertit le bénéfice en entier
            data.append(
                (action, cost, benefit)
            )  # Ajoute un tuple (action, coût, bénéfice) à la liste

    return data  # Retourne la liste des données


def brute_force_optimization(data, budget):
    """
    Optimise les bénéfices en essayant toutes les combinaisons possibles d'éléments
    sans dépasser le budget donné.
    Retourne la meilleure combinaison d'éléments et le bénéfice maximal.
    """
    best_combination = (
        []
    )  # Initialise une liste vide pour stocker la meilleure combinaison
    max_benefit = 0  # Initialise le bénéfice maximal à 0

    # Essaye toutes les combinaisons possibles
    for number_of_actions in range(
        1, len(data) + 1
    ):  # Pour chaque nombre d'actions de 1 à n
        for subset in combinations(
            data, number_of_actions
        ):  # Pour chaque sous-ensemble de données
            total_cost = sum(
                item[1] for item in subset
            )  # Calcule le coût total du sous-ensemble
            total_benefit = sum(
                (item[1] * item[2] / 100) for item in subset
            )  # Calcule le bénéfice total du sous-ensemble

            # Vérifie si le coût total est dans le budget et si le bénéfice est maximisé
            if total_cost <= budget and total_benefit > max_benefit:
                max_benefit = total_benefit  # Met à jour le bénéfice maximal
                best_combination = [
                    item for item in subset
                ]  # Met à jour la meilleure combinaison

    return (
        sorted(best_combination),
        max_benefit,
    )  # Retourne la meilleure combinaison triée et le bénéfice maximal


def main():
    args = parse_args()  # Analyse les arguments de la ligne de commande
    file_path = args.file  # Récupère le chemin du fichier CSV
    budget = args.budget  # Récupère le budget d'investissement
    data = read_csv(file_path)  # Lit les données du fichier CSV
    start = time.time()  # Enregistre le temps de début

    best_combination, max_benefit = brute_force_optimization(
        data, budget
    )  # Optimise les bénéfices

    print(f"Best combination: {best_combination}")  # Affiche la meilleure combinaison
    print(f"Max benefit: {max_benefit}")  # Affiche le bénéfice maximal
    print(
        f"Budget restant: {500 - sum([item[1] for item in best_combination]):.2f}"
    )  # Affiche le budget restant
    print(time.time() - start)  # Affiche le temps d'exécution


if __name__ == "__main__":
    main()  # Exécute la fonction main si le script est exécuté directement

