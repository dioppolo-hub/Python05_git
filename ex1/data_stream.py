from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self):
        self.Memory = []
        self.counter = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self.Memory:
            return (-1, "No Data")
        value = self.Memory[0]
        self.Memory = self.Memory[1:]
        index = self.counter
        self.counter += 1
        return (index, value)


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        elif isinstance(data, list):
            for item in data:
                if not isinstance(item, (int, float)):
                    return False
            return True
        else:
            return False

    def ingest(self, data: Any) -> None:
        try:
            self.counter = 0
            if isinstance(data, (int, float)):
                s = f"{data}"
                self.Memory.append(s)
            elif isinstance(data, list):
                for item in data:
                    if not isinstance(item, (int, float)):
                        raise ValueError
                for item in data:
                    s = f"{item}"
                    self.Memory.append(s)
            else:
                raise ValueError
        except ValueError:
            print("Invalid value to process, need Int or Float!")


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        elif isinstance(data, list):
            for item in data:
                if not isinstance(item, str):
                    return False
            return True
        else:
            return False

    def ingest(self, data: Any) -> None:
        try:
            self.counter = 0
            if isinstance(data, str):
                self.Memory.append(data)
            elif isinstance(data, list):
                for item in data:
                    if not isinstance(item, str):
                        raise ValueError
                for item in data:
                    self.Memory.append(item)
            else:
                raise ValueError
        except ValueError:
            print("Invalid value to process, need Str!")


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            return True
        elif isinstance(data, list):
            for item in data:
                if not isinstance(item, dict):
                    return False
            return True
        else:
            return False

    def ingest(self, data: Any) -> None:
        try:
            self.counter = 0

            def is_valid_dict(d):
                return(
                        isinstance(d, dict) and
                        all(isinstance(k, str) and
                            isinstance(v, str) for k, v in d.items())
                )

            if isinstance(data, dict):
                if not is_valid_dict(data):
                    raise ValueError
                self.Memory.append(data)
            elif isinstance(data, list):
                for item in data:
                    if not is_valid_dict(item):
                        raise ValueError
                for item in data:
                    self.Memory.append(item)
            else:
                raise ValueError
        except ValueError:
            print("Invalid value to process, need Dict[Str:Str]!")


class DataStream():
    def register_processor(self, proc: DataProcessor) -> None:


    def process_stream(self, stream: list[typing.Any]) -> None:


    def print_processors_stats(self) -> None:


if __name__ == "__main__":
