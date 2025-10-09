# test-automation-assignments
## Python Selenium Automation Framework!

### Features
- Page Object Model (check pages directory)

- Used reabable assertions like `assert_that(123).is_greater_than(100)` [documentation](https://github.com/assertpy/assertpy)


### Pre-requisite
- Python3

### Installation 
```
pip install -r requirements.txt
```

### How to run

- Example API Test cases
```
pytest -vsrP --env=QA --testdata=testdata/example_test_data.json tests/example_rest_api_tests.py
```
- Example Run with HTML report
```
pytest --html=report.html --self-contained-html -vsrP --env=QA --testdata=testdata/example_test_data.json tests/example_rest_api_tests.py
```

### Test tags

- To skip a test, use this decorator `@pytest.mark.skip(reason="<reason>")`

- To run specific tags, use `-m "<tag_name>"` or `-m "not <tag_name>` etc.
Ex. `pytest -m smoke -vsrP --env=QA --testdata=testdata/example_test_data.json tests/example_tests/example_rest_api_tests.py`


### GitHub Actions CI/CD

- A workflow is configured in .github/workflows/ci.yml
- On every push or pull request to main branch, it will:
    1. Install dependencies
    2. Run all test cases
    3. Generate report.html
    4. Upload it as an artifact

- View workflow runs:
1. Go to your GitHub repository → Actions tab
2. Click on a workflow run → Artifacts → Download test-report.zip


## Test Coverage

- PATCH endpoints: positive and negative test scenarios
- POST endpoints: validation of required fields
- GET endpoints: handling invalid query parameters

## Observations

- API returns 400 for invalid data types
- PATCH endpoint correctly updates existing resources
- Negative tests confirmed proper error handling