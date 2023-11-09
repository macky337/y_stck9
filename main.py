import yfinance as yf
import matplotlib.pyplot as plt


def fetch_data(symbol, weeks):
    data = yf.download(symbol, period=f"{weeks}wk")
    return data


def plot_data(ax, ax2, data, ticker_symbol):
    prices = data['Close']
    volumes = data['Volume']
    dates = data.index.strftime('%Y-%m-%d').tolist()

    ax.plot(dates, prices, color='tab:red', label='Closing Price')

    if len(prices) >= 52:
        moving_avg_52 = prices.rolling(window=52).mean()
        ax.plot(dates, moving_avg_52, label='52w Moving Average', color='tab:blue')

    if len(prices) >= 26:
        moving_avg_26 = prices.rolling(window=26).mean()
        ax.plot(dates, moving_avg_26, label='26w Moving Average', color='tab:green')

    ax.set_ylabel('Price')
    ax.set_title(f'{ticker_symbol}')
    ax.legend()
    ax.set_xticks(range(len(dates)))
    ax.set_xticklabels(dates, rotation=45, fontsize=8)
    ax.xaxis.set_major_locator(plt.MaxNLocator(3))

    ax2.bar(range(len(dates)), volumes, color='tab:grey')
    ax2.set_ylabel('Volume', fontsize=8)
    ax2.set_xticks(range(len(dates)))
    ax2.set_xticklabels(dates, rotation=45, fontsize=8)
    ax2.xaxis.set_major_locator(plt.MaxNLocator(3))
    ax2.tick_params(axis='y', labelsize=8)

    plt.tight_layout(pad=1)


if __name__ == "__main__":
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'NFLX', 'BA']
    weeks = 52

    fig, axs = plt.subplots(3, 3, figsize=(18, 12))

    for idx, symbol in enumerate(symbols):
        i, j = divmod(idx, 3)
        data = fetch_data(symbol, weeks)
        if data is not None:
            ax2 = axs[i, j].twinx()
            plot_data(axs[i, j], ax2, data, symbol)

    plt.show()
