import matplotlib.pyplot as plt
import numpy as np

class GraphInterface:
    def __init__(self, points,  label=None):
        self.points = points
        self.labels = label

    def plot_Total(self):
        self.data_x = list(0, len(self.points))
        self.data_y = self.points.values()
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
        self.data_x = list(0, len(self.points))
        self.data_y = self.points.values()
        plt.plot(self.data_x, self.data_y, label='DPNL', color='red')
        plt.xlabel('Date')
        plt.ylabel('DPNL')
        plt.title('DPNL Plot')
        plt.fill_between(self.data_x, self.data_y, np.zeros_like(self.data_y), color='red', alpha=0.3)
        plt.axis([0,None,0,None])
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
      
    # def plot_balance(self):
    #     plt.figure(figsize=(16, 6))
    #     plt.xlabel('Date')
    #     plt.ylabel('balance')
    #     plt.title('Balance Plot')
    #     colors = ['blue', 'green', 'yellow', 'red']
    #     plt.stackplot(rate, y, labels=['Free', 'LkoH', 'PHoS', 'SBoR'], colors=colors, alpha=0.5)
    #     plt.legend(loc='upper left')
    #     plt.grid(True, linestyle='--', alpha=0.5)
    #     plt.show()

graph_interface_1 = GraphInterface(points, label='Total')
graph_interface_2 = GraphInterface(points, label='DPNL')
#graph_interface_3 = GraphInterface(points, label='Sharpe')
#graph_interface_4 = GraphInterface(points, label='relatire_Total')
#graph_interface_5 = GraphInterface(points)

graph_interface_1.plot_Total()
graph_interface_2.plot_DPNL()
#graph_interface_3.plot_sharpe()
#graph_interface_4.plot_relatire_Total()
#graph_interface_5.plot_balance()