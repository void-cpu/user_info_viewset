import random

from django.contrib.auth.hashers import make_password, check_password
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from urith.Pagination import BasePagination
from urith.Response import BaseResponse
from urith.ResponseMessage import ResponseMessage
from .serializers import *


class UserViewSets(ModelViewSet):
    queryset = UserModels.objects.all()
    serializer_class = UserListSerializers
    pagination_class = BasePagination
    filter_backends = [DjangoFilterBackend]
    filter_fields = {"UserName": ["exact", "in", "contains"], "phone": ["exact", "contains"]}

    # {"UserName": ['exact', 'lt', 'gt', "in", "contains"], "phone": ['exact', 'lt', 'gt', "in", "contains"]}

    def create(self, request, *args, **kwargs):
        password = request.data['UserPwd'] if 'UserPwd' in request.data else None
        password = make_password(password)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(UserPwd=password)
        return Response(serializer.data)

    @action(methods=['put'], detail=True)
    def set_password(self, request, pk=None):
        phone = request.data.get("phone")
        password, userNewPassword, userNewAgentPassword = request.data.get('password'), \
                                                          request.data.get("userNewPassword"), \
                                                          request.data.get("userNewAgentPassword")

        if not self.is_value_json(phone, password, userNewPassword, userNewAgentPassword):
            return Response(BaseResponse(Message=ResponseMessage.NoteFound.value).__str__(),
                            status=status.HTTP_400_BAD_REQUEST)
        if self.is_same_code(a_password=userNewPassword, b_password=userNewAgentPassword):
            try:
                if pk is not None:
                    _object = UserModels.objects.get(id=pk)
                else:
                    _object = UserModels.objects.get(phone=phone)
            except UserModels.DoesNotExist:
                return Response(BaseResponse(Message=ResponseMessage.NoteFound.value).__str__(),
                                status=status.HTTP_404_NOT_FOUND)
            if check_password(password, _object.pass_word):
                _object.pass_word = make_password(userNewPassword)
                _object.save()
                return Response(UserListSerializers(_object, many=False).data, status=status.HTTP_201_CREATED)
            else:
                return Response(BaseResponse(Message=ResponseMessage.NoteFound.value).__str__(),
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(BaseResponse(Message=ResponseMessage.Code(is_True=False), Phone=phone),
                            status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def is_value_json(*args):
        """:return 检查其中的元素是否有空值(有空值:True, 无空值:False)"""
        return not all(list(args))

    @staticmethod
    def is_same_code(code_01, code_02):
        return code_01 == code_02

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializers
        elif self.action == 'update':
            return UserUpdateSerializers
        else:
            return UserListSerializers

    @action(methods=['post'], detail=True)
    def login(self, request, pk=None):
        """
        - request {"username":"user phone", password="user password"}
        """
        username, password = request.data.get("username"), request.data.get("password")
        if not self.is_value_json(username, password):
            return Response(BaseResponse(Message=ResponseMessage.NullMessage.value).__str__(),
                            status=status.HTTP_401_UNAUTHORIZED)
        try:
            _object = UserModels.objects.get(user_name=username)
        except UserModels.DoesNotExist:
            return Response(BaseResponse(Message=ResponseMessage.NoteFound.value).__str__(),
                            status=status.HTTP_404_NOT_FOUND)
        if check_password(password, _object.pass_word):
            return Response(UserListSerializers(_object, many=False).data, status=status.HTTP_200_OK)
        else:
            return Response(BaseResponse(Message=ResponseMessage.NoteFound.value).__str__(),
                            status=status.HTTP_404_NOT_FOUND)

    @action(methods=["get", "set"], detail=True)
    def PhoneCode(self, request, pk=None):
        """
        get:得到手机验证码 request {"Phone": Phone}
        post:手机验证码验证 request {"Phone": Phone, "PhoneCode_01": GetPhoneCode, "PhoneCode_02":SetPhoneCode}
        """
        if request.method == "GET":
            Phone = request.data.get('Phone')
            if self.is_value_json(Phone):
                return Response(BaseResponse(Message=ResponseMessage.NullMessage.value).__str__(),
                                status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(BaseResponse(Phone=Phone, Message=random.randint(1000, 9999)),
                                status=status.HTTP_200_OK)
        elif request.method == "POST":
            Phone = request.data.get('Phone')
            PhoneCode_01 = request.data.get("PhoneCode_01")
            PhoneCode_02 = request.data.get("PhoneCode_02")
            if self.is_value_json(Phone, PhoneCode_02, PhoneCode_01):
                return Response(BaseResponse(Message=ResponseMessage.NullMessage.value).__str__(),
                                status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(BaseResponse(
                    Message=ResponseMessage.Code(is_True=self.is_same_code(code_02=PhoneCode_01, code_01=PhoneCode_02)),
                    Phone=Phone),
                    status=status.HTTP_401_UNAUTHORIZED)
