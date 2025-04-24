from django.contrib import admin
from .models import User, Medal, LeaderBoard, TransactionHistory, Question, News, Comment, Wallet, Profile

admin.site.register(User)
admin.site.register(Medal)
admin.site.register(LeaderBoard)
admin.site.register(TransactionHistory)
admin.site.register(Question)
admin.site.register(News)
admin.site.register(Comment)
admin.site.register(Wallet)
admin.site.register(Profile)