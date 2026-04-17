from abc import ABC, abstractmethod
from typing import Any

class DataProcessor(ABC):
    def __init__(self):
        self.Memory = []

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self.Memory:
            return (-1, "No Data")
        print(f"{self.Memory}")
        key, value = self.Memory[0]
        self.Memory = self.Memory[1:]
        return (key, value)


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
            if isinstance(data, dict[str, str]):
                return True
            elif isinstance(data, list):
                for item in data:
                    if not isinstance(item, dict[str, str]):
                        return False
                return True
            else:
                return False

    def ingest(self, data: Any) -> None:
        try:
            if isinstance(data, dict[str, str]):
                self.Memory.append(data)
            elif isinstance(data, list):
                for item in data:
                    if not isinstance(item, dict[str, str]):
                        raise ValueError
                for item in data:
                    self.Memory.append(item)
            else:
                raise ValueError
        except ValueError:
            print("Invalid value to process, need Dict[Str, Str]!")


if __name__ == "__main__":
    print("=== Code Nexus - Data Processor ===\n")
    NumInput1 = 42
    NumInput2 = "Hello"
    NumInput3 = [1, 2, 3, 4, 5]
    temp = NumericProcessor()
    print(
        f"Trying to validate input '{NumInput1}':"
        f"{temp.validate(NumInput1)}"
    )
    print(
        f"Trying to validate input '{NumInput2}':"
        f"{temp.validate(NumInput2)}"
    )
    print(f"Trying to ingest input 'foo': ", end="")
    temp.ingest("foo")
    print(f"Processing data: {NumInput3}")
    temp.ingest(NumInput3)
    i = 1
    while i <= 3:
        temp.output()
        i += 1
