import os
import os.path
import random
import json
import cv2

from flask import Flask
from flask import request, send_file, redirect, send_from_directory

with open("config.json", encoding='utf-8') as f:
    config = json.load(f)

app = Flask(__name__)
    
app.config['IMG_FOLDER'] = 'images' # папка с изобрвжениями
app.config['JS_FOLDER'] = 'js' # папка с js кодом
app.config['CSS_FOLDER'] = 'css' # папка со стилями

@app.route('/images/<filename>')
def image_file(filename):
    return send_from_directory(app.config['IMG_FOLDER'], filename)

@app.route('/js/<filename>')
def js_file(filename):
    return send_from_directory(app.config['JS_FOLDER'], filename)

@app.route('/css/<filename>')
def css_file(filename):
    return send_from_directory(app.config['CSS_FOLDER'], filename)

def make_classifier(task_id, title, image, default_label, multiclass):
    labels = []

    for label_info in config["labels"]:
        label = label_info["label"]
        color = label_info.get("color", "")
        label_str = "label: \"" + label + "\""
        color_str = "" if color == "" else ", color: \"" + color + "\""
        checked_str = ", checked: true" if label == default_label else ""
        labels.append("{" + label_str + color_str + checked_str + " }")

    return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title}</title>
            <link rel="stylesheet" type="text/css" href="css/styles.css?v=2">
        </head>
        <body>
            <div class="classifier">
                <div class="classifier-img" id="img">
                    <img src={image}>
                </div>

                <div class="classifier-controls">
                    <div id="labels"></div>

                    <div class="button" onclick=classifier.Reset()>Сбросить</div><br>
                    <div class="button" onclick=classifier.Save()>Сохранить</div>

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

            <script src="js/classifier.js?v=19"></script>
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
        instruction=config["instruction"],
        multiclass=("true" if multiclass else "false"),
        task_id=task_id,
        confirm_required=("true" if config["confirm_required"] else "false"),
        labels=",\n".join(labels))

def get_by_key_list(task, keys):
    value = task

    for key in keys:
        value = value[key]

    return value

def read_tasks():
    with open(config["input_path"], "r", encoding='utf-8') as f:
        tasks = json.load(f)

    with open(config["output_path"], 'r', encoding='utf-8') as f:
        completed_tasks = json.load(f)
    
    available_tasks = []

    for task_id, task in tasks.items():
        if task_id in completed_tasks:
            continue

        img_name = get_by_key_list(task, config["image_key"])
        default_label = get_by_key_list(task, config["default_label_key"])

        available_tasks.append({ "id": task_id, "img": img_name, "label": default_label })

    return available_tasks

@app.route('/', methods=['GET'])
def classify_image():
    available_tasks = read_tasks()

    if len(available_tasks) == 0: # если их нет, то и размечать нечего
        return "Размечать нечего"

    if config["sampling"] == "random":
        task = random.choice(available_tasks)
    else: #  config["sampling"] == "sequential":
        task = available_tasks[0]

    title = "Lost: " + str(len(available_tasks)) + " | " + config["title"]
    return make_classifier(task["id"], title, task["img"], task["label"], config["multiclass"])

@app.route('/save')
def save_file():
    task_id = request.args.get('task_id')
    labels = request.args.get('labels')
    
    with open(config["input_path"], "r", encoding='utf-8') as f:
        tasks = json.load(f)

    with open(config["output_path"], 'r', encoding='utf-8') as f:
        completed_tasks = json.load(f)

    completed_tasks[task_id] = tasks[task_id] # добавляем выполненное задание
    completed_tasks[task_id][config["result_key"]] = labels.split(';')

    with open(config["output_path"], 'w', encoding='utf-8') as f:
        json.dump(completed_tasks, f, indent=2, ensure_ascii=False)

    return redirect("/") # возвращаем на страницу разметки

if __name__ == '__main__':
    if not os.path.exists(config["output_path"]):
        with open(config["output_path"], "w", encoding='utf-8') as f:
            f.write("{\n}");

    app.run(debug=config["debug"], port=config["port"])