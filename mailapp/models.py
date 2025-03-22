from django.db import models

from users.models import CustomUser


class RecipientMail(models.Model):
    email = models.EmailField(max_length=100, unique=True, verbose_name="Email")
    full_name = models.CharField(max_length=100, verbose_name="Ф.И.О.")
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Владелец", null=True, blank=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Получатель письма"
        verbose_name_plural = "Получатели писем"
        ordering = ["full_name"]


class MailMessage(models.Model):
    subject = models.CharField(max_length=200, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Тело письма")
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Владелец", null=True, blank=True)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["subject"]


class Mailing(models.Model):
    CREATED = "Создана"
    STARTED = "Запущена"
    FINISHED = "Завершена"
    MINUTLY = "раз в минуту"
    DAILY = ("раз в день",)
    WEEKLY = ("раз в неделю",)
    MONTHLY = ("раз в месяц",)

    STATUS_CHOICES = (
        (CREATED, "Создана"),
        (STARTED, "Запущена"),
        (FINISHED, "Завершена"),
    )

    FREQUENCY_CHOICES = (
        ("MINUTLY", "раз в минуту"),
        ("DAILY", "раз в день"),
        ("WEEKLY", "раз в неделю"),
        ("MONTHLY", "раз в месяц"),
    )

    start_time = models.DateTimeField(verbose_name="Дата и время первой отправки", blank=True, null=True)
    end_time = models.DateTimeField(verbose_name="Дата и время последней отправки", blank=True, null=True)
    status = models.CharField(max_length=15, verbose_name="Статус рассылки", default=CREATED, choices=STATUS_CHOICES)
    message = models.ForeignKey(MailMessage, verbose_name="Сообщение", on_delete=models.CASCADE, blank=True, null=True)
    recipients = models.ManyToManyField(RecipientMail, verbose_name="Получатели писем")
    frequency = models.CharField(verbose_name="Частота рассылки", max_length=20, choices=FREQUENCY_CHOICES)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Владелец рассылки", null=True, blank=True)

    def __str__(self):
        return f"{self.message} - {self.status}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [("can_view_mailing", "Can view mailing"), ("can_disabling_mailing", "Can disabling mailing")]


class MailingAttempt(models.Model):

    SUCCESSFULLY = "Успешно"
    UNSUCCESSFULLY = "Не успешно"

    STATUS_CHOICES = (
        (SUCCESSFULLY, "Успешно"),
        (UNSUCCESSFULLY, "Не успешно"),
    )

    date_mailing = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, verbose_name="Статус попытки", choices=STATUS_CHOICES)
    mail_server_response = models.TextField(blank=True, null=True)
    mailing = models.ForeignKey(Mailing, verbose_name="Рассылка", on_delete=models.CASCADE)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Владелец", null=True, blank=True)

    class Meta:
        verbose_name = "Попытка отправки письма"
        verbose_name_plural = "Попытки отправки писем"