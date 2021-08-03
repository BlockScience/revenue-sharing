import random


def may_act_this_timestep(params, step, sL, s):
    acting_delegator_ids = []
    for id, delegator in s['delegators'].items():
        if delegator.will_act():
            acting_delegator_ids.append(id)

    # randomize list.
    # print(f'{acting_delegator_ids=}')
    random.shuffle(acting_delegator_ids)
    # print(f'shuffled: {acting_delegator_ids=}')

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


def get_most_profitable_delegator_id(delegators):
    profitability = {id: d.unrealized_gains_from_shares + d.realized_gains_from_shares for id, d in delegators.items()}
    max_id = max(profitability, key=profitability.get)
    return max_id


def update_delegator_2_to_best_strategy(params, step, sL, s, inputs):
    # decide what the best strategy is
    # who is most profitable?
    # possibly add a parameter where they only look back so far
    delegators = s['delegators']
    key = 'delegators'
    value = delegators
    if len(delegators) > 3:
        most_profitable_delegator_id = get_most_profitable_delegator_id(delegators)
        # add realized and unrealized and whichever delegator is highest, make 2's strategy equal to that. every timestep, reanalyze
        if delegators[2].component_weights != delegators[most_profitable_delegator_id].component_weights:
            old_weights = delegators[2].component_weights
            new_weights = delegators[most_profitable_delegator_id].component_weights
            print(f'Changing delegator 2s component_weights from {old_weights} to {new_weights}')
            delegators[2].component_weights = new_weights
    return key, value
    
