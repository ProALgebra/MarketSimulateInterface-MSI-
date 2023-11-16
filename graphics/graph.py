import io

import matplotlib.pyplot as plt
import numpy as np


class GraphInterface:
    def __init__(self, metrics, idTask, client):
        self.points_for_total = metrics.totals
        self.points_for_relative_totals = metrics.relative_totals
        self.points_for_balances = metrics.balance
        self.points_for_commissions = metrics.commissions
        self.points_for_DPNL = metrics.DPNL
        self.idTask = idTask
        self.all_plots = {}
        self.client = client

    def plot_Total(self):
        data_x = list(self.points_for_total.keys())
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
        self.all_plots['Total'] = (binary_data)
        plt.clf()

    def plot_DPNL(self):
        data_x = list(self.points_for_DPNL.keys())
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
        self.all_plots['DPNL'] = (binary_data)
        plt.clf()

    def plot_relatire_Total(self):
        data_x = list(self.points_for_relative_totals.keys())
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
        self.all_plots['relatire_Total'] = (binary_data)
        plt.clf()

    def plot_comissions(self):
        data_x = list(self.points_for_commissions.keys())
        data_y = list(self.points_for_commissions.values())
        plt.plot(data_x, data_y, label='comissions', color='red')
        plt.xlabel('Date')
        plt.xticks(rotation='vertical')
        plt.ylabel('comissions')
        plt.title('Comissions Plot')
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.legend()
        buffer = io.BytesIO()
        plt.savefig(buffer, format='jpg')
        buffer.seek(0)
        binary_data = buffer.read()
        self.all_plots['comissions'] = (binary_data)
        plt.clf()

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
        self.all_plots['balance'] = binary_data
        plt.clf()

    def save_plots(self):
        self.client.put_plots(self.idTask, self.all_plots.values())


def main():
    pass


if __name__ == "__main__":
    main()
