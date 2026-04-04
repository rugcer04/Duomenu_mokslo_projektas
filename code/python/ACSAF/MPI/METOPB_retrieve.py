from ftplib import FTP
import os
import argparse
import numpy as np
from mpi4py import MPI
import time
import h5py
import xarray
import calendar


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
    parser.add_argument("--year", type=list, default=list(range(2017, 2027, 1)), help="Reikalingi metai parsiuntimui ir apdorojimui")

    num_A_workers = round((size-1)*0.3, 0)
    num_B_workers = size-1-num_A_workers

    if rank == 0:
        args = parser.parse_args()
        base_path = "/gome2b/offline/"

        years = args.year

        all_links = []
        for year in years:
            for month in range(1, 13):
                _, num_days = calendar.monthrange(year, month)

                for day in range(1, num_days + 1):
                    link = f"{base_path}{year}/{month:02d}/{day:02d}"
                    all_links.append(link)

        print(f"{now()} [0]: Prepared {len(all_links)} total daily links.", flush=True)