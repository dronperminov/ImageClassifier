import json
import os
from sklearn.metrics import cohen_kappa_score


def get_labels(task_path: str) -> dict:
    with open(task_path, encoding='utf-8') as f:
        task = json.load(f)

    return {task_id: task[task_id]["labeled"] for task_id in task}


def main():
    path = ''  # path to labeled tasks, for example: 'labeled_tasks/'
    labeled_task_paths = os.listdir(path)

    task2labels = [get_labels(os.path.join(path, task_path)) for task_path in labeled_task_paths]
    task_ids = task2labels[0].keys()
    labels = [[task2label[task_id] for task_id in task_ids] for task2label in task2labels]

    for i, path1 in enumerate(labeled_task_paths):
        print(path1 + ':')

        for j, path2 in enumerate(labeled_task_paths):
            if i == j:
                continue

            print('    {0}: {1}'.format(path2, cohen_kappa_score(labels[i], labels[j])))

        print('')


if __name__ == '__main__':
    main()
