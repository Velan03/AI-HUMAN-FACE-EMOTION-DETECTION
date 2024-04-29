# Let us import the Libraries required.
import os
import numpy as np
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, flash
from Graphical_Visualisation import Emotion_Analysis

# Let us Instantiate the app
app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




def allowed_file(filename):
    """ Checks the file format when file is uploaded"""
    return ('.' in filename and
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)



def mood(result):
    if result=="Happy":
        return 'Since you are happy, lets keep up the good mood with some amazing music!'
    elif result=="Sad":
        return 'It seems that you are having a bad day, lets cheer you up with some amazing music!'
    elif result=="Disgust":
        return 'It seems something has got you feeling disgusted. Lets improve your mood with some great music!'
    elif result=="Neutral":
         return 'It seems like a normal day. Lets turn it into a great one with some amazing music!'
    elif result=="Fear":
        return 'You seem very scared. We are sure that some music will help!'
    elif result=="Angry":
        return 'You seem angry. Listening to some music will surely help you calm down!'
    elif result=="Surprise":
        return 'You seem surprised! Hopefully its some good news. Lets celebrate it with some great music!'


def provide_url(result):
    if result=="Happy":
        return 'https://open.spotify.com/playlist/1BVPSd4dynzdlIWehjvkPj'
    elif result=="Sad":
        return 'https://www.writediary.com/ '
    elif result=="Disgust":
        return 'https://open.spotify.com'
    elif result=="Neutral":
         return 'https://www.netflix.com/'
    elif result=="Fear":
        return 'https://www.youtube.com/watch?v=KWt2-lUpg-E'
    elif result=="Angry":
        return 'https://www.onlinemeditation.org/'
    elif result=="Surprise":
        return 'https://www.google.com/search?q=hotels+near+me&oq=hotels+&aqs=chrome.1.69i57j0i433i457j0i402l2j0i433l4j0l2.3606j0j7&sourceid=chrome&ie=UTF-8'


def activities(result):

    if result == "Happy":
        return '• Try out some dance moves'
    
    elif result == "Sad":
        return '• Write in a journal'

    elif result == "Disgust":
        return '• Listen soothing music'

    elif result == "Neutral":
        return '• Watch your favourite movie'

    elif result == "Fear":
        return '• Get a good sleep'

    elif result == "Angry":
        return '• Do meditation'


    elif result == "Surprise":
        return '• Give yourself a treat' 


@app.route('/')
def Start():
    return render_template('Start.html')


@app.route('/ManualUpload', methods=['POST'])
def ManualUpload():
    return render_template('ManualUpload.html')


@app.route('/uploadimage', methods=['POST'])
def uploadimage():
    """ Loads Image from System, does Emotion Analysis & renders."""

    if request.method == 'POST':

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # If user uploads the correct Image File
        if file and allowed_file(file.filename):

            # Pass it a filename and it will return a secure version of it.
            # The filename returned is an ASCII only string for maximum portability.
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            result = Emotion_Analysis(filename)

            # When Classifier could not detect any Face.
            if len(result) == 1:

                return render_template('NoDetection.html', orig=result[0])

            sentence = mood(result[3])
            activity = activities(result[3])
            link = provide_url(result[3])
            return render_template('Visual.html', orig=result[0], pred=result[1], bar=result[2], music=result[3],
                                   sentence=sentence, activity=activity, image=result[3], link=link)


if __name__ == '__main__':
    app.run(debug=False)
