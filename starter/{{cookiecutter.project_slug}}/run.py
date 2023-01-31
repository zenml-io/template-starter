{% include 'license_header' %}

import click
from typing import Any, Dict, Optional
from steps import (
    data_loader,
    data_processor,
    data_splitter,
    model_trainer,
    model_evaluator,
{%- if cookiecutter.use_step_params == 'y' %}
    DataLoaderStepParameters,
    DataProcessorStepParameters,
    DataSplitterStepParameters,
    SklearnDataset,
    ModelTrainerStepParameters,
    ModelEvaluatorStepParameters,
    SklearnClassifierModel,
{%- endif %}
)
from pipelines import (
    model_training_pipeline,
)

{% if cookiecutter.use_step_params == 'y' %}
def process_hyper_parameters(params: Optional[str] = None) -> Dict[str, Any]:
    """Process hyper parameters entered by the user from the command line.
    
    This function is used to parse hyper parameters entered by the user in
    the command line from a key-value string format (e.g. "C=0.1,max_iter=1000")
    to a dictionary with the correct data types (int, float, bool).

    Args:
        params: A string of comma-separated key-value pairs.
    
    Returns:
        A dictionary of hyper parameters converted to the correct type (int,
        float, bool)
    """
    if not params:
        return {}
    try:
        params = params.split(",")
        params = [param.split("=") for param in params]
        params = {key: value for key, value in params}
    except ValueError:
        raise ValueError(
            "Invalid format for hyperparameters. "
            "Expected a comma-separated list of key-value pairs "
            "(e.g. 'C=0.1,max_iter=1000')."
        )
    for key, value in params.items():
        try:
            params[key] = int(value)
            continue
        except ValueError:
            pass
        try:
            params[key] = float(value)
            continue
        except ValueError:
            pass
        if value.lower() == "true":
            params[key] = True
            continue
        if value.lower() == "false":
            params[key] = False
            continue
    return params
{%- endif %}


