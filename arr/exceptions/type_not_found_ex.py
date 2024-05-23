
class TypeNotFoundException(Exception):

    def __init__(self, *args: object) -> None:
        super(TypeNotFoundException, self).__init__(*args)

