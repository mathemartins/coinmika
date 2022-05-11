import os

import requests

api_key: str = os.environ.get("TATUM_API_KEY")
network: str = os.environ.get("TATUM_NETWORK_TYPE")

"""
Get Mnemonic seed phrase for user and coin
curl --request GET \
  --url 'https://api-eu1.tatum.io/v3/{coin}/wallet'.format(coin="litecoin") \
  --header 'x-api-key: 2e2468f5-d6d2-4e76-b364-02d25dc62e3e'
  
  curl --request GET \
  --url 'https://api-eu1.tatum.io/v3/ethereum/wallet' \
  --header 'x-api-key: 2e2468f5-d6d2-4e76-b364-02d25dc62e3e'
  
  for ethereum 
  {"xpub":"xpub6FFhTcsQeuLM3xhuMmtpH5t9m3hh1NRZJKJPUHe2Vx1gkrHH9pTJTrkwjYKcjVGExgmnzjex1u8foPEjoTRbpFrBu7Qh92zqTfxY2L2Jr6P",
  "mnemonic":"moral salmon pond clip artwork choice inject zoo measure bunker approve capital story deliver mask toward pumpkin crumble lava brand defense street smart near"}
  
  
  Response
  {"mnemonic":"snake village rifle perfect put twenty horn lemon victory shield eternal tired assume prosper frozen market syrup loyal retire panic inside snap rug nuclear",
  "xpub":"tpubDFhQBEALpPC1svdY8FwinTRd9oEqojVgqpA8HQ9kPVz3zQPosuEZyPXmDmu9GrNAGzhTGeqJ1ca4f7M89HLnhMsWf1HAUdTtaAXryE2rHv8"}
"""


def get_mnemonic_seed_phrase(coin: str):
    headers = {'x-api-key': api_key}
    response = requests.get('https://api-eu1.tatum.io/v3/{coin}/wallet'.format(coin=coin), headers=headers)
    return response.json()


"""
Create Ledger Wallet for user and coin
curl --request POST \
  --url https://api-eu1.tatum.io/v3/ledger/account \
  --header 'content-type: application/json' \
  --header 'x-api-key: 2e2468f5-d6d2-4e76-b364-02d25dc62e3e' \
  --data '{"currency":"ETH","xpub":"xpub6FFhTcsQeuLM3xhuMmtpH5t9m3hh1NRZJKJPUHe2Vx1gkrHH9pTJTrkwjYKcjVGExgmnzjex1u8foPEjoTRbpFrBu7Qh92zqTfxY2L2Jr6P",
  "customer":{"accountingCurrency":"USD", "externalId": "62795458cf1a66a279592bbd"},
  "compliant":false,"accountingCurrency":"USD"}'
  
  
  for ethereum
  {"currency":"ETH","active":true,"balance":{"accountBalance":"0","availableBalance":"0"},"frozen":false,
  "xpub":"xpub6FFhTcsQeuLM3xhuMmtpH5t9m3hh1NRZJKJPUHe2Vx1gkrHH9pTJTrkwjYKcjVGExgmnzjex1u8foPEjoTRbpFrBu7Qh92zqTfxY2L2Jr6P",
  "accountingCurrency":"USD","customerId":"62795ff574ee9be5450db94b","id":"627966c5257a72ebe4df114f"}
  
  
  Response
  {"currency":"BTC","active":true,"balance":{"accountBalance":"0","availableBalance":"0"},
  "frozen":false,"xpub":"tpubDFhQBEALpPC1svdY8FwinTRd9oEqojVgqpA8HQ9kPVz3zQPosuEZyPXmDmu9GrNAGzhTGeqJ1ca4f7M89HLnhMsWf1HAUdTtaAXryE2rHv8",
  "customerId":"62781ba7e9e4efcfd4e6c75c","accountingCurrency":"USD","id":"62781ba7e9e4efcfd4e6c75b"}
"""


def create_ledger_account(coin_symbol: str, xpub: str):
    headers = {
        # 'content-type': 'application/json',
        'x-api-key': api_key,
    }

    json_data = {
        'currency': coin_symbol.upper(),
        'xpub': xpub,
        'customer': {'accountingCurrency': 'USD', 'externalId': '123654'},
        'compliant': False,
        'accountingCurrency': 'USD',
    }

    response = requests.post('https://api-eu1.tatum.io/v3/ledger/account', headers=headers, json=json_data)
    return response.json()


def create_ledger_account_for_added_coin(coin_symbol: str, xpub: str, ledger_id: str):
    headers = {
        # 'content-type': 'application/json',
        'x-api-key': api_key,
    }

    customer_payload = {'accountingCurrency': 'USD', 'externalId': ledger_id}

    json_data = {
        'currency': coin_symbol.upper(),
        'xpub': xpub,
        'customer': customer_payload,
        'accountingCurrency': 'USD',
    }

    response = requests.post('https://api-eu1.tatum.io/v3/ledger/account', headers=headers, json=json_data)
    return response.json()


