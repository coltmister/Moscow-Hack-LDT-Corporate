import datetime
import logging

from users.models import User, UserProfile, UserAddInfo

logger = logging.getLogger(__name__)


class UserData:

    def validate_dob(self, date_text):
        if not date_text:
            return None
        try:
            return str(datetime.datetime.strptime(date_text, '%Y-%m-%d').date())
        except ValueError:
            return None

    @staticmethod
    def register(userinfo):
        name = userinfo.get('given_name')
        surname = userinfo.get('family_name')
        patronymic = userinfo.get('patronymic')
        email = userinfo.get('email')
        birthdate = UserData().validate_dob(userinfo.get('dob'))
        username = userinfo.get('preferred_username')
        user_id = userinfo.get('sub')

        user = User.objects.create(id=user_id,
                                   username=username,
                                   name=name,
                                   surname=surname,
                                   patronymic=patronymic,
                                   email=email)
        UserProfile.objects.create(user=user, birthdate=birthdate)
        UserAddInfo.objects.create(user=user)
        return user
