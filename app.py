import os
import os.path
import random
import json
import hashlib
import uuid

from flask import Flask
from flask import request, redirect, send_from_directory


app = Flask(__name__)


@app.route('/<path:filename>')
def image_file(filename):
    return send_from_directory(".", filename)


@app.route('/js/<filename>')
def js_file(filename):
    return send_from_directory(app.config['JS_FOLDER'], filename)


@app.route('/css/<filename>')
def css_file(filename):
    return send_from_directory(app.config['CSS_FOLDER'], filename)


@app.route('/fonts/<filename>')
def font_file(filename):
    return send_from_directory(app.config['FONTS_FOLDER'], filename)


def get_by_key_list(task, keys):
    value = task

    for key in keys:
        value = value[key]

    return value


def read_tasks():
    with open(os.path.abspath(config["input_path"]), "r", encoding='utf-8') as f:
        tasks = json.load(f)

    completed_tasks = get_completed_tasks()
    available_tasks = []

    for task_id, task in tasks.items():
        if task_id in completed_tasks:
            continue

        img_name = get_by_key_list(task, config["image_key"])
        default_label = get_by_key_list(task, config["default_label_key"])

        instruction = ""

        if "task_instruction_key" in config:
            try:
                instruction = "<h3>Task instruction</h3>" + get_by_key_list(task, config["task_instruction_key"])
            except:
                pass

        available_tasks.append({"id": task_id, "img": img_name, "label": default_label, "instruction": instruction})

    return available_tasks


def get_completed_tasks():
    with open(config["output_path"], 'r', encoding='utf-8') as f:
        completed_tasks = json.load(f)

    return completed_tasks


