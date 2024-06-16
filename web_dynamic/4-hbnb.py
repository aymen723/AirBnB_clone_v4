#!/usr/bin/python3
"""
Flask App that integrates with AirBnB static HTML Template
"""
import uuid
from flask import Flask, render_template, url_for
from models import storage

# flask setup
app = Flask(__name__)
app.url_map.strict_slashes = False
p = 5000
h = '0.0.0.0'


# begin flask page rendering
@app.teardown_appcontext
def teardown_db(exception):
    """
    call this function after this request
    """
    storage.close()


@app.route('/4-hbnb/')
def hbnb_filters(the_id=None):
    """
    handles request 
    """
    sobjs = storage.all('State').values()
    s = dict([state.name, state] for state in sobjs)
    a = storage.all('Amenity').values()
    p = storage.all('Place').values()
    u = dict([user.id, "{} {}".format(user.first_name, user.last_name)]
                 for user in storage.all('User').values())
    c = (str(uuid.uuid4()))
    return render_template('4-hbnb.html',
                           states=s,
                           amens=a,
                           places=p,
                           users=u,
                           cache_id=c)


if __name__ == "__main__":
    """
    MAIN"""
    app.run(host=h, port=p)
