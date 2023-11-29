# {% include 'template/license_header' %}

from typing_extensions import Annotated

import pandas as pd
from sklearn.base import ClassifierMixin
from zenml import ArtifactConfig, log_artifact_metadata, step
from zenml.client import Client
from zenml.logger import get_logger

logger = get_logger(__name__)


@step
def model_trainer(
    dataset_trn: pd.DataFrame,
    model: ClassifierMixin,
    target: str,
    name: str,
) -> Annotated[
    ClassifierMixin, ArtifactConfig(name="model", is_model_artifact=True)
]:
    """Configure and train a model on the training dataset.

    This is an example of a model training step that takes in a dataset artifact
    previously loaded and pre-processed by other steps in your pipeline, then
    configures and trains a model on it. The model is then returned as a step
    output artifact.

    Model training steps should have caching disabled if they are not
    deterministic (i.e. if the model training involve some random processes
    like initializing weights or shuffling data that are not controlled by
    setting a fixed random seed). This example step ensures the outcome is
    deterministic by initializing the model with a fixed random seed.

    This step is parameterized to configure the step independently of the step code,
    before running it in a pipeline. In this example, the step can be configured
    to use a different model, change the random seed, or pass different
    hyperparameters to the model constructor. See the documentation for more
    information:

        https://docs.zenml.io/user-guide/advanced-guide/configure-steps-pipelines

    Args:
        dataset_trn: The preprocessed train dataset.
        model: The model instance to train.
        target: Name of target columns in dataset.
        name: The name of the model.

    Returns:
        The trained model artifact.
    """

    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
    # Initialize the model with the hyperparameters indicated in the step
    # parameters and train it on the training set.
    logger.info(f"Training model {model}...")
    model.fit(
        dataset_trn.drop(columns=[target]),
        dataset_trn[target],
    )

    # keep track of mlflow version for future use
    model_registry = Client().active_stack.model_registry
    if model_registry:
        versions = model_registry.list_model_versions(name=name)
        if versions:
            log_artifact_metadata(
                metadata={"model_registry_version": versions[-1].version},
                artifact_name="model",
            )
    ### YOUR CODE ENDS HERE ###

    return model
