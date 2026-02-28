# semopy
[Visit our website for a detailed introduction](https://semopy.com)


**semopy** is a Python package that includes numerous Structural Equation Modelling (SEM) techniques. 

## Features
  - Write down a model description in a user-friendly syntax
  - Estimate model's parameters using a variety of objective functions
  - Estimate models with population structure via random effects
  - Restricted Maximum Likelihood
  - Integration with gaussian processes/mixture models to tackle huge variety of phenomena
  - Calculate numerous statistics and fit indices
  - Estimate model's parameters in presence of ordinal variables
  - A vast number of settings to fit a researcher's needs
  - Fast and accurate
  - Automatically create fancy HTML reports

## Installation
**semopy** is available at PyPi and can be installed by typing the following line into terminal:

`pip install semopy`


## Syntax
To specify SEM models, The **semopy** uses the syntax, which is natural to describe regression models in R. The syntax supports three operator symbols characterising relationships between variables:

- ~ to specify structural part,
- =~ to specify measurement part,
- ~~ to specify common variance between variables.

For example, let a linear equation in the structural part of SEM model take the form:

`y = β1 x1 + β2 x2 + ε` 

Then, in **semopy** syntax it becomes:

`y ~ x1 + x2`

Parameters β1, β2 are to be estimated by **semopy**. In some cases a user might want to fix some of parameters to particular value. For instance, let's assume that we want Î²1 to stay equal to 2.0 and we are only interested in estimating β2:

`y ~ 2*x1 + x2`


Likewise, if a latent variable Î· is explained by manifest variables y1, y2, y3, then in **semopy** syntax it can be written down this way:

`eta =~ y1 + y2 + y3`

## Quickstart

The pipeline for working with SEM models in **semopy** consists of three steps:
1. Specifying a model
2. Loading a dataset.
3. Estimating parameters of the model.

Main object required for scpecifying and estimating an SEM model is `Model`.

`Model` is responsible for setting up a model from the proposed SEM syntax:
~~~
# The first step
from semopy import Model
mod = """ x1 ~ x2 + x3
          x3 ~ x2 + eta1
          eta1 =~ y1 + y2 + y3
          eta1 ~ x1
      """
model = Model(mod)
~~~
Then a dataset should be provided:
~~~
# The second step
from pandas import read_csv
data = read_csv("my_data_file.csv", index_col=0)
~~~


To estimate parameters of the model we run a `fit` method with the dataset as an argument:
~~~
# The third step
model.fit(data)
~~~

The default objective function for estimating parameters is the likelihood function and the optimisation method is SLSQP (Sequential Least-Squares Quadratic Programming). However, the *semopy* supports a wide range of other objective functions and optimisation schemes being specified as parameters in the `fit` method.

Finally, user can `inspect` parameters' estimates:

~~~
model.inspect()
~~~
## Would you like to know more?
Tutorial and overview of **semopy** features are available at the [project's website](https://semopy.com).

## Requirements
**numpy**, **pandas**, **scipy**, **sympy**, **sklearn**, **statmodels**
## Authors

* **Mescheryakov A. Georgy** - *Developer* - [georgy.m](https://gitlab.org/georgy.m) - student, SPbPU
* **Igolkina A. Anna** - *Supervisor* - [iganna](https://github.com/iganna) - Engineer, SPbPU

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.