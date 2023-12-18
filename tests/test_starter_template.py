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


import os
import pathlib
import platform
import shutil
import subprocess
import sys
from typing import Optional

import pytest
from copier import Worker
from zenml.client import Client
from zenml.enums import ExecutionStatus

TEMPLATE_DIRECTORY = str(pathlib.Path.joinpath(pathlib.Path(__file__).parent.parent))


def generate_and_run_project(
    tmp_path_factory: pytest.TempPathFactory,
    open_source_license: Optional[str] = "apache",
    product_name: str = "starter_project",
):
    """Generate and run the starter project with different options."""

    answers = {
        "project_name": "Pytest Templated Project",
        "version": "0.0.1",
        "open_source_license": str(open_source_license).lower(),
        "product_name": product_name,
    }
    if open_source_license:
        answers["email"] = "pytest@zenml.io"
        answers["full_name"] = "Pytest"

    # generate the template in a temp path
    current_dir = os.getcwd()
    dst_path = tmp_path_factory.mktemp("pytest-template")
    os.chdir(str(dst_path))
    with Worker(
        src_path=TEMPLATE_DIRECTORY,
        dst_path=str(dst_path),
        data=answers,
        unsafe=True,
        vcs_ref="HEAD",
    ) as worker:
        worker.run_copy()

    # run the project
    call = [
        sys.executable,
        "run.py",
        "--training-pipeline",
        "--feature-pipeline",
        "--inference-pipeline",
        "--no-cache"
    ]

    try:
        subprocess.check_output(
            call,
            cwd=str(dst_path),
            env=os.environ.copy(),
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Failed to run project generated with parameters: {answers}\n"
            f"{e.output.decode()}"
        ) from e

    # check the pipeline run is successful
    for pipeline_name in ["training", "inference", "feature_engineering"]:
        pipeline = Client().get_pipeline(pipeline_name)
        assert pipeline
        runs = pipeline.runs
        assert len(runs) == 1
        assert runs[0].status == ExecutionStatus.COMPLETED

        # clean up
        Client().delete_pipeline(pipeline_name)
    Client().delete_model("breast_cancer_classifier")

    os.chdir(current_dir)
    shutil.rmtree(dst_path)


@pytest.mark.parametrize("open_source_license", ["mit", None], ids=["oss", "css"])
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


def test_custom_product_name(
    clean_zenml_client,
    tmp_path_factory: pytest.TempPathFactory,
):
    """Test using custom pipeline name."""

    generate_and_run_project(
        tmp_path_factory=tmp_path_factory,
        product_name="custom_product_name",
    )
