from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"mensaje": "Servidor Multibase funcionando correctamente :)"})

if __name__ == '__main__':
    app.run(debug=True, port=3000)