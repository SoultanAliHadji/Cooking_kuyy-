import pickle
import os
import numpy as np
from flask import Flask, render_template, request, redirect, url_for
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.preprocessing import image
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

#part of fungsi 1
size_ = 32

model = Sequential()

model.add(Conv2D(128, (3, 3), input_shape = (size_, size_, 3), activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2, 2)))
model.add(Conv2D(64, (3, 3), activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2, 2)))
model.add(Conv2D(32, (3, 3), activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2, 2)))
model.add(Flatten())

model.add(Dense(units = 10000, activation = 'relu'))
model.add(Dense(units = 100, activation = 'relu'))
model.add(Dense(units = 3, activation = 'softmax'))

model.compile(optimizer = 'sgd', loss = 'categorical_crossentropy', metrics = ['categorical_accuracy'])
model.load_weights('static/otak1.h5')

UPLOAD_FOLDER = 'static/upload'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

nama_train_data = {
    0: 'ayam',
    1: 'ikan', 
    2: 'sapi'
}
#end of part 1

#part of fungsi 2 & 3
file3 = open('static/otak3.pickle', 'rb')
otak3 = pickle.load(file3)
file3.close()

neigh_ayam = otak3[0]
neigh_sapi = otak3[1]
neigh_ikan = otak3[2]

listMakanan = {
    0 : 'ayam saus tiram',
    1 : 'ayam bumbu kuning',
    2 : 'ikan kembung acar kuning',
    3 : 'ikan goreng sambal matah',
    4 : 'semur daging kecap',
    5 : 'rendang',
}
#end of part 2 & 3

#basic config
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#end of config

#fungsi 1
@app.route('/uploadImg', methods=['POST'])
def upload_file():
    if 'fileImg' not in request.files:
        return 'there is no fileImg in form!'
    fileImg = request.files['fileImg']
    path = os.path.join(app.config['UPLOAD_FOLDER'], fileImg.filename)
    fileImg.save(path)
    img = image.load_img('static/upload/' + fileImg.filename, target_size = (size_, size_))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis = 0)

    hasil = model.predict_classes(img)
    hasil = nama_train_data[hasil[0]]
    
    if hasil == "ayam":
        return redirect(url_for("ayam"))
    elif hasil == "ikan":
        return redirect(url_for("ikan"))
    else:
        return redirect(url_for("sapi"))
#end of fungsi 1

#fungsi 2
@app.route('/output', methods=['POST'])
def output():
    kolom = ['ayam', 'ikan', 'sapi', 'bawang putih', 'bawang merah', 'bawang bombay',
       'cabai', 'jahe', 'lada', 'kecap', 'garam', 'gula', 'santan', 'lengkuas',
       'kunyit']
       
    hasil = []

    makanan = request.form.getlist('data')
    print(makanan)
    for i in kolom:
        hasil.append((i in makanan)*1)

    if "ayam" in makanan:
        makanan = listMakanan[neigh_ayam.predict([hasil])[0]]
    elif "ikan" in makanan:
        makanan = listMakanan[neigh_ikan.predict([hasil])[0]]
    else:
        makanan = listMakanan[neigh_sapi.predict([hasil])[0]]

    if makanan == "ayam saus tiram":
        return redirect(url_for("ayamsaustiram"))
    elif makanan == "ayam bumbu kuning":
        return redirect(url_for("ayambumbukuning"))
    elif makanan == "ikan kembung acar kuning":
        return redirect(url_for("ikankembungacarkuning"))
    elif makanan == "ikan goreng sambal matah":
        return redirect(url_for("ikangorengsambalmatah"))
    elif makanan == "semur daging kecap":
        return redirect(url_for("semurdagingkecap"))
    else:
        return redirect(url_for("rendang"))
#end of fungsi 2

#fungsi 3
@app.route('/submit', methods=['POST'])
def submit():
    kolom = ['ayam', 'ikan', 'sapi', 'bawang putih', 'bawang merah', 'bawang bombay',
       'cabai', 'jahe', 'lada', 'kecap', 'garam', 'gula', 'santan', 'lengkuas',
       'kunyit']

    kata = request.form['inputan']
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    katadasar = stemmer.stem(kata)
    katadasar.split(" ")
    print(katadasar)
    
    hasil = []
    for i in kolom:  
        hasil.append((i in katadasar)*1)
    print(listMakanan[neigh_ayam.predict([hasil])[0]])

    if "ayam" in katadasar:
        makanan = listMakanan[neigh_ayam.predict([hasil])[0]]
    elif "ikan" in katadasar:
        makanan = listMakanan[neigh_ikan.predict([hasil])[0]]
    else:
        makanan = listMakanan[neigh_sapi.predict([hasil])[0]]

    if makanan == "ayam saus tiram":
        return redirect(url_for("ayamsaustiram"))
    elif makanan == "ayam bumbu kuning":
        return redirect(url_for("ayambumbukuning"))
    elif makanan == "ikan kembung acar kuning":
        return redirect(url_for("ikankembungacarkuning"))
    elif makanan == "ikan goreng sambal matah":
        return redirect(url_for("ikangorengsambalmatah"))
    elif makanan == "semur daging kecap":
        return redirect(url_for("semurdagingkecap"))
    else:
        return redirect(url_for("rendang"))
#end of fungsi 3

#basic routing
@app.route('/')
def home():
    return render_template('index.html')
                    
if __name__ == '__main__':
    app.run(host='127.0.0.1',port='5000', debug=True)

@app.route('/tentang')
def tentang():
    return render_template('tentang.html')

@app.route('/kontak')
def kontak():
    return render_template('kontak.html')

@app.route('/ayam')
def ayam():
    return render_template('ayam.html')

@app.route('/sapi')
def sapi():
    return render_template('sapi.html')

@app.route('/ikan')
def ikan():
    return render_template('ikan.html')

@app.route('/ayambumbukuning')
def ayambumbukuning():
    return render_template('ayambumbukuning.html')

@app.route('/ayamsaustiram')
def ayamsaustiram():
    return render_template('ayamsaustiram.html')

@app.route('/ikangorengsambalmatah')
def ikangorengsambalmatah():
    return render_template('ikangorengsambalmatah.html')

@app.route('/ikankembungacarkuning')
def ikankembungacarkuning():
    return render_template('ikankembungacarkuning.html')

@app.route('/semurdagingkecap')
def semurdagingkecap():
    return render_template('semurdagingkecap.html')

@app.route('/rendang')
def rendang():
    return render_template('rendang.html')
#end of routing