import pytest

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="QA", help="pass environment type")
    parser.addoption("--secret", action="store", default="secret_sauce", help="pass password")
    parser.addoption("--testdata", action="store", default="testdata/example_test_data.json", help="pass data file")