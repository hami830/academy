from flask import Flask, render_template, request, flash, url_for, redirect
import psycopg2 as psy
def ConnexionDB():
    try:
        #Connexion à la base de données
        connection = psy.connect(user="postgres",password="H@midou8",
                                    host="localhost",
                                    port="5432",
                                    database="sonatel4" 
                                    )
        return connection
    except (Exception) as error :
        print ("Problème de connexion au serveur PostgreSQL", error)
con = ConnexionDB()
cur = con.cursor()
app = Flask(__name__) #permet de localiser les ressources cad les templates
@app.route('/')
def index():
    return render_template("image.html")
@app.route('/accueil')
def accueil():
    return redirect(url_for('index'))
@app.route('/SCOLARITÉ/inscription')
def Inscription():
    return render_template("Inscription.html")
################menu inscription###################
@app.route('/SCOLARITÉ/inscription', methods=['GET','POST'])
def inscription():
    cur.execute("SELECT * FROM promotion")
    promo=cur.fetchall()
    if request.method == "POST":
        details = request.form
        matricule =details['matricule']
        nom = details['nom']
        prenom= details['prenom']
        date_naissance= details['date_naissance']
        requete_ajout_ap="INSERT INTO apprenant(matricule,nom,prenom,date_naissance) VALUES (  %s, %s, %s, %s)"
        cur.execute(requete_ajout_ap,(matricule, nom, prenom, date_naissance))
        con.commit()
    return render_template('Inscription.html',n=promo)
###################modifier apprenant####################
@app.route('/modifap2', methods = ['POST', 'GET'])
def modifap2():
    cur.execute("SELECT * FROM promotion")
    lister2=cur.fetchall()
    cur.execute("SELECT apprenant.id_app,apprenant.matricule,apprenant.nom,apprenant.prenom,apprenant.date_naissance,promotion.nom_promo FROM apprenant,promotion ")
    lister1=cur.fetchall()
    if request.method == 'POST':
        details = request.form
        id_app=details['id_app']
        nom = details['nom']
        prenom = details['prenom']
        date_naissance= details['date_naissance']
        id_promo= int(details['id_promo'])
        cur.execute("""
        UPDATE apprenant
        SET nom=%s, prenom=%s,date_naissance=%s,id_promo=%s   
        WHERE id_app=%s 
        """,(nom,prenom,date_naissance,id_promo,id_app))
        cur.execute("SELECT apprenant.id_app,apprenant.matricule,apprenant.nom,apprenant.prenom,apprenant.date_naissance,promotion.nom_promo FROM apprenant,promotion ")  
        lister11=cur.fetchall()
        con.commit()
        return render_template('modifap2.html',l1=lister11,l2=lister2)
    return render_template('modifap2.html',l1=lister1,l2=lister2)
##########################annuler apprenant#########################
@app.route('/listapan')
def listapan():
    cur.execute("SELECT apprenant.id_app,apprenant.nom,apprenant.prenom,apprenant.date_naissance,apprenant.statu,promotion.nom_promo FROM apprenant,promotion where statu='inscrit' ")
    lister1=cur.fetchall()
    return render_template('anulap.html',l1=lister1)
@app.route('/anulap/<string:id_data>', methods = ['POST', 'GET'])
def anulap(id_data):
    flash("Data annuler Successfully")
    cur.execute("""UPDATE apprenant SET statu='annuler'WHERE id_app=%s""",(id_data))
    con.commit()
    return redirect(url_for('listapan'))
#########################suspendre apprenant##################
@app.route('/listapsus')
def listapsus():
    cur.execute("SELECT apprenant.id_app,apprenant.nom,apprenant.prenom,apprenant.date_naissance,apprenant.statu,promotion.nom_promo FROM apprenant,promotion where statu='inscrit' ")
    lister1=cur.fetchall()
    return render_template('suspenap.html',l1=lister1)
