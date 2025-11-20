import sys
sys.path.insert(0,"db/")
from db.dbhelper import *

from flask import Flask,render_template,request,redirect,url_for

upload_folder = "static/images"
app = Flask(__name__)
app.config['UPLOAD_FOLDER']= upload_folder

@app.route("/savestudent", methods=['POST','GET'])
def savestudent()->None:
    if request.method=="POST":
        file:any = request.files['webcam']
        idno:str = request.args.get('idno')
        lastname:str = request.args.get('lastname')
        firstname:str = request.args.get('firstname')
        course:str = request.args.get('course')
        level:str = request.args.get('level')
        #
        filename:str = upload_folder+"/"+str(lastname).strip()+".jpeg"
        file.save(filename)
        
        
        ok:bool = addrecord('students', idno=idno,lastname=lastname,firstname=firstname,course=course,level=level,image=filename)
        
        message:str = "Student Information Saved" if ok else "Error Saving Student"
        print(message)
    
    return redirect(url_for('index'))

@app.route("/")
def index()->None:
    return render_template("index.html")
    
if __name__=="__main__":
    app.run(debug=True)
   