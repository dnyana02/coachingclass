import django_filters
from django_filters import DateFilter,CharFilter
from .models import *


class YclassFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name',lookup_expr='icontains')
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['timestamp','data_created','phone']