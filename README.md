# 📜 ZenML Project Templates

This repository contains a collection of templates from which a ZenML project
can be generated: a collection of steps, pipelines, stack configurations and
other artifacts and useful resources that can get you started with ZenML.

🔥 **Do you have a personal project powered by ZenML that you would like to see here ?** At
ZenML, we are looking for design partnerships and collaboration to help us
better understand the real-world scenarios in which MLOps is being used and to
build the best possible experience for our users. If you are interested in
sharing all or parts of your project with us in the form of a ZenML project
template, please [join our Slack](https://zenml.io/slack-invite/) and leave us a
message!

## 📦 Prerequisites

To use the templates, you need to have cookieninja installed, along with the
ansible Jinja2 filter library. You can install them by running:

```bash
pip install cookieninja jinja2-ansible-filters
```

## 🚀 Generate a ZenML Project

You can generate a project from one of the existing templates by running e.g.:

```bash
cookieninja gh:zenml-io/zenml-project-templates --directory=starter
```

where `starter` is the name of the template you want to use.

You will be prompted to enter various values for the template variables. Once
you have entered them, the project will be generated in a subdirectory.

## 📃 List of Project Templates

| Project Template | Tags     | Description                                                                       |
|------------------|----------|-----------------------------------------------------------------------------------|
| [starter](https://github.com/zenml-io/zenml-project-templates/tree/main/starter) | basic scikit-learn | All the basic ML ingredients you need to get you started with ZenML: parameterized steps, a model training pipeline, a flexible configuration and a simple CLI. All created around a representative and versatile model training use-case implemented with the scikit-learn library. |
