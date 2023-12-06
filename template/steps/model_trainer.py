# {% include 'template/license_header' %}

import pandas as pd
from sklearn.base import ClassifierMixin
from sklearn.tree import DecisionTreeClassifier
from typing_extensions import Annotated
from zenml import ArtifactConfig, step
from zenml.logger import get_logger

logger = get_logger(__name__)


@step(enable_cache=False) #, step_operator="sagemaker-eu")
def model_trainer(
    dataset_trn: pd.DataFrame,
) -> Annotated[ClassifierMixin, ArtifactConfig(name="model", is_model_artifact=True)]:
    """Configure and train a model on the training dataset.

    This is an example of a model training step that takes in a dataset artifact
    previously loaded and pre-processed by other steps in your pipeline, then
    configures and trains a model on it. The model is then returned as a step
    output artifact.

    Args:
        dataset_trn: The preprocessed train dataset.
        target: The name of the target column in the dataset.

    Returns:
        The trained model artifact.
    """

    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###

    # Use the dataset to fetch the target
    # context = get_step_context()
    # target = context.inputs["dataset_trn"].run_metadata['target'].value
    target = "target"

    # Initialize the model with the hyperparameters indicated in the step
    # parameters and train it on the training set.
    model = DecisionTreeClassifier()
    logger.info(f"Training model {model}...")

    model.fit(
        dataset_trn.drop(columns=[target]),
        dataset_trn[target],
    )
    ### YOUR CODE ENDS HERE ###

    return model
