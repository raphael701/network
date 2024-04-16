from scapy.all import TCP,IP,rdpcap

pcapFile = rdpcap(r"C:\Users\rpak3\Downloads\SYNflood.pcapng")

syn_timestamps = {}

for pck in pcapFile:
    if TCP in pck and pck[TCP].flags == 2: #Check for SYN packets
        src_ip = pck[IP].src
        timestamp = pck.time 

        if src_ip not in syn_timestamps:
            syn_timestamps[src_ip] = []
        syn_timestamps[src_ip].append(timestamp)

# Identify suspicious IPs based on multiple SYN packets sent in less than 2 seconds
threshold_seconds = 2 #Adjust the threshold time interval

with open("sus_ips.txt", "a") as file:
    for ip, timestamps in syn_timestamps.items():
        timestamps.sort()
        time_intervals = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]
        
        #Check for time intervals less than threshold
        if any(interval < threshold_seconds for interval in time_intervals):
                file.write(ip + "\n")
        
        else:
            pass