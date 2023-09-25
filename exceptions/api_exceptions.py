class ApiConnectionError(Exception):
    def __init__(self, *args, **kwargs):
        self.message = (
            args[0] if args else "Не удалось подключиться к API"
        )