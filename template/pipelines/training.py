# {% include 'template/license_header' %}

from typing import Optional

from zenml import pipeline
from zenml.logger import get_logger
from uuid import UUID


from steps import model_trainer, model_evaluator

from pipelines import (
    _feature_engineering,
)

from zenml import ExternalArtifact
from zenml.client import Client


logger = get_logger(__name__)


@pipeline
def _training(
    train_dataset_id: Optional[UUID] = None,
    test_dataset_id: Optional[UUID] = None,
    min_train_accuracy: float = 0.0,
    min_test_accuracy: float = 0.0,
):
    """
    Model training pipeline.

    This is a pipeline that loads the data, processes it and splits
    it into train and test sets, then search for best hyperparameters,
    trains and evaluates a model.

    Args:
        test_size: Size of holdout set for training 0.0..1.0
        drop_na: If `True` NA values will be removed from dataset
        normalize: If `True` dataset will be normalized with MinMaxScaler
        drop_columns: List of columns to drop from dataset
    """
    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
    # Link all the steps together by calling them and passing the output
    # of one step as the input of the next step.

    # Execute Feature Engineering Pipeline
    if train_dataset_id is None or test_dataset_id is None:
        dataset_trn, dataset_tst = _feature_engineering()
    else:
        dataset_trn = ExternalArtifact(id=train_dataset_id)
        dataset_tst = ExternalArtifact(id=test_dataset_id)

    # Use the metadata of the dataset to understand what the target is
    client = Client()
    target = client.get_artifact("dataset_trn").run_metadata["target"].value

    model = model_trainer(
        dataset_trn=dataset_trn,
        target=target,
    )

    model_evaluator(
        model=model,
        dataset_trn=dataset_trn,
        dataset_tst=dataset_tst,
        min_train_accuracy=min_train_accuracy,
        min_test_accuracy=min_test_accuracy,
        target=target,
    )
