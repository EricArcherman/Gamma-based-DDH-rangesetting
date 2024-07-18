import matplotlib.pyplot as plt

##########################                              ##########################                              ##########################
### Graphing functions ###                              ### Graphing functions ###                              ### Graphing functions ###
##########################                              ##########################                              ##########################
                            ##########################                              ##########################
                            ### Graphing functions ###                              ### Graphing functions ###
                            ##########################                              ##########################
##########################                              ##########################                              ##########################
### Graphing functions ###                              ### Graphing functions ###                              ### Graphing functions ###
##########################                              ##########################                              ##########################
                            ##########################                              ##########################
                            ### Graphing functions ###                              ### Graphing functions ###
                            ##########################                              ##########################
##########################                              ##########################                              ##########################
### Graphing functions ###                              ### Graphing functions ###                              ### Graphing functions ###
##########################                              ##########################                              ##########################


def raw_data_plot(hf_data, daily_data):
    # Plot high-frequency data
    fig, ax1 = plt.subplots(figsize=(14, 7))

    # Plot indexPrice from high-frequency data
    plt.subplot(2, 1, 1)
    plt.plot(hf_data['timestamp'], hf_data['indexPrice'], label='HF Index Price', color='blue')
    plt.plot(daily_data['timestamp'], daily_data['indexPrice'], label='Daily Index Price', color='red')
    plt.title('High-Frequency Data')
    plt.xlabel('Time')
    plt.ylabel('Index Price')
    plt.legend()

    # Plot daily data
    plt.subplot(2, 1, 2)
    plt.plot(daily_data['timestamp'], daily_data['volATM'], label='Volatility ATM', color='purple')
    plt.plot(daily_data['timestamp'], daily_data['vol10C'], label='Volatility 10C', color='orange')
    plt.plot(daily_data['timestamp'], daily_data['vol10P'], label='Volatility 10P', color='pink')
    plt.plot(daily_data['timestamp'], daily_data['vol25C'], label='Volatility 25C', color='brown')
    plt.plot(daily_data['timestamp'], daily_data['vol25P'], label='Volatility 25P', color='grey')

    plt.title('Daily Data')
    plt.xlabel('Time')
    plt.ylabel('Values')
    plt.legend()

    plt.tight_layout()
    # plt.savefig('raw_data.png')
    plt.show()

def vol_plot(daily, interpolated, with_noise):
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 10))

    ax1.plot(daily['timestamp'], daily['volATM'], label='Volatility ATM', color='purple')
    ax1.plot(daily['timestamp'], daily['vol10C'], label='Volatility 10C', color='orange')
    ax1.plot(daily['timestamp'], daily['vol10P'], label='Volatility 10P', color='pink')
    ax1.plot(daily['timestamp'], daily['vol25C'], label='Volatility 25C', color='brown')
    ax1.plot(daily['timestamp'], daily['vol25P'], label='Volatility 25P', color='grey')
    ax1.set_title('daily vol')
    ax1.legend()

    ax2.plot(interpolated['timestamp'], interpolated['volATM'], label='Volatility ATM', color='purple')
    ax2.plot(interpolated['timestamp'], interpolated['vol10C'], label='Volatility 10C', color='orange')
    ax2.plot(interpolated['timestamp'], interpolated['vol10P'], label='Volatility 10P', color='pink')
    ax2.plot(interpolated['timestamp'], interpolated['vol25C'], label='Volatility 25C', color='brown')
    ax2.plot(interpolated['timestamp'], interpolated['vol25P'], label='Volatility 25P', color='grey')
    ax2.set_title('cubic spline interpolated')
    ax2.legend()

    ax3.plot(with_noise['timestamp'], with_noise['volATM'], label='Volatility ATM', color='purple')
    ax3.plot(with_noise['timestamp'], with_noise['vol10C'], label='Volatility 10C', color='orange')
    ax3.plot(with_noise['timestamp'], with_noise['vol10P'], label='Volatility 10P', color='pink')
    ax3.plot(with_noise['timestamp'], with_noise['vol25C'], label='Volatility 25C', color='brown')
    ax3.plot(with_noise['timestamp'], with_noise['vol25P'], label='Volatility 25P', color='grey')
    ax3.set_title('added noise')
    ax3.legend()

    plt.tight_layout()
    # plt.savefig('vol_plot.png')
    plt.show()


##########################                              ##########################                              ##########################
### Graphing functions ###                              ### Graphing functions ###                              ### Graphing functions ###
##########################                              ##########################                              ##########################
                            ##########################                              ##########################
                            ### Graphing functions ###                              ### Graphing functions ###
                            ##########################                              ##########################
##########################                              ##########################                              ##########################
### Graphing functions ###                              ### Graphing functions ###                              ### Graphing functions ###
##########################                              ##########################                              ##########################
                            ##########################                              ##########################
                            ### Graphing functions ###                              ### Graphing functions ###
                            ##########################                              ##########################
##########################                              ##########################                              ##########################
### Graphing functions ###                              ### Graphing functions ###                              ### Graphing functions ###
##########################                              ##########################                              ##########################