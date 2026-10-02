from django.db import models

class RefBook(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=300, )
    description = models.TextField(blank=True, )

    class Meta:
        verbose_name = "Справочник"
        verbose_name_plural = "Справочники"

    def __str__(self):
        return f"{self.code} - {self.name}"

class RefBookVersion(models.Model):
    refbook = models.ForeignKey(
        RefBook,
        on_delete=models.CASCADE,
        related_name="versions",
    )
    version = models.CharField(max_length=50, )
    start_date = models.DateField(
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Версия справочника"
        verbose_name_plural = "Версии справочников"
        constraints = [
            models.UniqueConstraint(
                fields=["refbook", "version"],
                name="unique_refbook_version",
            ),
            models.UniqueConstraint(
                fields=["refbook", "start_date"],
                name="unique_refbook_start_date",
            ),
        ]

    def __str__(self):
        return f"{self.refbook.code} - {self.version}"

class RefBookElement(models.Model):
    version = models.ForeignKey(
        RefBookVersion,
        on_delete=models.CASCADE,
        related_name="elements",
    )
    code = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Элемент справочника"
        verbose_name_plural = "Элементы справочника"
        constraints = [
            models.UniqueConstraint(
                fields=["version", "code"],
                name="unique_version_element_code",
            ),
        ]

    def __str__(self):
        return f"{self.code} - {self.value}"