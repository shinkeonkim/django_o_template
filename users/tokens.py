"""# users tokens
사용자 관련 토큰 제네레이터 모듈입니다.
"""

from django.contrib.auth.tokens import PasswordResetTokenGenerator


class UserActivationTokenGenerator(PasswordResetTokenGenerator):
    """# UserActivationTokenGenerator
    사용자 계정 활성화를 위한 토큰 제네레이터입니다.
    """

    def _make_hash_value(self, user, timestamp: int) -> str:
        return super()._make_hash_value(user, timestamp)


user_activation_token_generator = UserActivationTokenGenerator()
