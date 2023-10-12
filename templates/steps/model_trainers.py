{% include 'templates/license_header' %}

{%- if use_step_params %}
from typing import Any, Dict
{%- endif %}
import pandas as pd

from sklearn.base import ClassifierMixin
{%- if use_step_params and configurable_model %}
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier
{%- elif sklearn_model_name == 'LogisticRegression' %}
from sklearn.linear_model import LogisticRegression
{%- elif sklearn_model_name == 'SVC' %}
from sklearn.svm import SVC
{%- elif sklearn_model_name == 'LinearSVC' %}
from sklearn.svm import LinearSVC
{%- elif sklearn_model_name == 'RandomForestClassifier' %}
from sklearn.ensemble import RandomForestClassifier
{%- elif sklearn_model_name == 'KNeighborsClassifier' %}
from sklearn.neighbors import KNeighborsClassifier
{%- elif sklearn_model_name == 'GaussianNB' %}
from sklearn.naive_bayes import GaussianNB
{%- elif sklearn_model_name == 'Perceptron' %}
from sklearn.linear_model import Perceptron
{%- elif sklearn_model_name == 'SGDClassifier' %}
from sklearn.linear_model import SGDClassifier
{%- elif sklearn_model_name == 'DecisionTreeClassifier' %}
from sklearn.tree import DecisionTreeClassifier
{%- endif %}
{% if use_custom_artifacts %}
from artifacts import ModelMetadata
from materializers import ModelMetadataMaterializer
{%- endif %}

{%- if use_step_params %}
from zenml.enums import StrEnum
{%- endif %}
from zenml.logger import get_logger
from zenml.steps import (
{%- if use_step_params %}
    BaseParameters,
{%- endif %}
    Output,
    step,
)

logger = get_logger(__name__)

{% if use_step_params %}
{%- if configurable_model %}
class SklearnClassifierModel(StrEnum):
    """Scikit-learn models used for classification."""
    LogisticRegression = "LogisticRegression"
    SVC = "SVC"
    LinearSVC = "LinearSVC"
    RandomForestClassifier = "RandomForestClassifier"
    KNeighborsClassifier = "KNeighborsClassifier"
    GaussianNB = "GaussianNB"
    Perceptron = "Perceptron"
    SGDClassifier = "SGDClassifier"
    DecisionTreeClassifier = "DecisionTreeClassifier"
{%- endif %}

class ModelTrainerStepParameters(BaseParameters):
    """Parameters for the model trainer step.

    This is an example of how to use step parameters to make your model trainer
    step configurable independently of the step code. This is useful for example
    if you want to try out different models in your pipeline without having to
    change the step code.
    """

    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
{%- if configurable_model %}
    # The name of the scikit-learn classifier model to train.
    model: SklearnClassifierModel = SklearnClassifierModel.{{ sklearn_model_name }}
{%- endif %}
    # The random seed to use for reproducibility.
    random_state: int = 42
    # The parameters to pass to the model constructor.
    hyperparameters: Dict[str, Any] = {}
    ### YOUR CODE ENDS HERE ###

    class Config:
        """Pydantic config class.
        
        This is used to configure the behavior of Pydantic, the library used to
        parse and validate step parameters. See the documentation for more
        information:

            https://pydantic-docs.helpmanual.io/usage/model_config/

        It is recommended to explicitly forbid extra parameters here to ensure
        that the step parameters are always valid.
        """
        extra = "forbid"


