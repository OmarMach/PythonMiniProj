from flask import Flask, render_template, request
import mysql.connector as msqlc
from forms import AjouterReclamationForm, adminConnectionForm,ajouterAdmin

#TODO choice list -
#Configuration variables
app = Flask(__name__)
app.config['SECRET_KEY'] = 'GInf2020'

#Usefull requests variable placeholders
insertRequest = "INSERT INTO reclamation (type,msg) VALUES (%s,%s)"
deleteRequest = "DELETE FROM reclamation WHERE id = %s"
selectRequest = "SELECT * FROM reclamation"
connectAdminRequest = "Select * FROM admin where login = %s and password = %s"
AddAdminRequest = "INSERT INTO admin (login,password) VALUES (%s,%s)"

isConnected = False
def connected():
    isConnected = True
def disconnected():
    isConnected = False
def connectionStatus():
    return isConnected

#Database connection and cursor definition
db = msqlc.connect(host="localhost",user="root",passwd="",database="PythonMiniProjet")
cursor = db.cursor(buffered=True)

#Routes :
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/AjouterReclamation", methods = ['GET', 'POST'])
def AjouterReclmation():
    form = AjouterReclamationForm()
    if form.is_submitted():
        result = (request.form.get('type'),request.form.get('message'))
        cursor.execute(insertRequest,result)
        db.commit()
        return render_template("AjouterReclamation.html", form=form, added = True)
    return  render_template("AjouterReclamation.html", form = form)

@app.route("/AjouterAdmin", methods = ['GET', 'POST'])
def AjouterAdmin():
    form = ajouterAdmin()
    if form.is_submitted():
        result = (request.form.get('login'),request.form.get('password'))
        try:
            cursor.execute(AddAdminRequest,result)
        except:
            return render_template("AjouterAdmin.html", form=form, added = False)
        db.commit()
        return render_template("AjouterAdmin.html", form=form, added = True)
    return  render_template("AjouterAdmin.html", form = form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = adminConnectionForm()
    if connectionStatus() == True:
        return render_template("showReclamations.html", reclamations=cursor)
    if form.is_submitted():
        cursor.execute(connectAdminRequest, (request.form.get('login'), request.form.get('password')))
        adminExists = cursor.fetchone()
        if adminExists != None:
            connected()
            cursor.execute(selectRequest)
            return render_template("showReclamations.html",reclamations = cursor)
        else:
            return render_template("admin.html", form=form, wrong = True)
    return render_template("admin.html", form=form, wrong = False)

@app.route("/logout")
def logout():
    disconnected()
    return render_template("home.html")

@app.route("/showReclamations")
def showReclamations():
    cursor.execute(selectRequest)
    if connectionStatus():
        return render_template("showReclamations.html",reclamations = cursor, deleted = False)
    else:
        return render_template("home.html",reclamations = cursor, deleted = False)


@app.route("/deleteReclamation/<id>")
def deleteReclamation(id):
    cursor.execute(deleteRequest,(str(id),))
    db.commit()
    cursor.execute(selectRequest)
    return render_template("showReclamations.html", reclamations = cursor, deleted = True)

#Main execution program
if __name__ == "__main__":
    app.run(debug=True)