from win10toast import ToastNotifier


class Notifier():
    def __init__(self):
        self.toaster = ToastNotifier()

    def notify(self, title, messages):
        joinedMessage = "\n".join(messages)
        self.toaster.show_toast(title, joinedMessage)
