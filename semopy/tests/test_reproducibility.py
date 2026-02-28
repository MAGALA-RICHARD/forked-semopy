# https://gitlab.com/georgy.m/semopy/-/issues/26#note_913412910

from semopy.examples import political_democracy as pd
from multiprocessing import Process, Queue

import numpy as np
import random
import semopy


def fit_model() -> np.array:
    random.seed(0)
    np.random.seed(0)

    desc = pd.get_model()
    data = pd.get_data()

    m = semopy.Model(desc)
    return m.fit(data).x


atol, rtol = 1e-16, 0
n_tries = 2


def test_reproducible_same_process():
    results = [fit_model() for _ in range(n_tries)]
    assert np.isclose(*results, atol=atol, rtol=rtol).all()


def fit_model_async(q: Queue) -> None:
    q.put(fit_model())


def test_reproducibile_different_processes():  # TODO failing!
    q = Queue()
    processes = [Process(target=fit_model_async, args=(q,)) for _ in range(n_tries)]
    for p in processes:
        p.start()
        p.join()
    results = [q.get() for _ in range(n_tries)]
    assert np.isclose(*results, atol=atol, rtol=rtol).all()