@step
def model_trainer(
    params: ModelTrainerStepParameters,
    train_set: pd.DataFrame,
) -> ClassifierMixin:
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
    
    This step is parameterized using the `ModelTrainerStepParameters` class,
    which allows you to configure the step independently of the step code,
{%- if configurable_model %}
    before running it in a pipeline. In this example, the step can be configured
    to use a different model, change the random seed, or pass different
    hyperparameters to the model constructor. See the documentation for more
    information:
{%- else %}
    before running it in a pipeline. In this example, the step can be configured
    to change the random seed, or pass different hyperparameters to the model
    constructor. See the documentation for more information:
{%- endif %}

        https://docs.zenml.io/user-guide/starter-guide/cache-previous-executions

    Args:
        params: The parameters for the model trainer step.
        train_set: The training data set artifact.

    Returns:
        The trained model artifact.
    """
    X_train = train_set.drop("target", axis=1)
    Y_train = train_set["target"]

    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
    # Initialize the model with the hyperparameters indicated in the step
    # parameters and train it on the training set.
{%- if configurable_model %}
    if params.model == SklearnClassifierModel.LogisticRegression:
        model = LogisticRegression(
            random_state=params.random_state,
            **params.hyperparameters,
        )
    elif params.model == SklearnClassifierModel.SVC:
        model = SVC(
            random_state=params.random_state,
            **params.hyperparameters,
        )
    elif params.model == SklearnClassifierModel.LinearSVC:
        model = LinearSVC(
            random_state=params.random_state,
            **params.hyperparameters,
        )
    elif params.model == SklearnClassifierModel.RandomForestClassifier:
        model = RandomForestClassifier(
            random_state=params.random_state,
            **params.hyperparameters,
        )
    elif params.model == SklearnClassifierModel.KNeighborsClassifier:
        model = KNeighborsClassifier(**params.hyperparameters)
    elif params.model == SklearnClassifierModel.GaussianNB:
        model = GaussianNB(**params.hyperparameters)
    elif params.model == SklearnClassifierModel.Perceptron:
        model = Perceptron(
            random_state=params.random_state,
            **params.hyperparameters,
        )
    elif params.model == SklearnClassifierModel.SGDClassifier:
        model = SGDClassifier(
            random_state=params.random_state,
            **params.hyperparameters
        )
    elif params.model == SklearnClassifierModel.DecisionTreeClassifier:
        model = DecisionTreeClassifier(
            random_state=params.random_state,
            **params.hyperparameters,
        )
{%- else %}
{%- if not sklearn_model_name in [ 'KNeighborsClassifier', 'GaussianNB' ] %}
    model = {{ sklearn_model_name }}(random_state=42, **params.hyperparameters)
{%- else %}
    model = {{ sklearn_model_name }}(**params.hyperparameters)
{%- endif %}
{%- endif %}

    logger.info(f"Training model {model}...")
    model.fit(X_train, Y_train)
    ### YOUR CODE ENDS HERE ###

    return model


class ModelEvaluatorStepParameters(BaseParameters):
    """Parameters for the model evaluator step.

    This is an example of how to use step parameters to make your model
    evaluator step configurable independently of the step code. This is useful
    for example if you want to control the acceptable thresholds for your model
    metrics in your pipeline without having to change the step code.
    """

    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
    # The minimum acceptable accuracy on the train set.
    min_train_accuracy: float = 0.8
    # The minimum acceptable accuracy on the test set.
    min_test_accuracy: float = 0.8
    # The maximum acceptable difference between train and test accuracy.
    max_train_test_accuracy_difference: float = 0.1
    # Whether to raise an error and fail the pipeline step if the model
    # performance does not meet the minimum criteria.
    fail_on_warnings: bool = False
    ### YOUR CODE ENDS HERE ###

    class Config:
        """Pydantic config class.
        
        This is used to configure the behavior of Pydantic, the library used to
        parse and validate step parameters. See the documentation for more
        information:

            https://pydantic-docs.helpmanual.io/usage/model_config/

        It is recommended to explicitly forbid extra parameters here to ensure
        that the step parameters are always valid.
        """
        extra = "forbid"


@step
{%- if use_custom_artifacts -%}
(output_materializers=ModelMetadataMaterializer)
{%- endif %}
def model_evaluator(
    params: ModelEvaluatorStepParameters,
    model: ClassifierMixin,
    train_set: pd.DataFrame,
    test_set: pd.DataFrame,
{%- if use_custom_artifacts %}
) -> ModelMetadata:
{%- else %}
) -> Output(
    train_accuracy=float,
    test_accuracy=float,
):
{%- endif %}
    """Evaluate a trained model.
    
    This is an example of a model evaluation step that takes in a model artifact
    previously trained by another step in your pipeline, and a training
    and validation data set pair which it uses to evaluate the model's
{%- if use_custom_artifacts %}
    performance. The step returns a custom type of artifact containing metadata
    about the trained model. Note that using a custom data type also requires
    implementing a custom materializer for it. See the `materializer` folder
    or the following ZenML docs for more information about materializers:

        https://docs.zenml.io/user-guide/advanced-guide/artifact-management/handle-custom-data-types
{%- else %}
    performance. The model metrics are then returned as step output artifacts
    (in this case, the model accuracy on the train and test set).
{%- endif %}

    The suggested step implementation also outputs some warnings if the model
    performance does not meet some minimum criteria. This is just an example of
    how you can use steps to monitor your model performance and alert you if
    something goes wrong. As an alternative, you can raise an exception in the
    step to force the pipeline run to fail early and all subsequent steps to
    be skipped.

    This step is parameterized using the `ModelEvaluatorStepParameters` class,
    which allows you to configure the step independently of the step code,
    before running it in a pipeline. In this example, the step can be configured
    to use different values for the acceptable model performance thresholds and
    to control whether the pipeline run should fail if the model performance
    does not meet the minimum criteria. See the documentation for more
    information:

        https://docs.zenml.io/user-guide/starter-guide/cache-previous-executions

    Args:
        params: The parameters for the model evaluator step.
        model: The pre-trained model artifact.
        train_set: The training data set artifact.
        test_set: The test data set artifact.

    Returns:
{%- if use_custom_artifacts %}
        A model metadata artifact.
{%- else %}
        The model accuracy on the train and test set.
{%- endif %}
    """
    X_train = train_set.drop("target", axis=1)
    Y_train = train_set["target"]
    X_test = test_set.drop("target", axis=1)
    Y_test = test_set["target"]

    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
    # Calculate the model accuracy on the train and test set
    train_acc = model.score(X_train, Y_train)
    logger.info(f"Train accuracy: {train_acc}")
    test_acc = model.score(X_test, Y_test)
    logger.info(f"Test accuracy: {test_acc}")

    messages = []
    if train_acc < params.min_train_accuracy:
        messages.append(
            f"Train accuracy is below {params.min_train_accuracy*100}% !"
        )
    if test_acc < params.min_test_accuracy:
        messages.append(
            f"Test accuracy is below {params.min_test_accuracy*100}% !"
        )
    if test_acc - train_acc > params.max_train_test_accuracy_difference:
        messages.append(
            f"Train accuracy is more than "
            f"{params.max_train_test_accuracy_difference*100}% "
            f"higher than test accuracy. The model is overfitting the training "
            f"dataset."
        )
    if params.fail_on_warnings and messages:
        raise RuntimeError(
            "Model performance did not meet the minimum criteria:\n" +
            "\n".join(messages)
        )
    else:
        for message in messages:
            logger.warning(message)
{% if use_custom_artifacts %}
    model_metadata = ModelMetadata()
    model_metadata.collect_metadata(
        model = model,
        train_accuracy = train_acc,
        test_accuracy = test_acc,
    )
    return model_metadata
{%- else %}
    return train_acc, test_acc
{%- endif %}
    ### YOUR CODE ENDS HERE ###

{% else %}
@step
def model_trainer(
    train_set: pd.DataFrame,
) -> ClassifierMixin:
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
    
    As an alternative, try modelling the random seed as a step parameter to make
    your model training steps deterministic. Another way step parameters may be
    useful here is to configure the model hyperparameters rather than
    hard-coding them in the step implementation. See the documentation for more
    information:

        https://docs.zenml.io/user-guide/starter-guide/cache-previous-executions

    Args:
        train_set: The training data set artifact.

    Returns:
        The trained model artifact.
    """
    X_train = train_set.drop("target", axis=1)
    Y_train = train_set["target"]

    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
    # Train a model on the training set.
{%- if not sklearn_model_name in [ 'KNeighborsClassifier', 'GaussianNB' ] %}
    model = {{ sklearn_model_name }}(random_state=42)
{%- else %}
    model = {{ sklearn_model_name }}()
{%- endif %}
    logger.info(f"Training model {model}...")

    model.fit(X_train.to_numpy(), Y_train.to_numpy())
    ### YOUR CODE ENDS HERE ###

    return model


