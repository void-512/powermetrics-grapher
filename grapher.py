import matplotlib.pyplot as plt

def display_usage(lot, dfusage, save):
    if dfusage.empty:
        return
    plt.figure(figsize=(10, 6))
    plt.title('Usage')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Usage (percent)')
    for column in dfusage.columns:
        plt.plot(lot, dfusage[column], label=column)
    plt.legend()
    plt.grid(True)
    if save:
        plt.savefig('Usage.png')

def display_frequency(lot, dffrequency, save):
    if dffrequency.empty:
        return
    plt.figure(figsize=(10, 6))
    plt.title('Frequency')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Frequency (MHz)')
    for column in dffrequency.columns:
        plt.plot(lot, dffrequency[column], label=column)
    plt.legend()
    plt.grid(True)
    if save:
        plt.savefig('Frequency.png')

def display_power(lot, dfpower, save):
    if dfpower.empty:
        return
    plt.figure(figsize=(10, 6))
    plt.title('Power')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Power (mW)')
    for column in dfpower.columns:
        plt.plot(lot, dfpower[column], label=column)
    plt.legend()
    plt.grid(True)
    if save:
        plt.savefig('Power.png')

def display(lot, dfusage, dffrequency, dfpower, save):
    display_usage(lot, dfusage, save)
    display_frequency(lot, dffrequency, save)
    display_power(lot, dfpower, save)
    if not save: 
        plt.show()