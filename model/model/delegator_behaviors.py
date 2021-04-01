import random


def may_act_this_timestep(params, step, sL, s):
    acting_delegator_ids = []
    for id, delegator in s['delegators'].items():
        if delegator.will_act():
            acting_delegator_ids.append(id)

    # randomize list.
    random.shuffle(acting_delegator_ids)

    return {'acting_delegator_ids': acting_delegator_ids}


def act(params, step, sL, s, inputs):
    #  loop through acting delegators id list
    spot_price = s['spot_price']
    reserve = s['reserve']
    supply = s['supply']
    timestep = s['timestep']
    mininum_required_price_pct_diff_to_act = params['mininum_required_price_pct_diff_to_act']

    acting_delegator_ids = inputs['acting_delegator_ids']
    # print(f'act: {acting_delegator_ids=}')
    for delegator_id in acting_delegator_ids:
        #   accounting of current state (previous actor will have changed it)
        #   active delegator computes their evaluation (private price)
        delegator = s['delegators'][delegator_id]

        # created_shares and added_reserve will be positive on buy and negative for a sell.
        # print(f'act: {delegator.shares=}')
        created_shares, added_reserve = delegator.buy_or_sell(supply, reserve, spot_price,
                                                              mininum_required_price_pct_diff_to_act,
                                                              timestep)
        # print(f'act: {delegator_id=}, {created_shares=}, {added_reserve=}')
        supply += created_shares
        reserve += added_reserve

        spot_price = 0
        if supply > 0:
            spot_price = 2 * reserve / supply

        #  if buy, compute amount of reserve to add such that realized price is equal to private price
        #    if the amount is greater than reserve assets i have personally, then do it all

    key = 'delegators'
    value = s['delegators']
    return key, value
