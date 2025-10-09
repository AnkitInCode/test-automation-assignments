from configs.env_data import envData

def get_env_details(request):
    env_vars = {
        'env': request.config.getoption("--env"),
        'secret': request.config.getoption("--secret"),
        'testdata': request.config.getoption("--testdata"),
        'apiurl': envData[request.config.getoption("--env")]['apiurl'],
        'envData': envData[request.config.getoption("--env")]  
        # use 'envData' to get all other data mentioned in configs.env_data under a given env.
    }
    return env_vars
