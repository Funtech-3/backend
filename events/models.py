from django.db import models


REGISTRATION_STATUSES = [
    ("OPEN", "Регистрация открыта"),
    ("CLOSED", "Регистрация завершена"),
    ("PENDING", "Ожидание регистрации")
]

EVENT_MODES = [
    ("ONLINE", "Онлайн"),
    ("OFFLINE", "Офлайн")
]


class City(models.Model):
    """Модель городов."""
    name = models.CharField("Название города", max_length=150, unique=True)

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "города"

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Модель тегов."""
    title = models.CharField("Название тега", max_length=150, unique=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "теги"

    def __str__(self):
        return self.title


class Speaker(models.Model):
    """Модель спикеров."""
    first_name = models.CharField("Имя", max_length=150)
    last_name = models.CharField("Фамилия", max_length=150)
    work_place = models.CharField("Место работы", max_length=256)
    position = models.CharField("Должность", max_length=256)
    image = models.ImageField("Фото", upload_to="speakers")

    class Meta:
        verbose_name = "Спикер"
        verbose_name_plural = "спикеры"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name}"


class Event(models.Model):
    """Модель события."""
    title = models.CharField("Название", max_length=150)
    description = models.TextField("Описание")
    slug = models.CharField("Символьный код", max_length=150, unique=True)
    city = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        verbose_name="Город проведения"
    )
    address = models.CharField("Адрес", max_length=150)
    date = models.DateField("Дата проведения", null=True)
    registration_status = models.CharField(
        "Статус регистрации",
        max_length=7,
        choices=REGISTRATION_STATUSES
    )
    tags = models.ManyToManyField(Tag)
    mode = models.CharField(
        "Формат проведения",
        max_length=7,
        choices=EVENT_MODES
    )

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "события"
        default_related_name = "events"
        ordering = ("-date", "title")

    def __str__(self):
        return self.title


class EventStep(models.Model):
    """Модель этапов программы события."""
    title = models.CharField("Название", max_length=256)
    start_time = models.TimeField("Начало этапа")
    description = models.TextField("Описание", blank=True)
    speakers = models.ManyToManyField(
        Speaker,
        blank=True,
        verbose_name="Спикер",
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        verbose_name="Событие"
    )

    class Meta:
        verbose_name = "Этап мероприятия"
        verbose_name_plural = "этапы мероприятия"
        ordering = ('start_time',)

    def __str__(self):
        return self.title
