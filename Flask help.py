import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, render_template_string, url_for

app = Flask(__name__)

def generate_graphs():
    # Read the CSV file
    df = pd.read_csv('/Users/Ragya/Downloads/DigiDB_digimonlist.csv')
    
    print("Columns in the CSV file:")
    print(df.columns)
    print("\nFirst few rows of the data:")
    print(df.head())

    # Create a bar chart showing the number of Digimon by stage
    plt.figure(figsize=(10, 6))
    try:
        stage_column = 'Stage'  # This is the correct column name for levels/stages
        stage_count = df[stage_column].value_counts()
        sns.barplot(x=stage_count.index, y=stage_count.values, palette='viridis')
        plt.title(f'Number of Digimon by {stage_column}')
        plt.xlabel(stage_column)
        plt.ylabel('Count')
        stage_count_path = os.path.join('static', 'stage_count.png')
        plt.savefig(stage_count_path)
        plt.show()
        print(f"Saved stage count graph to {stage_count_path}")
    except KeyError as e:
        print(f"Error: Column '{e.args[0]}' not found in the CSV file.")

    # Create a scatter plot of Digimon's attack vs. defense
    plt.figure(figsize=(10, 6))
    try:
        attack_column = 'Lv50 Atk'  # This is the correct column name for attack
        defense_column = 'Lv50 Def'  # This is the correct column name for defense
        sns.scatterplot(x=attack_column, y=defense_column, data=df, hue=stage_column, palette='viridis')
        plt.title(f'{attack_column} vs. {defense_column} of Digimon')
        plt.xlabel(attack_column)
        plt.ylabel(defense_column)
        attack_vs_defense_path = os.path.join('static', 'attack_vs_defense.png')
        plt.savefig(attack_vs_defense_path)
        plt.show()
        print(f"Saved attack vs defense graph to {attack_vs_defense_path}")

    except KeyError as e:
        print(f"Error: Column '{e.args[0]}' not found in the CSV file.")

# Update the HTML template to reflect the new graph names
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Digimon Graphs</title>
</head>
<body>
    <h1>Digimon Graphs</h1>
    <h2>Number of Digimon by Stage</h2>
    <img src="{{ url_for('static', filename='stage_count.png') }}" alt="Number of Digimon by Stage">
    <h2>Lv50 Atk vs. Lv50 Def of Digimon</h2>
    <img src="{{ url_for('static', filename='attack_vs_defense.png') }}" alt="Lv50 Atk vs. Lv50 Def of Digimon">
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

if __name__ == "__main__":
    generate_graphs()
    app.run(debug=True)
