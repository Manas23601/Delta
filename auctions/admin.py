from django.contrib import admin
from .models import Comment, Bid, User, listing, Watchlist


# Register your models here.
admin.site.register(listing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(User)
admin.site.register(Watchlist)