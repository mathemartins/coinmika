from django.db import models


# Create your models here.
class BitcoinMnemonics(models.Model):
    seed_phrase = models.TextField()
    xpub = models.CharField(500, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "bitcoin_mnemonics"
        verbose_name = "bitcoin mnemonics"
        verbose_name_plural = "bitcoin mnemonics"

    def __str__(self):
        return self.xpub
