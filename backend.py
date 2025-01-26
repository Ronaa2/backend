from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Charger la base de données (un fichier JSON ici)
try:
    with open("base_de_donnees.json", "r") as f:
        base_de_donnees = json.load(f)
except FileNotFoundError:
    base_de_donnees = {}

# Route pour répondre aux questions
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("question", "").lower()
    
    # Chercher la réponse dans la base de données
    reponse = base_de_donnees.get(question, "Je ne sais pas encore répondre à cette question.")
    
    # Si la réponse est inconnue, on demande à l'utilisateur
    if reponse == "Je ne sais pas encore répondre à cette question.":
        return jsonify({"reponse": reponse, "unknown": True})
    
    return jsonify({"reponse": reponse})

# Route pour apprendre une nouvelle réponse
@app.route("/apprendre", methods=["POST"])
def apprendre():
    data = request.get_json()
    question = data.get("question", "").lower()
    reponse = data.get("reponse", "")
    
    # Enregistrer dans la base de données
    base_de_donnees[question] = reponse
    with open("base_de_donnees.json", "w") as f:
        json.dump(base_de_donnees, f)
    
    return jsonify({"message": "Merci, j'ai appris une nouvelle réponse !"})

if __name__ == "__main__":
    app.run(debug=True)
