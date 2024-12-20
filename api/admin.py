from django.contrib import admin
from api.models import User, Category, Profile, Post, Group
from django.db.models import QuerySet
import random


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'mobile', 'date_joined')
    list_editable = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name', 'email')

    @admin.display(ordering='-age', description='Возрастной статус')
    def age_status(self, user):
        if user.age < 18:
            return 'Еще пиздюк'
        elif user.age < 30:
            return 'Пацан'
        elif user.age < 45:
            return 'Мужык'
        else:
            return 'Старец'

    actions = ['set_shit', 'set_good', 'set_perfect', 'set_elder']

    @admin.action(description='Сменить возраст и возрастной статус на "Еще пиздюк"')
    def set_shit(self, request, qs: QuerySet):
        count_updated = qs.count()
        for user in qs:
            user.age = random.randint(0, 17)
            user.rating = random.randint(0, 17)
            user.save()
        self.message_user(request, f'Было обновлено {count_updated} записей')

    @admin.action(description='Сменить возраст и возрастной статус на "Пацан"')
    def set_good(self, request, qs: QuerySet):
        count_updated = qs.count()
        for user in qs:
            user.age = random.randint(18, 29)
            user.rating = random.randint(18, 29)
            user.save()
        self.message_user(request, f'Было обновлено {count_updated} записей')

    @admin.action(description='Сменить возраст и возрастной статус на "Мужык"')
    def set_perfect(self, request, qs: QuerySet):
        count_updated = qs.count()
        for user in qs:
            user.age = random.randint(30, 44)
            user.rating = random.randint(30, 44)
            user.save()
        self.message_user(request, f'Было обновлено {count_updated} записей')

    @admin.action(description='Сменить возраст и возрастной статус на "Старец"')
    def set_elder(self, request, qs: QuerySet):
        count_updated = qs.count()
        for user in qs:
            user.age = random.randint(45, 999)
            user.rating = random.randint(45, 999)
            user.save()
        self.message_user(request, f'Было обновлено {count_updated} записей')


class RatingFilter(admin.SimpleListFilter):
    title = 'Фильтр по возрасту'
    parameter_name = 'rating'

    def lookups(self, request, model_admin):
        return [
            ('<18', 'Еще пиздюк'),
            ('<30', 'Пацан'),
            ('<45', 'Мужык'),
            ('>45', 'Старец')
        ]

    def queryset(self, request, queryset):
        if self.value() == '<18':
            return queryset.filter(rating__lt=18)
        elif self.value() == '<30':
            return queryset.filter(rating__gte=18, rating__lt=30)
        elif self.value() == '<45':
            return queryset.filter(rating__gte=30, rating__lt=45)
        elif self.value() == '>45':
            return queryset.filter(rating__gte=45)
        return queryset


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio',)
    search_fields = ('user__first_name', 'user__last_name', 'user__email')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'title',)
    search_fields = ('user__first_name', 'user__last_name', 'user__email')

    @admin.display(ordering='title')
    def title(self, obj):
        return obj.title


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    @admin.display(ordering='name')
    def name(self, obj):
        return obj.name
