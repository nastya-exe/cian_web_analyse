from flask import Flask, request, jsonify, render_template


app = Flask(__name__)

@app.route('/')
def start_page():
    return render_template('main.html')

@app.route('/predict')
def predict_page():
    return render_template('predict.html')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)