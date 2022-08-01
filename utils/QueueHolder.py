class _QueueHolder:
    _instance = None
    _queue = {}

    @property
    def queue(self):
        return self._queue


def queue_holder():
    if _QueueHolder._instance is None:
        _QueueHolder._instance = _QueueHolder()
    return _QueueHolder._instance

