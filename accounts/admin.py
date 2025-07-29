from django.contrib import admin
from .models import (
    User, Medal, Leaderboard, TransactionHistory, Question, News, Comment, Wallet, Profile,
    Task, Option, Bet, SiteBalance, NewsComment
)

admin.site.register(User)
admin.site.register(Medal)
admin.site.register(Leaderboard)
admin.site.register(TransactionHistory)
admin.site.register(Question)
admin.site.register(News)
admin.site.register(Comment)
admin.site.register(Wallet)
admin.site.register(Profile)
admin.site.register(Task)
admin.site.register(Option)
admin.site.register(Bet)
admin.site.register(SiteBalance)
admin.site.register(NewsComment)