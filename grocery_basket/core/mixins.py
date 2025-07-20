from django.db import models


class DateAutoMixin(models.Model):
    """
    Во все наследуемые модели добавит поля дата создания и дата обновления.
    """

    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True)

    class Meta:
        abstract = True

    def __repr__(self):
        return f'{self.__class__.__name__}'
