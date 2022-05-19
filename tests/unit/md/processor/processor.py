import md.processor
import unittest.mock


def test_worker() -> None:
    # arrange
    task_1 = unittest.mock.Mock(md.processor.TaskInterface)
    task_2 = unittest.mock.Mock(md.processor.TaskInterface)
    task_3 = unittest.mock.Mock(md.processor.TaskInterface)

    provider = unittest.mock.Mock(md.processor.ProviderInterface)
    processor = unittest.mock.Mock(md.processor.ProcessorInterface)
    worker = md.processor.Worker(provider=provider, processor=processor)

    provider.provide = unittest.mock.MagicMock(return_value=[task_1, task_2, task_3])
    processor.process = unittest.mock.MagicMock()

    # act
    worker.run()

    # assert
    processor.process.assert_has_calls([
        unittest.mock.call(task=task_1),
        unittest.mock.call(task=task_2),
        unittest.mock.call(task=task_3),
    ])
