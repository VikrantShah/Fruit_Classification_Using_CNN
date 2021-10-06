import os

from flask import Flask, request, render_template, send_from_directory

app = Flask(__name__)
# Flask(__name__) : Used to set some path behind the scenes

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

classes = ["Fresh Apple", "Fresh Banana", "Fresh Orange", "Rotten Apple", "Rotten Banana", "Rotten Orange"]

@app.route("/")
def index() :
    return render_template("index.html")

@app.route("/upload", methods = ["POST"])
def upload() :
    target = os.path.join(APP_ROOT, "images/")
    print(target)
    
    if not os.path.isdir(target) :
        os.mkdir(target)
    else :
        print("Couldn't create upload directory :", target)
        
    print(request.files.getlist("file"))
    # Upload multiple files
    
    for upload in request.files.getlist("file") :
        print(upload)
        print(upload.filename, "is the file name")
        
        filename = upload.filename
        destination = "/".join([target, filename])
        
        print("Accept Incoming File :", filename)
        print("Save it to :", destination)
        
        upload.save(destination)
        
        import numpy as np
        from keras.preprocessing import image
        from keras.models import load_model
        
        model = load_model("model.h5")
        model.summary()
        
        test_image = image.load_img("images\\" + filename, target_size = (64, 64))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)
        
        result = model.predict(test_image)
        res = result[0]
        
        for i in range(6) :
            if res[i] == 1. :
                break;
        
        prediction = classes[i]
        
        return render_template("template.html", image_name = filename, text = prediction)

@app.route("/apload/<filename>")
def send_image(filename) :
    return send_from_directory("images", filename)

if __name__ == "__main__" :
    app.run(debug = False)