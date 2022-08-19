
class LibrarySystemException(Exception):
    """Base exception for this script.
    :note: This exception should not be raised directly."""
    pass

class UserResizeTerminalException(LibrarySystemException):
    pass
