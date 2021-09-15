import json
import os


# from sklearn
def cohen_kappa_score(y1, y2, *, labels=None, weights=None,
                      sample_weight=None):
    r"""Cohen's kappa: a statistic that measures inter-annotator agreement.
    This function computes Cohen's kappa [1]_, a score that expresses the level
    of agreement between two annotators on a classification problem. It is
    defined as
    .. math::
        \kappa = (p_o - p_e) / (1 - p_e)
    where :math:`p_o` is the empirical probability of agreement on the label
    assigned to any sample (the observed agreement ratio), and :math:`p_e` is
    the expected agreement when both annotators assign labels randomly.
    :math:`p_e` is estimated using a per-annotator empirical prior over the
    class labels [2]_.
    Read more in the :ref:`User Guide <cohen_kappa>`.
    Parameters
    ----------
    y1 : array of shape (n_samples,)
        Labels assigned by the first annotator.
    y2 : array of shape (n_samples,)
        Labels assigned by the second annotator. The kappa statistic is
        symmetric, so swapping ``y1`` and ``y2`` doesn't change the value.
    labels : array-like of shape (n_classes,), default=None
        List of labels to index the matrix. This may be used to select a
        subset of labels. If None, all labels that appear at least once in
        ``y1`` or ``y2`` are used.
    weights : {'linear', 'quadratic'}, default=None
        Weighting type to calculate the score. None means no weighted;
        "linear" means linear weighted; "quadratic" means quadratic weighted.
    sample_weight : array-like of shape (n_samples,), default=None
        Sample weights.
    Returns
    -------
    kappa : float
        The kappa statistic, which is a number between -1 and 1. The maximum
        value means complete agreement; zero or lower means chance agreement.
    References
    ----------
    .. [1] J. Cohen (1960). "A coefficient of agreement for nominal scales".
           Educational and Psychological Measurement 20(1):37-46.
           doi:10.1177/001316446002000104.
    .. [2] `R. Artstein and M. Poesio (2008). "Inter-coder agreement for
           computational linguistics". Computational Linguistics 34(4):555-596
           <https://www.mitpressjournals.org/doi/pdf/10.1162/coli.07-034-R2>`_.
    .. [3] `Wikipedia entry for the Cohen's kappa
            <https://en.wikipedia.org/wiki/Cohen%27s_kappa>`_.
    """
    confusion = confusion_matrix(y1, y2, labels=labels,
                                 sample_weight=sample_weight)
    n_classes = confusion.shape[0]
    sum0 = np.sum(confusion, axis=0)
    sum1 = np.sum(confusion, axis=1)
    expected = np.outer(sum0, sum1) / np.sum(sum0)

    if weights is None:
        w_mat = np.ones([n_classes, n_classes], dtype=int)
        w_mat.flat[:: n_classes + 1] = 0
    elif weights == "linear" or weights == "quadratic":
        w_mat = np.zeros([n_classes, n_classes], dtype=int)
        w_mat += np.arange(n_classes)
        if weights == "linear":
            w_mat = np.abs(w_mat - w_mat.T)
        else:
            w_mat = (w_mat - w_mat.T) ** 2
    else:
        raise ValueError("Unknown kappa weighting type.")

    k = np.sum(w_mat * confusion) / np.sum(w_mat * expected)
    return 1 - k


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
