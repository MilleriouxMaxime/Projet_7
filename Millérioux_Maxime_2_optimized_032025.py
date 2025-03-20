import argparse
import csv
import time


def parse_args():
    parser = argparse.ArgumentParser(description="Optimize stock portfolio")
    parser.add_argument(
        "--file", type=str, required=True, help="Path to CSV file with stock data"
    )
    parser.add_argument(
        "--budget", type=float, default=500, help="Investment budget (default: 500)"
    )
    return parser.parse_args()


def read_csv(file_path):
    """
    Lit un fichier CSV et retourne une liste de tuples (action, coût, bénéfice).
    Chaque ligne du fichier doit contenir une action, un coût et un bénéfice en pourcentage.
    """
    data = []  # Initialise une liste vide pour stocker les données
    with open(file_path, "r") as file:  # Ouvre le fichier CSV en mode lecture
        reader = csv.reader(file)  # Crée un lecteur CSV
        next(reader)  # Passe la ligne d'en-tête

        for row in reader:  # Pour chaque ligne dans le fichier CSV
            action = row[0]  # Récupère le nom de l'action
            cost = float(row[1])  # Convertit le coût en float
            benefit = float(
                row[2].rstrip("%")
            )  # Supprime le '%' et convertit le bénéfice en float
            data.append(
                (action, cost, benefit)
            )  # Ajoute un tuple (action, coût, bénéfice) à la liste

    return data  # Retourne la liste des données


def greedy_optimization(data, budget):
    """
    Optimise la sélection d'actions en maximisant le bénéfice tout en respectant un budget donné.
    Trie les actions par ratio bénéfice/coût et sélectionne les meilleures jusqu'à épuisement du budget.
    """
    data = [
        action for action in data if action[1] > 0
    ]  # Supprime les actions dont le coût est 0 ou inférieur
    data.sort(
        key=lambda x: (x[1] * x[2]) / 100 / x[1], reverse=True
    )  # Trie les actions par ratio bénéfice/coût en ordre décroissant

    total_cost = 0  # Initialise le coût total à 0
    total_benefit = 0  # Initialise le bénéfice total à 0
    selected_actions = (
        []
    )  # Initialise une liste vide pour stocker les actions sélectionnées

    for action in data:  # Pour chaque action dans les données triées
        _, cost, benefit = action  # Décompose l'action en nom, coût et bénéfice
        benefit_value = (
            cost * benefit
        ) / 100  # Convertit le pourcentage de bénéfice en valeur réelle

        if (
            total_cost + cost <= budget
        ):  # Si le coût total avec cette action ne dépasse pas le budget
            selected_actions.append(
                action
            )  # Ajoute l'action à la liste des actions sélectionnées
            total_cost += cost  # Ajoute le coût de l'action au coût total
            total_benefit += (
                benefit_value  # Ajoute la valeur du bénéfice au bénéfice total
            )

    return (
        selected_actions,
        total_benefit,
    )  # Retourne les actions sélectionnées et le bénéfice total


def main():
    args = parse_args()
    file_path = args.file
    budget = args.budget
    data = read_csv(file_path)
    start = time.time()
    best_combination, max_benefit = greedy_optimization(data, budget)

    print(f"Best combination: {best_combination}")
    print(f"Max benefit: {max_benefit}")
    print(f"Budget restant: {500 - sum([item[1] for item in best_combination]):.2f}")
    print(f"Temps : {time.time() - start} secondes")


if __name__ == "__main__":
    main()