@step
{%- if use_custom_artifacts -%}
(output_materializers=ModelMetadataMaterializer)
{%- endif %}
def model_evaluator(
    model: ClassifierMixin,
    train_set: pd.DataFrame,
    test_set: pd.DataFrame,
{%- if use_custom_artifacts %}
) -> ModelMetadata:
{%- else %}
) -> Output(
    train_accuracy=float,
    test_accuracy=float,
):
{%- endif %}
    """Evaluate a trained model.
    
    This is an example of a model evaluation step that takes in a model artifact
    previously trained by another step in your pipeline, and a training
    and validation data set pair which it uses to evaluate the model's
{%- if use_custom_artifacts %}
    performance. The step returns a custom type of artifact containing metadata
    about the trained model. Note that using a custom data type also requires
    implementing a custom materializer for it. See the `materializer` folder
    or the following ZenML docs for more information about materializers:

        https://docs.zenml.io/user-guide/advanced-guide/artifact-management/handle-custom-data-types
{%- else %}
    performance. The model metrics are then returned as step output artifacts
    (in this case, the model accuracy on the train and test set).
{%- endif %}

    The suggested step implementation also outputs some warnings if the model
    performance does not meet some minimum criteria. This is just an example of
    how you can use steps to monitor your model performance and alert you if
    something goes wrong. As an alternative, you can raise an exception in the
    step to force the pipeline run to fail early and all subsequent steps to
    be skipped.

    The threshold performance values used to evaluate the model are hard-coded
    in this example. As an alternative, try modelling them as step parameters to
    make your model evaluation steps more flexible. See the documentation for
    more information:

        https://docs.zenml.io/user-guide/starter-guide/cache-previous-executions

    Args:
        model: The pre-trained model artifact.
        train_set: The training data set artifact.
        test_set: The test data set artifact.

    Returns:
{%- if use_custom_artifacts %}
        A model metadata artifact.
{%- else %}
        The model accuracy on the train and test set.
{%- endif %}
    """
    X_train = train_set.drop("target", axis=1)
    Y_train = train_set["target"]
    X_test = test_set.drop("target", axis=1)
    Y_test = test_set["target"]

    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
    # Calculate the model accuracy on the train and test set
    train_acc = model.score(X_train, Y_train)
    logger.info(f"Train accuracy: {train_acc}")
    test_acc = model.score(X_test, Y_test)
    logger.info(f"Train accuracy: {test_acc}")

    if train_acc < 0.8:
        logger.warning("Train accuracy is below 80% !")
    if test_acc < 0.8:
        logger.warning("Test accuracy is below 80% !")
    if test_acc - train_acc > 0.1:
        logger.warning(
            "Train accuracy is more than 10% higher than test accuracy. The "
            "model is overfitting the training dataset."
        )
{%- if use_custom_artifacts %}
    model_metadata = ModelMetadata()
    model_metadata.collect_metadata(
        model = model,
        train_accuracy = train_acc,
        test_accuracy = test_acc,
    )
    return model_metadata
{%- else %}
    return train_acc, test_acc
{%- endif %}
    ### YOUR CODE ENDS HERE ###

{%- endif %}
