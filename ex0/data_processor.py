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

    def ingest(self, data: int | float | list[int | float]) -> None:
        try:
            if isinstance(data, (int, float)):
                self.Memory.append(str(data))
            elif isinstance(data, list):
                for item in data:
                    if not isinstance(item, (int, float)):
                        raise ValueError
                for item in data:
                    self.Memory.append(str(item))
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

    def ingest(self, data: str | list[str]) -> None:
        try:
            if isinstance(data, str):
                self.Memory.append(str(data))
            elif isinstance(data, list):
                for item in data:
                    if not isinstance(item, str):
                        raise ValueError
                for item in data:
                    self.Memory.append(str(item))
            else:
                raise ValueError
        except ValueError:
            print("Invalid value to process, need Str!")


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:

        def is_valid_dict(d):
            return(
                    isinstance(d, dict) and
                    all(isinstance(k, str) and
                        isinstance(v, str) for k, v in d.items())
            )

        if is_valid_dict(data):
            return True
        if isinstance(data, list):
            return all(is_valid_dict(item) for item in data)
        return False

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        try:

            def is_valid_dict(d):
                return(
                        isinstance(d, dict) and
                        all(isinstance(k, str) and
                            isinstance(v, str) for k, v in d.items())
                )

            if isinstance(data, dict):
                if not is_valid_dict(data):
                    raise ValueError
                self.Memory.append(str(data))
            elif isinstance(data, list):
                for item in data:
                    if not is_valid_dict(item):
                        raise ValueError
                for item in data:
                    self.Memory.append(str(item))
            else:
                raise ValueError
        except ValueError:
            print("Invalid value to process, need Dict[Str:Str]!")


if __name__ == "__main__":
    print("=== Code Nexus - Data Processor ===\n")

    print("Testing Numeric Processor...")
    NumInput1 = 42
    NumInput2 = "Hello"
    NumInput3 = [42, 67, 98, 55, 66]
    tempNum = NumericProcessor()
    print(
        f" Trying to validate input '{NumInput1}': "
        f"{tempNum.validate(NumInput1)}"
    )
    print(
        f" Trying to validate input '{NumInput2}': "
        f"{tempNum.validate(NumInput2)}"
    )
    print(" Trying to ingest input 'foo': ", end="")
    tempNum.ingest("foo")
    print(f" -Processing data: {NumInput3}-")
    tempNum.ingest(NumInput3)
    for num in NumInput3:
        key, value = tempNum.output()
        print(f" Numeric value {key}: {value}")
    print(f" -Processing data: {NumInput1}-")
    tempNum.ingest(NumInput1)
    key, value = tempNum.output()
    print(f" Numeric value {key}: {value}")

    print("\nTesting Text Processor...")
    tempStr = TextProcessor()
    StrInput1 = 42
    StrInput2 = ["Hello", "Word", "42rs"]
    print(
        f" Trying to validate input '{StrInput1}': "
        f"{tempStr.validate(StrInput1)}"
    )
    print(" Trying to ingest input 42: ", end="")
    tempStr.ingest(42)
    print(f" -Processing data: {StrInput2}-")
    tempStr.ingest(StrInput2)
    for word in StrInput2:
        key, value = tempStr.output()
        print(f" Text value {key}: {value}")

    print("\nTesting Log Processor...")
    tempDict = LogProcessor()
    DictInput1 = "Hello"
    DictInput2 = [
        {"log_1": "NOTICE"},
        {"log_msg": "SRVR"},
        {"log_1": "ERROR"}
    ]
    print(
        f" Trying to validate input '{DictInput1}': "
        f"{tempDict.validate(DictInput1)}"
    )
    print(
        f" Trying to validate input '{DictInput2}': "
        f"{tempDict.validate(DictInput2)}"
    )
    print(f" Processing data: {DictInput2}: ")
    tempDict.ingest(DictInput2)
    for dictionary in DictInput2:
        key, value = tempDict.output()
        print(f"Log entry {key}: {value}")
