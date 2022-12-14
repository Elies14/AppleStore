from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from AppStoreCrawler import AppStoreCrawler

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///apps.db"
db.init_app(app)

from models import *

with app.app_context():
    db.create_all()


@app.route('/', defaults={'n': 100})
@app.route('/<int:n>')
def show_all(n):
    """
    Show n top App Store apps and all its data
    """
    process_top_apps(n)
    return render_template('show_all.html',
                           apps=Application.query.order_by(Application.created_date).limit(n).all(), n=n)


@app.route('/<int:n>/json')
def get_apps_to_json(n):
    process_top_apps(n)
    data = [{k: v for k, v in application.__dict__.items() if k != '_sa_instance_state'}
            for application in Application.query.order_by(Application.created_date).all()]
    return jsonify(data)


def process_top_apps(n: int):
    crawler = AppStoreCrawler()
    top_apps = crawler.get_top_apps(n=n)
    for i, (app_id, app_name) in enumerate(top_apps):
        print(f'Processing App {i + 1}, {app_name} - id : {app_id}')
        data = {'id': app_id, 'name': app_name}
        crawler.navigate_to_page(data)
        crawler.get_data_from_url(data)
        application = Application()
        application.__dict__.update(data)
        db.session.add(application)


