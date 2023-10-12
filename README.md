# 📜 ZenML Starter Project Template

What would you need to get a quick understanding of the ZenML framework and
start building your own ML pipelines? The answer is a simple project template
to cover the basics of ZenML: a collection of steps and pipelines, a stack
configuration and, to top it all off, a simple but useful CLI. This is exactly
what the ZenML starter template is all about.

This project template is a good starting point for anyone starting out with
ZenML. It showcases the following fundamental ZenML concepts in a relatable
ML context:

* Designing [ZenML pipeline steps](https://docs.zenml.io/user-guide/starter-guide#pipelines-and-steps)
in general, but also particularly useful for the following applications:
    * Data ingestion, data transformation and data train/test splitting
    * >odel training and evaluation
* Using [step parameterization and caching](https://docs.zenml.io/user-guide/starter-guide/cache-previous-executions)
to design flexible and reusable steps
* Using [custom data types for your artifacts and writing materializers for them](https://docs.zenml.io/user-guide/advanced-guide/artifact-management/handle-custom-data-types)
* Constructing and running a [ZenML pipeline](https://docs.zenml.io/user-guide/starter-guide#pipelines-and-steps)
* Accessing ZenML pipeline run artifacts in [the post-execution phase](https://docs.zenml.io/user-guide/starter-guide/fetch-runs-after-execution),
after a pipeline run has concluded
* Best practices for implementing and running reproducible and reliable ML
pipelines with ZenML

In addition to that, the entire project is implemented with the [scikit-learn](https://scikit-learn.org)
library and showcases how to use ZenML with a popular ML framework. It makes
heavy use of the tabular datasets and classification models that scikit-learn
provides, but the concepts and patterns it showcases are applicable to any
other ML framework.

## 📃 Template Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| Name | The name of the person/entity holding the copyright | ZenML GmbH |
| Email | The email of the person/entity holding the copyright | info@zenml.io |
| Project Name | Short name for your project | ZenML Starter |
| Project Slug | A slugified version of the project name (automatically generated from the project name) | zenml_starter |
| Project Version | The version of your project | 0.1.0 |
| Project License | The license under which your project will be released (one of `Apache Software License 2.0`, `MIT license`, `BSD license`, `ISC license`, `GNU General Public License v3` and `Not open source`) | Apache Software License 2.0 |
| Auto-Format | Whether to automatically format and cleanup the generated code with [black](https://black.readthedocs.io/), [ruff](https://beta.ruff.rs/docs/) and [autoflake](https://github.com/PyCQA/autoflake) (yes/no). You also need to have these Python packages installed for this option to take effect. | no |
| Use ZenML Step Params | Whether to showcase using parameters for the ZenML steps in the project (yes/no). If selected, all generated ZenML pipeline steps will be parameterized. | yes |
| Use ZenML Materializers | Whether to showcase using custom data types for the ZenML artifacts in the project (yes/no). If selected, the generated code will demonstrate the use of custom artifact data types and materializers in the generated steps and pipelines. | yes |
| UCI Dataset | The name of the UCI provided scikit-learn dataset to use in the project (one of `Iris`, `Breast Cancer` and `Wine`) | Wine |
| Scikit-learn Model | The name of the scikit-learn classifier model to use in the project (one of `Logistic Regression`, `SVC`, `Linear SVC`, `Random Forest`, `KNN`, `Gaussian NB`, `Perceptron`, `SGD Classifier` and `Decision Tree`) | Logistic Regression |
| Runtime Configurable Dataset | Whether to make the dataset a configurable parameter of the data loader step and CLI (yes/no). Only has effect if the step parameters were also selected. | yes |
| Runtime Configurable Model | Whether to make the model a configurable parameter of the model trainer step and CLI (yes/no). Only has effect if the step parameters were also selected. | yes |

## 🚀 Generate the Project

### 📦 Prerequisites

To use the templates, you need to have Zenml and its `templates` extras
installed: 

```bash
pip install zenml[templates]
```

### 🚀 Generate a ZenML Project

You can generate a project byusing the `--template` flag with the `zenml init` command:

```bash
zenml init --template starter
```

Under the hood, ZenML uses the popular [Copier](https://copier.readthedocs.io/en/stable/)
library and a set of Jinja2 templates to generate the project. So you may also
interact with Copier directly to generate a project, e.g.:

```bash
copier gh:zenml-io/template-starter <directory>
```

You will be prompted to enter various values for
the template variables. Once you have entered them, the project will be
generated in the indicated path.