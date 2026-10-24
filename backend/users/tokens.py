from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)


def blacklist_all_tokens(user):
    """Blacklist every outstanding refresh token of the user.

    Tokens that are already blacklisted are skipped. OutstandingToken.user is
    SET_NULL, so the blacklist rows survive if the user is deleted afterwards.
    """
    outstanding = OutstandingToken.objects.filter(user=user)
    BlacklistedToken.objects.bulk_create(
        [BlacklistedToken(token=token) for token in outstanding],
        ignore_conflicts=True,
    )
