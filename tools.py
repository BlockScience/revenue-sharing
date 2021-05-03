import numpy as np


def line_plot(thing, subsets, df, timesteps_per_subset, plt):

    for subset in subsets:
        # d = df['regression_to_mean_private_prices']
        # d = df['value_private_prices']
        d = df[thing][subset * timesteps_per_subset:(subset + 1) * timesteps_per_subset].reset_index()
        # print(d)

        timestep = 0
        delegateId = 0

        # initialize a list of 4 lists
        x = [[] for _ in range(4)]
        y = [[] for _ in range(4)]

        fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(2, 2)
        axs = [ax0, ax1, ax2, ax3]

        for timestep in range(2000):
            # print(d)
            # print(f'{timestep=}, {d.private_prices.iloc[timestep]=}')
            for delegateId, value in d.iloc[timestep][thing].items():
                # print(f'{delegateId=}, {price=}')
                # The data has to be in the form x = [timesteps], y = [values]
                # the data is in the form y = dict({key=delegator, value=private_price})
                x[delegateId].append(timestep)
                # print(delegateId, value)
                y[delegateId].append(value)

        colors = 'rgby'
        private_price_mapping = ['Value', 'Regression to Mean', 'Value', 'Trendline']
        # make figures larger
        plt.rcParams["figure.figsize"] = (20, 10)
        for delegateId in range(4):
            # plot values for each delegate
            axs[delegateId].plot(x[delegateId], y[delegateId], colors[delegateId])

            axs[delegateId].set_title(f'{delegateId=} | {thing} | {subset=} | {private_price_mapping[delegateId]}')

        # make xticks invisible
        plt.setp(ax0.get_xticklabels(), visible=False)
        plt.setp(ax1.get_xticklabels(), visible=False)

        # make y-axes the same
        min_y = np.min([ax.get_ylim() for ax in axs])
        max_y = np.max([ax.get_ylim() for ax in axs])

        for ax in axs:
            ax.set_ylim(min_y, max_y)

        plt.show()
