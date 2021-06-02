from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class Balance(BaseModel):
    asset: str
    delegated: float
    unbonding: float


class ValidatorStatus(Enum):
    active = 0
    inactive = 1
    in_jail = 2

    def __str__(self):
        return self.name


class Validator(BaseModel):
    apr: Optional[float]
    commission_rate: float = Field(alias='commissionRate')
    status: ValidatorStatus
    name: str = Field(alias='valName')
    address: str = Field(alias='validator')
    voting_power: float = Field(alias='votingPower')
    voting_power_proportion: float = Field(alias='votingPowerProportion')


class Validators(BaseModel):
    total: int
    validators: List[Validator]


class OperationType(Enum):
    delegate = 0
    undelegate = 1
    redelegate = 2

    def __str__(self) -> str:
        return self.name


class Operation(BaseModel):
    amount: float
    delegator: str
    operation_type: OperationType = Field(alias='operationType')
    src_validator: Optional[str] = Field(alias='srcValidator')
    src_val_name: Optional[str] = Field(alias='srcValName')
    time: datetime
    tx_hash: str = Field(alias='txHash')
    val_name: str = Field(alias='valName')
    validator: str


class Operations(BaseModel):
    total: int
    operations: List[Operation]


class Reward(BaseModel):
    chain_id: str = Field(alias='chainId')
    delegator: str
    height: int
    reward: float
    time: datetime = Field(alias='rewardTime')
    val_name: str = Field(alias='valName')
    validator: str


class Rewards(BaseModel):
    total: int
    rewards: List[Reward] = Field(alias='rewardDetails')
