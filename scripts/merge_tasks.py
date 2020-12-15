import json
import os

path = ""  # directory with completed tasks
path_output = ""  # where to store result

task_id = 0
result_tasks = {}
for file in os.listdir(path):
    if file.endswith(".json"):
        with open(os.path.join(path, file)) as task_file:
            task = json.load(task_file)
        for k, v in task.items():
            v["id"] = task_id
            result_tasks[str(task_id)] = v
            task_id += 1

if os.path.isdir(path_output):
    path_output = os.path.join(path_output, "merged.json")

task_directory = os.path.dirname(path_output)
if not os.path.isdir(task_directory):
    os.makedirs(task_directory)


with open(path_output, "w") as file_out:
    json.dump(obj=result_tasks, fp=file_out, ensure_ascii=False, indent=4)
print("DONE save result into {}".format(path_output))

