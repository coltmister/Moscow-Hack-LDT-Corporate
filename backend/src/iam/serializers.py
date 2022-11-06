import datetime

from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


def validate_phone(value: str) -> str:
    if not value:
        return value
    answer, phone = check_phone(value)
    if not answer:
        raise ValidationError("Введите номер телефона в международном формате")
    return phone


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class UsernameSerializer(serializers.Serializer):
    username = serializers.CharField(validators=[validate_phone])


class PhoneNumSerializer(serializers.Serializer):
    phone_num = serializers.CharField(validators=[validate_phone])


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(validators=[validate_phone])
    token = serializers.UUIDField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    middle_name = serializers.CharField(allow_null=True, allow_blank=True)
    password = serializers.CharField()

    def validate(self, attrs):
        token = attrs['token']
        phone_num = self.initial_data['username']
        now = timezone.now()
        call = CallLog.objects.filter(
            phone_num=phone_num,
            token=token,
            is_call_made=True,
            call_until__gte=now,
            is_call_used=False)
        if not call.exists():
            raise ValidationError(
                f"Звонок для подтверждения номера телефона +{phone_num} не был совершен в последние {SECONDS_FOR_CALL // 60} минут(-ы)")
        self.context['call'] = call.last()
        return attrs

    def validate_password(self, value) -> str:
        phone_num = self.initial_data['username']
        if value == phone_num:
            raise ValidationError(f"Номер телефона не может являться паролем")
        if len(value) < 8:
            raise ValidationError(f"Пароль должен быть больше 7 символов")
        return value

    def create(self, validated_data):
        call = self.context.get('call')
        if not call:
            return False
        call.is_call_used = True
        call.save()
        return True


class CallSerializer(serializers.Serializer):
    timestamp = serializers.IntegerField()
    sip_phone_num = serializers.CharField(validators=[validate_phone])
    caller_id = serializers.CharField(validators=[validate_phone])

    def validate_timestamp(self, value: int) -> datetime.datetime:
        try:
            _datetime = make_local_time(datetime.datetime.fromtimestamp(value))
        except:
            raise ValueError("Переданное значение timestamp невалидно")
        return _datetime


class DidHeCallSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    sip_phone_num = serializers.CharField(validators=[validate_phone])
    phone_num = serializers.CharField(validators=[validate_phone])


class ResetPasswordViaCallSerializer(serializers.Serializer):
    phone_num = serializers.CharField(validators=[validate_phone])
    token = serializers.UUIDField()
    password = serializers.CharField()

    def validate(self, attrs):
        token = attrs['token']
        phone_num = self.initial_data['phone_num']
        now = timezone.now()
        call = CallLog.objects.filter(phone_num=phone_num,
                                      token=token,
                                      is_call_made=True,
                                      call_until__gte=now,
                                      is_call_used=False)
        if not call.exists():
            raise ValidationError(
                f"Звонок для подтверждения номера телефона +{phone_num} не был совершен в последние {SECONDS_FOR_CALL // 60} минут(-ы)")
        self.context['call'] = call.last()
        return attrs

    def validate_password(self, value) -> str:
        phone_num = self.initial_data['phone_num']
        if value == phone_num:
            raise ValidationError(f"Номер телефона не может являться паролем")
        if len(value) < 8:
            raise ValidationError(f"Пароль должен быть больше 7 символов")
        return value

    def create(self, validated_data):
        call = self.context.get('call')
        if not call:
            return False
        call.is_call_used = True
        call.save()
        return True
