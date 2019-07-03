from django.utils.translation import ugettext_lazy as _


class RequestStatus(object):
    """Enum for Request status"""

    SUCCESS = 'success'
    FAIL = 'fail'

    CHOICES = (
        (SUCCESS, _('Успешно')),
        (FAIL, _('Ошибка')),
    )