"""
Generate Deposit Address
curl --request POST \
  --url 'https://api-eu1.tatum.io/v3/offchain/account/627966c5257a72ebe4df114f/address' \
  --header 'x-api-key: 2e2468f5-d6d2-4e76-b364-02d25dc62e3e'
  
  
  for ethereum
  {"xpub":"xpub6FFhTcsQeuLM3xhuMmtpH5t9m3hh1NRZJKJPUHe2Vx1gkrHH9pTJTrkwjYKcjVGExgmnzjex1u8foPEjoTRbpFrBu7Qh92zqTfxY2L2Jr6P",
  "derivationKey":1,"address":"0x04266ac3a846a4c5930dbaf3e364d4fc521ad457","currency":"ETH"}
  
  
  Response
  {"xpub":"tpubDFhQBEALpPC1svdY8FwinTRd9oEqojVgqpA8HQ9kPVz3zQPosuEZyPXmDmu9GrNAGzhTGeqJ1ca4f7M89HLnhMsWf1HAUdTtaAXryE2rHv8",
  "derivationKey":1,"address":"tb1q8mn5lseq7440uyzh52uk43kwtfvvm8ywxm2m2d","currency":"BTC"}%
"""


def get_address(ledger_id: str):
    headers = {'x-api-key': api_key}
    response = requests.post(
        'https://api-eu1.tatum.io/v3/offchain/account/{ledger_id}/address'.format(ledger_id=ledger_id),
        headers=headers
    )
    return response.json()


"""
Integrate Transaction Alert
curl --request POST \
  --url https://api-eu1.tatum.io/v3/subscription \
  --header 'content-type: application/json' \
  --header 'x-api-key: 2e2468f5-d6d2-4e76-b364-02d25dc62e3e' \
  --data '{"type":"ADDRESS_TRANSACTION","attr":{"address":"tb1q8mn5lseq7440uyzh52uk43kwtfvvm8ywxm2m2d",
  "chain":"BTC","url":"https://webhook.tatum.io/account"}}'
  
  
  Response
  {"id":"62782eca15e52ab29ce7b02f"}
"""


def activate_transaction_alert(address: str, coin_symbol: str):
    headers = {
        # 'content-type': 'application/json',
        'x-api-key': api_key,
    }
    json_data = {
        'type': 'ADDRESS_TRANSACTION',
        'attr': {
            'address': address,
            'chain': coin_symbol.upper(),
            'url': 'https://webhook.tatum.io/account',
        },
    }
    response = requests.post('https://api-eu1.tatum.io/v3/subscription', headers=headers, json=json_data)
    return response.json()


"""
List All Customers Account
curl --request GET \
  --url 'https://api-eu1.tatum.io/v3/ledger/account/customer/62795ff574ee9be5450db94b?pageSize=10' \
  --header 'x-api-key: 2e2468f5-d6d2-4e76-b364-02d25dc62e3e'
  
  
  Response
  [{"currency":"BTC","active":true,"balance":{"accountBalance":"0","availableBalance":"0"},
  "accountCode":null,"accountNumber":null,"frozen":false,
  "xpub":"tpubDFhQBEALpPC1svdY8FwinTRd9oEqojVgqpA8HQ9kPVz3zQPosuEZyPXmDmu9GrNAGzhTGeqJ1ca4f7M89HLnhMsWf1HAUdTtaAXryE2rHv8",
  "customerId":"62781ba7e9e4efcfd4e6c75c","accountingCurrency":"USD","id":"62781ba7e9e4efcfd4e6c75b"}]
"""


def get_account_list(customer_id: str):
    headers = {'x-api-key': api_key}
    params = {'pageSize': '10'}
    response = requests.get(
        'https://api-eu1.tatum.io/v3/ledger/account/customer/{customer_id}'.format(customer_id=customer_id),
        params=params, headers=headers
    )
    return response.json()


"""
Last Transaction per account
curl --request POST \
  --url 'https://api-eu1.tatum.io/v3/ledger/transaction/customer?pageSize=10' \
  --header 'content-type: application/json' \
  --header 'x-api-key: 2e2468f5-d6d2-4e76-b364-02d25dc62e3e' \
  --data '{"id":"62781ba7e9e4efcfd4e6c75c"}'
  
  Response
  []
"""


def get_last_transactions(customer_id: str):
    headers = {
        # 'content-type': 'application/json',
        'x-api-key': api_key,
    }
    params = {'pageSize': '10'}

    json_data = {'id': customer_id}
    response = requests.post(
        'https://api-eu1.tatum.io/v3/ledger/transaction/customer',
        params=params, headers=headers, json=json_data
    )
    return response.json()


