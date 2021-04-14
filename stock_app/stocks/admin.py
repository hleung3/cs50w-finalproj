from django.contrib import admin

# Register your models here.
from .models import Room, Membership, Transaction,Saved_Stock

class RoomAdmin(admin.ModelAdmin):
    list_display = ("id","name", "create_date","max_users", "numUsers","starting_value")

class MembershipAdmin(admin.ModelAdmin):
    list_display = ("id","user","room","creator","date_join","total_asset_value","cash_remaining","stock_value","rank")

class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id","member","quantity","price","date","ticker")

class Saved_StockAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "date_added", "ticker", "initial_price")

admin.site.register(Room,RoomAdmin)
admin.site.register(Membership,MembershipAdmin)
admin.site.register(Transaction,TransactionAdmin)
admin.site.register(Saved_Stock,Saved_StockAdmin)