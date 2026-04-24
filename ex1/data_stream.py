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
            self.counter = 0
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
            self.counter = 0
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


class DataStream():
    def __init__(self):
        self.ProcMem = []
        self.textStream = 0
        self.numStream = 0
        self.logStream = 0
        self.sizeStream = 0


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
            self.sizeStream += 1
            for proc in self.ProcMem:
                if proc.validate(item):
                    proc.ingest(item)
                    if isinstance(proc, NumericProcessor):
                        self.numStream += 1
                    elif isinstance(proc, TextProcessor):
                        self.textStream += 1
                    elif isinstance(proc, LogProcessor):
                        self.logStream += 1
                    handled = True
            if not handled:
                print(
                    "DataStream error "
                    f"- Can't process element in stream: {item}"
                )


    def print_processors_stats(self) -> None:
        Tstream = self.textStream
        Nstream = self.numStream
        Lstream = self.logStream
        Sstream = self.sizeStream
        for proc in self.ProcMem:
            if isinstance(proc, NumericProcessor):
                NotPstream = Sstream - Nstream
                print(
                    f"Numeric Processor: total {Nstream} "
                    f"item processed, remaining {NotPstream} on processor"
                )
            elif isinstance(proc, TextProcessor):
                NotPstream = Sstream - Tstream
                print(
                    f"Text Processor: total {Tstream} "
                    f"item processed, remaining {NotPstream} on processor"
                )
            elif isinstance(proc, LogProcessor):
                NotPstream = Sstream - Lstream
                print(
                    f"Log Processor: total {Lstream} "
                    f"item processed, remaining {NotPstream} on processor"
                )
        print(f"Resume: Numeric {Nstream}, Text: {Tstream}, Log {Lstream}")


if __name__ == "__main__":
    print("=== Code Nexus - Data Strem ===\n")
    ds = DataStream()
    ds.register_processor(NumericProcessor())
    stream = [
        "Hello Word",
        42,
        [34, 56, 78],
        {"5": "sword"},
        ["x", "y"],
        3.14
    ]
    ds.register_processor(LogProcessor())
    ds.register_processor(TextProcessor())
    ds.process_stream(stream)
    print(f"Send first batch of data: {stream}")
    print("=== DataStress statistic ===\n")
    ds.print_processors_stats()
