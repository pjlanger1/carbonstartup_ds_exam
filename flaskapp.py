from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('foo.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/predict', methods = ['GET'])
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT reporting_period, TYPE, AVG(mean_fuel_consumption_kg_m) AS AVG_FUEL_CONSUMP, COUNT(imo_number) as vessel_count from carbon_reporting WHERE method_b == "Yes" GROUP BY reporting_period, TYPE ORDER BY AVG_FUEL_CONSUMP').fetchall()
    conn.close()
    lst = {'reporting_period':[],'type':[],'avg_fuel_consum':[],'n_ships':[]}
    for p in posts:
        lst['reporting_period'].append(p[0])
        lst['type'].append(p[1])
        lst['avg_fuel_consum'].append(p[2])
        lst['n_ships'].append(p[3])
    return jsonify(lst)

##Now running on port
def main():
    app.run(port=5003)

main()