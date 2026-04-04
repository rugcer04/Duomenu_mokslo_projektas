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
    root_dir = ftp.pwd()
    ftp.cwd(address)
    files = ftp.nlst()

    os.makedirs(address, exist_ok=True)
    for filename in files:
        local_path = os.path.join(address, filename)
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

    num_A_workers = int(round((size - 1) * 0.3, 0))
    num_B_workers = (size - 1) - num_A_workers

    a_worker_ranks = list(range(1, num_A_workers + 1))
    b_worker_ranks = list(range(num_A_workers + 1, size))

    my_jobs = []

    if rank == 0:
        args = parser.parse_args()
        base_path = "/gome2b/offline/"

        years = args.year
        USER = args.user
        PASS = args.key

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
