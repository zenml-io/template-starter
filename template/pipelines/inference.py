# {% include 'template/license_header' %}

from typing import List, Optional

from steps import (
    data_loader,
)
from zenml import pipeline
from zenml.logger import get_logger

logger = get_logger(__name__)


@pipeline
def _inference(
    test_size: float = 0.2,
    drop_na: Optional[bool] = None,
    normalize: Optional[bool] = None,
    drop_columns: Optional[List[str]] = None,
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
    random_state = client.get_artifact("dataset").run_metadata["random_state"].value
    target = client.get_artifact("dataset_trn").run_metadata["target"].value
    df_inference = data_loader(random_state=random_state, is_inference=True)
    df_inference = inference_preprocessor(
        dataset_inf=df_inference,
        preprocess_pipeline=ExternalArtifact(name="preprocess_pipeline"),
        target=target,
    )
    inference_predict(
        dataset_inf=df_inference,
    )


@pipeline
def _batch_inference():
    """
    Model batch inference pipeline.

    This is a pipeline that loads the inference data, processes
    it, analyze for data drift and run inference.
    """
    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
    # Link all the steps together by calling them and passing the output
    # of one step as the input of the next step.
    ########## ETL stage  ##########
    random_state = client.get_artifact("dataset").run_metadata["random_state"].value
    target = client.get_artifact("dataset_trn").run_metadata["target"].value
    df_inference = data_loader(random_state=random_state, is_inference=True)
    df_inference = inference_preprocessor(
        dataset_inf=df_inference,
        preprocess_pipeline=ExternalArtifact(name="preprocess_pipeline"),
        target=target,
    )
    inference_predict(
        dataset_inf=df_inference,
    )
