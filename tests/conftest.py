import os
import shutil
from typing import Generator
import pytest

from zenml.client import Client
from zenml.config.global_config import GlobalConfiguration
from zenml.constants import ENV_ZENML_CONFIG_PATH


@pytest.fixture(scope="module")
def clean_zenml_client(
    tmp_path_factory: pytest.TempPathFactory,
) -> Generator[Client, None, None]:
    """Context manager to initialize and use a clean local default ZenML client.

    This context manager creates a clean ZenML client with its own global
    configuration and local database.

    Args:
        tmp_path_factory: A pytest fixture that provides a temporary directory.

    Yields:
        A clean ZenML client.
    """
    # save the current global configuration and client singleton instances
    # to restore them later, then reset them
    orig_cwd = os.getcwd()
    original_config = GlobalConfiguration.get_instance()
    original_client = Client.get_instance()
    orig_config_path = os.getenv("ZENML_CONFIG_PATH")

    GlobalConfiguration._reset_instance()
    Client._reset_instance()

    # change the working directory to a fresh temp path
    tmp_path = tmp_path_factory.mktemp("pytest-clean-client")
    os.chdir(tmp_path)

    os.environ[ENV_ZENML_CONFIG_PATH] = str(tmp_path / "zenml")
    os.environ["ZENML_ANALYTICS_OPT_IN"] = "false"

    # initialize the global config client and store at the new path
    gc = GlobalConfiguration()
    gc.analytics_opt_in = False
    client = Client()
    _ = client.zen_store

    yield client

    # restore the global configuration path
    if orig_config_path:
        os.environ[ENV_ZENML_CONFIG_PATH] = orig_config_path
    else:
        del os.environ[ENV_ZENML_CONFIG_PATH]

    # restore the global configuration and the client
    GlobalConfiguration._reset_instance(original_config)
    Client._reset_instance(original_client)

    # remove all traces, and change working directory back to base path
    os.chdir(orig_cwd)
    shutil.rmtree(str(tmp_path))
