from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from coinmika.restconf.permissions import AnonPermissionOnly
from coinmika.utils import get_mnemonic_seed_phrase, create_ledger_account, get_address, activate_transaction_alert, \
    get_account_list, create_ledger_account_for_added_coin
from wallet.models import BitcoinMnemonics, LedgerAccount, Address, AddedCoinMnemonics


class WalletCreate(APIView):
    permission_classes = [AnonPermissionOnly]

    def get(self, *args, **kwargs):
        user_seed: dict = get_mnemonic_seed_phrase(coin="bitcoin")
        bitcoin_mnemonics_obj = BitcoinMnemonics.objects.create(
            seed_phrase=user_seed.get("mnemonic"),
            xpub=user_seed.get("xpub")
        )

        ledger_account: dict = create_ledger_account(coin_symbol="BTC", xpub=user_seed.get("xpub"))
        LedgerAccount.objects.create(
            coin_symbol=ledger_account.get("currency"),
            available_balance=ledger_account.get("balance")["availableBalance"],
            account_balance=ledger_account.get("balance")["accountBalance"],
            xpub=bitcoin_mnemonics_obj,
            customer_id=ledger_account.get("customerId"),
            ledger_id=ledger_account.get("id"),
        )

        address: dict = get_address(ledger_account.get("id"))
        public_key_obj = Address.objects.create(
            xpub=bitcoin_mnemonics_obj,
            derivation_key=address.get("derivationKey"),
            address_key=address.get("address"),
            coin_symbol=address.get("currency")
        )

        # Activate Transaction alert on system
        activate_transaction_alert(public_key_obj.address_key, public_key_obj.coin_symbol)

        return Response(
            {
                "message": "successful",
                "success": True,
                "data": {
                    "mnemonic": user_seed.get("mnemonic"),
                    "xpub": user_seed.get("xpub"),
                    "coin_symbol": ledger_account.get("currency"),
                    "address_public_key": address.get("address"),
                    "availableBalance": ledger_account.get("balance")["availableBalance"],
                    "accountBalance": ledger_account.get("balance")["accountBalance"],
                    "customer_id": ledger_account.get("customerId"),
                    "ledger_id": ledger_account.get("id"),
                    "active": True,
                    "frozen": False
                }
            },
            status=status.HTTP_201_CREATED
        )


class AddCoin(APIView):
    permission_classes = [AnonPermissionOnly]

    def post(self, *args, **kwargs):
        """
        Sample Data:
        {
            "coin: "ethereum",
            "coinSymbol": "ETH",
            "ledgerId": "someRandomKeyOfFirstLedgerId",
        }
        """
        data = self.request.data
        user_seed: dict = get_mnemonic_seed_phrase(coin=data.get("coin"))
        mnemonics_obj = AddedCoinMnemonics.objects.create(
            seed_phrase=user_seed.get("mnemonic"),
            xpub=user_seed.get("xpub"),
            coin=data.get("coin")
        )

        ledger_account: dict = create_ledger_account_for_added_coin(
            coin_symbol=data.get("coinSymbol"),
            xpub=user_seed.get("xpub"),
            ledger_id=data.get("ledgerId")
        )
        LedgerAccount.objects.create(
            coin_symbol=ledger_account.get("currency"),
            available_balance=ledger_account.get("balance")["availableBalance"],
            account_balance=ledger_account.get("balance")["accountBalance"],
            xpub_added_coin=mnemonics_obj,
            customer_id=ledger_account.get("customerId"),
            ledger_id=ledger_account.get("id"),
        )

        address: dict = get_address(ledger_id=data.get("ledgerId"))
        public_key_obj = Address.objects.create(
            xpub_added_coin=mnemonics_obj,
            derivation_key=address.get("derivationKey"),
            address_key=address.get("address"),
            coin_symbol=address.get("currency")
        )

        # Activate Transaction alert on system
        activate_transaction_alert(public_key_obj.address_key, public_key_obj.coin_symbol)

        return Response(
            {
                "message": "successful",
                "success": True,
                "data": {
                    "mnemonic": user_seed.get("mnemonic"),
                    "xpub": user_seed.get("xpub"),
                    "coin_symbol": ledger_account.get("currency"),
                    "address_public_key": address.get("address"),
                    "availableBalance": ledger_account.get("balance")["availableBalance"],
                    "accountBalance": ledger_account.get("balance")["accountBalance"],
                    "active": True,
                    "frozen": False
                }
            },
            status=status.HTTP_201_CREATED
        )


class WalletRestore(APIView):
    permission_classes = [AnonPermissionOnly]

    def post(self, *args, **kwargs):
        """
        Sample Data:
        {
            "seedphrase: "goat, chicken, rat, house, monkey"
        }
        """
        data = self.request.data
        try:
            seed_obj = BitcoinMnemonics.objects.get(seed_phrase=data.get("seedphrase"))
            ledger_obj: LedgerAccount = LedgerAccount.objects.get(xpub=seed_obj)
            customer_id = ledger_obj.customer_id
            account_list: dict = get_account_list(customer_id=customer_id)
            return Response(
                {
                    "message": "Successful",
                    "success": True,
                    "data": account_list,
                },
                status=status.HTTP_200_OK
            )
        except BitcoinMnemonics.DoesNotExist:
            return Response(
                {
                    "message": "Invalid Seed",
                    "success": False,
                },
                status=status.HTTP_404_NOT_FOUND
            )


class ListWallets(APIView):
    permission_classes = [AnonPermissionOnly]

    def post(self, *args, **kwargs):
        """
        Sample Data:
        {
            "customerId: "someRandomKey"
        }
        """
        data = self.request.data
        try:
            account_list = get_account_list(customer_id=data.get("customerId"))
            return Response(
                {
                    "message": "Successful",
                    "success": True,
                    "data": account_list,
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "message": "Invalid Customer Id",
                    "success": False,
                },
                status=status.HTTP_404_NOT_FOUND
            )
