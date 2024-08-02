#Import necessary libraries
from flask import Flask, render_template, request
 
import numpy as np
import os
 
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model

model = load_model('model.h5')

def pred_cot_dieas(cott_plant):
    test_image = load_img(cott_plant, target_size = (224, 224)) # load image 
    print("@@ Got Image for prediction")      

    test_image = img_to_array(test_image)/255 # convert image to np array and normalize
    test_image = np.expand_dims(test_image, axis = 0) # change dimention 3D to 4D
        
    result = model.predict(test_image).round(3) # predict diseased palnt or not
    print('@@ Raw result = ', result)
        
    pred = np.argmax(result) # get the index of max value
    
    if pred == 0:
        return "Epidural Haemorrhage", '1.html' 
        
    elif pred == 1:
        return 'Intracranial Haemorrhage', '2.html' 

    elif pred == 2:
        return 'Intraparenchymal Haemorrhage', '3.html'
        
    elif pred == 3:
        return 'Subarachnoid Haemorrhage', '4.html'
        
    elif pred == 4:
        return 'Subdural Haemorrhage', '5.html'  

        
    else:
        return "Invaild Image", 'index.html' # if index 3


app = Flask(__name__)

 
# render index.html page
@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index1.html')
     

# render index.html page
@app.route("/index1", methods=['GET', 'POST'])
def index1():
    return render_template('index1.html')
  
# get input image from client then predict class and render respective .html page for solution
@app.route("/predict", methods = ['GET','POST'])
def predict():
    if request.method == 'POST':
        file = request.files['image'] # fet input
        filename = file.filename        
        print("@@ Input posted = ", filename)
         
        file_path = os.path.join('static/user uploaded', filename)
        file.save(file_path)
 
        print("@@ Predicting class......")
        pred, output_page = pred_cot_dieas(cott_plant=file_path)
               
        return render_template(output_page, pred_output = pred, user_image = file_path)


# For local system &amp; cloud
if __name__ == "__main__":
    app.run(debug=True,threaded=False) 
