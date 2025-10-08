import pytest

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="pass browser type")
    parser.addoption("--env", action="store", default="QA", help="pass environment type")
    parser.addoption("--login", action="store", default="standard_user", help="pass username")
    parser.addoption("--secret", action="store", default="secret_sauce", help="pass password")
    parser.addoption("--headless", action="store", default="false", help="pass true or false")
    parser.addoption("--testdata", action="store", default="testdata/example_test_data.json", help="pass data file")
