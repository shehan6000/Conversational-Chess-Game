import os
from typing import Dict, Any
from dataclasses import dataclass
import yaml


@dataclass
class LLMConfig:
    model: str = "gpt-4-turbo"
    api_key: str = None
    temperature: float = 0.7
    max_tokens: int = 1000


@dataclass
class GameConfig:
    max_turns: int = 50
    max_nested_turns: int = 5
    board_size: int = 200


class Config:
    def __init__(self, config_path: str = None):
        self.llm_config = LLMConfig()
        self.game_config = GameConfig()
        
        # Load from environment variables first
        self._load_from_env()
        
        # Load from config file if provided
        if config_path and os.path.exists(config_path):
            self._load_from_file(config_path)
    
    def _load_from_env(self):
        self.llm_config.model = os.getenv('LLM_MODEL', self.llm_config.model)
        self.llm_config.api_key = os.getenv('LLM_API_KEY')
        self.llm_config.temperature = float(os.getenv('LLM_TEMPERATURE', self.llm_config.temperature))
        self.game_config.max_turns = int(os.getenv('GAME_MAX_TURNS', self.game_config.max_turns))
    
    def _load_from_file(self, config_path: str):
        with open(config_path, 'r') as file:
            config_data = yaml.safe_load(file)
            
        if 'llm' in config_data:
            self.llm_config = LLMConfig(**config_data['llm'])
        if 'game' in config_data:
            self.game_config = GameConfig(**config_data['game'])
    
    def get_llm_config_dict(self) -> Dict[str, Any]:
        return {
            "model": self.llm_config.model,
            "api_key": self.llm_config.api_key,
            "temperature": self.llm_config.temperature,
            "max_tokens": self.llm_config.max_tokens
        }