import flask 
import smtplib
import config
from transcribe import transcription
from werkzeug.utils import secure_filename
import os
import base64
from PIL import Image
from io import BytesIO
import canny
import threshold_segmentation
import sudoku_solver
import summarization

app = flask.Flask(__name__)
transcript = []
summary = {}
board = 0

@app.route('/')
def home():
    return flask.render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email():
   data = flask.request.form

   smtp_server = smtplib.SMTP('smtp.mail.me.com', 587)

   # using port 587 so need to enable TLS encryption
   smtp_server.starttls()
   smtp_server.login(config.EMAIL, config.PWD)

   e_mail = 'From: ' + str(config.EMAIL) + '\nTo: ' + str(config.EMAIL) + '\nSubject: Contact Notification from Website\n' + str(data['name']) + ' has contacted you. Reply back at ' + str(data['email']) + '. Message: ' + str(data['message'])

   success = smtp_server.sendmail(from_addr=config.EMAIL, to_addrs=config.EMAIL, msg=e_mail)

   # destory connection
   smtp_server.quit()

   print(success)

   if success != {}:
      return flask.jsonify('ERROR')
   else:
      return flask.jsonify('OK')


@app.route('/get_summary', methods = ['POST'])
def get_summary():
   global summary

   # get file 
   data = flask.request.files['text']

   # check for proper extension
   extension = data.filename.split('.')[-1]

   if extension != 'txt' :
      summary['ERROR'] = ['Please upload a txt file.']
   else:
      filename = secure_filename(data.filename)
      data.save(filename)

      extractive, abstractive = summarization.generate_summaries(filename)

      if type(extractive) == int:
         summary['ERROR'] = abstractive

      else:
         summary['Extractive'] = extractive
         summary['Abstractive'] = abstractive
   
   return flask.redirect('/summarize', 302)

@app.route('/summarize')
def summarize():
   return flask.render_template('summarization.html', data=summary)


@app.route('/get_audio', methods = ['POST'])
def get_audio():

   global transcript 

   audio_extensions = ['mp3', 'wav']

   # get file 
   data = flask.request.files['audio']

   # check for proper extension
   extension = data.filename.split('.')[-1]

   if extension not in audio_extensions :
      transcript = ['Please enter a wav or mp3 file.']

   else:
      filename = secure_filename(data.filename)
      data.save(filename)
      transcript = transcription(filename)

   return flask.redirect('/transcribe', 302)

@app.route('/transcribe')
def transcribe():
   return flask.render_template('transcription.html', data=transcript)


@app.route('/formData', methods=['POST'])
def formData():

   # get form data in dictionary
   # index with url key
   url = flask.request.form['url']

   # make youtube-dl command
   command = 'python3 yt_dlp/__main__.py -x --audio-format "mp3" --audio-quality 0 ' + url
   os.system(command)

   # get file
   files = os.listdir()
   audio = None
   for f in files:
      if f[-4:] == '.mp3':
         audio = f

   return flask.send_file(audio, mimetype='audio/mpeg', as_attachment=True)

@app.route('/youtube-dl')
def youtube_dl():
   return flask.render_template('youtube_dl.html')


@app.route('/computer-vision')
def computer_vision():
   return flask.render_template('computer_vision.html')


# edge detection
@app.route('/edges', methods = ['POST'])
def edge_detection():

   # receive file and save
   img = flask.request.get_data()
   save_file(img)
   
   # run edge detection
   canny.edge_detector()

   # load image
   img = encode()
   
   return flask.json.dumps(img)


@app.route('/segments', methods = ['POST'])
def image_segmentation():

   # receive file and save
   img = flask.request.get_data()
   save_file(img)

   # run image segmentation
   threshold_segmentation.image_segmentation()

   # load image
   img = encode()

   return flask.json.dumps(img)


# convert image to base64 to send with ajax
def encode():
   # encode image in base64 to send to client
   with open('output.jpg', 'rb') as image:
      encoding = base64.b64encode(image.read())
   encoding = encoding.decode('utf-8')

   return encoding


# save image uploaded from client
def save_file(data):
   # convert byte data back to image
   im = Image.open(BytesIO(base64.b64decode(data)))

   # save image
   im.save('uploaded_file.jpg', 'JPEG')

   return


# render html
@app.route('/sudoku')
def sudoku():
   return flask.render_template('sudoku.html')


@app.route('/backtrack', methods=['POST'])
def backtrack():

   # print(board)
   global board 
   board = None
   board = sudoku_solver.get_board()

   return jsonify(board)


@app.route('/solve', methods=['POST'])
def solve():
   states = sudoku_solver.solver_wrapper(board)

   jsons = {}
   count = 1

   for state in states:
      jsons[count] = jsonify(state)
      count += 1

   return jsons

def jsonify(b):
   data = {}
   count = 1

   for r in range(9):
      for c in range(9):
         data[count] = b[r][c]
         count += 1

   return data


@app.route('/shortest_route')
def shortest_route():
   return flask.render_template('distance.html')

@app.route('/matrix')
def matrix():
   return flask.render_template('matrix.html')

@app.route('/download_resume', methods=['POST'])
def download_resume():
   return flask.send_file('resume/resume.pdf', as_attachment=True)

if __name__ == '__main__':
   # app.run(host ='0.0.0.0', port = 5000, debug = True) 
   app.run(host ='0.0.0.0', port = int(os.getenv('PORT', 5000))) 