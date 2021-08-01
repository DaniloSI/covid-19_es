class Subscriber():
    def update():
        raise NotImplementedError()

class Publisher():
    _subscribers = []

    def subscribe(self, subscriber):
        self._subscribers.append(subscriber)
    
    def notify_subscribers(self):
        for subscriber in self._subscribers:
            subscriber.update()