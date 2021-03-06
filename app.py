from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

from trips import get_flights

app = Flask(__name__)


def bad_arguments(cause):
    return 'Sorry, bad city set... Go back and try again, please!\nPossible fault: {}.'.format(cause)


def get_static_path(filename):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)),
                        'static', filename)


@app.route('/cities', methods=('GET', 'POST'))
def cities():
    with open(get_static_path('city_suggest.json')) as fin:
    	return jsonify(json.load(fin))


@app.route('/', methods=('GET', 'POST'))
def main():
    if request.method == 'POST':
        cities = []
        for key, values in request.form.lists():
            if key == 'city[]':
                cities = list(values)
        return redirect(url_for('render_map', cities='+'.join(cities)))
    return render_template('index.html')


@app.route('/<path:cities>')
def render_map(cities):
    cities = cities.split('+')
    if len(cities) < 2:
        return bad_arguments('are you travelling alone? You should add more than 1 city')
    if len(cities) > 5:
        date, destination, flights = get_flights(cities, hackupc=True)
        return render_template('map_upc.html',
                           found=True,
                           flights=flights,
                           date=date,
                           cost=0,
                           flights_num=len(flights),
                           destination=destination)

    date, destination, flights = get_flights(cities)
    cost = 0
    for flight in flights:
        cost += flight['cost']
    found = date is not None and destination is not None and len(flights) == len(cities)
    return render_template('map.html',
                           found=found,
                           flights=flights,
                           date=date,
                           cost=cost,
                           flights_num=len(flights),
                           destination=destination)


if __name__ == '__main__':
    app.run()
