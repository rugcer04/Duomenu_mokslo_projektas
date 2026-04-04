from ftplib import FTP
import os
import argparse
import numpy as np
from mpi4py import MPI
import time
import h5py
import xarray
import calendar
import sys


def now() -> str:
    return(time.strftime("%H:%M:%S", time.localtime() ))


def get_day(address: str, ftp: FTP, rank: int):
    """
    Downloads all daily files to the same local directory.

    Args:
        address (str): The server file address.
        ftp (ftplib.FTP): The open FTP connection object.
    
    Returns:
        None
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = ftp.pwd()
    ftp.cwd(address)
    files = ftp.nlst()

    relative_address = address.lstrip('/')
    local_dir = os.path.join(base_dir, relative_address)

    os.makedirs(local_dir, exist_ok=True)
    for filename in files:
        local_path = os.path.join(local_dir, filename)
        if not os.path.exists(local_path):
            with open(local_path, 'wb') as f:
                ftp.retrbinary(f"RETR {filename}", f.write)

    print(f"{now()} [{rank}]: Finished: {address}.", flush=True)
    ftp.cwd(root_dir)


if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    parser = argparse.ArgumentParser(description="MPI AC SAF data Donwload and Processing")
    parser.add_argument(
        "--year", 
        type=int, 
        nargs="+", 
        default=list(range(2017, 2027)), 
        help="Reikalingi metai parsiuntimui ir apdorojimui"
    )

    parser.add_argument("--user", type=str, help="AC SAF DLR naudotojo vardas")
    parser.add_argument("--key", type=str, help="AC SAF DLR slaptažodis")

    num_A_workers = int(round((size - 1) * 0.4, 0))
    num_B_workers = (size - 1) - num_A_workers

    a_worker_ranks = list(range(1, num_A_workers + 1))
    b_worker_ranks = list(range(num_A_workers + 1, size))

    my_jobs = []
    creds = None

    if rank == 0:
        args = parser.parse_args()
        base_path = "/gome2b/offline/"

        years = args.year

        creds = {
            'user': args.user,
            'pass': args.key,
            'host': "acsaf.eoc.dlr.de"
        }

    creds = comm.bcast(creds, root=0)

    if rank == 0:
        all_links = []
        for year in years:
            for month in range(1, 13):
                _, num_days = calendar.monthrange(year, month)

                for day in range(1, num_days + 1):
                    link = f"{base_path}{year}/{month:02d}/{day:02d}"
                    all_links.append(link)

        print(f"{now()} [0]: Prepared {len(all_links)} total daily links.", flush=True)

        batches = np.array_split(all_links, num_A_workers)

        for i, target_rank in enumerate(a_worker_ranks):
            comm.send(batches[i].tolist(), dest=target_rank, tag=11)

    elif rank in a_worker_ranks:
        my_jobs = comm.recv(source=0, tag=11)
        print(f"{now()} [{rank}]: A-Worker received {len(my_jobs)} days to fetch.", flush=True)

    elif rank in b_worker_ranks:
        print(f"{now()} [{rank}]: B-Worker ready for processing.", flush=True)

    if rank == 0:
        finished_count = 0
        total_to_receive = len(all_links)
        
        print(f"{now()} [0]: Listening for finished addresses...", flush=True)

        while finished_count < total_to_receive:
            status = MPI.Status()
            if comm.Iprobe(source=MPI.ANY_SOURCE, tag=99):
                msg = comm.recv(source=MPI.ANY_SOURCE, tag=99)
                print(f"{now()} [0]: Confirmation received for {msg}", flush=True)
                finished_count += 1
            
            time.sleep(0.1)
    
    elif rank in a_worker_ranks:
        try:
            ftp = FTP(creds['host'])
            ftp.login(user=creds['user'], passwd=creds['pass'])
            print(f"{now()} [{rank}]: FTP Connected.")
            
            for link in my_jobs:
                get_day(link, ftp, rank)
                comm.send(link, dest=0, tag=99)
                
            ftp.quit()
        except Exception as e:
            print(f"{now()} [{rank}]: FTP Error: {e}")