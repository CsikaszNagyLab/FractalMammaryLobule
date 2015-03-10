
class Notifier:
    def __init__(self):
        self.__callbacks = {}

    def add_callback(self, func):
        self.__callbacks[func] = 1

    def remove_callback(self, func):
        del self.__callbacks[func]

    def notify(self, *args):
        for func in self.__callbacks:
            func(*args)


class ProxyNotifier:
    def __init__(self):
        self.__callbacks = {}
        self.__notifier = None

    def add_callback(self, func):
        self.__callbacks[func] = 1
        if self.__notifier:
            self.__notifier.add_callback(func)

    def remove_callback(self, func):
        del self.__callbacks[func]
        if self.__notifier:
            self.__notifier.remove_callback(func)

    def attach(self, notifier):
        if self.__notifier:
            for f in self.__callbacks:
                self.__notifier.remove_callback(f)
        self.__notifier = notifier
        if self.__notifier:
            for f in self.__callbacks:
                self.__notifier.add_callback(f)

    def detach(self):
        self.attach(None)
