from . import delegator


def reinitialize_delegators(params, step, sL, s, inputs):
    key = 'delegators'
    delegators = s['delegators']
    timestep = s['timestep']
    if timestep == 0:
        delegator.Delegator.delegate_counter = 0
        delegators = {0: delegator.Delegator(shares=10, minimum_shares=1, delegator_type=2, reserve_token_holdings=10000)}
        # make sure we start counting delegator id at 1 again.

    value = delegators
    print(f'{timestep=}, {delegators=}')
    return key, value


def reinitialize_supply(params, step, sL, s, inputs):
    key = 'supply'
    timestep = s['timestep']
    supply = s['supply']
    if timestep == 0:
        supply = 10

    value = supply
    # print(f'{timestep=}, {supply=}')
    return key, value


def reinitialize_reserve(params, step, sL, s, inputs):
    key = 'reserve'
    timestep = s['timestep']
    reserve = s['reserve']
    if timestep == 0:
        reserve = 10

    value = reserve
    # print(f'{timestep=}, {supply=}')
    return key, value
