"""
This file contains code similar to Pandas DataFrame.
It was designed as an alternative to external libraries
so that University students can use, heterogeneous
size-mutable, tables to complete a task or implementation.

Originally created by lightless.

"""

import csv
import typing


def read_csv(file_name) -> typing.List[typing.List]:
    """
    Similarly to getting a text file,
    we return comma seperated values data.
    """

    csv_data = []
    with open(file_name, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            csv_data.append(row)
    return csv_data


class DataFrame:
    """
    A heterogeneous tabular data structure with rows and columns.
    Similarly to a Pandas DataFrame except coded in a python environment
    to prevent additional use of external libraries.
    """

    def __init__(self, data: typing.List = None, columns: typing.List = None):
        self.columns = columns

        # Fill empty columns
        for row in data:
            if len(row) != len(columns):
                row.extend("" for _ in range(len(columns) - len(row)))

        self.data = data

    def __str__(self):
        """
        A visualised display of our Data Frame.
        Useful for interpreting data.
        """

        df_len = 50

        index_column = "Index"
        index_width = len(index_column) + 1
        index_values = [str(idx) for idx in range(len(self.data[:df_len]))]

        col_widths = [
            max(len(col), max(len(str(row[i])) for row in self.data[:df_len]))
            for i, col in enumerate(self.columns)
        ]
        idx_width = max(index_width, max(len(idx) for idx in index_values))
        idx_values = [idx.ljust(idx_width) for idx in index_values]

        headers = "\n\n" + index_column.ljust(idx_width) + " | " + " | ".join(
            col.ljust(width) for col, width in zip(self.columns, col_widths)
        )
        separator = "-" * (
            idx_width + 3 + sum(col_widths) + (len(self.columns) - 1) * 3
        )

        rows = [
            idx_values[i] + " | " +
            " | ".join(
                str(row[i]).ljust(width) for i, width in enumerate(col_widths)
            )
            for i, row in enumerate(self.data[:df_len])
        ]

        return "\n".join([headers, separator] + rows)

    def add_row(self, row_data: typing.List | typing.Tuple):
        """
        Insert a row to the existing Data Frame.
        """

        return self.data.append(row_data)

    def add_row_data(self, index: int, data: typing.List):
        """
        Add data to an existing row in a Data Frame.
        """

        if len(data) != len(self.columns):
            raise ValueError("Data row is out of range.")

        if index < 0 or index >= len(self.data):
            raise IndexError("This index does not exist.")

        self.data[index] = data
        return self

    def remove_row(
        self,
        index: int = None
    ):
        """
        Remove a row from the existing Data Frame.
        """

        self.data.remove(self.data[index])
        return self

    def add_column(self, columns: typing.List[str]):
        """
        Insert a column to an existing DataFrame.
        """

        if len(columns) == 1:
            return DataFrame(self.data, self.columns + columns)

        return DataFrame(self.data, self.columns + columns)

    def remove_column(self, columns: typing.List[str]) -> 'DataFrame':
        """
        Remove column(s) and corresponding data
        """
        indices_to_remove = [self.columns.index(col) for col in columns]
        self.columns = [col for col in self.columns if col not in columns]
        self.data = [
            [row[i] for i in range(len(row)) if i not in indices_to_remove]
            for row in self.data
        ]
        return self

    def get_columns(self, columns: typing.List):
        """
        Get a column and row data for it from a DataFrame.
        """

        for col in columns:
            if col not in self.columns:
                raise ValueError(f"Column '{col}' not found.")

        data_columns = [
            [row[self.columns.index(col)] for row in self.data]
            for col in columns
        ]

        transposed_data = list(zip(*data_columns))
        return DataFrame(transposed_data, columns)

    def get_row(self, index):
        """
        Get row data via index from a DataFrame.
        """

        return self.data[index]

    def head(self, n: int):
        """
        Display the 'n' number of rows from the top
        of the Data Frame.
        """

        return DataFrame(self.data[0:n], self.columns)

    def tail(self, n: int):
        """
        Display the 'n' number of rows from the bottom
        of the Data Frame.
        """

        return DataFrame(self.data[-1-n::], self.columns)