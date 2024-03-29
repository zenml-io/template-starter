# 📜 ZenML Starter Template

This repository contains a starter template from which a simple ZenML project
can be generated easily. It contains a collection of steps, pipelines, stack configurations and
other artifacts and useful resources that can get you started with ZenML.

🔥 **Do you have a personal project powered by ZenML that you would like to see here?** 

At ZenML, we are looking for design partnerships and collaboration to help us
better understand the real-world scenarios in which MLOps is being used and to
build the best possible experience for our users. If you are interested in
sharing all or parts of your project with us in the form of a ZenML project
template, please [join our Slack](https://zenml.io/slack/) and leave us a
message!

## 📦 Prerequisites

To use the templates, you need to have Zenml and its `templates` extras
installed: 

```bash
pip install "zenml[templates]"
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
copier gh:zenml-io/template-starter <directory>
```

You will be prompted to select the project template and enter various values for
the template variables. Once you have entered them, the project will be
generated in the indicated path.

To update an already generated project, with different parameters you can run
the same command again. If you want to skip the prompts to use the values you
already entered and overwrite all files in the existing project, you can run:

```bash
copier -wf gh:zenml-io/template-starter <directory>
```
