from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self):
        self.Memory = []
        self.total_processed = 0
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
                self.total_processed += 1
            elif isinstance(data, list):
                for item in data:
                    if not isinstance(item, (int, float)):
                        raise ValueError
                for item in data:
                    self.Memory.append(str(item))
                self.total_processed += len(data)
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
                self.total_processed += 1
            elif isinstance(data, list):
                for item in data:
                    if not isinstance(item, str):
                        raise ValueError
                for item in data:
                    self.Memory.append(str(item))
                self.total_processed += len(data)
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
                self.total_processed += 1
            elif isinstance(data, list):
                for item in data:
                    if not is_valid_dict(item):
                        raise ValueError
                for item in data:
                    self.Memory.append(str(item))
                self.total_processed += len(data)
            else:
                raise ValueError
        except ValueError:
            print("Invalid value to process, need Dict[Str:Str]!")


class DataStream():
    def __init__(self):
        self.ProcMem = []


    def register_processor(self, proc: DataProcessor) -> None:
        if isinstance(proc, DataProcessor):
            self.ProcMem.append(proc)
            if isinstance(proc, NumericProcessor):
                print("Registering NumericProcessor\n")
            elif isinstance(proc, TextProcessor):
                print("Registering TextProcessor\n")
            elif isinstance(proc, LogProcessor):
                print("Registering LogProcessor\n")
            else:
                print("No Processor Found, no data\n")


    def process_stream(self, stream: list[Any]) -> None:
        for item in stream:
            handled = False
            for proc in self.ProcMem:
                if proc.validate(item):
                    proc.ingest(item)
                    handled = True
                    break
            if not handled:
                print(
                    "DataStream error "
                    f"- Can't process element in stream: {item}"
                )


    def print_processors_stats(self) -> None:
        for proc in self.ProcMem:
            print(
                f"{proc.__class__.__name__}: "
                f"{proc.total_processed} items processed, "
                f"{len(proc.Memory)} items remaining on processor"
            )


if __name__ == "__main__":
    print("\n=== Code Nexus - Data Strem ===")
    ds = DataStream()
    stream = [
        "Hello Word",
        42,
        [34, 56, 78],
        {"5": "sword"},
        ["x", "y"],
        3.14
    ]
    ds.register_processor(NumericProcessor())
    ds.register_processor(LogProcessor())
    ds.register_processor(TextProcessor())
    ds.process_stream(stream)
    print(f"Send first batch of data: {stream}")
    print("\n=== DataStream statistic BEFORE output ===")
    ds.print_processors_stats()
    print("\n=== Consuming data from processors ===")
    for proc in ds.ProcMem:
        while True:
            idx, val = proc.output()
            if idx == -1:
                break
            print(f"{proc.__class__.__name__} -> ({idx}, {val})")
    print("\n=== DataStream statistic AFTER output ===")
    ds.print_processors_stats()
