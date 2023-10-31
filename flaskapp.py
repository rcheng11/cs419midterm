from flask import Flask, request, make_response, render_template
import database
import random

# create an instance of a Flask app
# set template folder location to current directory
app = Flask(__name__, template_folder='.')

# valid_ids
valid_ids = database.get_ids()

# create an app route for the index
@app.route("/")
def index():
    return render_template("index.html", num_ids=len(valid_ids))

# search route
@app.route("/searchresults")
def search():
    obj_id = random.choice(valid_ids)
    try:
        results = database.query_details(str(obj_id))
        # modify results:
        html = f"<img style='max-height=240px; width: auto' src='https://media.collections.yale.edu/thumbnail/yuag/obj/{results[0][0]}' alt='{str(results[0][0]) + ', ' + str(results[0][2])}'>"
        html += f"<p id='obj-id'>Object Id: {results[0][0]}</p>"
        html += f"<p id='label'>Label: {results[0][1]}</p>"
        html += f"<p id='date'>Date: {results[0][2]}</p>"
        html += "<h2>Agents Involved</h2>"
        if len(results[0][3]) > 0:
            html += f"<ul>"
            for agent in results[0][3].split(","):
                html += f"<li>{agent}</li>"
            html += "</ul>"
        else:
            html += "<p>None listed in the database</p>"
        return make_response(html)
    except Exception as err:
        return make_response(str(err))