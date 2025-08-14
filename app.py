
import os
from flask import Flask,render_template,redirect,request 
from supabase import create_client, Client 
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__) 

app.config['SUPABASE_URL'] = os.getenv('SUPABASE_URL')
app.config['SUPABASE_SECRET'] = os.getenv('SUPABASE_SECRET')

url = app.config['SUPABASE_URL']
key = app.config['SUPABASE_SECRET']
supabase: Client = create_client(url, key) 


# student routes
@app.route('/') 
def index(): 
    data = supabase.table('students').select('*').execute() 
    students = data.data 
    return render_template("index.html", students=students) 
 
@app.route('/add_student', methods=['POST']) 
def add_student(): 
    name = request.form['name'] 
    faculty = request.form['faculty'] 
    supabase.table('students').insert({ 
'name': name,  
'faculty': faculty 
}).execute() 
    return redirect('/') 
 
@app.route('/delete_student/<int:id>') 
def delete_student(id): 
    supabase.table('students').delete().eq('id', id).execute() 
    return redirect('/') 
 
@app.route('/get_student/<int:id>',methods=['GET']) 
def get_student(id): 
    student = supabase.table('students').select('*').eq('id',id).single().execute().data 
    return render_template("edit.html", student=student) 
 
@app.route('/update_student/<int:id>', methods=['POST']) 
def update_student(id): 
    name = request.form['name'] 
    faculty = request.form['faculty'] 
    supabase.table('students').update({ 
        'name': name, 
        'faculty': faculty 
    }).eq('id', id).execute() 
    return redirect('/') 


if __name__ == "__main__": 
    app.run(debug=True) 