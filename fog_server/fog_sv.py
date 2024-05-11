from flask import render_template
import config
from models import MData
import uvicorn

app = config.connex_app
app.add_api(config.basedir / "swagger.yml")


@app.route('/')
def home():
    data = MData.query.all()
    return render_template("home.html", data=data)

if __name__ == '__main__':
    uvicorn.run(app, port=8000)