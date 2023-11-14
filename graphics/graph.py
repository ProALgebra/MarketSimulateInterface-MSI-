import matplotlib.pyplot as plt
import numpy as np

class GraphInterface:
    def __init__(self, metrics):
        self.points_for_total = metrics.totals
        self.points_for_relative_totals = metrics.relative_totals
        self.points_for_balances = metrics.balance
        self.points_for_DPNL = metrics.DPNL
        self.points_for_comissions = metrics.commissions


    def plot_Total(self):
        data_x = list(range(0, len(self.points_for_total)))
        data_y = list(self.points_for_total.values())
        plt.plot(data_x, data_y, label='Total')
        plt.xlabel('Date')
        plt.ylabel('Total')
        plt.title('Total Plot')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.show()
        #plt.savefig('my_chart.png')

    def plot_DPNL(self):
        data_x = list(range(0, len(self.points_for_DPNL)))
        data_y = list(self.points_for_DPNL.values())
        plt.plot(data_x, data_y, label='DPNL', color='red')
        plt.xlabel('Date')
        plt.ylabel('DPNL')
        plt.title('DPNL Plot')
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.legend()
        plt.show()

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
        data_x = list(range(0, len(self.points_for_relative_totals)))
        data_y = list(self.points_for_relative_totals.values())
        plt.plot(data_x, data_y, label='relatire_Total', color='red')
        plt.xlabel('Date')
        plt.ylabel('relatire total')
        plt.title('Relatire Total Plot')
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.legend()
        plt.show()

    def plot_comissions(self):
        data_x = list(range(0, len(self.points_for_comissions)))
        data_y = list(self.points_for_comissions.values())
        plt.plot(data_x, data_y, label='comissions', color='red')
        plt.xlabel('Date')
        plt.ylabel('comissions')
        plt.title('comissions')
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.legend()
        plt.show()
      
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
        plt.ylabel('balance')
        plt.title('Balance Plot')
        plt.stackplot(data_x, y, labels=tikers, alpha=0.5)
        plt.legend(loc='upper left')
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.show()


def main():
    pass


if __name__ == "__main__":
    main()