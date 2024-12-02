import matplotlib.pyplot as plt

def display_usage(lot, dfusage):
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

def display_frequency(lot, dffrequency):
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

def display_power(lot, dfpower):
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

def display(lot, dfusage, dffrequency, dfpower):
    display_usage(lot, dfusage)
    display_frequency(lot, dffrequency)
    display_power(lot, dfpower)
    plt.show()