from django.db import models


# Create your models here.
class BitcoinMnemonics(models.Model):
    seed_phrase = models.TextField()
    xpub = models.CharField(max_length=500, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "bitcoin_mnemonics"
        verbose_name = "bitcoin mnemonics"
        verbose_name_plural = "bitcoin mnemonics"

    def __str__(self):
        return self.xpub


class LedgerAccount(models.Model):
    coin_symbol = models.CharField(max_length=300)
    active = models.BooleanField(default=True)
    available_balance = models.CharField(max_length=300)
    account_balance = models.CharField(max_length=300)
    frozen = models.BooleanField(default=False)
    xpub = models.ForeignKey(BitcoinMnemonics, on_delete=models.CASCADE)
    customer_id = models.CharField(max_length=300)
    currency = models.CharField(max_length=300, default="USD")
    ledger_id = models.CharField(max_length=300)

    class Meta:
        db_table = "ledger_account"
        verbose_name = "ledger account"
        verbose_name_plural = "ledger accounts"

    def __str__(self):
        return self.ledger_id


class Address(models.Model):
    xpub = models.ForeignKey(BitcoinMnemonics, on_delete=models.CASCADE)
    derivation_key = models.IntegerField()
    address_key = models.CharField(max_length=300)
    coin_symbol = models.CharField(max_length=300)

    class Meta:
        db_table = "address"
        verbose_name = "address"
        verbose_name_plural = "address"

    def __str__(self):
        return self.address_key
