from django.contrib import admin

from .models import RefBook, RefBookVersion, RefBookElement

class RefBookVersionInline(admin.TabularInline):
    model = RefBookVersion
    extra = 0

class RefBookElementInline(admin.TabularInline):
    model = RefBookElement
    extra = 0

@admin.register(RefBook)
class RefBookAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "code",
        "name",
        "current_version",
        "current_version_start_date",
    )

    search_fields = (
        "code",
        "name",
    )

    inlines = (
        RefBookVersionInline,
    )

    @admin.display(description="Текущая версия")
    def current_version(self, obj):
        version = obj.get_current_version()

        return version.version if version else "-"

    @admin.display(description="Дата начала действия версии")
    def current_version_start_date(self, obj):
        version = obj.get_current_version()

        return version.start_date if version else "-"

@admin.register(RefBookVersion)
class RefBookVersionAdmin(admin.ModelAdmin):
    list_display = (
        "refbook_code",
        "refbook_name",
        "version",
        "start_date",
    )

    list_select_related = (
        "refbook",
    )

    list_filter = (
        "refbook",
        "start_date",
    )

    inlines = (
        RefBookElementInline,
    )

    @admin.display(description="Код справочника")
    def refbook_code(self, obj):
        return obj.refbook.code

    @admin.display(description="Наименование справочника")
    def refbook_name(self, obj):
        return obj.refbook.name

@admin.register(RefBookElement)
class RefBookElementAdmin(admin.ModelAdmin):
    list_display = (
        "version",
        "code",
        "value",
    )

    list_select_related = (
        "version",
        "version_refbook",
    )

    search_fields = (
        "code",
        "value",
        "version__version",
        "version__refbook__code",
    )