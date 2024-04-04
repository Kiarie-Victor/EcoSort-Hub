from django.contrib import admin
from Accounts.models import Otp, PendingUserModel, Member


# Register your models here.
admin.site.register(Otp)
admin.site.register(PendingUserModel)
admin.site.register(Member)
