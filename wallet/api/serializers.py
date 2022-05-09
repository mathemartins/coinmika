from rest_framework import serializers

from wallet.models import BitcoinMnemonics


class BitcoinMnemonicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BitcoinMnemonics
        fields = [
            'seed_phrase',
            'xpub',
            'timestamp',
            'updated',
        ]