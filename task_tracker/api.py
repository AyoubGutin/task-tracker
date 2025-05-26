from flask import Flask, render_template

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Main route
@app.route('/')
def index():
    '''
    Render the main page
    '''
    return render_template('index.html')

if __name__ == '__main__':
    '''
    Run the Flask app
    '''
    app.run(debug=True, port=5500)

