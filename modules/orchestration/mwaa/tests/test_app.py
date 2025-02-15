# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import os
import sys

import pytest


@pytest.fixture(scope="function")
def stack_defaults():
    os.environ["SEEDFARMER_PROJECT_NAME"] = "test-project"
    os.environ["SEEDFARMER_DEPLOYMENT_NAME"] = "test-deployment"
    os.environ["SEEDFARMER_MODULE_NAME"] = "test-module"
    os.environ["CDK_DEFAULT_ACCOUNT"] = "111111111111"
    os.environ["CDK_DEFAULT_REGION"] = "us-east-1"
    os.environ["SEEDFARMER_PARAMETER_RETENTION_TYPE"] = "DESTROY"
    os.environ["SEEDFARMER_PARAMETER_VPC_ID"] = "vpc-12345"
    os.environ["SEEDFARMER_PARAMETER_PRIVATE_SUBNET_IDS"] = '["subnet-12345", "subnet-54321"]'
    os.environ["SEEDFARMER_PARAMETER_DAG_BUCKET_NAME"] = "test-idf-dag-bucket"
    os.environ["SEEDFARMER_PARAMETER_DAG_PATH"] = "test-dags-path"
    os.environ["SEEDFARMER_PARAMETER_AIRFLOW_VERSION"] = "2.5.1"

    # Unload the app import so that subsequent tests don't reuse
    if "app" in sys.modules:
        del sys.modules["app"]


def test_app(stack_defaults):
    import app  # noqa: F401


def test_project_deployment_name_length(stack_defaults):
    os.environ["SEEDFARMER_PROJECT_NAME"] = "test-project-incredibly"

    with pytest.raises(Exception) as e:
        import app  # noqa: F401
    assert "module cannot support a project+deployment name character length greater than" in str(e)


def test_vpc_id(stack_defaults):
    del os.environ["SEEDFARMER_PARAMETER_VPC_ID"]

    with pytest.raises(Exception):
        import app  # noqa: F401

        assert os.environ["SEEDFARMER_PARAMETER_VPC_ID"] == "vpc-12345"


def test_private_subnet_ids(stack_defaults):
    del os.environ["SEEDFARMER_PARAMETER_PRIVATE_SUBNET_IDS"]

    with pytest.raises(Exception):
        import app  # noqa: F401

        assert os.environ["SEEDFARMER_PARAMETER_PRIVATE_SUBNET_IDS"] == ["subnet-12345", "subnet-54321"]


def test_batch_cmpute(stack_defaults):
    del os.environ["SEEDFARMER_PARAMETER_DAG_BUCKET_NAME"]

    with pytest.raises(Exception):
        import app  # noqa: F401

        assert os.environ["SEEDFARMER_PARAMETER_DAG_BUCKET_NAME"] == "test-idf-dag-bucket"
