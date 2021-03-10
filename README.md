# ImageClassifier
Implementation of images classifier in JS and Flask

## How to start labeling
* Move your images to ```images``` directory
* Fill file with task (format description down)
* Change ```config.json``` (change labels, image_key, default_label_key and etc options)
* Open terminal and run ```python app.py```
* Go to ```localhost:port```, where port is described in config.json

## How to label
Click on button(s) and then click to ```save``` button or use short ```keys 1-9``` for first labels and press ```Enter```

## How to reset current labeling
Press button ```reset``` or ```0 key```

## How to get result
Result tasks saved to ```output_path``` output path defined in ```config.json```. All task from ```input_path``` copied to ```output_path``` with one addition key — ```result_key```

## Config example
```json
{
  "title": "Some title",
  "port": 5000,
  "debug": false,
  "labels": [
    { "label": "raw_text", "color": "#f00" },
    { "label": "header", "color": "#0f0", "html": "<span class='fa fa-header'></span> header" },
    { "label": "title", "color": "ff1500" },
    { "label": "item", "color": "#00f" },
    { "label": "footer", "color": "#00f080" },
    { "label": "article", "color": "#00f" },
    { "label": "part", "color": "#00f" },
    { "label": "subitem", "color": "#00f" },
    { "label": "struct_unit", "color": "#00f" },
    { "label": "Other", "color": "#00f" }
  ],
  "multiclass": true,
  "input_path": "tasks.json",
  "image_key": ["task_path"],
  "default_label_key": ["data", "bbox", "label"],
  "task_instruction_key": ["instruction"],
  "result_key": "labeled",
  "output_path": "labeled_tasks.json",
  "instruction": "Type some <b>hypertext</b> for label experts!",
  "templates_dir": "examples",
  "confirm_required": false,
  "sampling": "sequential"
}
```
## Config format
`title` — title of page

```port``` — port of Flask application

```debug``` — debug mode of Flask

```labels``` — dictionary of labels with colors

```multiclass``` — available more than one label

```input_path``` — file with tasks

```image_key``` — key for get path to image in tasks file (list of sequential keys)

```default_label_key``` — key for get default label (list of sequential keys)

```task_instruction_key``` — key for get instruction for task (list of sequential keys)

```result_key``` — key for saving results

```output_path``` — path to file with output tasks

```instruction``` — html content with instruction

```templates_dir``` — not used now

```confirm_required``` — require confirmation for save or not

```sampling``` — sampling mode for getting task (random or sequential)

## Labels item format
* label — name of class (not HTML)
* color — border and text color while button is pressed
* html — (optional) html content for button, for example icon: ```"html": "<span class='fa fa-header'></span> header"```

## Colors format of labels
* hex format — ```#ff00ff```
* rgb format — ```rgb(255, 0, 0)```
* hsl format — ```hsl(70, 80%, 50%)```

## Format of tasks.json
```json
{
  "task_id": {
    "image_key": "image_path",
    "default_label_key": "label",
  }
}
```

## Example of tasks.json
```"image_key": ["task_path"]``` — image getting by only one key — tasks[task_id]["task_path"]

```"default_label_key": ["data", "bbox", "label"]``` — default label getting by three keys — tasks[task_id]["data"]["bbox"]["label"]

```json
{
  "0": {
    "task_path": "images/img_000.jpg",
    "id": 0,
    "instruction": "instruction for task 0 (<b>hypertext</b>)",
    "predictions": [
      {
        "result": [
          {
            "type": "choices",
            "value": {
              "choices": [
                "raw_text"
              ]
            },
            "id": "UtdEoBaQU2",
            "to_name": "img",
            "from_name": "choice"
          }
        ],
        "id": 0
      }
    ],
    "data": {
      "bbox": {
        "line_num": 0,
        "text": " ",
        "bbox": {
          "height": 199,
          "y_lower_left": 72,
          "width": 225,
          "x_lower_left": 796
        },
        "label": "raw_text",
        "page_num": 0
      },
      "image_url": "http://localhost:8200/data/img_000.jpg?d=/tmp/task_c8c090a8-ab0f-11ea-a918-b42e99d2ac06/images",
      "original_image_name": "img_000001_00.png"
    }
  },
  "1": {
    "task_path": "images/img_001.jpg",
    "id": 1,
    "predictions": [
      {
        "result": [
          {
            "type": "choices",
            "value": {
              "choices": [
                "header"
              ]
            },
            "id": "UtdEoBaQU2",
            "to_name": "img",
            "from_name": "choice"
          }
        ],
        "id": 1
      }
    ],
    "data": {
      "bbox": {
        "line_num": 1,
        "text": "ВОРОНЕЖСКАЯ ОБЛАСТЬ",
        "bbox": {
          "height": 51,
          "y_lower_left": 342,
          "width": 878,
          "x_lower_left": 483
        },
        "label": "header",
        "page_num": 0
      },
      "image_url": "http://localhost:8200/data/img_001.jpg?d=/tmp/task_c8c090a8-ab0f-11ea-a918-b42e99d2ac06/images",
      "original_image_name": "img_000001_00.png"
    }
  },
}
```