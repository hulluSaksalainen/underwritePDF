""" für tonys unterschriften"""
import os
from flask import Flask, request, render_template, send_file
import fitz  # PyMuPDF
# from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    """ hol sich halt alle daten"""
    if request.method == "POST":
        # Eingaben holen
        ort = request.form["ort"]
        datum = request.form["datum"]
        margin_left = int(request.form["margin_left"])
        margin_right = int(request.form["margin_right"])
        margin_bottom = int(request.form["margin_bottom"])
        layout = request.form["layout"]

        # Dateien holen
        pdf_file = request.files["pdf"]
        img_file = request.files["image"]

        # Temporäre Pfade
        pdf_path = os.path.join(UPLOAD_FOLDER, "input.pdf")
        img_path = os.path.join(UPLOAD_FOLDER, "sig.png")
        output_path = os.path.join(UPLOAD_FOLDER, "output.pdf")

        pdf_file.save(pdf_path)
        img_file.save(img_path)

        # PDF bearbeiten
        doc = fitz.open(pdf_path)
        for page in doc:
            width, height = page.rect.width, page.rect.height
            if layout == "landscape" and width < height:
                page.set_rotation(90)
                width, height = height, width

            # Text links unten
            text = f"{ort}, {datum}"
            page.insert_text(
                fitz.Point(margin_left, height - margin_bottom),
                text,
                fontsize=11,
                fontname="helv",
                color=(0, 0, 0),
            )

            # Bild rechts unten
            img_rect = fitz.Rect(
                width - margin_right - 100,  # X0
                height - margin_bottom - 40,  # Y0
                width - margin_right,  # X1
                height - margin_bottom,  # Y1
            )
            page.insert_image(img_rect, filename=img_path)

        doc.save(output_path)
        doc.close()

        return send_file(output_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
