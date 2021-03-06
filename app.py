import datetime
import os
import psycopg2

from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

@app.route("/", methods=('GET', 'POST'))
def index():
    # Connect to database
    conn = psycopg2.connect(host='db', database=os.environ['POSTGRES_DB'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'])
    cur = conn.cursor()

    # Get number of all GET requests
    sql_all = """SELECT COUNT(*) FROM weblogs;"""
    cur.execute(sql_all)
    all = cur.fetchone()[0]

    # Get number of all succesful requests
    sql_success = """SELECT COUNT(*), source  FROM weblogs WHERE status LIKE \'2__\' group by source order by 2;"""
    cur.execute(sql_success)
    local_success  = cur.fetchone()[0]
    remote_success  = cur.fetchone()[0]



    # Determine rate if there was at least one request
    rate = "No entries yet!"
    if all != 0:
        local_rate = str(local_success / all)
        remote_rate = str(remote_success / all)

    return render_template('index.html', local_rate = local_rate, remote_rate = remote_rate)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
