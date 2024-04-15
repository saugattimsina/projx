from rest_framework.response import Response
from rest_framework import status


class SuccessResponse:
    def __new__(cls, message, data):
        response_dict = {"message": message, "data": data, "status": True}
        return Response(response_dict, status=status.HTTP_200_OK)


class FailedResponse:
    def __new__(cls, message, data=None):
        response_dict = {
            "error": message,
            "data": data if data is not None else [],
            "status": False,
        }
        return Response(response_dict, status=status.HTTP_400_BAD_REQUEST)
