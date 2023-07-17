from ruamel import yaml

def parse_yaml(file: str) -> dict:
    ''' Parse yaml file into dict '''
    try:
        info = yaml.safe_load(open(file))
        return info
    except Exception as e:
        print("Unable to find file....... ")
        return False

def get_username() -> str:
    ''' Collecting rabbit mq connection username '''
    info=parse_yaml('./config.yaml')
    try:
        return info['graph_username']
    except Exception as e:
        print("Unable to find neo4j User Name..... ")
        return False

def get_password() -> str:
    ''' Collecting rabbit mq connection password '''
    info=parse_yaml('./config.yaml')
    try:
        return info['graph_password']
    except Exception as e:
        print("Unable to find neo4j password..... ")
        return False
        
def get_url() ->str:
    ''' Collecting url '''
    info = parse_yaml('./config.yaml')
    try:
        return info['graph_url']
    except Exception as e:
        print("Unable to find url..... ")
        return False

def get_acqn_timeout() ->str:
    ''' Collecting acquisition timeout limit in sec '''
    info = parse_yaml('./config.yaml')
    try:
        return info['acquisitiontimeout']
    except Exception as e:
        print("Unable to find acquisition timeout..... ")
        return False

def get_conn_timeout() ->str:
    ''' Collecting connection timeout limit in sec '''
    info = parse_yaml('./config.yaml')
    try:
        return info['connectiontimeout']
    except Exception as e:
        print("Unable to find connection timeout..... ")
        return False

