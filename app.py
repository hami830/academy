from flask import Flask, render_template ,url_for,request,redirect
import psycopg2 as psy 
import datetime

#On donne ensuite un nom à l’application ici ce sera app
app = Flask(__name__)



def connectionDB():
    try:
        #connection a la base de donnee
        connection=psy.connect(host= "localhost",
                                database="sonatel4",
                                user="postgres",
                                password="H@midou8",
                                port ="5432"
                            )
        return connection
    except (Exception) as error:
        print(" PROBLE;E DE CONNECTION AU SERVEUR ",error)
connection=connectionDB()
curseur=connection.cursor()
#@app.route permet de préciser à quelle adresse ce qui suit va s’appliquer
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/')
def fond():
    return render_template('fond.html')


@app.route('/inscription')
def kha():
    curseur.execute("SELECT id_promo ,nom_promo FROM promotion WHERE date_deb>DATE( NOW() )")
    promo=curseur.fetchall()
    requete_liste_matricule = "SELECT max(id_ap) FROM apprenant2"
    curseur.execute(requete_liste_matricule)
    result_matricule = curseur.fetchall()
    for mat in result_matricule:                
        matricule=mat[0]
    date_actu=datetime.datetime.today().strftime('%Y')

    if matricule == None:
        num=1
        val='-'+str(num)+'-'
        naf = "SA"+val+str(date_actu)
    else:
        num=matricule+1
        val='-'+str(num)+'-'
        naf="SA"+val+str(date_actu)
    return render_template('inscription.html',n=promo,naf=naf)



@app.route('/inscription', methods=['GET','POST'])
def inscription():
    if request.method == "POST":
        details = request.form
        matricule= details['matricule']
        nom_ap = details['nom_ap']
        prenom_ap = details['prenom_ap']
        date_nais= details['date_nais']
        add_ap= details['add_ap']
        sexe_ap= details['sexe_ap']
        requete_ajout_ap="INSERT INTO apprenant2(matricule,nom_ap,prenom_ap,date_nais,add_ap,sexe_ap) VALUES (  %s,%s, %s, %s,%s, %s)"
        curseur.execute(requete_ajout_ap,(matricule,nom_ap,prenom_ap,date_nais,add_ap,sexe_ap))
        connection.commit()
    return render_template('inscription.html')
        
    




# -----------------------------SCOLARITE------------------------------
# ------------------LIST---DES-----APPRENANTS--------------------------
@app.route('/listapp', methods=['GET','POST'])
def listapp():
    curseur.execute("SELECT *FROM apprenant2")
    lister1=curseur.fetchall()   
    return render_template('listapp.html',l1=lister1)
# -----------------------UPDATE-APPRENANT----------------------

@app.route('/modifap2', methods = ['POST', 'GET'])
def modifap2():
    
    
    curseur.execute("SELECT *FROM promotion")
    lister2=curseur.fetchall()
    curseur.execute("SELECT  id_ap,matricule,nom_ap,prenom_ap,date_nais,add_ap,sexe_ap,nom_promo FROM promotion,apprenant2 where apprenant2.id_promo=promotion.id_promo")
    lister1=curseur.fetchall()
    
    if request.method == 'POST':
        details = request.form
        id_ap=details['id_ap']
        matricule =details['matricule']
        nom_ap = details['nom_ap']
        prenom_ap = details['prenom_ap']
        date_nais= details['date_nais']
        add_ap= details['add_ap']
        sexe_ap= details['sexe_ap']
        id_promo= int(details['id_promo'])
        curseur.execute("""
        UPDATE apprenant2
        SET matricule=%s,nom_ap=%s, prenom_ap=%s,date_nais=%s,add_ap=%s,sexe_ap=%s,id_promo=%s   
        WHERE id_ap=%s 
        """, (matricule,nom_ap,prenom_ap,date_nais,add_ap,sexe_ap,id_promo,id_ap))
        curseur.execute("SELECT id_ap,matricule,nom_ap,prenom_ap,date_nais,add_ap,sexe_ap, nom_promo FROM apprenant2 ,promotion where apprenant2.id_promo=promotion.id_promo")
        lister11=curseur.fetchall()
        
        connection.commit()
        return render_template('modifap2.html',l1=lister11,l2=lister2)
    return render_template('modifap2.html',l1=lister1,l2=lister2)

#----------------annuler--ap---------------------

