#  Copyright (c) ZenML GmbH 2023. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.
import shutil
import subprocess
import sys
from typing import Optional
from copier import Worker
import os
import pathlib
import pytest

from zenml.enums import ExecutionStatus
from zenml.post_execution import get_pipeline
from zenml.client import Client

TEMPLATE_DIRECTORY = str(pathlib.Path(__file__).parent.parent)


def generate_and_run_project(
    tmp_path_factory: pytest.TempPathFactory,
    open_source_license: Optional[str] = "apache",
    auto_format: bool = True,
    use_step_params: bool = True,
    use_custom_artifacts: bool = True,
    configurable_dataset: bool = True,
    configurable_model: bool = True,
    sklearn_dataset_name: str = "wine",
    sklearn_model_name: str = "SVC",
    pipeline_name: str = "model_training_pipeline",
):
    """Generate and run the starter project with different options."""

    answers = {
        "template": "starter",
        "project_name": "Pytest Starter",
        "version": "0.0.1",
        "open_source_license": open_source_license,
        "email": "pytest@zenml.io",
        "full_name": "Pytest",
        "auto_format": auto_format,
        "use_custom_artifacts": use_custom_artifacts,
        "use_step_params": use_step_params,
        "configurable_dataset": configurable_dataset,
        "configurable_model": configurable_model,
        "sklearn_dataset_name": sklearn_dataset_name,
        "sklearn_model_name": sklearn_model_name,
    }

    # generate the template in a temp path
    current_dir = os.getcwd()
    dst_path = tmp_path_factory.mktemp("pytest-template")
    os.chdir(str(dst_path))
    with Worker(
        src_path=TEMPLATE_DIRECTORY,
        dst_path=str(dst_path),
        data=answers,
        unsafe=True,
    ) as worker:
        worker.run_copy()

    # run the project
    call = [sys.executable, "run.py"]

    try:
        subprocess.check_call(
            call,
            cwd=str(dst_path),
            env=os.environ.copy(),
        )
    except Exception as e:
        raise RuntimeError(
            f"Failed to run project generated with parameters: {answers}"
        ) from e

    # check the pipeline run is successful
    pipeline = get_pipeline(pipeline_name)
    assert pipeline
    runs = pipeline.runs
    assert len(runs) == 1
    assert runs[0].status == ExecutionStatus.COMPLETED

    # clean up
    Client().delete_pipeline(pipeline_name)

    os.chdir(current_dir)
    shutil.rmtree(dst_path)


@pytest.mark.parametrize("open_source_license", ["mit", None])
def test_generate_license(
    clean_zenml_client,
    tmp_path_factory: pytest.TempPathFactory,
    open_source_license: Optional[str],
):
    """Test generating licenses."""

    generate_and_run_project(
        tmp_path_factory=tmp_path_factory,
        open_source_license=open_source_license,
    )


def test_no_auto_format(
    clean_zenml_client,
    tmp_path_factory: pytest.TempPathFactory,
):
    """Test turning off code auto-format."""

    generate_and_run_project(
        tmp_path_factory=tmp_path_factory,
        auto_format=False,
    )


@pytest.mark.parametrize("use_custom_artifacts", [True, False])
@pytest.mark.parametrize("sklearn_dataset_name", ["wine", "iris"])
@pytest.mark.parametrize(
    "sklearn_model_name",
    [
        "SGDClassifier",
        "DecisionTreeClassifier",
    ],
)
def test_step_params_disabled(
    clean_zenml_client,
    tmp_path_factory: pytest.TempPathFactory,
    use_custom_artifacts: bool,
    sklearn_dataset_name: str,
    sklearn_model_name: str,
):
    """Test generating the starter template with step parameters disabled ."""

    generate_and_run_project(
        tmp_path_factory=tmp_path_factory,
        use_step_params=False,
        use_custom_artifacts=use_custom_artifacts,
        configurable_dataset=False,
        configurable_model=False,
        sklearn_dataset_name=sklearn_dataset_name,
        sklearn_model_name=sklearn_model_name,
    )


@pytest.mark.parametrize("use_custom_artifacts", [True, False])
@pytest.mark.parametrize("configurable_dataset", [True, False])
@pytest.mark.parametrize("configurable_model", [True, False])
@pytest.mark.parametrize("sklearn_dataset_name", ["iris", "breast_cancer"])
@pytest.mark.parametrize(
    "sklearn_model_name",
    [
        "RandomForestClassifier",
        "KNeighborsClassifier",
    ],
)
def test_step_params_enabled(
    clean_zenml_client,
    tmp_path_factory: pytest.TempPathFactory,
    use_custom_artifacts: bool,
    configurable_dataset: bool,
    configurable_model: bool,
    sklearn_dataset_name: str,
    sklearn_model_name: str,
):
    """Test generating the starter template with step parameters enabled ."""

    generate_and_run_project(
        tmp_path_factory=tmp_path_factory,
        use_step_params=False,
        use_custom_artifacts=use_custom_artifacts,
        configurable_dataset=configurable_dataset,
        configurable_model=configurable_model,
        sklearn_dataset_name=sklearn_dataset_name,
        sklearn_model_name=sklearn_model_name,
    )
