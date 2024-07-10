from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from fuzzywuzzy import fuzz

class Stock(models.Model):
    company_name = models.CharField(max_length=255)
    company_symbol = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.company_name} ({self.company_symbol})"

# Signal handler to invalidate cache on Stock changes
@receiver(post_save, sender=Stock)
@receiver(post_delete, sender=Stock)
def invalidate_stocks_cache(sender, instance, **kwargs):
    cache.delete('stocks_list')