"""
Get Account Details
curl --request GET \
  --url https://api-eu1.tatum.io/v3/ledger/account/62781ba7e9e4efcfd4e6c75b \
  --header 'x-api-key: 2e2468f5-d6d2-4e76-b364-02d25dc62e3e'
  
  
  Response
  {"currency":"BTC","active":true,"balance":{"accountBalance":"0","availableBalance":"0"},
  "accountCode":null,"accountNumber":null,"frozen":false,
  "xpub":"tpubDFhQBEALpPC1svdY8FwinTRd9oEqojVgqpA8HQ9kPVz3zQPosuEZyPXmDmu9GrNAGzhTGeqJ1ca4f7M89HLnhMsWf1HAUdTtaAXryE2rHv8",
  "customerId":"62781ba7e9e4efcfd4e6c75c","accountingCurrency":"USD","id":"62781ba7e9e4efcfd4e6c75b"}
"""


def get_account_details(ledger_id: str):
    headers = {'x-api-key': api_key}
    response = requests.get(
        'https://api-eu1.tatum.io/v3/ledger/account/{ledger_id}'.format(ledger_id=ledger_id),
        headers=headers
    )
    return response.json()


"""
Transactions connected to this account
curl --request POST \
  --url 'https://api-eu1.tatum.io/v3/ledger/transaction/account?pageSize=10' \
  --header 'content-type: application/json' \
  --header 'x-api-key: 2e2468f5-d6d2-4e76-b364-02d25dc62e3e' \
  --data '{"id":"62781ba7e9e4efcfd4e6c75b"}'
  
  
  Response
  []
"""


def get_transactions_for_account(ledger_id: str):
    headers = {
        # 'content-type': 'application/json',
        'x-api-key': api_key,
    }
    params = {'pageSize': '10'}
    json_data = {'id': ledger_id}
    response = requests.post(
        'https://api-eu1.tatum.io/v3/ledger/transaction/account',
        params=params, headers=headers, json=json_data
    )
    return response.json()


"""
Get all deposit address
curl --request GET \
  --url https://api-eu1.tatum.io/v3/offchain/account/62781ba7e9e4efcfd4e6c75b/address \
  --header 'x-api-key: 2e2468f5-d6d2-4e76-b364-02d25dc62e3e'
  
  
  Response
  [{"xpub":"tpubDFhQBEALpPC1svdY8FwinTRd9oEqojVgqpA8HQ9kPVz3zQPosuEZyPXmDmu9GrNAGzhTGeqJ1ca4f7M89HLnhMsWf1HAUdTtaAXryE2rHv8",
  "derivationKey":1,"address":"tb1q8mn5lseq7440uyzh52uk43kwtfvvm8ywxm2m2d","currency":"BTC"},
  {"xpub":"tpubDFhQBEALpPC1svdY8FwinTRd9oEqojVgqpA8HQ9kPVz3zQPosuEZyPXmDmu9GrNAGzhTGeqJ1ca4f7M89HLnhMsWf1HAUdTtaAXryE2rHv8",
  "derivationKey":2,"address":"tb1qavdnz083xar0njnulgl6wnrpkzp0za064qumj3","currency":"BTC"}]
"""


def get_deposit_addresses(ledger_id: str):
    headers = {'x-api-key': api_key}
    response = requests.get(
        'https://api-eu1.tatum.io/v3/offchain/account/{ledger_id}/address'.format(ledger_id=ledger_id),
        headers=headers
    )
    return response.json()


"""
Transfer Asset
curl --request POST \
  --url https://api-eu1.tatum.io/v3/offchain/bitcoin/transfer \
  --header 'content-type: application/json' \
  --header 'x-api-key: 2e2468f5-d6d2-4e76-b364-02d25dc62e3e' \
  --data '{"senderAccountId":"5e68c66581f2ee32bc354087","address":"mpTwPdF8up9kidgcAStriUPwRdnE9MRAg7","amount":"0.001",
  "mnemonic":"urge pulp usage sister evidence arrest palm math please chief egg abuse",
  "xpub":"xpub6EsCk1uU6cJzqvP9CdsTiJwT2rF748YkPnhv5Qo8q44DG7nn2vbyt48YRsNSUYS44jFCW9gwvD9kLQu9AuqXpTpM1c5hgg9PsuBLdeNncid"}'
 
  
  Response
  {
      "id": "5e68c66581f2ee32bc354087",
      "txId": "c83f8818db43d9ba4accfe454aa44fc33123d47a4f89d47b314d6748eb0e9bc9",
      "completed": true
  }

"""


def transfer(coin: str, ledger_id: str, address: str, amount: str, seed_phrase: str, xpub: str):
    headers = {
        # 'content-type': 'application/json',
        'x-api-key': api_key,
    }
    json_data = {
        'senderAccountId': ledger_id,
        'address': address,
        'amount': amount,
        'mnemonic': seed_phrase,
        'xpub': xpub
    }
    response = requests.post(
        'https://api-eu1.tatum.io/v3/offchain/{coin}/transfer'.format(coin=coin),
        headers=headers, json=json_data
    )
    return response.json()
