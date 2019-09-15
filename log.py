import os
import logging
import logging.config

import yaml

def setup_logging(
    default_path='logging.yaml',
    defualt_level=logging.INFO,
    env_key='LOG_CFG'
    ):
    """Setup logging configuration from logging.yaml config file.

    Keyword arguments:
    defaulth_path -- config .yaml file path (default logging.yaml)
    default_level -- default logging level (default logging.INFO)
    env_key -- environment variable name for logging config file path
    """
    path = os.getenv(env_key, default_path)
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=defualt_level)