from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer


class UserRegistrationAPIView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
        except serializers.ValidationError as err:
            return Response(
                data=serializer.errors,
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        tokens = RefreshToken.for_user(user)
        return Response(
            data={
                "message": "user registered successfully",
                "data": {"access_token": str(tokens.access_token), "refresh_token": str(tokens)},
            },
            status=status.HTTP_201_CREATED,
        )
