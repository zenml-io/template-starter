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
def inference(random_state: str, target: str):
    """
    Model inference pipeline.
    
    This is a pipeline that loads the inference data, processes it with
    the same preprocessing pipeline used in training, and runs inference
    with the trained model.
    """
    # Get the production model artifact
    model = get_pipeline_context().model_version.get_artifact("model")
        
    # Get the preprocess pipeline artifact associated with this version
    preprocess_pipeline = get_pipeline_context().model_version.get_artifact("preprocess_pipeline")

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
