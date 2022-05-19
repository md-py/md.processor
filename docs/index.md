# Documentation
## Overview

md.process component defines task processing contracts.

## Architecture overview

[![Architecture overview][architecture-overview]][architecture-overview]

## Installation

```sh
pip install md.processor --index-url https://source.md.land/python/
```

## Usage example
### Image format converting 

```python3
import typing
import subprocess

import md.processor


class ConvertException(md.processor.ProcessException):
    """ Usually occurs when imagick processing failed """
    pass


class ConvertImageTask(md.processor.TaskInterface):
    def __init__(self, source_path: str, target_path: str) -> None:
        self.source_path = source_path
        self.target_path = target_path
        

class ConvertImageProcessor(md.processor.ProcessorInterface):
    def process(self, task: ConvertImageTask) -> None:
        command_parts = ['convert', task.source_path, task.target_path]

        command = subprocess.list2cmdline(seq=command_parts)
        process = subprocess.Popen(command_parts, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()

        if 0 == process.returncode:
            return

        raise ConvertException({
            'command': command,
            'code': process.returncode,
            'stdout': out.decode('utf-8'),
            'stderr': err.decode('utf-8'),
        })
```

```python3
if __name__ == '__main__':
    convert_image_processor = ConvertImageProcessor()
    
    # Use case #1: single task processing
    try:
        convert_image_processor.process(
            task=ConvertImageTask(
                source_path='../var/image.svg',
                target_path='../var/image.png',
            )
        )
    except ConvertException as e:
        exit(1)
```

```python3
if __name__ == '__main__':
    # Use case #2: task processing with task provider
    class ConvertImageTaskProvider(md.processor.ProviderInterface):
        def __init__(self, path: str, from_: str, to: str) -> None:
            self._path: str = path
            self._from: str = from_
            self._to: str = to
        
        def provide(self) -> typing.Iterator[ConvertImageTask]:
            import os
            import re
            
            for file in os.listdir(self._path):
                if not file.endswith(self._from):
                    continue
                
                yield ConvertImageTask(
                    source_path=self._path + '/' + file,
                    target_path=self._path + '/' + re.sub(rf'\.{self._from}$', f'.{self._to}', file),
                )

    convert_image_task_provider = ConvertImageTaskProvider(
        path='../var/',
        from_='png',
        to='svg',
    )
    
    for convert_image_task in convert_image_task_provider.provide():
        try:
            convert_image_processor.process(task=convert_image_task)
        except ConvertException as e:
            exit(1)
```

```python3
if __name__ == '__main__':            
    # Use case #3: as same as #2 using `worker` concept 
    worker = md.processor.Worker(
        provider=convert_image_task_provider,
        processor=convert_image_processor,
    )
    
    try:
        worker.run()
    except ConvertException as e:
        exit(1)
```

[architecture-overview]: _static/architecture.class-diagram.svg
