from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response: response.data = {"result": "error"}

    # Now add the HTTP status code to the response.
    if response is not None:
        reason = isinstance(exc.detail, list) and exc.detail[0] or exc.detail
        if isinstance(exc.detail, dict):
            reason = list(exc.detail.values())[0]
            if isinstance(reason, list):
                reason = reason[0]
        response.data['reason'] = reason

    return response
