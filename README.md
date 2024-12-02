# Visualizer of powermetrics logs on MacOS

This is a tool for visualize information provided by powermetrics, including CPU usage, CPU frequency, CPU power, GPU frequency, GPU usage, GPU power, ANE power, and SOC power.

## How to run
Use following command to generate log through powermetrics:
```
sudo powermetrics -o log.txt
```

Use following command to run the program and specify the log file, '-s' to save the figures
```
./pmGrapher -l <log file> [-s]
```
or
```
python main.py -l <log file> [-s]
```

Choose items in checkbox to select items to display

Submit, and figure(s) will be shown

## Notes
The graphs will be displayed according to 3 classes: Frequency, Usage, and Power.

Each class will be shown in a separated figure