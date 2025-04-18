import re
import argReader
import numpy as np
import pandas as pd
from datetime import datetime
import multiprocessing

log = argReader.log

def extract_pattern(pattern, dtype):
    file = open(log, 'r')
    results = []

    for line in file:
        try:
            match = re.search(pattern, line)
            if match:
                if dtype == 'i':
                    results.append(int(match.group(1)))
                elif dtype == 'f':
                    results.append(float(match.group(1)))
                elif dtype == 'd':
                    date_str = match.group(1)
                    date_format = '%a %b %d %H:%M:%S %Y'
                    date = datetime.strptime(date_str, date_format)
                    results.append(date)
        except Exception as e:
            print(f"An error occurred: {e}")

    return results

def cpu_counter():
    pattern = r'CPU\s*(\d):'
    return max(extract_pattern(pattern, 'i')) + 1

def get_sample_time():
    pattern = r'Sampled system activity \(([A-Za-z]{3} [A-Za-z]{3}\s*\d+ \d{2}:\d{2}:\d{2} \d{4})'
    sample_time_list = extract_pattern(pattern, 'd')
    start_time = sample_time_list[0]
    for i in range(len(sample_time_list)):
        timedelta = sample_time_list[i] - start_time
        sample_time_list[i] = int(timedelta.total_seconds())
    return sample_time_list

def get_cpu_freq():
    pattern_template = r"CPU _CPUID_ frequency:\s*(\d+) MHz"
    cpu_freq_list = []
    for cpu_id in range(0, cpu_count):
        pattern = re.sub(r"_CPUID_", str(cpu_id), pattern_template)
        cpu_freq_list.append(extract_pattern(pattern, 'i'))
    return cpu_freq_list

def get_E_cluster_freq():
    pattern = r'E-Cluster HW active frequency:\s*(\d+) MHz'
    E_cluster_freq_list = extract_pattern(pattern, 'i')
    return E_cluster_freq_list

def get_P_cluster_freq():
    pattern = r'P-Cluster HW active frequency:\s*(\d+) MHz'
    P_cluster_freq_list = extract_pattern(pattern, 'i')
    return P_cluster_freq_list

def get_cpu_usage():
    pattern_template = r'CPU _CPUID_ active residency:\s*(\d+\.\d+)%'
    cpu_usage_list = []
    for cpu_id in range(0, cpu_count):
        pattern = re.sub(r"_CPUID_", str(cpu_id), pattern_template)
        cpu_usage_list.append(extract_pattern(pattern, 'f'))
    return cpu_usage_list

def get_E_cluster_usage():
    pattern = r'E-Cluster HW active residency:\s*(\d+\.\d+)%'
    E_cluster_usage_list = extract_pattern(pattern, 'f')
    return E_cluster_usage_list

def get_P_cluster_usage():
    pattern = r'P-Cluster HW active residency:\s*(\d+\.\d+)%'
    P_cluster_usage_list = extract_pattern(pattern, 'f')
    return P_cluster_usage_list

def get_CPU_power():
    pattern = r'CPU Power:\s*(\d+)\s*mW'
    CPU_power_list = extract_pattern(pattern, 'i')
    return CPU_power_list

def get_GPU_freq():
    pattern = r'GPU HW active frequency:\s*(\d+) MHz'
    GPU_freq_list = extract_pattern(pattern, 'i')
    return GPU_freq_list

def get_GPU_usage():
    pattern = r'GPU HW active residency:\s*(\d+\.\d+)%'
    GPU_usage_list = extract_pattern(pattern, 'f')
    return GPU_usage_list

def get_GPU_power():
    pattern = r'GPU Power:\s*(\d+)\s*mW'
    GPU_power_list = extract_pattern(pattern, 'i')
    return GPU_power_list[0::2]

def get_ANE_power():
    pattern = r'ANE Power:\s*(\d+)\s*mW'
    ANE_power_list = extract_pattern(pattern, 'i')
    return ANE_power_list

def get_SOC_power():
    pattern = r'Combined Power \(CPU \+ GPU \+ ANE\):\s*(\d+)\s*mW'
    SOC_power_list = extract_pattern(pattern, 'i')
    return SOC_power_list

def fetch_data(func):
    return func()

