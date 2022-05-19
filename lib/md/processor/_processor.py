import typing


# Metadata
__author__ = 'https://md.land/md'
__version__ = '1.0.0'
__all__ = (
    # Metadata
    '__author__',
    '__version__',
    # Exception
    'ProcessorException',
    'ProcessException',
    'ProvideException',
    # Contract
    'TaskInterface',
    'ProviderInterface',
    'ProcessorInterface',
    # Implementation
    'Worker',
)


# Exception
class ProcessorException(RuntimeError):
    """ Component marker exception """
    pass


class ProcessException(ProcessorException):
    """ Exception occurred while task processing """
    pass


class ProvideException(ProcessorException):
    """ Exception occurred while task providing """
    pass


# Contract
class TaskInterface:
    """ Task to process """
    pass


class ProviderInterface:
    """ Provides task to process """
    def provide(self) -> typing.Iterator[TaskInterface]:
        raise NotImplementedError


class ProcessorInterface:
    """ Processes task """
    def process(self, task: TaskInterface) -> None:
        raise NotImplementedError


# Implementation
class Worker:  # nt: unit
    def __init__(self, provider: ProviderInterface, processor: ProcessorInterface) -> None:
        self._provider = provider
        self._processor = processor

    def run(self) -> None:
        for task in self._provider.provide():
            self._processor.process(task=task)
