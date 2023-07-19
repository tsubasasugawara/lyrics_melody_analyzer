import matplotlib.pyplot as plt

def print_scatter(x: list, y: list, colors: list) -> None:
    if len(x) != len(y) or len(y) != len(colors):
        return
    
    for i in range(0, len(x)):
        plt.scatter(x[i], y[i], c=colors[i])
    
    plt.show()