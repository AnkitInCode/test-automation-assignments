from configs.env_data import envData

def get_env_details(request):
    env_vars = {
        'browser': request.config.getoption("--browser"),
        'env': request.config.getoption("--env"),
        'login': request.config.getoption("--login"),
        'secret': request.config.getoption("--secret"),
        'headless': request.config.getoption("--headless"),
        'testdata': request.config.getoption("--testdata"),
        'baseurl': envData[request.config.getoption("--env")]['baseurl'],
        'apiurl': envData[request.config.getoption("--env")]['apiurl'],
        'envData': envData[request.config.getoption("--env")]  
        # use 'envData' to get all other data mentioned in configs.env_data under a given env.
    }
    return env_vars
