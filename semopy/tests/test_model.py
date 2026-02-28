#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import numpy as np
import pandas as pd
from ..model import Model
from ..examples import univariate_regression, multivariate_regression, political_democracy

np.random.seed(2021)
n = 100
p = 3
params = [np.random.uniform(0.2, 1.2, size=(p - 1, 1)),
          np.random.uniform(0.2, 1.2, size=(p - 1, 1))]
params = list(map(lambda x: np.append([1], x), params))
y = np.random.normal(size=(n, 2 * p))
eta1 = np.random.normal(scale=1, size=(n, 1))
eta2 = np.random.normal(scale=1, size=(n, 1)) + 3 * eta1
y[:, :p] += np.kron(params[0], eta1)
y[:, p:] += np.kron(params[1], eta2)

res = list()
d = {'eta1': list(), 'eta2': list()}
y_names = list()
for i in range(1, p + 1):
    res.append((f'y{i}', '~', 'eta1', params[0][i - 1]))
    y_names.append(res[-1][0])
    d['eta1'].append(y_names[-1])
for j in range(1, p + 1):
    res.append((f'y{j + i}', '~', 'eta2', params[1][j - 1]))
    y_names.append(res[-1][0])
    d['eta2'].append(y_names[-1])
desc = '\n'.join(f"{eta} =~ {' + '.join(ys)}" for eta, ys in d.items())
desc += '\neta2 ~ eta1'
params = pd.DataFrame.from_records(res, columns=['lval', 'op', 'rval',
                                                 'Estimate'])
data = pd.DataFrame(np.append(np.append(y, eta1, axis=1), eta2, axis=1),
                    columns=y_names + ['eta1', 'eta2'])


class TestModel(unittest.TestCase):
    def evaluate(self, desc: str, data: pd.DataFrame, true: pd.DataFrame,
                 obj: str = "MLW", pval_thresh: float = .05, max_abs_err: float = .1) -> None:
        m = Model(desc)
        r = m.fit(data, obj=obj)
        assert r.success, f"Optimization routine failed. [{obj}]"
        ins = m.inspect()
        errs = list()
        for _, row in true.iterrows():
            t = (ins['op'] == row['op']) & (ins['lval'] == row['lval']) & \
                (ins['rval'] == row['rval'])
            if sum(t) == 0:
                continue
            t = ins[t]
            try:
                assert t['p-value'].values[0] < pval_thresh, \
                    f"Incorrect p-value estimate [{obj}]."
            except TypeError:
                pass
            est = t['Estimate'].values[0]
            errs.append(abs((est - row['Estimate']) / row['Estimate']))
        err = np.mean(errs)
        assert err < max_abs_err, \
            f"Parameter estimation quality is too low: {err} [{obj}]"

    def test_univariate_regression(self):
        desc = univariate_regression.get_model()
        data = univariate_regression.get_data()
        true = univariate_regression.get_params()
        self.evaluate(desc, data, true, 'MLW')
        self.evaluate(desc, data, true, 'ULS')
        self.evaluate(desc, data, true, 'GLS')
        self.evaluate(desc, data - data.mean(), true, 'FIML')

    def test_multivariate_regression(self):
        desc = multivariate_regression.get_model()
        data = multivariate_regression.get_data()
        true = multivariate_regression.get_params()
        self.evaluate(desc, data, true, 'MLW')
        self.evaluate(desc, data, true, 'ULS')
        self.evaluate(desc, data, true, 'GLS')
        self.evaluate(desc, data - data.mean(), true, 'FIML')

    def test_political_democracy(self):
        pdem = political_democracy
        model_desc, pdem_data, ref_params = pdem.get_model(), pdem.get_data(), pdem.get_params()
        for obj_fun in ("MLW", "ULS", "GLS"):
            print(obj_fun)
            self.evaluate(model_desc, pdem_data, ref_params, obj_fun,
                          pval_thresh=1,  # well, we just do not care about p-values
                          max_abs_err=.3)

    def test_random_model(self):
        global params
        global desc
        global data
        self.evaluate(desc, data, params, 'MLW')
        self.evaluate(desc, data, params, 'ULS')
        self.evaluate(desc, data, params, 'GLS')
        self.evaluate(desc, data - data.mean(), params, 'FIML')
