'''Create fancy HTML report for a given fitted model.'''
import logging
from .. import semplot, calc_stats, __version__
from collections import defaultdict
import pandas as pd
import shutil
import os

__folder = os.path.dirname(os.path.abspath(__file__))
__index = os.path.join(__folder, 'report.html')
__vis = os.path.join(__folder, 'vis.txt')
__css = os.path.join(os.path.join(__folder, 'css'), 'bootstrap.min.css')
__js = os.path.join(os.path.join(__folder, 'js'), 'bootstrap.min.js')
__navitem = '''<li class="nav-item" role="presentation">
<button class="nav-link {2}" id="{0}-tab" data-bs-toggle="tab" data-bs-target="#{0}"
type="button" role="tab" aria-controls="{0}" aria-selected="{3}">{1}</button>
</li>'''
__tab = '''<div class="tab-pane fade {2}" id="{0}" role="tabpanel" aria-labelledby="{0}-tab">{1}</div>'''
__start = '''<ul class="nav nav-tabs" id="{0}" role="tablist">'''
__cont = '''</ul><div class="tab-content" id="{0}Content">'''
__end = '''</div>'''


def report(model, name: str, path='', std_est=False, se_robust=False,
           **kwargs):
    """
    Generate a report in the form of HTML file.

    Parameters
    ----------
    model : ModelBase
        Arbitrary fitted model instance.
    name : str
        A name that user gives to the model. Can be thought of as a title. Will
        be used as a directory name.
    path : str, optional
        Path to folder where report will be stored. The default is ''.
    std_est : bool, optional
        If True, then standardized estimates are used. The default is False.
    se_robust : TYPE, optional
        If True, then robust p-values are calculated. The default is False.
    **kwargs : dict
        Extra arguments for semplot.

    Returns
    -------
    None.

    """
    desc = model.description
    n_samples = model.n_samples
    model_name = type(model).__name__
    optresult = str(model.last_result)
    if model.last_result.success:
        color = 'success'
        converged = 'Yes'
    else:
        color = 'danger'
        converged = 'No'
    obj = model.last_result.name_obj
    clasv = str()
    pt = '<div class="row"><div class="col-sm-2">{}</div>' \
         '<div class="col-sm-6">{}</div></div>'
    for c, its in model.vars.items():
        clasv += pt.format(c, ', '.join(its))
    ins = model.inspect(std_est=std_est, se_robust=se_robust)
    measurement = defaultdict(list)
    reg = defaultdict(list)
    intercepts = defaultdict(list)
    var = defaultdict(list)
    cov = defaultdict(list)
    other = defaultdict(lambda: defaultdict(list))
    ests = str()
    outs = model.vars['_output']
    obs = model.vars['observed']
    lats = model.vars['latent']
    out_obs = set(outs) & set(obs)
    for _, row in ins.iterrows():
        lval = row['lval']
        op = row['op']
        rval = row['rval']
        pval = row['p-value']
        est = row['Estimate']
        try:
            pval = '{:.3f}'.format(float(pval))
        except ValueError:
            pass
        try:
            est = '{:.3f}'.format(float(est))
        except ValueError:
            pass
        if std_est:
            est_std = row['Est. Std']
            try:
                est_std = '{:.3f}'.format(float(est_std))
            except ValueError:
                pass
            t = [rval, est, est_std, pval]
        else:
            t = [rval, est, pval]
        if op == '~':
            if rval in (1, '1'):
                intercepts[lval].append(t)
            elif (rval in lats) and (lval in out_obs):
                t[0] = lval
                measurement[rval].append(t)
            else:
                reg[lval].append(t)
        elif op == '~~':
            if lval != rval:
                cov[lval].append(t)
            else:
                var[lval].append(t)
        else:
            other[op][lval].append(t)
    pt = "<div class='col-sm-2'>{}</div><div class='col-sm-2'>{}</div>" \
         "<div class='col-sm-1'>{}</div><div class='col-sm-1'>{}</div>"
    if std_est:
        pt += "<div class='col-sm-1'>{}</div>"
        t = pt.format('', '', 'Estimate', 'Std. Estimate',
                      'P-value')
    else:
        t = pt.format('', '', 'Estimate', 'P-value')
    ests = '<div class="row">' + t + '</div>'
    ptt = "<div class='col-sm-2 text-end'>{}</div>" \
          "<div class='col-sm-2'>{}</div><div class='col-sm-1'>{}</div>" \
          "<div class='col-sm-1'>{}</div>"
    if std_est:
        ptt += "<div class='col-sm-1'>{}</div>"
    if measurement:
        if std_est:
            t = pt.format('Measurement:', '', '', '', '')
            ests += '<div class="row">' + t + '</div>'
            for lval, its in measurement.items():
                t = ptt.format(lval + ' =~', '', '', '', '')
                ests += '<div class="row">' + t + '</div>'
                for (rval, est, est_std, pval) in its:
                    t = ptt.format('', rval, est, est_std, pval)
                    ests += '<div class="row">' + t + '</div>'
        else:
            ests += pt.format('Measurement:', '', '', '')
            for lval, its in measurement.items():
                t = ptt.format(lval + ' =~', '', '', '')
                ests += '<div class="row">' + t + '</div>'
                for (rval, est, pval) in its:
                    t = ptt.format('', rval, est, pval)
                    ests += '<div class="row">' + t + '</div>'
    if reg:
        if std_est:
            t = pt.format('Regressions:', '', '', '', '')
            ests += '<div class="row">' + t + '</div>'
            for lval, its in measurement.items():
                t = ptt.format(lval + ' ~', '', '', '', '')
                ests += '<div class="row">' + t + '</div>'
                for (rval, est, est_std, pval) in its:
                    t = ptt.format('', rval, est, est_std, pval)
                    ests += '<div class="row">' + t + '</div>'
        else:
            ests += pt.format('Regressions:', '', '', '')
            for lval, its in reg.items():
                t = ptt.format(lval + ' ~', '', '', '')
                ests += '<div class="row">' + t + '</div>'
                for (rval, est, pval) in its:
                    t = ptt.format('', rval, est, pval)
                    ests += '<div class="row">' + t + '</div>'
    if intercepts:
        if std_est:
            t = pt.format('Intercepts:', '', '', '', '')
            ests += '<div class="row">' + t + '</div>'
            for lval, its in intercepts.items():
                for (rval, est, est_std, pval) in its:
                    t = ptt.format('', lval, est, est_std, pval)
                    ests += '<div class="row">' + t + '</div>'
        else:
            ests += pt.format('Intercepts:', '', '', '')
            for lval, its in intercepts.items():
                for (rval, est, pval) in its:
                    t = ptt.format('', lval, est, pval)
                    ests += '<div class="row">' + t + '</div>'

    if var:
        if std_est:
            t = pt.format('Variances:', '', '', '', '')
            ests += '<div class="row">' + t + '</div>'
            for lval, its in var.items():
                for (rval, est, est_std, pval) in its:
                    t = ptt.format('', rval, est, est_std, pval)
                    ests += '<div class="row">' + t + '</div>'
        else:
            ests += pt.format('Variances:', '', '', '')
            for lval, its in var.items():
                for (rval, est, pval) in its:
                    t = ptt.format('', rval, est, pval)
                    ests += '<div class="row">' + t + '</div>'
    if cov:
        if std_est:
            t = pt.format('Covariances:', '', '', '', '')
            ests += '<div class="row">' + t + '</div>'
            for lval, its in cov.items():
                t = ptt.format(lval + ' ~', '', '', '', '')
                ests += '<div class="row">' + t + '</div>'
                for (rval, est, est_std, pval) in its:
                    t = ptt.format('', rval, est, est_std, pval)
                    ests += '<div class="row">' + t + '</div>'
        else:
            t = pt.format('Covariances:', '', '', '')
            ests += '<div class="row">' + t + '</div>'
            for lval, its in cov.items():
                t = ptt.format(lval + ' ~', '', '', '')
                ests += '<div class="row">' + t + '</div>'
                for (rval, est, pval) in its:
                    t = ptt.format('', rval, est, pval)
                    ests += '<div class="row">' + t + '</div>'
    if other:
        if std_est:
            t = pt.format('Other operators:', '', '', '', '')
        else:
            t = pt.format('Other operators:', '', '', '')
        ests += '<div class="row">' + t + '</div>'
        for op, rvals in other.items():
            if std_est:
                for lval, its in rvals.items():
                    t = ptt.format(lval + f' {op}', '', '', '', '')
                    ests += '<div class="row">' + t + '</div>'
                    for (rval, est, est_std, pval) in its:
                        t = ptt.format('', rval, est, est_std, pval)
                        ests += '<div class="row">' + t + '</div>'
            else:
                for lval, its in rvals.items():
                    t = ptt.format(lval + f' {op}', '', '', '')
                    ests += '<div class="row">' + t + '</div>'
                    for (rval, est, pval) in its:
                        t = ptt.format('', rval, est, pval)
                        ests += '<div class="row">' + t + '</div>'
    path = os.path.join(path, name)
    if not os.path.isdir(path):
        os.mkdir(path)
    try:
        pp = os.path.join(path, 'plots')
        if not os.path.isdir(pp):
            os.mkdir(pp)
        semplot(model, os.path.join(pp, '1.png'), plot_ests=False, **kwargs)
        semplot(model, os.path.join(pp, '2.png'), plot_ests=True, **kwargs)
        semplot(model, os.path.join(pp, '3.png'), plot_ests=False,
                plot_covs=True, **kwargs)
        semplot(model, os.path.join(pp, '4.png'), plot_ests=True,
                plot_covs=True, **kwargs)
        with open(__vis, 'r') as f:
            vis = f.read()
    except Exception as e:
        s = 'Could not plot model. Possible Graphviz installation issues.'
        logging.warning(s + ' ' + str(e))
        vis = f'<div class="alert alert-warning" role="alert">{s}</div>'
    stats = calc_stats(model)
    fitindices = str()
    for i in range(0, stats.shape[1], 5):
        fitindices += '<table class="table">'
        a = "<thead><tr>"
        b = "<tbody><tr>"
        for j in range(i, min(stats.shape[1], i + 5)):
            a += "<th scope='col'>{}</th>".format(stats.columns[j])
            t = stats[stats.columns[j]].values.flatten()[0]
            try:
                t = '{:.3f}'.format(t)
            except ValueError:
                pass
            b += "<td>{}</td>".format(t)
        b += "</tr></tbody>"
        a += "</tr></thead>"
        fitindices += a + b + '</table>'
    pt = '<center><h4>{}</h4></center>{}'
    fmt = lambda x: '{:.2f}'.format(x)
    c = 'table table-bordered'
    d = defaultdict(list)
    for n, mx in model.inspect('mx').items():
        d[n].append(mx.to_html(float_format=fmt, classes=c,
                               justify='center'))
    for n, mx in model.inspect('mx', what='start').items():
        d[n].append(mx.to_html(float_format=fmt, classes=c,
                               justify='center'))
    for n, mx in model.inspect('mx', what='name').items():
        d[n].append(mx.to_html(float_format=fmt, classes=c,
                               justify='center'))
    obs = model.vars['observed']
    sigma, _ = model.calc_sigma()
    cov = pd.DataFrame(model.mx_cov, columns=obs, index=obs)
    cov = cov.to_html(float_format=fmt, classes=c, justify='center')
    if hasattr(model, 'calc_l'):
        sigma = model.calc_l(sigma=sigma)
    sigma = pd.DataFrame(sigma, columns=obs, index=obs)
    sigma = sigma.to_html(float_format=fmt, classes=c, justify='center')
    matrices = '<center><h4>Covariance matrix</h4></center>\n'
    matrices += __start.format('cov')
    matrices += __navitem.format('sample', 'Sample', 'active', 'true')
    matrices += __navitem.format('modelimplied', 'Model-implied', '', 'false')
    matrices += __cont.format('cov')
    matrices += __tab.format('sample', cov, 'show active')
    matrices += __tab.format('modelimplied', sigma, '')
    matrices += __end
    matrices += '<br><center><h4>Model matrices</h4></center>'
    matrices += __start.format('modelmatrices')
    for i, n in enumerate(d.keys()):
        if i == 0:
            matrices += __navitem.format(f'mx{n}', n, 'active', 'true')
        else:
            matrices += __navitem.format(f'mx{n}', n, '', 'false')
    matrices += __cont.format('cov')
    for i, (n, mxs) in enumerate(d.items()):
        sub = __start.format(n + 'sub')
        for j, (mode, mx) in enumerate(zip(('Estimates', 'Start', 'Names'),
                                           mxs)):
            if j == 0:
                sub += __navitem.format(n + mode, mode, 'active', 'true')
            else:
                sub += __navitem.format(n + mode, mode, '', 'false')
        sub += __cont.format(name + 'sub')
        for j, (mode, mx) in enumerate(zip(('Estimates', 'Start', 'Names'),
                                           mxs)):
            if j == 0:
                sub += __tab.format(n + mode, mx, 'show active')
            else:
                sub += __tab.format(n + mode, mx, '')
        sub += __end
        if i == 0:
            matrices += __tab.format(f'mx{n}', sub, 'show active')
        else:
            matrices += __tab.format(f'mx{n}', sub, '')
    matrices += __end

    with open(__index, 'r') as f:
        html = f.read()
    html = html.format(ModelName=name, OptimizerReport=optresult,
                       ModelDescription=desc, VariableClassification=clasv,
                       NSamples=n_samples, ConvColor=color,
                       Converged=converged, Objective=obj,
                       Visualization=vis, Estimates=ests, Matrices=matrices,
                       InspectionTable=str(ins), FitIndices=fitindices,
                       Version=__version__, ModelClass=model_name)

    with open(os.path.join(path, 'report.html'), 'w') as f:
        f.write(html)
    css = os.path.join(path, 'css')
    if not os.path.isdir(css):
        os.mkdir(css)
    shutil.copy(__css, css)
    js = os.path.join(path, 'js')
    if not os.path.isdir(js):
        os.mkdir(js)
    shutil.copy(__js, js)
