import os
from flask import Flask, flash, request, redirect, url_for, render_template, redirect
from werkzeug.utils import secure_filename
from procesImage import test_image
app = Flask(__name__)

UPLOAD_FOLDER = "/Users/SamuelYeboah/Desktop/Digital Image Processing/Project/BackEnd/static/uploads"
ALLOWED_EXTENSIONS = set(['png','jpg','jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('home.html')

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/" , methods=['POST'])
def upload_picture():
    if request.method == 'POST':
        if 'image' not in request.files:
            return render_template('home.html')
        image = request.files['image']
        if image.filename == '':
            return render_template('home.html')
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            imagePath = '/uploads/' + str(filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            #Save image and begin SIFT algo
            return redirect(url_for('rate_parking', imagePath = imagePath))
    else:
        render_template('home.html')


@app.route("/rate_parking/<path:imagePath>" , methods=['GET' , 'POST'])
def rate_parking(imagePath):
    if request.method == 'POST':
        if 'submit' in request.form:
            rating = request.form['submit']
            #Save the rating and return a page that shows whether your lime was parked correctly
            return redirect(url_for('verification_results', imagePath = imagePath))
        return render_template('rate_parking.html' , imagePath = imagePath) 
    else:
        return render_template('rate_parking.html' , imagePath = imagePath) 

@app.route("/verification_results/<path:imagePath>" , methods=['GET' ,'POST'])
def verification_results(imagePath):
    #check to see if algorithim is done
    #
    #
    result = test_image(imagePath)
    print(result)
    if request.method == 'POST':
        print(request)
        if 'submit' in request.form:
            rating = request.form['submit'].lower()
            print(rating)
            if rating == 'yes':
                return redirect(url_for('home'))
            else:
                noMoreVerification = True
                return render_template('verified_parking.html', imagePath=imagePath, done = noMoreVerification)
        return render_template('verified_parking.html', imagePath=imagePath)
    else:    
        return render_template('verified_parking.html', imagePath=imagePath, results=result)
    return render_template('verified_parking.html', imagePath=imagePath)
    