from flask import Flask, render_template

app = Flask(__name__, template_folder='../templates', static_folder='../static')


# Main route
@app.route('/')
def index():
    """
    Render the main page
    """
    return render_template('index.html')


@app.route('/task/new', methods=['GET'])
def add_new_task_page():
    return render_template('add_task.html')


@app.route('/task/edit', methods=['GET'])
def edit_task_page():
    return render_template('edit_task.html')


@app.route('/calendar', methods=['GET'])
def calendar_page():
    return render_template('calendar.html')


@app.route('/tasks', methods=['GET'])
def tasks_page():
    return render_template('tasks.html')


if __name__ == '__main__':
    """
    Run the Flask app
    """
    app.run(debug=True, port=5500)