@click.command()
@click.option(
    "--no-cache",
    is_flag=True,
    default=False,
    help="Disable caching for the pipeline run.",
)
{%- if cookiecutter.use_step_params == 'y' %}
@click.option(
    "--dataset",
    default="wine",
    type=click.Choice(SklearnDataset.values()),
    help="The scikit-learn dataset to load.",
)
@click.option(
    "--model",
    default="logistic_regression",
    type=click.Choice(SklearnClassifierModel.values()),
    help="The scikit-learn model to train.",
)
@click.option(
    "--no-drop-na",
    is_flag=True,
    default=False,
    help="Whether to skip dropping rows with missing values in the dataset.",
)
@click.option(
    "--drop-columns",
    default=None,
    type=click.STRING,
    help="Comma-separated list of columns to drop from the dataset.",
)
@click.option(
    "--no-normalize",
    is_flag=True,
    default=False,
    help="Whether to skip normalizing the dataset.",
)
@click.option(
    "--test-size",
    default=0.2,
    type=click.FloatRange(0.0, 1.0),
    help="Proportion of the dataset to include in the test split.",
)
@click.option(
    "--no-shuffle",
    is_flag=True,
    default=False,
    help="Whether to skip shuffling the data before splitting.",
)
@click.option(
    "--no-stratify",
    is_flag=True,
    default=False,
    help="Whether to skip stratifying the data before splitting.",
)
@click.option(
    "--random-state",
    default=42,
    type=click.INT,
    help="Controls the randomness during data shuffling and model training. "
    "Pass an int for reproducible and cached output across multiple "
    "pipeline runs.",
)
@click.option(
    "--hyper-parameters",
    default=None,
    type=click.STRING,
    help="Comma-separated list of hyper-parameters to pass to the model "
    "trainer (e.g. 'C=0.1,max_iter=1000').",
)
@click.option(
    "--min-train-accuracy",
    default=0.8,
    type=click.FloatRange(0.0, 1.0),
    help="Minimum training accuracy to pass to the model evaluator.",
)
@click.option(
    "--min-test-accuracy",
    default=0.8,
    type=click.FloatRange(0.0, 1.0),
    help="Minimum test accuracy to pass to the model evaluator.",
)
@click.option(
    "--max-train-test-diff",
    default=0.1,
    type=click.FloatRange(0.0, 1.0),
    help="Maximum difference between training and test accuracy to pass to "
    "the model evaluator.",
)
@click.option(
    "--fail-on-eval-warnings",
    is_flag=True,
    default=False,
    help="Whether to fail the pipeline run if the model evaluation step "
    "finds that the model is not accurate enough.",
)
{%- endif %}
def main(
    no_cache: bool = False,
{%- if cookiecutter.use_step_params == 'y' %}
    dataset: str = SklearnDataset.wine.value,
    model: str = SklearnClassifierModel.logistic_regression.value,
    no_drop_na: bool = False,
    drop_columns: Optional[str] = None,
    no_normalize: bool = False,
    test_size: float = 0.2,
    no_shuffle: bool = False,
    no_stratify: bool = False,
    random_state: int = 42,
    hyper_parameters: Optional[str] = None,
    min_train_accuracy: float = 0.8,
    min_test_accuracy: float = 0.8,
    max_train_test_diff: float = 0.1,
    fail_on_eval_warnings: bool = False,
{%- endif %}
):
    """Main entry point for the pipeline execution.

    This entrypoint is where everything comes together:
      
      * instantiating the steps and configuring them with the required
        parameters (some of which may come from command line arguments)

      * creating a pipeline instance that brings together all step instances

      * launching the pipeline

      * looking at the results of the pipeline run

    Example usage:

        python run.py

    """

    # Initialize a pipeline. This is also where we instantiate the steps and
    # configure them with the required parameters. The step instances are
    # then passed to the pipeline constructor. The result is a pipeline
    # instance that is ready to be run.
    pipeline = model_training_pipeline(
{%- if cookiecutter.use_step_params == 'y' %}
        data_loader=data_loader(
            params=DataLoaderStepParameters(
                dataset=SklearnDataset(dataset),
            ),
        ),
        data_processor=data_processor(
            params=DataProcessorStepParameters(
                drop_na=not no_drop_na,
                drop_columns=drop_columns.split(",") if drop_columns else [],
                normalize=not no_normalize,
            ),
        ),
        data_splitter=data_splitter(
            params=DataSplitterStepParameters(
                test_size=test_size,
                shuffle=not no_shuffle,
                stratify=not no_stratify,
                random_state=random_state,
            ),
        ),
        model_trainer=model_trainer(
            params=ModelTrainerStepParameters(
                model=SklearnClassifierModel(model),
                random_state=random_state,
                hyperparameters=process_hyper_parameters(hyper_parameters),
            ),
        ),
        model_evaluator=model_evaluator(
            params=ModelEvaluatorStepParameters(
                min_train_accuracy=min_train_accuracy,
                min_test_accuracy=min_test_accuracy,
                max_train_test_accuracy_difference=max_train_test_diff,
                fail_on_warnings=fail_on_eval_warnings,
            ),
        ),
{%- else %}
        data_loader=data_loader(),
        data_splitter=data_splitter(),
        data_processor=data_processor(),
        model_trainer=model_trainer(),
        model_evaluator=model_evaluator(),
{%- endif %}
    )

    pipeline_args = {}
    if no_cache:
        pipeline_args["enable_cache"] = False

    # Run the pipeline. This executes all steps in the pipeline in the
    # correct order using the orchestrator stack component that is configured
    # in your active ZenML stack.
    pipeline.run(**pipeline_args)


    # TODO:
    # extract the evaluator result and show here
    # Point to the dashboard URL (if running); instruct to start the dashboard
    # info on how to use the CLI to show pipeline run details.
    # add experiment tracker to steps (flag)

    # materialization:
    # * - create a dummy class (statistics, report, visualization) and use that
    #   in the pipeline step and post-execution


if __name__ == "__main__":
    main()
