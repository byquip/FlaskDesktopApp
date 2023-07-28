import os
import sys
from tkinter import filedialog

import numpy as np
from datetime import datetime
from typing import List


def get_file_path() -> List[str]:
    file_paths = filedialog.askopenfilenames(filetypes=[("data", "*.txt")])
    return file_paths


def read_data(file_name: str, skiprows=1, dtype=np.float64) -> np.ndarray:
    """
    function to Read data from file created by WriteData class
    """
    return np.loadtxt(file_name, delimiter="\t", skiprows=skiprows, dtype=dtype)


class WriteData:
    """
    class to write data to file.
    always create a folder with the current date 'dd.mm.yyyy'
    and a file with the current time '(prefix)_(hh)h(mm)m(ss)s.txt'
    """
    folder: str
    file_name: str

    def __init__(self, file_prefix: str = "", folder: str = "", file_name: str = "", rewrite: bool = False) -> None:
        self.file_prefix = file_prefix
        self.folder = folder
        self.file_name = file_name
        self._rewrite = rewrite
        self._create_folder()

    def _create_folder(self) -> None:

        n = datetime.now()
        if self.folder == "":
            self.folder = f"{n.day:02d}.{n.month:02d}.{n.year:04d}"
        if self.file_name == "":
            self.file_name = f"{self.file_prefix}_{n.hour:02d}h{n.minute:02d}m{n.second:02d}s.txt"
        self.file_name = os.path.join(self.folder, self.file_name)
        if os.path.exists(self.file_name) and self._rewrite:
            os.remove(self.file_name)
        try:
            if not os.path.isdir(self.folder):
                os.makedirs(self.folder)
        except:
            print("in file creation: ", sys.exc_info())

    def _write_data(self, data: str) -> bool:
        with open(self.file_name, "a+") as file:
            try:
                file.write(data)
            except:
                print("in file writing: ", sys.exc_info())
                return 0
        return 1

    def create_header(self, headers: List[str]) -> bool:
        header: str = "# "
        for h in headers[:-1]:
            header += f"{h}\t"
        header += f"{headers[-1]}"
        header += "\n"
        return self._write_data(header)

    def write_data(self, data: list) -> bool:
        """
        Append data to the file.
        :param data: a list of data to be written to the file
        :return: True if successful, False otherwise
        """
        write_format = ""
        s = 3
        for d in data[:-1]:
            write_format += f"{d}\t"
        write_format += f"{data[-1]}"
        write_format += "\n"
        return self._write_data(write_format)


def write_data() -> None:
    wr = WriteData("test")
    headers = ["time", "pressure", "temperature"]
    wr.create_header(headers)
    for i in range(10):
        data = [i, 2*i, 3*i]
        wr.write_data(data)


def read() -> None:
    file_paths = get_file_path()
    for path in file_paths:
        table = read_data(path)
        print(table, table.shape)


def main() -> None:
    write_data()
    read()


if __name__ == '__main__':
    main()
