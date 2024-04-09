from django.http import Http404
from django.contrib.auth.hashers import check_password
from django.utils.translation import gettext_lazy as _

from rest_framework import views, permissions, status, viewsets, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken

from .auth import UserTokenAuthentication
from utils.mixins import PaginationMixin
from utils.paginations import FetusPageNumberPagination
from utils.exceptions import (
    UserException,
    handle_exceptions
)
from .models import User
from .serializers import (
    UserSerializer,
    UserLoginSerializer,
    RegisterUserSerializer
)


class UsersViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    PaginationMixin,
):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer
    pagination_class = FetusPageNumberPagination
    authentication_classes = [UserTokenAuthentication]
    queryset = User.objects.all().order_by('id')

    def list(self, request):
        """
        API to list all users

        ### Example Request:
            GET /api/users/
        ### Example Response:
        {
            "response_code": 200,
            "data": {
                "count": 10,
                "next": "http://127.0.0.1:8000/api/users/?page=2",
                "prev": null,
                "results": [
                    {
                        "id": 24,
                        "first_name": "MitraTest2",
                        "last_name": "Test2",
                        "email": "test2@gmail.com",
                        "phone_number": "004928166432",
                        "profile_image": null,
                    },.....
                ],
            },
            "response_message": "User details sent successfully."
        }
        """

        try:
            _ = get_object_or_404(User, pk=request.user.id)
            users_query = self.queryset.filter(is_active=True, is_superuser=False)
            page = self.paginate_queryset(users_query)
            if page is not None:
                serializer = self.get_paginated_response(
                    self.get_serializer(page, many=True).data
                )
            else:
                serializer = self.get_serializer(users_query, many=True)
            return Response({
                    'response_code': status.HTTP_200_OK,
                    'data': serializer.data,
                    'response_message': _('User details sent successfully.')
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return handle_exceptions(e, 'No user details found.')

    def update(self, request, *args, **kwargs):
        """
        API to update user fields

        ### Example Request:
            PUT /api/users/<user_id>/
            {
                "first_name": "Mitra",
                "last_name": "Home",
                "phone_number": "004912225922",
                "email": "test123@example.com".
                "profile_image": 'image_to_upload.png',
            }
        ### Example Response:
            {
                "response_code": 200,
                "data": {
                    "id": 24,
                    "first_name": "MitraTest2",
                    "last_name": "Test2",
                    "email": "test2@gmail.com",
                    "phone_number": "004928166432",
                    "profile_image": '{base_url}/media/image_to_upload.png',
                },
                "response_message": "User details sent successfully."
            }
        """

        try:
            instance = self.get_object()
            self.validate_request_user(request, instance)
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response({
                    'response_code': status.HTTP_200_OK,
                    'data': serializer.data,
                    'response_message': _('User updated successfully.'),
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return handle_exceptions(e, 'User does not exist.')

    def retrieve(self, request, *args, **kwargs):
        """
        API to retrieve details of a single user.

        ### Example Request:
            GET /api/users/<user_id>/
        ### Example Response:
        {
            "response_code": 200,
            "data": {
                "id": 24,
                "first_name": "MitraTest2",
                "last_name": "Test2",
                "email": "test2@gmail.com",
                "phone_number": "004928166432",
                "profile_image": null,
            },
            "response_message": "User details sent successfully."
        }
        """

        try:
            _ = get_object_or_404(User, pk=request.user.id)
            instance = self.get_object()
            self.validate_request_user(request, instance)

            return Response({
                    'response_code': status.HTTP_200_OK,
                    'data': self.get_serializer(instance).data,
                    'response_message': _('User details sent successfully.'),
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return handle_exceptions(e, 'User does not exist.')

    def delete(self, request, pk):
        """
        API to de-activate a User

        ### Example Request:
            DELETE /api/users/<user_id>/
        ### Example Response:
        {
            "response_code": 200,
            "data": {
                "id": 24,
                "first_name": "MitraTest2",
                "last_name": "Test2",
                "email": "test2@gmail.com",
                "phone_number": "004928166432",
                "profile_image": null,
            },
            "response_message": "User details sent successfully."
        }
        """

        try:
            user_to_deactivate = get_object_or_404(User, pk=pk)
            self.validate_request_user(request, user_to_deactivate)

            if user_to_deactivate:
                user_to_deactivate.is_active = False
                user_to_deactivate.save()

            return Response({
                    "response_code": status.HTTP_200_OK,
                    "response_message": _('User De-activated successfully.'),
                    "data": UserSerializer(user_to_deactivate).data,
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return handle_exceptions(e, 'User does not exist.')

    def validate_request_user(self, request, instance):
        if not request.user == instance:
            raise UserException()


class RegisterUserAPIView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def post(self, request):
        """
        This API is used to register user.

        ### Example Request:
        POST /api/register/
        {
            "first_name": "test",
            "last_name": "23"
            "email": "test_signup2@yopmail.com",
            "password": "123",
            "phone_number": "123456"
        }

        ### Example Response:
        {
            "response_code": 201,
            "response_message": "User registered successfully.",
            "data": {
                'user': {
                    "id": 14,
                    "first_name": "test",
                    "last_name": "23"
                    "email": "test_signup2@yopmail.com",
                    "phone_number": "123456",
                    "profile_image": null
                },
            },
        }
        """
        print(request)
        print(request.body, request.POST)
        try:
            serializer = RegisterUserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            payload = serializer.data

            user = User.objects.filter(email=payload.get("email"))
            if user:
                return Response({
                        "response_code": status.HTTP_200_OK,
                        "response_message": _('User with this email already exist.'),
                        "data": None,
                    }, status=status.HTTP_200_OK)

            user = User.objects.filter(phone_number=payload.get("phone_number"))
            if user:
                return Response({
                        "response_code": status.HTTP_200_OK,
                        "response_message": _('User with this phone already exist.'),
                        "data": None,
                    }, status=status.HTTP_200_OK)

            user = User.objects.create(
                username=payload.get("email"),
                email=payload.get("email"),
                first_name=payload.get('first_name'),
                last_name=payload.get('last_name'),
                phone_number=payload.get('phone_number'),
                is_logged_in=False,
            )
            user.set_password(payload.get("password"))
            user.save()

            return Response({
                    "response_code": status.HTTP_201_CREATED,
                    "response_message": _('User registered successfully.'),
                    "data": {
                        'user': self.serializer_class(user).data,
                    },
                }, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({
                "response_code": status.HTTP_400_BAD_REQUEST,
                "response_message": _('Some thing went wrong. Please try again later.'),
                "data": None,
            }, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def post(self, request):
        """
        API to used to login from dashboard

        ### Example Request:
        POST /api/login/
        {
            "email": "example@abc.com",
            "password": "xyz"
        }

        ### Example Response:
        {
            "response_code": 200,
            "response_message": Logged in successfully.,
            "data": {
                'user': {
                    "id": 13,
                    "first_name": "test",
                    "last_name": "23"
                    "email": "test_signup2@yopmail.com",
                    "phone_number": "123456"
                    "profile_image": "/media/pexels-luca-nardone-4827696_MBMxW8e.jpg"
                },
            },
        },
        """

        try:
            payload = request.data
            serializer = UserLoginSerializer(data=payload)
            serializer.is_valid(raise_exception=True)
            user = get_object_or_404(User, email=payload['email'])
            if check_password(payload['password'], user.password):
                user.is_logged_in = True
                user.save()

                return Response({
                        'response_code': status.HTTP_200_OK,
                        'response_message': _('Logged in successfully.'),
                        'data': {
                            'user': self.serializer_class(user).data,
                        }
                    }, status=status.HTTP_200_OK)

            return Response({
                    'response_code': status.HTTP_401_UNAUTHORIZED,
                    'response_message': _('Please enter a valid password.'),
                    'data': None
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Http404:
            return Response({
                    "response_code": status.HTTP_404_NOT_FOUND,
                    "response_message": _('Please enter a valid email.'),
                    "data": None,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                    "response_code": status.HTTP_400_BAD_REQUEST,
                    "response_message": _('Some thing went wrong. Pleae try again later.'),
                    "data": None,
                }, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [UserTokenAuthentication]

    def post(self, request):
        """
        API to used to login from dashboard

        ### Example Request:
        POST /api/logout/

        ### Example Response:
        {
            "response_code": 200,
            "response_message": User logged out successfully.,
            "data": None
        },
        """

        try:
            user = request.user
            user = get_object_or_404(User, pk=user.id)
            user.is_logged_in = False
            user.auth_token.delete()
            user.save()

            return Response({
                    "response_code": status.HTTP_200_OK,
                    "response_message": _('User logged out successfully.'),
                    "data": None,
                }, status=status.HTTP_200_OK)
        except Http404:
            return Response({
                    "response_code": status.HTTP_404_NOT_FOUND,
                    "response_message": _('Unauthorized user.'),
                    "data": None,
                }, status=status.HTTP_404_NOT_FOUND)


class AuthTokenView(ObtainAuthToken):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        payload = request.data
        try:
            username = payload.get('username')
            password = payload.get('password')
            user = get_object_or_404(User, email=username)

            if not check_password(password, user.password) or not user:
                return Response({
                        'response_code': status.HTTP_401_UNAUTHORIZED,
                        'response_message': _('User with provided credentials does not exist.'),
                        'data': None
                    }, status=status.HTTP_401_UNAUTHORIZED)

            if not user.is_active or not user.is_logged_in:
                return Response({
                    'response_code': status.HTTP_401_UNAUTHORIZED,
                    'response_message': _('User is not authenticated.'),
                    'data': None
                }, status=status.HTTP_401_UNAUTHORIZED)

        except Http404:
            return Response({
                    'response_code': status.HTTP_401_UNAUTHORIZED,
                    'response_message': _('User does not exists.'),
                    'data': None
                }, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({
                    'response_code': status.HTTP_400_BAD_REQUEST,
                    'response_message': _('Unable to create token.'),
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)

        token_data = super().post(request=request, *args, **kwargs).data
        return Response({
                'response_code': status.HTTP_200_OK,
                'response_message': _('Token successfully created.'),
                'data': {
                    'token': token_data['token']
                }
            }, status=status.HTTP_200_OK)
