import sys
sys.path.insert(0,"db/")
from db.dbhelper import *

from flask import Flask,render_template,request,redirect,url_for,jsonify

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
    
    return redirect(url_for('mainindex'))

@app.route("/")
def mainindex():
    students = getall('students')
    return render_template("mainindex.html", students=students)

@app.route("/add")
def add():
    return render_template("index.html")

@app.route("/getstudent/<idno>")
def getstudent(idno):
    student_list = getrecord('students', idno=idno)
    if student_list and len(student_list) > 0:
        student = student_list[0]
        return jsonify({
            'idno': student['idno'],
            'lastname': student['lastname'],
            'firstname': student['firstname'],
            'course': student['course'],
            'level': student['level'],
            'image': student['image']
        })
    return jsonify({'error': 'Student not found'}), 404

@app.route("/deletestudent/<idno>", methods=['POST'])
def deletestudent(idno):
    ok = deleterecord('students', idno=idno)
    if ok:
        return jsonify({'success': True, 'message': 'Student deleted successfully'})
    return jsonify({'success': False, 'message': 'Error deleting student'}), 500
    
if __name__=="__main__":
    app.run(debug=True)