# This function is re-implemented by ChatGPT with multiprocessing
# Cost nearly half time compared with original constructor (0.71s -> 0.35s)
def dfconstructor():
    
    
    # Define functions to be called in parallel
    functions = {
        "sample_time": get_sample_time,
        "cpu_freq": get_cpu_freq,
        "E_cluster_freq": get_E_cluster_freq,
        "P_cluster_freq": get_P_cluster_freq,
        "cpu_usage": get_cpu_usage,
        "E_cluster_usage": get_E_cluster_usage,
        "P_cluster_usage": get_P_cluster_usage,
        "CPU_power": get_CPU_power,
        "GPU_freq": get_GPU_freq,
        "GPU_usage": get_GPU_usage,
        "GPU_power": get_GPU_power,
        "ANE_power": get_ANE_power,
        "SOC_power": get_SOC_power,
    }
    
    # Use multiprocessing to fetch data in parallel
    with multiprocessing.Pool(processes=len(functions)) as pool:
        results_list = pool.map(fetch_data, functions.values())
    
    # Store results in a dictionary with the correct order
    results = dict(zip(functions.keys(), results_list))
    
    # Construct the combined list in the correct order
    combined_list = [
        results["sample_time"],
        *results["cpu_freq"],
        results["E_cluster_freq"],
        results["P_cluster_freq"],
        *results["cpu_usage"],
        results["E_cluster_usage"],
        results["P_cluster_usage"],
        results["CPU_power"],
        results["GPU_freq"],
        results["GPU_usage"],
        results["GPU_power"],
        results["ANE_power"],
        results["SOC_power"],
    ]
    
    # Generate labels
    cpuid_freq_label = [f'CPU {cpuid} Frequency' for cpuid in range(cpu_count)]
    cpuid_usage_label = [f'CPU {cpuid} Usage' for cpuid in range(cpu_count)]
    
    label_list = [
        'Sample Time',
        *cpuid_freq_label,
        'E-Cluster Frequency',
        'P-Cluster Frequency',
        *cpuid_usage_label,
        'E-Cluster Usage',
        'P-Cluster Usage',
        'CPU Power',
        'GPU Frequency',
        'GPU Usage',
        'GPU Power',
        'ANE Power',
        'SOC Power'
    ]
    
    return pd.DataFrame(np.transpose(combined_list).tolist(), columns=label_list)

# Original dfconstructor
'''
def dfconstructor():
    sample_time = get_sample_time()
    cpu_freq = get_cpu_freq()
    E_cluster_freq = get_E_cluster_freq()
    P_cluster_freq = get_P_cluster_freq()
    cpu_usage = get_cpu_usage()
    E_cluster_usage = get_E_cluster_usage()
    P_cluster_usage = get_P_cluster_usage()
    CPU_power = get_CPU_power()
    GPU_freq = get_GPU_freq()
    GPU_usage = get_GPU_usage()
    GPU_power = get_GPU_power()
    ANE_power = get_ANE_power()
    SOC_power = get_SOC_power()

    combined_list = []
    combined_list.append(sample_time)
    combined_list.extend(cpu_freq)
    combined_list.append(E_cluster_freq)
    combined_list.append(P_cluster_freq)
    combined_list.extend(cpu_usage)
    combined_list.append(E_cluster_usage)
    combined_list.append(P_cluster_usage)
    combined_list.append(CPU_power)
    combined_list.append(GPU_freq)
    combined_list.append(GPU_usage)
    combined_list.append(GPU_power)
    combined_list.append(ANE_power)
    combined_list.append(SOC_power)

    cpuid_freq_label = []
    cpuid_usage_label = []

    for cpuid in range(0, cpu_count):
        cpuid_freq_label.append(f'CPU {cpuid} Frequency')
        cpuid_usage_label.append(f'CPU {cpuid} Usage')

    label_list = []
    label_list.append('Sample Time')
    label_list.extend(cpuid_freq_label)
    label_list.append('E-Cluster Frequency')
    label_list.append('P-Cluster Frequency')
    label_list.extend(cpuid_usage_label)
    label_list.append('E-Cluster Usage')
    label_list.append('P-Cluster Usage')
    label_list.append('CPU Power')
    label_list.append('GPU Frequency')
    label_list.append('GPU Usage')
    label_list.append('GPU Power')
    label_list.append('ANE Power')
    label_list.append('SOC Power')

    return pd.DataFrame(np.transpose(combined_list).tolist(), columns=label_list)
'''

cpu_count = cpu_counter()