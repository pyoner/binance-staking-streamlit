import requests
import pydantic

from .models import Balance, Operations, Rewards, Validators

BASE_URL = 'https://api.binance.org'


def reponse_to_model(r: requests.Response, model: pydantic.BaseModel):
    json = r.json()
    if r.status_code:
        return model.parse_obj(json)
    else:
        raise Exception(r.status_code, json)


def get_balance(address: str) -> Balance:
    return reponse_to_model(
        requests.get(f'{BASE_URL}/v1/staking/accounts/{address}/balance'),
        Balance)


def get_validators(offset: int = 0, limit: int = 100, chain_id: str = 'bsc') -> Validators:
    return reponse_to_model(
        requests.get(f'{BASE_URL}/v1/staking/chains/{chain_id}/validators',
                     params={'offset': offset, 'limit': limit}), Validators)


def get_operations_by_delegator(delegator: str, offset: int = 0, limit: int = 100, chain_id: str = 'bsc') -> Operations:
    return reponse_to_model(
        requests.get(
            f'{BASE_URL}/v1/staking/chains/{chain_id}/delegators/{delegator}/operations',
            params={'offset': offset, 'limit': limit}),
        Operations)


def get_delegator_rewards(delegator: str, offset: int = 0, limit: int = 100, chain_id: str = 'bsc') -> Rewards:
    return reponse_to_model(
        requests.get(f'{BASE_URL}/v1/staking/chains/{chain_id}/delegators/{delegator}/rewards',
                     params={'offset': offset, 'limit': limit}),
        Rewards
    )
