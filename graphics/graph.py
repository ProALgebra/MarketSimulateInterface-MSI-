import matplotlib.pyplot as plt
import numpy as np

class GraphInterface:
    def __init__(self, points,  label=None):
        self.points = points
        self.labels = label

    def plot_Total(self):
        self.data_x = list(range(0, len(self.points)))
        self.data_y = list(self.points.values())
        print(self.data_y)
        plt.plot(self.data_x, self.data_y, label='Total')        
        plt.xlabel('Date')
        plt.ylabel('Total')
        plt.title('Total Plot')
        plt.fill_between(self.data_x, self.data_y, np.zeros_like(self.data_y), color='blue', alpha=0.3)
        plt.axis([0,None,0,None])
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.show()
        #plt.savefig('my_chart.png')

    def plot_DPNL(self):
        self.data_x = list(range(0, len(self.points)))
        self.data_y = list(self.points.values())
        plt.plot(self.data_x, self.data_y, label='DPNL', color='red')
        plt.xlabel('Date')
        plt.ylabel('DPNL')
        plt.title('DPNL Plot')
        plt.fill_between(self.data_x, self.data_y, np.zeros_like(self.data_y), color='red', alpha=0.3)
        # plt.axis([0,None,0,None])
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
      
    # def plot_relatire_Total(self):
    #     self.data_x = list(0, len(self.points))
    #     self.data_y = self.points.values()
    #     plt.plot(self.data_x, self.data_y, label='relatire_Total', color='yellow')
    #     plt.xlabel('Date')
    #     plt.ylabel('relatire total')
    #     plt.title('Relatire Total Plot')
    #     plt.fill_between(self.data_x, self.data_y, np.zeros_like(self.data_y), color='yellow', alpha=0.3)
    #     plt.axis([0,None,0,None])
    #     plt.grid(True, linestyle='--', alpha=0.5)
    #     plt.legend()
    #     plt.show()
      
    def plot_balance(self):
        dates = sorted(list(self.points))
        tikers = list(self.points[dates[0]].keys())
        y = list(map(list, list(np.empty((len(tikers), 0)))))
        for date in dates:
            for i, tiker in enumerate(tikers):
                y[i].append(self.points[date][tiker])
        y = np.array(y, dtype=float)
        data_x = np.array(range(0, len(y[0])), dtype=float)
        print(len(data_x))
        print(len(y[0]))

        plt.figure(figsize=(16, 6))
        plt.xlabel('Date')
        plt.ylabel('balance')
        plt.title('Balance Plot')
        plt.stackplot([0,1,2,3,4], [2,3,5,7,11], [1,2,3,4,5], [3,1,4,6,8], labels = ['123', '1234', '12345'])
        # plt.stackplot(data_x, y, labels=tikers, alpha=0.5)
        plt.legend(loc='upper left')
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.show()


def main():
    pass


if __name__ == "__main__":
    main()