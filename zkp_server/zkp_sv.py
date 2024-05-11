from flask import render_template
import connexion
import uvicorn

app = connexion.App(__name__, specification_dir="./")
app.add_api("zkp_key.yml")

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    uvicorn.run(app, port=8000)