@app.route('/suspenqp/<string:id_data>', methods = ['POST', 'GET'])
def suspenap(id_data):
    flash("Data annuler Successfully")
    cur.execute(""" UPDATE apprenant SET statu='suspend' WHERE id_app=%s""",(id_data))
    con.commit()
    return redirect(url_for('suspenap'))
#####################menu promotion###################
@app.route('/PROMOTION/Nouveau',methods=['GET','POST'])
def nouveaupromo():
    cur.execute("SELECT id_ref ,nom_ref FROM referentiel")
    promo=cur.fetchall()
    if request.method == "POST":
        details = request.form
        nom_promo = details['nom_promo']
        date_debut = details['date_debut']
        date_fin = details['date_fin']
        id_ref=int(details['referentiel'])
        requete_ajout_promo="INSERT INTO promotion(nom_promo,date_debut,date_fin,id_ref) VALUES ( %s,%s, %s,%s)"
        cur.execute(requete_ajout_promo,(nom_promo,date_debut,date_fin,id_ref))
        con.commit()
    return render_template('promo.html',n = promo)
##################lister promotion#############################
@app.route('/listpromo', methods=['GET','POST'])
def listpromo():
    cur.execute("SELECT id_promo,nom_promo,date_debut,date_fin,nom_ref FROM referentiel, promotion WHERE referentiel.id_ref=promotion.id_ref")
    listpro=cur.fetchall()
    return render_template('listpromo.html',promotion=listpro)
###################modifier promotion###########################
@app.route('/modifpromo',  methods=['GET','POST'])
def modifpromo():
    cur.execute("SELECT *FROM referentiel")
    ref=cur.fetchall()
    cur.execute("SELECT id_promo,nom_promo,date_debut,date_fin,nom_ref FROM referentiel, promotion WHERE referentiel.id_ref=promotion.id_ref ")
    listpro=cur.fetchall()
    if request.method == 'POST':
            details = request.form
            id_promo =details['id_promo']
            nom_promo =details['nom_promo']
            date_debut =details['date_debut']
            date_fin =details['date_fin']
            id_ref =details['id_ref']
            cur.execute("""

            UPDATE promotion
            SET nom_promo=%s, 
            date_debut=%s, 
            date_fin=%s,
            id_ref=%s
            WHERE id_promo=%s

            """, (nom_promo, date_debut,date_fin,id_ref,id_promo))
           

            cur.execute("SELECT id_promo,nom_promo,date_debut,date_fin,nom_ref FROM referentiel, promotion WHERE referentiel.id_ref=promotion.id_ref")
            listpro1=cur.fetchall()
            con.commit()
            return render_template('modifpromo.html',referentiel=ref,promotion=listpro1)    
    return render_template('modifpromo.html',referentiel=ref,promotion=listpro)
#####################menu referentiel###########################
@app.route('/RÉFÉRENTIEL/nouveau')
def ref():
    return render_template("ref.html")
@app.route('/RÉFÉRENTIEL/nouveau', methods=['GET','POST'])
def nouveauref():
    if request.method == "POST":
        details = request.form
        nom_ref = details['nom_ref']
        requete_ajout_ref="INSERT INTO referentiel(nom_ref) VALUES (%s)"
        cur.execute(requete_ajout_ref,(nom_ref,))
        con.commit()
    return render_template("ref.html")
################update referentiel#################################
@app.route('/modifref', methods = ['POST', 'GET'])
def modifref():
    cur.execute("SELECT * FROM referentiel")
    listrefe=cur.fetchall()
    if request.method == 'POST':
            details = request.form
            id_ref =details['id_ref']
            nom_ref =details['nom_ref']
            cur.execute("""
            
            UPDATE referentiel
            SET nom_ref=%s 
            WHERE id_ref=%s

            """, (nom_ref, id_ref))
            con.commit()
            cur.execute("SELECT *FROM referentiel")
            listrefe1=cur.fetchall()
            return render_template('modifref.html', referentiel=listrefe1)
    return render_template('modifref.html', referentiel=listrefe)

if __name__ == '__main__': #si le fichier est executer alors execute le bloc
    app.run(debug=True) #debug=True relance le serveur à chaque modification