from flask import Flask, request, jsonify
import os


FILENAME = "data.txt"
app = Flask(__name__)


def main(mode, cmd, opts=None):
    os.system("chcp 65001")

    if opts is None:
        os.system(f"./rac {mode} {cmd} > {FILENAME}")
    else:
        os.system(f"./rac {mode} {cmd} {opts} > {FILENAME}")

    keys, values = [], []
    with open(FILENAME, "r") as f:
        text = f.readlines()
    for line in text:
        key, value = line.split(":")
        keys.append(key.strip())
        values.append(value.strip())

    return {key: value for key, value in zip(keys, values)}


@app.route("/", methods=["GET"])
def output():
    mode = request.args.get("mode")
    if not mode or mode == "":
        return "Error: Invalid Parameters"
    command = request.args.get("command")
    options = request.args.get("options")

    return jsonify(main(mode, command, options))


if __name__ == "__main__":
    app.debug = True
    app.run(host="127.0.0.1", port=3000)
