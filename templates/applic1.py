from flask import Flask, render_template, request, flash, url_for, redirect
import psycopg2 as psy

def ConnexionDB():
    try:
        #Connexion à la base de données
        connection = psy.connect(user="postgres",password="H@midou8",
                                    host="localhost",
                                    port="5432",
                                    database="FlaskApps"
                                    )
        return connection
    except (Exception) as error :
        print ("Problème de connexion au serveur PostgreSQL", error)
connection = ConnexionDB()
curseur = connection.cursor()
app = Flask(__name__) #permet de localiser les ressources cad les templates

@app.route('/')
def index():
    return render_template("index0.html")

@app.route('/SCOLARITÉ/inscription')
def Inscription():
    return render_template("Inscription.html")

@app.route('/SCOLARITÉ/Modifier')
def modifer():
    return render_template("modifier.html")

@app.route('/PROMOTION/Nouveau')
def promo():
    return render_template("promo.html")

@app.route('/RÉFÉRENTIEL/nouveau')
def ref():
    return render_template("ref.html")

@app.route('/RÉFÉRENTIEL/Nouveau', methods=["POST"])
def inf_ref():
    if request.method == "POST":
        nom_ref = request.form["nom_ref"]
        requete_ref = "INSERT INTO referentiel (libelle) VALUES (%s)"
        curseur.execute(requete_ref,(nom_ref,))
        connection.commit()
        return redirect(url_for('ref'))

if __name__ == '__main__': #si le fichier est executer alors execute le bloc
    app.run(debug=True) #debug=True relance le serveur à chaque modification