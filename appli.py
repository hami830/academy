from flask import Flask, render_template, url_for, request,flash,redirect
import psycopg2 as psy
app = Flask(__name__)
def connexiondb():
	try:
		connexion = psy.connect(host="localhost",
					database="sonatel1",
					user="postgres",
					password="H@midou8"
					)
		return connexion
	except (Exception) as error:
		print("Problème de connexion au serveur Postgres", error)
con = connexiondb()
cur = con.cursor()
@app.route('/')
def home():
	return render_template('index0.html')
#########################Inscription apprenant##################
@app.route('/inscription', methods=['GET','POST'])
def inscription():
    cur.execute("SELECT id_promo ,nom_promo FROM promotion")
    promo=cur.fetchall()
    if request.method == "POST":
        details = request.form
        matricule = details['matricule']
        prenom = details['prenom']
        nom = details['nom']
        date_naissance= details['date_naissance']
        requete_ajout_ap="INSERT INTO apprenant(matricule,prenom,nom,date_naissance) VALUES ( %s,%s, %s,%s)"
        cur.execute(requete_ajout_ap,(matricule,prenom,nom,date_naissance))
        con.commit()
    return render_template('Inscription.html',n=promo)

########################istes de promotion########################
@app.route('/list', methods=['GET','POST'])
def liste():
    cur.execute("SELECT * FROM promotion")
    liste=cur.fetchall()
    return render_template('list.html',apprenant=liste)
#####################modifier des apprenants####################
@app.route('/modiref', methods = ['GET','POST'])
def modiref():
	cur=con.cursor()
	cur.execute("SELECT * FROM apprenant")
	var1=cur.fetchall()
	con.commit()

	cur.execute("SELECT * FROM promotion")
	var2=cur.fetchall()
	con.commit()

	if request.method == 'POST':
		id_data = request.form['id']
		matricule = request.form['matricule']
		prenom = request.form['prenom']
		nom = request.form['nom']
		date_naissance = request.form['date_naissance']
		id_promo = int(request.form['nom_promo'])
		cur = con.cursor
		cur.execute("""
		UPDATE apprenant
		SET matricule=%s, prenom=%s, nom=%s, date_naissance=%s, id_promo=%s
		WHERE id_app=%s """, (matricule, prenom, nom, date_naissance, id_promo,id_data))
		con.commit()
		flash("Données mises a jour avec succées")
		
		cur=con.cursor()
		cur.execute("SELECT * FROM apprenant")
		var3=cur.fetchall()
		con.commit()

		return render_template('modiref.html', apprenant=var3, promo= var2)
	return render_template('modiref.html', apprenant=var1, promo = var2)
#---------------------Menu Referentiel----------------
@app.route('/referentiel', methods=['GET','POST'])
def nouveauref():
    if request.method == "POST":
        details = request.form
        nom_ref = details['nom_ref']
        requete_ajout_ref="INSERT INTO referentiel(nom_ref) VALUES (%s)"
        cur.execute(requete_ajout_ref,(nom_ref,))
        con.commit()
    return render_template('ref.html')
#----------------lister referentiel-----------------
@app.route('/modif_ref')
def modif_ref():
	cur = con.cursor()
	cur.execute("SELECT * FROM referentiel")
	data =cur.fetchall()
	cur.close()
	return render_template('modif_ref.html', apprenant = data)
##############modifier referentiel###########################
# @app.route('/update', methods = ['POST', 'GET'])
# def update():
# 	if request.method == 'POST':
# 		id_data = request.form['id']
# 		nom_ref = request.form['nom_ref']
# 		cur = con.cursor()
# 		cur.execute("""
# 		UPDATE referentiel
# 		SET nom_ref=%s
# 		WHERE id=%s



# 		""", (nom_ref, id_data))
# 		flash("Data Update Successfully")
# 		con.commit()
# 		return redirect(url_for('modif_ref'))



		
    #return render_template('mod_ref.html', l=row)
#------------------- Menu Promo--------------------
@app.route('/promotion',methods=['GET','POST'])
def ajout_promo():
     cur.execute("SELECT id_ref ,nom_ref FROM referentiel")
     promo=cur.fetchall()
     if request.method == "POST":
         details = request.form
         nom_promo = details['nom_promo']
         date_debut = details['date_debut']
         date_fin = details['date_fin']
         id_promo=int(details['referentiel'])
         requete_ajout_promo="INSERT INTO promotion(nom_promo,date_debut,date_fin,id_ref) VALUES ( %s,%s, %s,%s)"
         cur.execute(requete_ajout_promo,(nom_promo,date_debut,date_fin,id_promo))
         con.commit()
     return render_template('promo.html',n = promo)
if __name__ == '__main__':
    app.run(debug=True, port=3000)