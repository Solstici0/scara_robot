import matplotlib.pyplot as plt
import pickle as pkl
import paramiko
from pathlib import Path
import argparse
import numpy as np

remote_file_path = Path("~/data/last_data.pkl").expanduser()
local_file_path = Path("~/data/last_data.pkl").expanduser()

def download_file(hostname,port,username,password):
    # Create a Paramiko SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the remote server
        client.connect(hostname, port, username, password)

        # Create an SFTP client
        sftp = client.open_sftp()

        # Download the file
        sftp.get(str(remote_file_path), str(local_file_path))
        

    finally:
        # Close the SSH and SFTP connections
        sftp.close()
        client.close()

def load_data():
    with open(local_file_path, 'rb') as file:
        data = pkl.load(file)
    return data

def plot(data:list):
    n = len(data)
    time = [0.0]*n
    hombro_pos_set_point = [0.0]*n
    hombro_pos_estimate = [0.0]*n
    hombro_vel_set_point = [0.0]*n
    hombro_vel_estimate = [0.0]*n
    hombro_Iq_set_point = [0.0]*n
    hombro_Iq_measured = [0.0]*n
    codo_pos_set_point = [0.0]*n
    codo_pos_estimate = [0.0]*n
    codo_vel_set_point = [0.0]*n
    codo_vel_estimate = [0.0]*n
    codo_Iq_set_point = [0.0]*n
    codo_Iq_measured = [0.0]*n
    const = -2*np.pi/7
    for i in range(n):
        time[i] = data[i][0]/1e9
        hombro_pos_set_point[i] = data[i][1]*const
        hombro_pos_estimate[i] = data[i][2]*const
        hombro_vel_set_point[i] = data[i][3]*const
        hombro_vel_estimate[i] = data[i][4]*const
        hombro_Iq_set_point[i] = data[i][5]
        hombro_Iq_measured[i] = data[i][6]
        codo_pos_set_point[i] = data[i][7]*const
        codo_pos_estimate[i] = data[i][8]*const
        codo_vel_set_point[i] = data[i][9]*const
        codo_vel_estimate[i] = data[i][10]*const
        codo_Iq_set_point[i] = data[i][11]
        codo_Iq_measured[i] = data[i][12]
    
    # Create the first figure with three subplots
    fig1, (ax1, ax2, ax3) = plt.subplots(3, 1)
    l_expected, = ax1.plot(time,hombro_pos_set_point)
    l_actual, = ax1.plot(time,hombro_pos_estimate)

    ax2.plot(time,hombro_vel_set_point)
    ax2.plot(time,hombro_vel_estimate)

    ax3.plot(time,hombro_Iq_set_point)
    ax3.plot(time,hombro_Iq_measured)

    ax1.set_ylabel('Position [rads]')
    ax2.set_ylabel('Speed [rads/s]')
    ax3.set_ylabel('Current [A]')
    ax3.set_xlabel('time [s]')
    fig1.legend((l_expected,l_actual),('Set_point','Actual'), bbox_to_anchor=(0.75, 1))
    fig1.suptitle('Hombro',x=0.4,y = 0.95)
    

    fig2, (ax4, ax5, ax6) = plt.subplots(3, 1)
    l_expected2, = ax4.plot(time,hombro_pos_set_point)
    l_actual2, = ax4.plot(time,hombro_pos_estimate)

    ax5.plot(time,hombro_vel_set_point)
    ax5.plot(time,hombro_vel_estimate)

    ax6.plot(time,hombro_Iq_set_point)
    ax6.plot(time,hombro_Iq_measured)

    ax4.set_ylabel('Position [rads]')
    ax5.set_ylabel('Speed [rads/s]')
    ax6.set_ylabel('Current [A]')
    ax6.set_xlabel('time [s]')
    fig2.legend((l_expected2,l_actual2),('Set_point','Actual'), bbox_to_anchor=(0.75, 1))
    fig2.suptitle('Codo',x=0.4,y = 0.95)
    fig2.show()
    fig1.show()
    

        

def main():
    parser = argparse.ArgumentParser(description="Download and load data from a remote file using Paramiko. and plot it")
    parser.add_argument("hostname", type=str, help="Hostname or IP address of the remote server.")
    parser.add_argument("port", type=int, help="SSH port of the remote server.")
    parser.add_argument("username", type=str, help="Username for authentication.")
    parser.add_argument("password", type=str, help="Password for authentication.")

    args = parser.parse_args()

    # Download file from the remote server
    download_file(args.hostname, args.port, args.username, args.password)

    # Load data from the downloaded file
    data = load_data()
    plot(data)