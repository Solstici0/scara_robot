import matplotlib.pyplot as plt

def plots(input_array, case='cartesian'):
    fig, axs = plt.subplots(2, 2)
    if case == 'cartesian':
        axs[0, 0].set_title('X, Y trayectory')
        axs[0,0].plot(input_array[0],input_array[4])
        axs[0,0].set(xlabel='X',ylabel='Y')
        
        axs[0, 1].set_title('X and Y speed')
        axs[0, 1].plot()
        axs[1, 0].set_title('Joint pos and ')
        axs[1, 1].set_title('Axis [1, 1]')
        axs[0,1].plot(input_array[1])
        axs[0,1].plot(input_array[5])
        
        
