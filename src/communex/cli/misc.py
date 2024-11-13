import typer
from typer import Context

from communex._common import BalanceUnit, format_balance
from communex.balance import from_nano
from communex.cli._common import CustomCtx
from communex.client import CommuneClient
from communex.compat.key import local_key_addresses
from communex.misc import get_map_modules
from communex.types import ModuleInfoWithOptionalBalance

misc_app = typer.Typer(no_args_is_help = True)


def circulating_tokens(c_client: CommuneClient) -> int:
    """
    Gets total circulating supply
    """

    with c_client.get_conn(init = True) as substrate:
        block_hash = substrate.get_block_hash()

    total_balance = c_client.get_total_free_issuance(block_hash = block_hash)
    total_stake = c_client.get_total_stake(block_hash = block_hash)
    return total_stake + total_balance


@misc_app.command()
def circulating_supply(ctx: Context, unit: BalanceUnit = BalanceUnit.joule):
    """
    Gets the value of all keys on the network, stake + balances
    """
    context = CustomCtx.get(ctx)
    client = context.com_client()

    with context.progress_status(
        "Getting circulating supply, across all subnets..."
    ):
        supply = circulating_tokens(client)

    formatted_output = format_balance(supply, unit)

    if context.use_json_output:
        context.output_json(
            formatted_value = formatted_output,
            value = supply,
            unit = unit,
        )
    else:
        context.output_raw(formatted_output)


@misc_app.command()
def apr(ctx: Context, fee: int = 0):
    """
    Gets the current staking APR on validators.
    The miner reinvest rate & fee are specified in percentages.
    """
    context = CustomCtx.get(ctx)
    client = context.com_client()

    # adjusting the fee to the correct format
    # the default validator fee on the commune network is 20%
    fee_to_float = fee / 100

    # network parameters
    block_time = 8  # seconds
    seconds_in_a_day = 86400
    blocks_in_a_day = seconds_in_a_day / block_time

    with context.progress_status("Getting staking APR..."):
        unit_emission = client.get_unit_emission()
        total_staked_tokens = client.query("TotalStake")
    # 50% of the total emission goes to stakers
    daily_token_rewards = blocks_in_a_day * from_nano(unit_emission) / 2
    _apr = (
        (daily_token_rewards * (1 - fee_to_float) * 365)
        / total_staked_tokens
        * 100
    )

    if context.use_json_output:
        context.output_json(
            fee = fee,
            apr = _apr
        )
    else:
        context.output_raw(f"Fee {fee} | APR {_apr:.2f}%")


@misc_app.command(name = "stats")
def stats(ctx: Context, balances: bool = False, netuid: int = 0):
    context = CustomCtx.get(ctx)
    client = context.com_client()

    with context.progress_status(
        f"Getting Modules on a subnet with netuid {netuid}..."
    ):
        modules = get_map_modules(
            client, netuid = netuid, include_balances = balances
        )
    modules_to_list = [value for _, value in modules.items()]
    local_keys = local_key_addresses(password_provider = context.password_manager)
    local_modules = [
        *filter(
            lambda module: module["key"] in local_keys.values(), modules_to_list
        )
    ]
    local_miners: list[ModuleInfoWithOptionalBalance] = []
    local_validators: list[ModuleInfoWithOptionalBalance] = []
    local_inactive: list[ModuleInfoWithOptionalBalance] = []
    for module in local_modules:
        if module["incentive"] == module["dividends"] == 0:
            local_inactive.append(module)
        elif module["incentive"] > module["dividends"]:
            local_miners.append(module)
        else:
            local_validators.append(module)

    if context.use_json_output:
        context.output_json(
            local_inactive = local_inactive,
            local_miners = local_miners,
            local_validators = local_validators
        )
    else:
        context.output_module_information(
            client, local_inactive, netuid, "inactive"
        )
        context.output_module_information(client, local_miners, netuid, "miners")
        context.output_module_information(
            client, local_validators, netuid, "validators"
        )


@misc_app.command(name = "treasury-address")
def get_treasury_address(ctx: Context):
    context = CustomCtx.get(ctx)
    client = context.com_client()

    with context.progress_status("Getting DAO treasury address..."):
        dao_address = client.get_dao_treasury_address()

    if context.use_json_output:
        context.output_json(
            address = dao_address
        )
    else:
        context.output_raw(dao_address)


@misc_app.command()
def delegate_rootnet_control(ctx: Context, key: str, target: str):
    """
    Delegates control of the rootnet to a key
    """
    context = CustomCtx.get(ctx)
    client = context.com_client()
    resolved_key = context.load_key(key, None)
    ss58_target = context.resolve_key_ss58(target, None)

    with context.progress_status("Delegating control of the rootnet..."):
        client.delegate_rootnet_control(resolved_key, ss58_target)

    context.info("Control delegated.")
