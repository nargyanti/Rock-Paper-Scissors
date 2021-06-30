from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
import numpy as np
import os 
from PIL import Image
import random
  
try:
    import shutil
    shutil.rmtree('static/uploads')
    os.chdir('static')
    os.mkdir('uploads')
    os.chdir('..')
    print()
except:
    pass
  
model = tf.keras.models.load_model('model')
app = Flask(__name__)
Bootstrap(app)
  
app.config['UPLOAD_FOLDER'] = 'static/uploads'
  
@app.route('/')
def upload_f():
    return render_template('index.html')
  
def finds():
    test_datagen = ImageDataGenerator(
            rescale = 1./255,
            rotation_range = 20,
            # vertical_flip = True,
            horizontal_flip = True,
            shear_range = 0.2,
            fill_mode = 'nearest',
            validation_split = 0.4)
    vals = ['Paper', 'Rock', 'Scissors'] # change this according to what you've trained your model to do
    test_dir = 'static'
    test_generator = test_datagen.flow_from_directory(
            test_dir,            
            target_size = (150, 150), 
            batch_size = 1,
            color_mode ='rgb',
            class_mode = 'categorical')

    pred = model.predict(test_generator)
    print(pred)
    
    player = str(vals[np.argmax(pred)])
    bot = random.choice(vals)
    
    winorlose = "empty"
    winner = "empty"

    if player == bot:
        winorlose = "Both players selected " + player + ". It's a tie!"
        winner = 'player'
    elif player == "Rock":
        if bot == "Scissors":
            winorlose = "Rock smashes scissors! You win!"            
            winner = 'player'
        else:
            winorlose = "Paper covers rock! You lose."
            winner = 'bot'
    elif player == "Paper":
        if bot == "Rock":
            winorlose = "Paper covers rock! You win!"
            winner = 'player'
        else:
            winorlose = "Scissors cuts paper! You lose."
            winner = 'bot'
    elif player == "Scissors":
        if bot == "Paper":
            winorlose = "Scissors cuts paper! You win!"
            winner = 'player'
        else:
            winorlose = "Rock smashes scissors! You lose."
            winner = 'bot'
    
    result = [str(vals[np.argmax(pred)]), bot, winorlose, winner]
    # return str(vals[np.argmax(pred)])
    return result
  
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        shutil.rmtree('static/uploads')
        os.chdir('static')
        os.mkdir('uploads')
        os.chdir('..')        
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        val = finds()
        return render_template('result.html', player = val[0], bot = val[1], winorlose = val[2], winner = val[3], filename = secure_filename(f.filename))

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == '__main__':
    app.run()    