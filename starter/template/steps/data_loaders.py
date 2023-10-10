{% include 'templates/license_header' %}
{%- if use_step_params %}
from typing import List
{%- endif %}
import pandas as pd

from sklearn.datasets import (
{%- if use_step_params and configurable_dataset  %}
    load_wine,
    load_breast_cancer,
    load_iris,
{%- else %}
    load_{{ sklearn_dataset_name }},
{%- endif %}
)
from sklearn.model_selection import train_test_split
{%- if use_step_params %}
from zenml.enums import StrEnum
{%- endif %}
from zenml import (
{%- if use_step_params %}
    BaseParameters,
{%- endif %}
    Output,
    step,
)
from zenml.logger import get_logger

logger = get_logger(__name__)

{% if use_step_params and configurable_dataset %}
class SklearnDataset(StrEnum):
    """Built-in scikit-learn datasets."""
    wine = "wine"
    iris = "iris"
    breast_cancer = "breast_cancer"


@step
def data_loader(
    dataset_name: SklearnDataset = SklearnDataset.{{ sklearn_dataset_name }},
) -> pd.DataFrame:
    """Data loader step.
    
    This is an example of a data loader step that is usually the first step
    in your pipeline. It reads data from an external source like a file,
    database or 3rd party library, then formats it and returns it as a step
    output artifact.

    This step is parameterized using the `DataLoaderStepParameters` class, which
    allows you to configure the step independently of the step code, before
    running it in a pipeline. In this example, the step can be configured to
    load different built-in scikit-learn datasets. See the documentation for
    more information:

        https://docs.zenml.io/user-guide/starter-guide/cache-previous-executions

    Data loader steps should have caching disabled if they are not deterministic
    (i.e. if they data they load from the external source can be different when
    they are subsequently called, even if the step code and parameter values
    don't change).

    Args:
        dataset_name: SklearnDataset enum, one of "wine", "iris", or "breast_cancer".
    
    Returns:
        The loaded dataset artifact.
    """
    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
    # Load the dataset indicated in the step parameters and format it as a
    # pandas DataFrame
    if dataset_name == SklearnDataset.wine:
        dataset = load_wine(as_frame=True).frame
    elif dataset_name == SklearnDataset.iris:
        dataset = load_iris(as_frame=True).frame
    elif dataset_name == SklearnDataset.breast_cancer:
        dataset = load_breast_cancer(as_frame=True).frame
    elif dataset_name == SklearnDataset.diabetes:
        dataset = load_diabetes(as_frame=True).frame
    logger.info(f"Loaded dataset {dataset.value}: %s", dataset.info())
    logger.info(dataset.head())
    ### YOUR CODE ENDS HERE ###

    return dataset
{% else %}
@step
def data_loader() -> Output(
    dataset=pd.DataFrame,
):
    """Data loader step.
    
    This is an example of a data loader step that is usually the first step
    in your pipeline. It reads data from an external source like a file,
    database or 3rd party library, then formats it and returns it as a step
    output artifact.

    Data loader steps should have caching disabled if they are not deterministic
    (i.e. if they data they load from the external source is different when
    they are subsequently called, even if the step code doesn't change).
    
    As an alternative, try modelling the data source as a step parameter to make
    your data loader deterministic and configurable without the need to change
    the step implementation. See the documentation for more information:

        https://docs.zenml.io/user-guide/starter-guide/cache-previous-executions

    Returns:
        The loaded dataset artifact.
    """
    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
    # Load the {{ sklearn_dataset_name }} dataset and format it as a pandas DataFrame
    dataset = load_{{ sklearn_dataset_name }}(as_frame=True).frame
    dataset.info()
    logger.info(dataset.head())
    ### YOUR CODE ENDS HERE ###

    return dataset
{% endif %}
{% if use_step_params %}

@step
def data_processor(
    # Whether to drop rows with missing values.
    drop_na: bool = True,
    # Columns to drop from the dataset.
    drop_columns: List[str] = [],
    # Whether to normalize the data.
    normalize: bool = True,
    dataset: pd.DataFrame,
) -> pd.DataFrame:
    """Data processor step.
    
    This is an example of a data processor step that prepares the data so that
    it is suitable for model training. It takes in a dataset as an input step
    artifact and performs any necessary preprocessing steps like cleaning,
    feature engineering, feature selection, etc. It then returns the processed
    dataset as a step output artifact.
    
    This step is parameterized using the `DataProcessorStepParameters` class,
    which allows you to configure the step independently of the step code,
    before running it in a pipeline. In this example, the step can be configured
    to perform or skip different preprocessing steps (e.g. dropping rows with
    missing values, dropping columns, normalizing the data, etc.). See the
    documentation for more information:

        https://docs.zenml.io/user-guide/starter-guide/cache-previous-executions

    Args:
        params: Parameters for the data processor step.
        dataset: The dataset artifact to process.

    Returns:
        The processed dataset artifact.
    """
    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
    if drop_na:
        # Drop rows with missing values
        dataset = dataset.dropna()
    if drop_columns:
        # Drop columns
        dataset = dataset.drop(columns=drop_columns)
    if normalize:
        # Normalize the data
        target = dataset.pop('target')
        dataset = (dataset - dataset.mean()) / dataset.std()
        dataset['target'] = target
    ### YOUR CODE ENDS HERE ###

    return dataset

