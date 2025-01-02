from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class SearchShopHistory(models.Model):
    result = models.JSONField()
    user = models.ForeignKey(User, models.CASCADE, related_name="search_shop_history")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.created_at}"
