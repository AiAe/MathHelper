from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

last_update = '13.10.2017'
number_of_tasks = 6

config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "db": "math"
}

def connect():
    connection = pymysql.connect(host=config["host"], user=config["user"], passwd=config["password"], db=config["db"], charset='utf8')
    connection.autocommit(True)
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    return connection, cursor

def execute(connection, cursor, sql, args=None):
    try:
        cursor.execute(sql, args) if args is not None else cursor.execute(sql)
        return cursor
    except pymysql.err.OperationalError:
        connection.connect()
        return execute(sql, args)

def userexist(id):
    connection, cursor = connect()
    counter = execute(connection, cursor, 'SELECT id FROM checks WHERE id = %s', [id]).fetchone()
    if counter != None and len(counter) > 0:
        return True
    else:
        return False

def findall(tasks):
    connection, cursor = connect()

    checks = execute(connection, cursor, "SELECT * FROM checks WHERE tasks = %s", [tasks]).fetchall()

    names = []

    for u in checks:
        user = execute(connection, cursor, "SELECT * FROM users WHERE id = %s", [u["id"]]).fetchone()

        names.append(user["name"] + "\n")

    if len(checks) == 31:
        return 'Всички :D'
    else:
        return "".join(names)

def get_fn(n):

    return int(str(n)[-2:])

@app.route('/calc/')
def calculate():

    connection, cursor = connect()

    execute(connection, cursor, "TRUNCATE checks")

    users = execute(connection, cursor, "SELECT id, number FROM users").fetchall()
    temp = ''

    for user in users:
        for i in range(1, number_of_tasks + 1):
            form = ((((3 * get_fn(user["number"])) + 3 - i) % 3) + 1)
            temp += str(form)

        execute(connection, cursor, "INSERT INTO checks (id, tasks) VALUES (%s, %s)", [user["id"], temp])
        temp = ''

    return 'Done!'

@app.route('/', methods=['GET', 'POST'])
def index():

    connection, cursor = connect()

    itext = '17621719'
    text = ''
    post = False
    i = 1
    task = {"tasks": ""}


    if request.method == 'POST':

        f = int(request.form["f"])

        if f:
            post = True

            user = execute(connection, cursor, "SELECT id FROM users WHERE number = %s", [f]).fetchone()
            task = execute(connection, cursor, "SELECT tasks FROM checks WHERE id = %s", [user["id"]]).fetchone()

            tasks = list(str(task["tasks"]))

            for t in tasks:
                text += "Задача {0} - {0}.{1} \n".format(i, t)
                i += 1



    return render_template('index.html', text=text, post=post, last_update=last_update, itext=itext, users=findall(task["tasks"]))

app.run(debug=True, port=8080, host='127.0.0.1')