# {% include 'template/license_header' %}

from uuid import UUID
from typing import List, Optional

from steps import (
    data_loader,
    inference_preprocessor,
    inference_predict,
)
from zenml import pipeline, ArtifactVersionResponse, get_pipeline_context
from zenml.client import Client
from zenml.logger import get_logger

logger = get_logger(__name__)


@pipeline
def inference():
    """
    Model inference pipeline.
    
    This is a pipeline that loads the inference data, processes it with
    the same preprocessing pipeline used in training, and runs inference
    with the trained model.
    """
    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
    client = Client()
    
    # Get the production model artifact
    model: ArtifactVersionResponse = get_pipeline_context().model_version.get_artifact("model")
        
    # Get the preprocess pipeline artifact associated with this version
    preprocess_pipeline: ArtifactVersionResponse = get_pipeline_context().model_version.get_artifact("preprocess_pipeline")

    # Use the metadata of feature engineering pipeline artifact
    #  to get the random state and target column
    random_state = client.get_artifact_version(preprocess_pipeline.id).run_metadata["random_state"].value
    target = client.get_artifact_version(preprocess_pipeline.id).run_metadata['target'].value

    # Link all the steps together by calling them and passing the output
    #  of one step as the input of the next step.
    df_inference = data_loader(random_state=random_state, is_inference=True)
    df_inference = inference_preprocessor(
        dataset_inf=df_inference,
        preprocess_pipeline=preprocess_pipeline,
        target=target,
    )
    inference_predict(
        model=model,
        dataset_inf=df_inference,
    )
    ### END CODE HERE ###
