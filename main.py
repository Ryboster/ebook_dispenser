from flask import Flask, request, render_template, send_from_directory, redirect, url_for
import os
from pdf2image import convert_from_path


PORT = 10000
HOST = "0.0.0.0"
EBOOKS_DIR = os.path.join(os.getcwd(), "media", "ebooks")
THUMBNAILS_DIR = os.path.join(os.getcwd(), "media", "tmp")
ALLOWED_EXTENSIONS = ["pdf"]


app = Flask("Developer Portfolio", static_folder="static")
app.config['MEDIA_FOLDER'] = os.path.join(os.getcwd(), "media")


def clear_thumbnails():
    for filename in os.listdir(THUMBNAILS_DIR):
        os.remove(os.path.join(THUMBNAILS_DIR, filename))
        
def create_thumbnails():
    ebooks = os.listdir(EBOOKS_DIR)
    for i in enumerate(ebooks, start=0):
        image = convert_from_path(os.path.join(EBOOKS_DIR, ebooks[i[0]]), first_page=1, last_page=1)
        thumbnail_name = ebooks[i[0]].replace('.pdf', '')
        image[0].save(os.path.join(THUMBNAILS_DIR, f"{thumbnail_name}.jpg"), "JPEG")

def get_all_ebooks():
    ebooks = {}
    filenames = os.listdir(EBOOKS_DIR)
    for i in enumerate(filenames, start=0):
        title = i[1].replace('.pdf', '')
        ebooks[i[0]] = {}
        ebooks[i[0]]["title"] = title
        ebooks[i[0]]["thumbnail"] = title + ".jpg"
    return ebooks

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def catalogue():
    if request.method == "GET":
        return render_template("catalogue.html", catalogue=get_all_ebooks())
    else:
        if request.form["_method"] == "POST":
            file = request.files["ebookFile"]
            if allowed_file(file.filename):
                file.save(os.path.join(EBOOKS_DIR, file.filename))
                clear_thumbnails()
                create_thumbnails()
                return redirect(url_for("catalogue"))
            else:
                return "Unsupported type", 400;
        elif request.form["_method"] == "DELETE":
            os.remove(os.path.join(EBOOKS_DIR, request.form['title'] + ".pdf"))
            clear_thumbnails()
            create_thumbnails()
            return redirect(url_for("catalogue"))
    
    
@app.route("/media/<path:filename>")
def media(filename):
    return send_from_directory(app.config["MEDIA_FOLDER"], filename)

    
if __name__ == "__main__":
    clear_thumbnails()
    create_thumbnails()
    
    app.run(host=HOST, port=PORT)