import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import config  # 自作の設定ファイルをインポート

def run_monitor():
    targets = config.TARGET_MARKETS
    n_plots = len(targets)
    cols = 2
    rows = (n_plots + 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(12, 4 * rows))
    axes = axes.flatten()
    
    fig.suptitle(f"Market Monitoring ({datetime.now().strftime('%Y-%m-%d')})", fontsize=16)

    for i, (name, symbol) in enumerate(targets.items()):
        try:
            print(f"Fetching {name} ({symbol})...")
            data = yf.download(symbol, period=config.PERIOD, interval=config.INTERVAL)
            
            if not data.empty:
                ax = axes[i]
                ax.plot(data.index, data['Close'], color='teal', linewidth=1.5)
                ax.set_title(name, fontweight='bold')
                ax.grid(True, linestyle=':', alpha=0.6)
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
                
                # 終値を右端に表示する工夫
                last_price = data['Close'].iloc[-1]
                ax.annotate(f"{last_price:.2f}", 
                            xy=(data.index[-1], last_price), 
                            xytext=(5, 0), textcoords='offset points',
                            fontsize=9, color='darkred')
            
        except Exception as e:
            print(f"Error fetching {name}: {e}")

    # 余った空白のグラフを消す
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # 保存と表示
    plt.savefig(config.SAVE_FILENAME)
    print(f"\nReport saved as {config.SAVE_FILENAME}")
    plt.show()

if __name__ == "__main__":
    run_monitor()