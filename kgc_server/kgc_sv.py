# app.py

from flask import render_template
import connexion


app = connexion.App(__name__, specification_dir="./")
app.add_api("key.yml")

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=7000)