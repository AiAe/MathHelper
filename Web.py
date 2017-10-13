from flask import Flask, render_template, request

app = Flask(__name__)

last_update = '13.10.2017'
number_of_tasks = 6

def get_fn(n):

    return int(str(n)[-2:])

@app.route('/', methods=['GET', 'POST'])
def index():

    itext = '696969666'
    text = ''
    post = False

    if request.method == 'POST':

        f = int(request.form["f"])

        if f:

            last = get_fn(f)
            post = True
            itext = f

            text += "Номер {} задачите са ти: \n".format(last)

            for i in range(1, number_of_tasks + 1):

                text += str("Задача {0} - {0}.{1} \n".format(i, (((3 * last) + 3 - i) % 3) + 1))

    return render_template('index.html', text=text, post=post, last_update=last_update, itext=itext)

app.run(port=8080, host='127.0.0.1')