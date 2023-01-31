# 📜 ZenML Starter Project Template

What would you need to get a quick understanding of the ZenML framework and
start building your own ML pipelines? The answer is a simple project template
to cover the basics of ZenML: a collection of steps and pipelines, a stack
configuration and, to top it all off, a simple but useful CLI. This is exactly
what the ZenML starter template is all about.

This project template is a good starting point for anyone starting out with
ZenML. It showcases the following fundamental ZenML concepts in a relatable
ML context:

* designing [ZenML pipeline steps](https://docs.zenml.io/starter-guide/pipelines#step)
in general, but also particularly useful for the following applications:
    * data ingestion, data transformation and data train/test splitting
    * model training and evaluation
* using [step parameterization and caching](https://docs.zenml.io/starter-guide/pipelines/parameters-and-caching)
to design flexible and reusable steps
* using [custom data types for your artifacts and writing materializers for them](https://docs.zenml.io/advanced-guide/pipelines/materializers)
* constructing and running a [ZenML pipeline](https://docs.zenml.io/starter-guide/pipelines#pipeline)
* accessing ZenML pipeline run artifacts in [the post-execution phase](https://docs.zenml.io/starter-guide/pipelines/fetching-pipelines),
after a pipeline run has concluded
* best practices for implementing and running reproducible and reliable ML
pipelines with ZenML

In addition to that, the entire project is implemented with the [scikit-learn](https://scikit-learn.org)
library and showcases how to use ZenML with a popular ML framework. It makes
heavy use of the tabular datasets and classification models that scikit-learn
provides, but the concepts and patterns it showcases are applicable to any
other ML framework.

## 📃 Template Parameters

| Parameter | Description | Default |
|------------------|-----------------------------------------------------------------------------------|--|
| full_name | Your name or the name of your organization (shown in the generated license) | ZenML GmbH |
| email | Your email address (shown in the generated license) | info@zenml.io |
| project_name | A name for your project | ZenML Starter |
| project_slug | A slugified version of the project name (automatically generated from the project name) | zenml_starter |
| project_short_description | A short description of your project | |
| version | The version of your project | 0.1.0 |
| open_source_license | The license under which your project will be released (one of `Apache Software License 2.0`, `MIT license`, `BSD license`, `ISC license`, `GNU General Public License v3` and `Not open source`) | Apache Software License 2.0 |
| use_step_params | Whether to showcase using parameters for the ZenML steps in the project (`y` or `n`). If selected, all generated ZenML pipeline steps will be parameterized. | n |
| use_custom_artifacts | Whether to showcase using custom data types for the ZenML artifacts in the project (`y` or `n`). If selected, the generated code will demonstrate the use of custom artifact data types and materializers in the generated steps and pipelines. | n |
| sklearn_dataset_name | The name of the builtin scikit-learn dataset to use in the project (one of `Iris`, `Breast Cancer` and `Wine`) | Wine |
| sklearn_model_name | The name of the builtin scikit-learn model to use in the project (one of `Logistic Regression`, `SVC`, `Linear SVC`, `Random Forest`, `KNN`, `Gaussian NB`, `Perceptron`, `SGD Classifier` and `Decision Tree`) | Logistic Regression |
| configurable_dataset | Whether to make the dataset a configurable parameter of the data loader step and CLI (`y` or `n`). Only has effect if the step parameters were also selected. | n |
| configurable_model | Whether to make the model a configurable parameter of the model trainer step and CLI (`y` or `n`). Only has effect if the step parameters were also selected. | n |
| auto_format | Whether to automatically format and cleanup the generated code with [black](https://black.readthedocs.io/), [ruff](https://beta.ruff.rs/docs/) and [autoflake](https://github.com/PyCQA/autoflake) (`y` or `n`). You also need to have these Python packages installed for this option to take effect. | n |


## 📦 Prerequisites

To use the template, you need to have cookieninja installed, along with the
ansible Jinja2 filter library. You can install them by running:

```bash
pip install cookieninja jinja2-ansible-filters
```

If you also want to cleanup and format the generated project code, to avoid
any code style issues that might be left behind by the code generation
process (recommended), you will need to install the following additional
dependencies:

```bash
pip install black ruff autoflake
```

You can enable the automatic cleanup and formatting by setting the
`auto_format` parameter to `y` when generating the project.

## 🚀 Generate a ZenML Project

You can generate a project from this templates by running:

```bash
cookieninja gh:zenml-io/zenml-project-templates --directory=starter
```

You will be prompted to enter various values for the template variables. Once
you have entered them, the project will be generated in a subdirectory.
