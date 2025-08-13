from django.contrib import admin
from .models import *
admin.site.register(Buyer)
admin.site.register(Artist)
admin.site.register(Logo)
admin.site.register(Portraits)
admin.site.register(Payment)

admin.site.register(Spam)
admin.site.register(Message)
admin.site.register(Feedback)
admin.site.register(ProductFeedback)
# Register your models here.
# admin.site.register(Notification)

admin.site.register(PostModel)
admin.site.register(CommentSectionModel)
admin.site.register(Order)