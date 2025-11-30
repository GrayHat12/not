# Source - https://stackoverflow.com/q/6760685
# Posted by theheadofabroom, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-27, License - CC BY-SA 4.0

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
