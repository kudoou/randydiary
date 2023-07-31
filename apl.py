import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dairy', methods=['GET'])
def show_dairy():
    # sample_receive = request.args.get('sample_give')
    #  Kita perlu mengambil seluruh data title dan content dari database sebagai sebuah list 
    # Kita harus mengirimkan list datanya ke client
    articles =list(db.diary.find({},{'_id' : False}))
    return jsonify({'articles' : articles})

@app.route('/dairy', methods=['POST'])
def save_dairy():
    # sample_receive = request.form.get('sample_give')
    # print(sample_receive)
    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')
    # Menerima file
    today =datetime.now()
    mytime = today.strftime('%Y-%M-%d-%H-%M-%S')

    file = request.files["file_give"]
    # # Selanjutnya, mari buat nama file baru menggunakan function datetime
    extension = file.filename.split('.')[-1] #untuk memisahkan tanda titik .jpg
    filename = f'file-{mytime}.{extension}'
    # # Mari gunakan nama file baru tersebut dan ekstensi file original lalu save file nya
    save_to =f'static/{filename}'
    file.save(save_to)

    # server profile
    profile = request.files["profile_give"]
    # extension = profile.profilename.split('.')[-1]
    profilename = f'profile-{mytime}.{extension}'
    save_on = f'static/{profilename}'
    profile.save(save_on)
    
    time = today.strftime('%Y-%M-%d')

    doc = {
        'file' : filename,
        'profile' : profilename,
        'title' : title_receive,
        'content' : content_receive,
        'time' : time
    }
    db.diary.insert_one(doc)
    return jsonify({'msg' : 'POST, was saved'});


if __name__ == '__main__' :
    app.run('0.0.0.0',port=5000, debug=True)