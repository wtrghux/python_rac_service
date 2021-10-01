from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

WORKDIR = os.getcwd()


def lines_to_keys(lines):
    line_dict = {}

    for line in lines:
        key, values = line.split("=")
        line_dict[key.strip()] = values.strip()

    return line_dict


def without_equal(lines):
    keys = []
    values = []

    for line in lines:
        splited = line.split()
        length = len(splited)
        keys.append(" ".join(splited[: length - 2]))
        values.append([splited[length - 2], splited[length - 1]])

    return {
        key: {"Recieved": values[0], "Sent": values[1]}
        for key, values in zip(keys, values)
    }


def lines_to_dict_s(lines):
    keys = []
    values = []
    tmp1 = []  # without =
    tmp2 = []  # for =

    for line in lines:
        if "Received" in line and "Sent" in line:
            continue
        elif "=" in line:
            tmp2.append(line)
        elif "Pv" not in line:
            tmp1.append(line)
        else:
            if len(tmp2) != 0:
                values.append(lines_to_keys(tmp2))
                tmp2.clear()
            if len(tmp1) != 0:
                values.append(without_equal(tmp1))
                tmp1.clear()
            keys.append(line.strip())
    values.append(lines_to_keys(tmp2))
    tmp2.clear()

    return {key: value for key, value in zip(keys, values)}


def for_s():
    with open("new-s.txt", "r") as f:
        content = f.readlines()
    os.remove(WORKDIR + r"\\new-s.txt")

    content = [line.strip() for line in content if line != "\n"]
    # with open(WORKDIR + r"\\output-s.json", "w") as file:
    #     json.dump(lines, file, indent=4)

    return [lines_to_dict_s(content)]


def lines_to_dict_t(lines):
    keys = lines[0].split("  ")
    keys = [key.strip() for key in keys if key != ""]
    values = [line.split() for line in lines[1:]]
    return [
        {key: value for key, value in zip(keys, values[i])}
        for i in range(len(values) - 1)
    ]


def for_t():
    with open("new-t.txt", "r") as f:
        content = f.readlines()[3:]
    os.remove(WORKDIR + r"\\new-t.txt")

    content = [line.strip() for line in content if line != "\n"]
    # with open(WORKDIR + r"\\output-t.json", "w") as file:
    #     json.dump(lines, file, indent=4)

    return lines_to_dict_t(content)


def main(cmd, args):
    os.system("chcp 65001")
    args = args.split(",")

    for arg in args:
        command = f"{cmd} -{arg} > new-{arg}.txt"
        os.system(command)
    # os.system("netstat -s > new.txt")

    output_json = []

    if "s" in args:
        output_json.append(for_s())

    if "t" in args:
        output_json.append(for_t())

    # with open(WORKDIR + r"\\output.json", "w") as file:
    #     json.dump(out_s + out_t, file, indent=2)

    return output_json


@app.route("/", methods=["GET"])
def output():
    command = request.args.get("command")
    if not command or command == "":
        return "Error: Invalid Parameters"
    args = request.args.get("args")

    return jsonify(main(command, args))


if __name__ == "__main__":
    app.debug = True
    app.run(host="127.0.0.1", port=3000)