def get_md5(filename):
    with open(filename, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def save_completed_tasks(completed_tasks):
    with open(config["output_path"], 'w', encoding='utf-8') as f:
        json.dump(completed_tasks, f, indent=2, ensure_ascii=False)


def make_classifier(task_id, title, image, default_label, multiclass, task_instruction):
    labels = []

    if isinstance(default_label, str):
        default_label = [default_label]

    for label_info in config["labels"]:
        label = label_info["label"]
        color = label_info.get("color", "")
        html = label_info.get("html", label)

        label_str = "label: \"" + label + "\""
        color_str = "" if color == "" else ", color: \"" + color + "\""
        html_str = "" if html == "" else ", html: \"" + html + "\""
        checked_str = ", checked: true" if label in default_label else ""
        labels.append("{" + label_str + color_str + checked_str + html_str + " }")

    completed_tasks = get_completed_tasks()
    labeled = "" if len(completed_tasks) == 0 else "<a href='/labeled'>Labeled tasks</a>"
    previous = "" if len(
        completed_tasks) == 0 else '''<div class='button' onclick='window.location.replace("/restore?task_id=''' + \
                                   list(completed_tasks.keys())[-1] + '''")'>Restore previous</div>'''

    return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title}</title>
            <link rel="stylesheet" type="text/css" href="css/styles.css?v={style}">
            <link rel="stylesheet" type="text/css" href="css/font-awesome.min.css">
        </head>
        <body>
            <div class="classifier">
                <div class="classifier-img" id="img">
                    <img src={image}>
                </div>

                <div class="classifier-controls">
                    <div class="classifier-buttons">
                        <div id="labels"></div>

                        <div class="button" onclick=classifier.Reset()>Reset</div>
                        <div class="button" onclick=classifier.Save()>Save</div>
                        {previous}
                    </div>

                    <div class="text">
                        <b>Hot keys:</b><br>
                        <ul id="keys"></ul>
                    </div>
                </div>

                <div class="classifier-info">
                    <h2>Instruction</h2>
                    {instruction}
                </div>
            </div>

            <div>
                {labeled}
            </div>

            <script src="js/classifier.js?v={js}"></script>
            <script> 
                const MULTICLASS = {multiclass};
                const TASK_ID = {task_id};
                const REQUIRE_CONFIRMATION = {confirm_required};
                const LABELS = [
                    {labels}
                ]

                let classifier = new Classifier(LABELS)
            </script>
        </body>
        </html>
    '''.format(title=title,
               image=image,
               js=get_md5(app.config["JS_FOLDER"] + "/classifier.js"),
               style=get_md5(app.config["CSS_FOLDER"] + "/styles.css"),
               instruction=config["instruction"] + task_instruction,
               labeled=labeled,
               previous=previous,
               multiclass=("true" if multiclass else "false"),
               task_id=task_id,
               confirm_required=("true" if config["confirm_required"] else "false"),
               labels=",\n".join(labels))


def make_labeled(labeled_tasks):
    table = ''

    for task_id in labeled_tasks:
        task = labeled_tasks[task_id]
        img_name = get_by_key_list(task, config["image_key"])

        cells = "<td>" + str(task_id) + "</td>"
        cells += "<td><a target='_blank' href='" + img_name + "'>" + img_name + "</a></td>"
        cells += "<td>" + ",".join(task[config["result_key"]]) + "</td>"
        cells += "<td><a href='/restore?task_id=" + str(task_id) + "'>Restore</a></td>"
        table += "<tr>" + cells + "</tr>"

    return '''
    <!DOCTYPE html>
        <html>
        <head>
            <title>Labeled tasks</title>
            <link rel="stylesheet" type="text/css" href="css/styles.css?v={style}">
            <link rel="stylesheet" type="text/css" href="css/font-awesome.min.css">
        </head>
        <body>
            <table class='classifier-table'>
            <tr>
                <th>task_id</th>
                <th>image name</th>
                <th>labeled class(es)</th>
            </tr>
            {table}
            </table>
            <br>
            <a href="/">Go to label page</a>
        </body>
    </html>
    '''.format(
        style=get_md5(app.config["CSS_FOLDER"] + "/styles.css"),
        table=table
    )


@app.route('/', methods=['GET'])
def classify_image():
    available_tasks = read_tasks()

    if len(available_tasks) == 0:  # если их нет, то и размечать нечего
        return '''
        <p>There is nothing for labeling</p>
        <h1><a href="/get_results/{uid}">Results</a></h1>
        '''.format(uid=uuid.uuid1())

    if config["sampling"] in ["random", "shuffle"]:
        task = random.choice(available_tasks)
    elif config["sampling"] == "sequential":
        task = available_tasks[0]
    else:
        raise ValueError("Invalid sampling mode")

    title = "Lost: " + str(len(available_tasks)) + " | " + config["title"]
    return make_classifier(task["id"], title, task["img"], task["label"], config["multiclass"], task.get("instruction", ""))


@app.route('/save')
def save_file():
    task_id = request.args.get('task_id')
    labels = request.args.get('labels')

    with open(config["input_path"], "r", encoding='utf-8') as f:
        tasks = json.load(f)

    completed_tasks = get_completed_tasks()
    completed_tasks[task_id] = tasks[task_id]  # добавляем выполненное задание
    completed_tasks[task_id][config["result_key"]] = labels.split(';')

    save_completed_tasks(completed_tasks)

    return redirect("/")  # возвращаем на страницу разметки


@app.route('/labeled')
def view_labeled():
    completed_tasks = get_completed_tasks()

    if len(completed_tasks) == 0:
        return "No tasks have been labeled, <a href='/'>go to label page</a>:"

    return make_labeled(completed_tasks)


@app.route('/restore')
def restore_task():
    task_id = request.args.get('task_id')
    completed_tasks = get_completed_tasks()
    del completed_tasks[task_id]

    save_completed_tasks(completed_tasks)

    return redirect(request.referrer)


@app.route('/get_results/<uid>')
def get_results(uid=None):
    result_file = config["output_path"]
    if not os.path.isfile(result_file):
        return "Nothing to download!"
    directory = os.path.dirname(result_file)
    filename = os.path.basename(result_file)
    return send_from_directory(directory, filename, as_attachment=True)


def check_key(config: dict, key: str, default_value=None):
    if key not in config:
        if default_value is None:
            raise ValueError('{} is not set'.format(key))

        config[key] = default_value
        print('Warning: "{0}" is not set. Changed to "{1}"'.format(key, default_value))


def get_config(filename: str):
    with open(os.path.join(os.path.dirname(__file__), filename), encoding='utf-8') as f:
        config = json.load(f)

    check_key(config, 'title', '')
    check_key(config, 'port', '5000')
    check_key(config, 'output_path', 'labeled_tasks.json')
    check_key(config, 'input_path', 'tasks.json')
    check_key(config, 'labels')
    check_key(config, 'multiclass', False)
    check_key(config, 'result_key', 'labeled')
    check_key(config, 'sampling', 'sequential')

    if config['sampling'] not in ['sequential', 'random', 'shuffle']:
        raise ValueError('Invalid "sampling" mode: {0}'.format(config['sampling']))

    for label in config['labels']:
        if 'label' not in label:
            raise ValueError('All labels must have "label" key')

    if len(set(label['label'] for label in config['labels'])) != len(config['labels']):
        raise ValueError('Labels are not unique')

    return config


if __name__ == '__main__':
    try:
        config = get_config('config.json')
        host = "0.0.0.0"
        port = config["port"]

        app.config['JS_FOLDER'] = 'js'  # папка с js кодом
        app.config['CSS_FOLDER'] = 'css'  # папка со стилями
        app.config['FONTS_FOLDER'] = 'fonts'  # папка со шрифтами

        if not os.path.exists(config["output_path"]):
            with open(config["output_path"], "w", encoding='utf-8') as f:
                f.write("{\n}")

        app.run(debug=config.get("debug", False), host=host,  port=port)
    except ValueError as error:
        print(error)