@app.route('/delete/<string:id_ap>', methods = ['POST', 'GET'])
def delete(id_ap):
    
	curseur.execute("DELETE FROM apprenant2 WHERE id_ap =%s", (id_ap))
	connection.commit()

	return render_template('delete.html')

#------------reference--------------------------------------------------------------------
#--------insertion----------------------------

@app.route('/nouveauref', methods=['GET','POST'])
def nouveauref():
    if request.method == "POST":
        details = request.form
        nom_ref = details['nom_ref']
        requete_ajout_ref="INSERT INTO referentiel(nom_ref) VALUES (%s)"
        curseur.execute(requete_ajout_ref,(nom_ref,))
        connection.commit()
    return render_template('newref.html')

#------------list ref--------------------

@app.route('/listref', methods=['GET','POST'])
def listreferentiel():
    curseur.execute("SELECT *FROM referentiel")
    listrefe=curseur.fetchall()
    return render_template('listref.html',referentiel=listrefe)


#------------update ref---------------------------
@app.route('/modifref', methods = ['POST', 'GET'])
def modifref():
    curseur.execute("SELECT *FROM referentiel")
    listrefe=curseur.fetchall()
    if request.method == 'POST':
            details = request.form
            id_ref =details['id_ref']
            nom_ref =details['nom_ref']
            curseur.execute("""
            
            UPDATE referentiel
            SET nom_ref=%s 
            WHERE id_ref=%s

            """, (nom_ref, id_ref))
            connection.commit()
            curseur.execute("SELECT *FROM referentiel")
            listrefe1=curseur.fetchall()
            return render_template('modifref.html', referentiel=listrefe1)
    return render_template('modifref.html', referentiel=listrefe)

#---------------promo--------------------------
#----------------------insertion-----------------
@app.route('/nouveaupromo',methods=['GET','POST'])
def nouveaupromo():
    curseur.execute("SELECT id_ref ,nom_ref FROM referentiel")
    promo=curseur.fetchall()
    if request.method == "POST":
        details = request.form
        nom_promo = details['nom_promo']
        date_deb = details['date_deb']
        date_fin = details['date_fin']
        id_ref=int(details['referentiel'])
        requete_ajout_promo="INSERT INTO promotion(nom_promo,date_deb,date_fin,id_ref) VALUES ( %s,%s, %s,%s)"
        curseur.execute(requete_ajout_promo,(nom_promo,date_deb,date_fin,id_ref))
        connection.commit()
    return render_template('newpromo.html',n = promo)
#----------------------listpromo-------------------

@app.route('/listpromo', methods=['GET','POST'])
def listpromo():
    curseur.execute("SELECT id_promo,nom_promo,date_deb,date_fin,nom_ref FROM referentiel, promotion WHERE referentiel.id_ref=promotion.id_ref")
    listpro=curseur.fetchall()
    return render_template('listpromo.html',promotion=listpro)

#---------------update--------------------------------
@app.route('/modifpromo',  methods=['GET','POST'])
def modifpromo():
    curseur.execute("SELECT *FROM referentiel")
    ref=curseur.fetchall()

    curseur.execute("SELECT id_promo,nom_promo,date_deb,date_fin,nom_ref FROM referentiel, promotion WHERE referentiel.id_ref=promotion.id_ref ")
    listpro=curseur.fetchall()

    if request.method == 'POST':
            details = request.form
            id_promo =details['id_promo']
            nom_promo =details['nom_promo']
            date_deb =details['date_deb']
            date_fin =details['date_fin']
            id_ref =details['id_ref']
            curseur.execute("""
            
            UPDATE promotion
            SET nom_promo=%s, 
            date_deb=%s, 
            date_fin=%s,
            id_ref=%s
            WHERE id_promo=%s

            """, (nom_promo, date_deb,date_fin,id_ref,id_promo))
           

            curseur.execute("SELECT id_promo,nom_promo,date_deb,date_fin,nom_ref FROM referentiel, promotion WHERE referentiel.id_ref=promotion.id_ref")
            listpro1=curseur.fetchall()
            connection.commit()
            return render_template('modifpromo.html',referentiel=ref,promotion=listpro1)    
    return render_template('modifpromo.html',referentiel=ref,promotion=listpro)


@app.route('/suspendre')
def suspendre():
    return render_template('suspendre')





#def connexion():
if __name__ == "__main__":
    app.run(debug=True, port=5000)