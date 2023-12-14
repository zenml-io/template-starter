# :running: MLOps 101 with ZenML

Build your first MLOps pipelines with ZenML.

## :earth_americas: Overview

This repository is a minimalistic MLOps project intended as a starting point to learn how to put ML workflows in production. It features: 

- A feature engineering pipeline that loads data and prepares it for training.
- A training pipeline that loads the preprocessed dataset and trains a model.
- A batch inference pipeline that runs predictions on the trained model with new data.

This is a representation of how it will all come together: 

<img src=".assets/pipeline_overview.png" width="70%" alt="Pipelines Overview">

Along the way we will also show you how to:

- Structure your code into MLOps pipelines
- Automatically version, track, and cache data, models, and other artifacts
- Transition your ML models from development to production

## 🏃 Run on Colab

You can use Google Colab to see ZenML in action, no signup / installation required!

<a href="https://colab.research.google.com/github/zenml-io/zenml/blob/main/examples/quickstart/run.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## :computer: Run Locally

To run locally, install ZenML and pull this quickstart:

```shell
# Install ZenML
pip install "zenml[server]"

# clone the ZenML repository
git clone https://github.com/zenml-io/zenml.git
cd zenml/examples/quickstart
```

### :arrow_forward: Run Locally
Now we're ready to start. You have two options for running the quickstart locally:

#### Option 1 (*Recommended*) - Interactively explore the quickstart using Jupyter Notebook:
```bash
pip install notebook
jupyter notebook
# open notebooks/quickstart.ipynb
```

#### Option 2 - Execute the whole ML pipeline from a Python script:
```bash
# Install required zenml integrations
zenml integration install sklearn -y

# Initialize ZenML
zenml init

# Start the ZenServer to enable dashboard access
zenml up

# Run the feature engineering pipeline
python run.py --feature-pipeline

# Run the training pipeline
python run.py --training-pipeline

# Run the training pipeline with versioned artifacts
python run.py --training-pipeline --train-dataset-version-name=1 --test-dataset-version-name=1

# Run the inference pipeline
python run.py --inference-pipeline
```

## 🌵 Learning MLOps

### 🥇 Step 1: Load your data and execute feature engineering

We'll start off by importing our data. In this quickstart we'll be working with
[the Breast Cancer](https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic) dataset
which is publicly available on the UCI Machine Learning Repository. The task is a classification
problem, to predict whether a patient is diagnosed with breast cancer or not.

When you're getting started with a machine learning problem you'll want to do
something similar to this: import your data and get it in the right shape for
your training.

<img src=".assets/feature_engineering_pipeline.png" width="30%" alt="Feature engineering pipeline" />

### ⌚ Step 2: Training pipeline

Now that we have our data it makes sense to train some models to get a sense of
how difficult the task is. The Breast Cancer dataset is sufficiently large and complex 
that it's unlikely we'll be able to train a model that behaves perfectly since the problem 
is inherently complex, but we can get a sense of what a reasonable baseline looks like.

We'll start with two simple models, a SGD Classifier and a Random Forest
Classifier, both batteries-included from `sklearn`. We'll train them both on the
same data and then compare their performance.

<img src=".assets/training_pipeline.png" width="30%" alt="Training pipeline">

### 💯 Step 3: Associating a model with your pipeline

You can see it is relatively easy to train ML models using ZenML pipelines. But it can be somewhat clunky to track
all the models produced as you develop your experiments and use-cases. Luckily, ZenML offers a *Model Control Plane*,
which is a central register of all your ML models.

You can easily create a ZenML `Model` and associate it with your pipelines using the `ModelVersion` object. The interesting part is that ZenML goes ahead and links all artifacts produced by the
pipelines to that model version, including the two pickle files that represent our
SGD and RandomForest classifier. We can see all artifacts directly from the model
version object.

If you are a [ZenML Cloud](https://zenml.io/cloud) user, you can see all of this visualized in the dashboard:

<img src=".assets/cloud_mcp_screenshot.png" width="70%" alt="Model Control Plane">

There is a lot more you can do with ZenML models, including the ability to
track metrics by adding metadata to it, or having them persist in a model
registry. However, these topics can be explored more in the
[ZenML docs](https://docs.zenml.io).

For now, we will use the ZenML model control plane to promote our best
model to `production`. You can do this by simply setting the `stage` of
your chosen model version to the `production` tag.

Of course, normally one would only promote the model by comparing to all other model
versions and doing some other tests. But that's a bit more advanced use-case. See the
[e2e_batch example](https://github.com/zenml-io/zenml/tree/main/examples/e2e) to get
more insight into that sort of flow!

<img src=".assets/cloud_mcp.png" width="60%" alt="Model Control Plane">

Once the model is promoted, we can now consume the right model version in our
batch inference pipeline directly. Let's see how that works.

The batch inference pipeline simply takes the model marked as `production` and runs inference on it
with `live data`. The critical step here is the `inference_predict` step, where we load the model in memory and generate predictions. Apart from the loading the model, we must also load the preprocessing pipeline that we ran in feature engineering,
so that we can do the exact steps that we did on training time, in inference time. Let's bring it all together:

<img src=".assets/inference_pipeline.png" width="45%" alt="Inference pipeline">

ZenML automatically links all artifacts to the `production` model version as well, including the predictions
that were returned in the pipeline. This completes the MLOps loop of training to inference:

You can also see all predictions ever created as a complete history in the dashboard:

<img src=".assets/cloud_mcp_predictions.png" width="70%" alt="Model Control Plane">

### 🫅 Step 4: Consuming the model in production

## :bulb: Learn More

You're a legit MLOps engineer now! You trained two models, evaluated them against
a test set, registered the best one with the ZenML model control plane,
and served some predictions. You also learned how to iterate on your models and
data by using some of the ZenML utility abstractions. You saw how to view your
artifacts and stacks via the client as well as the ZenML Dashboard.

If you want to learn more about ZenML as a tool, then the 
[:page_facing_up: **ZenML Docs**](https://docs.zenml.io/) are the perfect place 
to get started.

Already have an MLOps stack in mind? ZenML most likely has
[**:link: Integrations**](https://docs.zenml.io/stacks-and-components/component-guide) 
for whatever tools you plan to use.

Also, make sure to join our <a href="https://zenml.io/slack" target="_blank">
    <img width="15" src="https://cdn3.iconfinder.com/data/icons/logos-and-brands-adobe/512/306_Slack-512.png" alt="Slack"/>
    <b>Slack Community</b> 
</a> to become part of the ZenML family!