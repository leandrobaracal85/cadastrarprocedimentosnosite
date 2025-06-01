from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

def executar_script(script_nome, pasta):
    if not pasta:
        return jsonify({"erro": "Caminho da pasta não fornecido"}), 400

    resultado = subprocess.run(
        ["python3", script_nome, pasta],
        capture_output=True,
        text=True
    )

    return jsonify({
        "stdout": resultado.stdout,
        "stderr": resultado.stderr,
        "codigo": resultado.returncode
    })

@app.route("/inquerito", methods=["POST"])
def inquerito():
    pasta = request.form.get("pasta")
    return executar_script("inquerito.py", pasta)

@app.route("/cautelar", methods=["POST"])
def cautelar():
    pasta = request.form.get("pasta")
    return executar_script("cautelar.py", pasta)

@app.route("/tc", methods=["POST"])
def tc():
    pasta = request.form.get("pasta")
    return executar_script("tc.py", pasta)

@app.route("/ai", methods=["POST"])
def ai():
    pasta = request.form.get("pasta")
    return executar_script("ai.py", pasta)

@app.route("/bo", methods=["POST"])
def bo():
    pasta = request.form.get("pasta")
    return executar_script("bo.py", pasta)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
