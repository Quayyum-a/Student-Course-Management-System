

# Validation Exceptions
class ValidationError(Exception):
    pass

class InvalidEmailError(ValidationError):
    pass

class EmptyFieldError(ValidationError):
    pass

class InvalidFormatError(ValidationError):
    pass

# Resource Exceptions
class ResourceError(Exception):
    pass

class ResourceNotFoundError(ResourceError):
    pass

class ResourceAlreadyExistsError(ResourceError):
    pass

# Data Access Exceptions
class DataAccessError(Exception):
    pass

class FileOperationError(DataAccessError):
    pass
