from rest_framework import exceptions
from rest_framework.views import exception_handler


class ValidationError(exceptions.APIException):
    status_code = 400
    default_code = 'invalid_inputs'


class NotAllowedError(exceptions.APIException):
    status_code = 401
    default_code = 'permission_denied'


class NotFound(exceptions.APIException):
    status_code = 404
    default_code = 'not_found'


class SomethingWrongHappened(exceptions.APIException):
    status_code = 500
    default_code = 'something_happened'


class ErrorHandler:
    default_message = 'مشکلی رخ داده است، ما در حال کار روی آن هستیم'
    default_exception = SomethingWrongHappened

    messages = {
        400: {
            'general': 'فیلدهای فرم ارائه شده دارای مشکلاتی هستند یا پر نشده اند',
            'invalid_phone': 'شماره تلفن معتبر نیست',
            'invalid_otp_code': 'کد امنیتی صحیح نمیباشد',
            'expired_otp_code': 'کد امنیتی منقضی شده است',
            'not_is_active': 'حساب کاربری شما غیر فعال گردیده است',
        },
        401: {
            'general': 'شما مجاز به انجام این کار نیستید',
        },
        404: {
            'general': 'پیدا نشد',
        },
        500: {
            'general': 'مشکلی در سرور وجود دارد',
        },
    }

    exception = {
        400: ValidationError,
        401: NotAllowedError,
        404: NotFound,
        500: SomethingWrongHappened,
    }

    @staticmethod
    def get_error_exception(error_code: int, message_id: str, exception=None) -> Exception:
        """
        Returns an exception based on error code and message id
        """
        try:
            message = ErrorHandler.messages[error_code][message_id]
        except KeyError:
            message = ErrorHandler.default_message

        if exception is None:
            try:
                exception = ErrorHandler.exception[error_code]
            except KeyError:
                exception = ErrorHandler.default_exception

        return exception({"messages": [{"message": message}], "code": message_id})

    @staticmethod
    def create_error_exception(error_code: int, message: str, exception=None) -> Exception:
        """
        Create an exception based on error code and message
        """
        if exception is None:
            try:
                exception = ErrorHandler.exception[error_code]
            except KeyError:
                exception = ErrorHandler.default_exception

        return exception({"messages": [{"message": message}], "code": 4})

    @staticmethod
    def get_error_message(error_code: int, message_id: str):
        """
        Returns a translated message based on the error code and message id
        """
        try:
            message = ErrorHandler.messages[error_code][message_id]
            return message
        except KeyError:
            return ErrorHandler.default_message


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,s
    # to get the standard error response.
    response = exception_handler(exc, context)
    messages = []

    if response and not response.data.get("messages"):
        for message in response.data:
            error_message = response.data[message]
            messages.append(
                {
                    "field": message,
                    "message": error_message if isinstance(error_message, exceptions.ErrorDetail) else error_message[0]
                }
            )
        response.data = {"messages": messages, "code": "serializer_errors"}

    return response
