from configs.env_data import envData

def get_env_details(request):

    env_vars = {
        'env': request.config.getoption("--env"),
        'secret': request.config.getoption("--secret"),
        'testdata': request.config.getoption("--testdata"),
        'apiurl': envData[request.config.getoption("--env")]['apiurl'],
        'headers': envData[request.config.getoption("--env")]['headers'],
    }

    return env_vars