from dataclasses import dataclass

import yaml


@dataclass
class Config:
    HOST: str = 'localhost'
    PORT: int = 8080

    def get_address(self):
        return self.HOST, self.PORT


def parse_config(path='api/config/config.yaml') -> Config:
    with open(path, 'r') as f:
        config = yaml.safe_load(f)
        config = Config(**config)
    return config
