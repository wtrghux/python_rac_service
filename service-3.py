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


@app.route("/", methods=["GET", "POST"])
def output():
    help = """
    PLEASE USE POST REQUEST!
    Fields:
    mode=%%mode_name%%
    command=%%command_name%%
    options=%%list_of_options%% (may be empty)

    Example:
    curl -X POST -H "Content-Type: application/json"
    -d '{"mode": "cluster", "command": "list"}'
    https://127.0.0.1:3000/
    """

    if request.method != "POST":
        return help

    request_data = request.get_json()
    mode = request_data["mode"]
    if not mode or mode == "":
        return "Error: Invalid Mode"
    if "command" in request_data.keys():
        command = request_data["command"]
    else:
        return "Error: Invalid Command"
    if "options" in request_data.keys():
        options = request_data["options"]
    else:
        options = None

    return jsonify(main(mode, command, options))


if __name__ == "__main__":
    app.debug = True
    app.run(host="127.0.0.1", port=3000)
