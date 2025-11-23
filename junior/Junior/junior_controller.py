from flask import Flask, request, render_template
from junior_model import push_into_stack, pop, get_stack


app = Flask(__name__)

@app.route('/')
def home():
    rv = render_template('main.html',message='WOBBLER')
    return rv

@app.route('/push', methods=['GET'])
def push():
    item = request.args['item']

    message = push_into_stack(item)
    return render_template('main.html', message=message)

@app.route('/print')
def print_():
    print(f"{get_stack()}")
    return render_template('stack.html', stack=reversed(get_stack()))

@app.route('/pop', methods=['GET'])
def pop_():
    pop()

    return render_template('main.html',message = 'Popped?')

if __name__ == '__main__':
    app.run(debug=True,  port=5000)


# does this program have bugs? Yes! But what are they? Let's try to fix them!