from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime  # 用于检查续订日期范围


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="输入一个日期，在今天和四周之内，默认是3周).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # 检查日期不在过去。
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # 检查日期在允许更改的范围内（+4周）。
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # 请记住始终返回清理过的数据。
        return data