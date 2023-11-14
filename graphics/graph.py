import matplotlib.pyplot as plt
import numpy as np
import io
import minio

class GraphInterface:
    def __init__(self, metrics, idTask):
        self.points_for_total = metrics.totals
        self.points_for_relative_totals = metrics.relative_totals
        self.points_for_balances = metrics.balance
        self.points_for_DPNL = metrics.DPNL
        self.idTask = idTask
        self.all_plots = {}
    
    
    def plot_Total(self):
        data_x = list(self.points_for_total.key())
        data_y = list(self.points_for_total.values())
        plt.plot(data_x, data_y, label='Total')
        plt.xlabel('Date')
        plt.xticks(rotation='vertical')
        plt.ylabel('Total')
        plt.title('Total Plot')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.5)
        buffer = io.BytesIO()
        plt.savefig(buffer, format='jpg')
        buffer.seek(0)
        binary_data = buffer.read()
        self.all_plots['Total']=(binary_data)
    
    
    def plot_DPNL(self):
        data_x = list(self.points_for_DPNL.key)
        data_y = list(self.points_for_DPNL.values())
        plt.plot(data_x, data_y, label='DPNL', color='red')
        plt.xlabel('Date')
        plt.xticks(rotation='vertical')
        plt.ylabel('DPNL')
        plt.title('DPNL Plot')
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.legend()
        buffer = io.BytesIO()
        plt.savefig(buffer, format='jpg')
        buffer.seek(0)
        binary_data = buffer.read()
        self.all_plots['DPNL']=(binary_data)
    
    # def plot_sharpe(self):
    #     plt.plot(self.data_x, self.data_y, label='Sharpe', color='green')
    #     plt.xlabel('Date')
    #     plt.ylabel('Sharpe')
    #     plt.title('Sharpe Plot')
    #     plt.fill_between(self.data_x, self.data_y, np.zeros_like(self.data_y), color='green', alpha=0.3)
    #     plt.axis([0,None,0,None])
    #     plt.grid(True, linestyle='--', alpha=0.5)
    #     plt.legend()
    #     plt.show()
    
    def plot_relatire_Total(self):
        data_x = list(self.points_for_relative_totals.key)
        data_y = list(self.points_for_relative_totals.values())
        plt.plot(data_x, data_y, label='relatire_Total', color='red')
        plt.xlabel('Date')
        plt.xticks(rotation='vertical')
        plt.ylabel('relatire total')
        plt.title('Relatire Total Plot')
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.legend()
        buffer = io.BytesIO()
        plt.savefig(buffer, format='jpg')
        buffer.seek(0)
        binary_data = buffer.read()
        self.all_plots['relatire_Total']=(binary_data)
    
    def plot_balance(self):
        dates = sorted(list(self.points_for_balances))
        tikers = list(self.points_for_balances[dates[0]].keys())
        y = list(map(list, list(np.empty((len(tikers), 0)))))
        for date in dates:
            for i, tiker in enumerate(tikers):
                y[i].append(self.points_for_balances[date][tiker])
        
        y = np.array(y, dtype=float)
        data_x = np.array(range(0, len(y[0])), dtype=float)
        
        plt.figure(figsize=(16, 6))
        plt.xlabel('Date')
        plt.xticks(rotation='vertical')
        plt.ylabel('balance')
        plt.title('Balance Plot')
        plt.stackplot(data_x, y, labels=tikers, alpha=0.5)
        plt.legend(loc='upper left')
        plt.grid(True, linestyle='--', alpha=0.5)
        buffer = io.BytesIO()
        plt.savefig(buffer, format='jpg')
        buffer.seek(0)
        binary_data = buffer.read()
                    self.all_plots['balance']=(binary_data)

def save_plots(self):
    client = minio.Minio(
                         "localhost:9000",
                         "STS9GtnODgKPvimPR5pm",
                         "3pOTPpbOlw1MbBWHGG7k48ihidhehAiVg4zXC8J9",
                         secure=False)
        bucket = f"{self.idTask}-plots"
        if not client.path.exists(bucket):
            client.makedirs(bucket)
        for key, value in self.all_figures:
            client.put_object(
                              bucket, f'{key}.jpg',
                              value,len(value))


def main():
    pass


if __name__ == "__main__":
    main()