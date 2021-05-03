import numpy as np


def two_by_two_plot(thing, subsets, df, timesteps_per_subset, plt, type="line_plot"):

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
        y1 = [[] for _ in range(4)]

        fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(2, 2)
        axs = [ax0, ax1, ax2, ax3]
        print(f'{type=}')
        if type == 'line_plot':
            for timestep in range(timesteps_per_subset):
                # print(d)
                # print(f'{timestep=}, {d.private_prices.iloc[timestep]=}')
                for delegateId, value in d.iloc[timestep][thing].items():
                    # print(f'{delegateId=}, {price=}')
                    # The data has to be in the form x = [timesteps], y = [values]
                    # the data is in the form y = dict({key=delegator, value=private_price})
                    x[delegateId].append(timestep)
                    # print(delegateId, value)
                    y[delegateId].append(value)
        elif type == 'stacked_plot':
            for t in thing:
                for timestep in range(timesteps_per_subset):
                    # print(d)
                    # print(f'{timestep=}, {d.private_prices.iloc[timestep]=}')
                    for delegateId, value in d.iloc[timestep][t].items():
                        # print(f'{delegateId=}, {price=}')
                        # The data has to be in the form x = [timesteps], y = [values]
                        # the data is in the form y = dict({key=delegator, value=private_price})
                        # print(f'{t=}, {thing=}, {t==thing[0]}, {t==thing[1]}, {value=}')
                        if t == thing[0]:
                            x[delegateId].append(timestep)
                            y[delegateId].append(value)
                        elif t == thing[1]:
                            y1[delegateId].append(value)
                        else:
                            raise('stacked chart with more than 2 items not supported at this time')
        colors = 'rgby'
        private_price_mapping = ['Value', 'Regression to Mean', 'Value', 'Trendline']
        # make figures larger
        plt.rcParams["figure.figsize"] = (20, 10)
        for delegateId in range(4):
            # plot values for each delegate
            if type == 'line_plot':
                axs[delegateId].plot(x[delegateId], y[delegateId], colors[delegateId])
            elif type == 'stacked_plot':
                # print(y[delegateId])
                axs[delegateId].stackplot(x[delegateId], y[delegateId], y1[delegateId], labels=thing)
                axs[delegateId].legend(loc='upper left')
            else:
                raise('Only line_plot and stacked_plot are supported types.')

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
