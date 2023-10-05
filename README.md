# THIS REPOSITORY WILL BE DEPRECATED AFTER 01/10/2023. 

# 📜 ZenML Project Templates

This repository contains a collection of templates from which a ZenML project
can be generated: a collection of steps, pipelines, stack configurations and
other artifacts and useful resources that can get you started with ZenML.

🔥 **Do you have a personal project powered by ZenML that you would like to see here?** At
ZenML, we are looking for design partnerships and collaboration to help us
better understand the real-world scenarios in which MLOps is being used and to
build the best possible experience for our users. If you are interested in
sharing all or parts of your project with us in the form of a ZenML project
template, please [join our Slack](https://zenml.io/slack-invite/) and leave us a
message!

## 📦 Prerequisites

To use the templates, you need to have Zenml and its `templates` extras
installed: 

```bash
pip install zenml[templates]
```

## 🚀 Generate a ZenML Project

You can generate a project from one of the existing templates by using the
`--template` flag with the `zenml init` command:

```bash
zenml init --template
```

Under the hood, ZenML uses the popular [Copier](https://copier.readthedocs.io/en/stable/)
library and a set of Jinja2 templates to generate the project. So you may also
interact with Copier directly to generate a project, e.g.:

```bash
copier gh:zenml-io/zenml-project-templates <directory>
```

You will be prompted to select the project template and enter various values for
the template variables. Once you have entered them, the project will be
generated in the indicated path.

To update an already generated project, with different parameters you can run
the same command again. If you want to skip the prompts to use the values you
already entered and overwrite all files in the existing project, you can run:

```bash
copier -wf gh:zenml-io/zenml-project-templates <directory>
```

## 📃 List of Project Templates

| Project Template | Tags     | Description                                                                       |
|------------------|----------|-----------------------------------------------------------------------------------|
| [ZenML Starter](https://github.com/zenml-io/zenml-project-templates/tree/main/starter) | basic scikit-learn | All the basic ML ingredients you need to get you started with ZenML: parameterized steps, a model training pipeline, a flexible configuration and a simple CLI. All created around a representative and versatile model training use-case implemented with the scikit-learn library. |
