from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserViewSerializer, UserUpdateSerializer
from .renderers import UserJSONRenderer

class UserRegistration(APIView):
    permission_classes = (AllowAny,)
    user_serializer_class = UserRegistrationSerializer
    renderer_classes = (UserJSONRenderer,)
    def post(self, request):
            user = request.data.get('user', {})
            user_serializer = self.user_serializer_class(data=user)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()
            return Response({'detail':'success'}, status=status.HTTP_201_CREATED)


class UserLogin(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserViewSerializer

    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserUpdate(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserUpdateSerializer

    def post(self, request):
        data = request.data.get('user', {})
        user = request.user
        serializer = self.serializer_class(user, data=data, partial=True)
        serializer.is_valid()
        serializer.save()
        return Response({'detail':'success'}, status=status.HTTP_200_OK)