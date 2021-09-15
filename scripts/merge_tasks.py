import json
import os

path = "/tmp/docreaderData/"  # directory with completed tasks
path_output = "/tmp/docreaderData/"  # where to store result

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
    path_output = os.path.join(path_output, "labeled.json")

task_directory = os.path.dirname(path_output)
if not os.path.isdir(task_directory):
    os.makedirs(task_directory)


with open(path_output, "w") as file_out:
    print(len(result_tasks))
    json.dump(obj=result_tasks, fp=file_out, ensure_ascii=False, indent=4)
print("DONE save result into {}".format(path_output))

