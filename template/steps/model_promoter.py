# {% include 'template/license_header' %}

from zenml import get_step_context, step
from zenml.logger import get_logger

logger = get_logger(__name__)


@step
def model_promoter(accuracy: float, stage: str = "production") -> bool:
    """Model promoter step.

    This is an example of a step that conditionally promotes a model.

    This step is parameterized, which allows you to configure the step
    independently of the step code, before running it in a pipeline.
    In this example, the step can be configured with the accuracy of the model
    and the target stage:

        https://docs.zenml.io/user-guide/advanced-guide/configure-steps-pipelines

    Args:
        accuracy: Accuracy of the model.
        stage: Which stage to promote the model to.

    Returns:
        Whether the model was promoted or not.
    """
    if accuracy < 0.8:
        logger.info(
            f"Model accuracy {accuracy*100:.2f}% is below 80% ! Not promoting model."
        )
        is_promoted = False
    else:
        logger.info(f"Model promoted to {stage}!")
        is_promoted = True
        model_version = get_step_context().model_version
        model_version.set_stage(stage, force=True)

    return is_promoted
