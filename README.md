# ImageClassifier
Implementation of images classifier in JS and Flask

## Config example
```json
{
  "title": "Some title",
  "port": 5000,
  "debug": false,
  "labels": {
      "raw_text": "#f00",
      "header": "#0f0",
      "title": "ff1500",
      "item": "#00f",
      "footer": "#00f080",
      "article": "#00f",
      "part": "#00f",
      "subitem": "#00f",
      "struct_unit": "#00f",
      "Other": "#00f"
  },
  "multiclass": true,
  "input_path": "tasks.json",
  "image_key": ["task_path"],
  "default_label_key": ["data", "bbox", "label"],
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

```image_key``` — key for get path to image in tasks file

```default_label_key``` — key for get default label

```result_key``` — key for saving results

```output_path``` — path to file with output tasks

```instruction``` — html content with instruction

```templates_dir``` — not used now

```confirm_required``` — require confirmation for save or not

```sampling``` — sampling mode for getting task (random or sequential)