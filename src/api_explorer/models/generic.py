import re
import typing as t
from pydantic import BaseModel as PydanticBase, root_validator


__all__ = ('AdvancedModel', 'BaseModel')


pattern = re.compile(r'(?<!^)(?=[A-Z])')


def camel_to_snake(camel: str) -> str:
    return pattern.sub('_', camel).lower()


class BaseModel(PydanticBase):
    class Config:
        arbitrary_types_allowed = True
        allow_mutation = True
        extra = 'allow'
    
    @root_validator
    def conver_cases(cls, values: t.Dict) -> t.Dict:
        updated_values = {}

        for attr_name, attr_value in values.items():
            updated_values[camel_to_snake(attr_name)] = attr_value
        return updated_values

    
    def __str__(self):
        return pattern.sub('_', self.__repr_name__()).lower()

class AdvancedModel(BaseModel):
    
    def to_file(self, file_name: t.Optional[str] = None) -> str:
        if file_name is None:
            file_name = f'{self}.json'
        
        with open(file_name, 'w') as json_file:
            json_file.write(self.json())
        
        return file_name