@step
def data_splitter(
    # The proportion of the dataset to include in the test split.
    test_size: float = 0.2,
    # The random seed to use for the split.
    random_state: int = 42,
    # Whether to shuffle the dataset before splitting.
    shuffle: bool = True,
    # Whether to stratify the split.
    stratify: bool = True,
    dataset: pd.DataFrame,
) -> Output(
    train_set=pd.DataFrame,
    test_set=pd.DataFrame,
):
    """Data splitter step.
    
    This is an example of a data splitter step that splits the dataset into
    training and dev subsets to be used for model training and evaluation. It
    takes in a dataset as an step input artifact and returns the training and
    dev subsets as two separate step output artifacts.

    Data splitter steps should have a deterministic behavior, i.e. they should
    use a fixed random seed and always return the same split when called with
    the same input dataset. This is to ensure reproducibility of your pipeline
    runs.

    This step is parameterized using the `DataSplitterStepParameters` class,
    which allows you to configure the step independently of the step code,
    before running it in a pipeline. In this example, the step can be configured
    to use a different random seed, change the split ratio, or control whether
    to shuffle or stratify the split. See the documentation for more
    information:

        https://docs.zenml.io/user-guide/starter-guide/cache-previous-executions

    Args:
        test_size: Size of the test set.
        random_state: The random seed to use for the split.
        shuffle: Whether to shuffle the dataset before splitting.
        stratify: Whether to stratify the split.
        dataset: The dataset to split.

    Returns:
        The resulting training and dev subsets.
    """

    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
    # Split the dataset into training and dev subsets
    train_set, test_set = train_test_split(
        dataset,
        test_size=test_size,
        shuffle=shuffle,
        stratify=dataset['target'] if stratify else None,
        random_state=random_state,
    )
    ### YOUR CODE ENDS HERE ###

    return train_set, test_set
{% else %}
@step
def data_processor(dataset: pd.DataFrame) -> pd.DataFrame:
    """Data processor step.
    
    This is an example of a data processor step that prepares the data so that
    it is suitable for model training. It takes in a dataset as an step input
    artifact and performs any necessary preprocessing steps like cleaning, feature
    engineering, feature selection, etc. The processed dataset is then returned
    as an step output artifact.
    
    Args:
        dataset: The dataset artifact to process.

    Returns:
        The processed dataset artifact.
    """
    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
    # Drop rows with missing values
    dataset = dataset.dropna()
    # Normalize the data
    target = dataset.pop('target')
    dataset = (dataset - dataset.mean()) / dataset.std()
    dataset['target'] = target
    ### YOUR CODE ENDS HERE ###

    return dataset


@step
def data_splitter(dataset: pd.DataFrame) -> Output(
    train_set=pd.DataFrame,
    test_set=pd.DataFrame,
):
    """Data splitter step.
    
    This is an example of a data splitter step that splits the dataset into
    training and dev subsets to be used for model training and evaluation. It
    takes in a dataset as a step input artifact and returns the training and
    dev subsets as two separate step output artifacts.

    Data splitter steps should have a deterministic behavior, i.e. they should
    use a fixed random seed and always return the same split when called with
    the same input dataset. This is to ensure reproducibility of your pipeline
    runs.

    As an alternative to hard-coding the seed in the step code, try modelling
    the random seed as a step parameter to make your data loader deterministic.
    See the documentation for more information:

        https://docs.zenml.io/user-guide/starter-guide/cache-previous-executions

    Args:
        dataset: The dataset to split.

    Returns:
        The resulting training and dev subsets.
    """

    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
    # Split the dataset into training and dev subsets
    train_set, test_set = train_test_split(
        dataset,
        test_size=0.2,
        shuffle=True,
        stratify=dataset['target'],
        random_state=42
    )
    ### YOUR CODE ENDS HERE ###

    return train_set, test_set
{%- endif %}
