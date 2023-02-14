# {{project_name}}

This is a basic supervised learning ML project built with the
ZenML framework and its scikit-learn integration. The project trains one or more
scikit-learn classification models to make predictions on one of the tabular
classification datasets provided by the scikit-learn library. The project was
generated from the [starter ZenML project template](https://github.com/zenml-io/zenml-project-templates/tree/main/starter)
with the following optional features enabled:
{%- if use_step_params == "y" %}
- parameterized ZenML steps
- ability to control the ZenML step parameters using the CLI
{%- if configurable_dataset == "y" %}
- ability to dynamically select and use a different dataset at runtime using the
CLI and/or a data loader step parameter
{%- endif %}
{%- if configurable_model == "y" %}
- ability to dynamically select and train a different classification model at
runtime using the CLI and/or a model trainer step parameter
{%- endif %}
{%- endif %}
{%- if use_custom_artifacts == "y" %}
- using custom data types for step artifacts and implementing custom materializers 
{%- endif %}

## 👋 Introduction

Welcome to your newly generated "{{project_name}}" project! This is
a great way to get started with ZenML. The project contains a collection of
basic ZenML steps, pipelines, stack configurations and other artifacts and
useful resources that can serve as a starting point for your journey with
ZenML.

What to do first? You can start by giving the the project a quick run. The
project is ready to be used and can run as-is without any further code
changes! You can try it right away by installing ZenML, the scikit-learn
ZenML integration and then calling the CLI included in the project. We also
recommend that you start the ZenML UI locally to get a better sense of what
is going on under the hood:

```bash
# Set up a Python virtual environment, if you haven't already
virtualenv .venv
source .venv/bin/activate
# Install requirements
pip install -r requirements.txt
# Start the ZenML UI locally (recommended, but optional);
# the default username is "admin" with an empty password
zenml up
# Run the pipeline included in the project
python run.py
```

When the pipeline is done running, you can check out the results in the ZenML
UI by following the link printed in the terminal (or you can go straight to
the [ZenML UI pipelines run page](http://127.0.0.1:8237/workspaces/default/all-runs?page=1).

Next, you should:

* look at the CLI help to see what you can do with the project:
```bash
python run.py --help
```
* go back and [try out different parameters](https://github.com/zenml-io/zenml-project-templates/tree/main/starter#-template-parameters)
for your generated project. For example, you could enable generating step
parameters or custom materializers for your project, if you haven't already. 
* take a look at [the project structure](#📜-project-structure) and the code
itself. The code is heavily commented and should be easy to follow.
* read the [ZenML documentation](https://docs.zenml.io) to learn more about
various ZenML concepts referenced in the code and to get a better sense of
what you can do with ZenML.
* start building your own ZenML project by modifying this code

## 📦 What's in the box?

The {{ project_name }} project showcases a basic ZenML model
training pipeline with all the usual components you would expect to find in
a simple machine learning project such as this one:

- a data ingestion step that loads one of the datasets provided through
scikit-learn
- a data processing step that does some basic preprocessing (drops rows with
missing values, normalizes the data)
- a data splitting step that breaks the data into train and test sets
- a training step that trains one of the scikit-learn models on the train set
- a model evaluation step that evaluates the trained model on the train and test
sets and warns or fails the pipeline if the model performance is below a
certain threshold

The project code is meant to be used as a template for your own projects. For
this reason, you will find a number of places in the code specifically marked
to indicate where you can add your own code:

```python
### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
...
### YOUR CODE ENDS HERE ###
```

## 📜 Project Structure

The project loosely follows [the recommended ZenML project structure](https://docs.zenml.io/guidelines/best-practices#recommended-repository-structure):

```
├── pipelines                   <- All pipelines in one place
│   ├── model_training.py       <- The main (training) pipeline
├── steps                       <- All steps in one place
│   ├── data_loaders.py         <- Data loader/processor/splitter steps
│   ├── model_trainers.py       <- Model trainer/evaluator steps
├── .dockerignore 
├── README.md                   <- This file
├── requirements.txt            <- Python dependencies  
└── run.py                      <- CLI entrypoint
```
