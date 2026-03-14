import pandas as pd

class EEGDataset:

    def __init__(self, path):

        # read Excel file instead of CSV
        self.data = pd.read_excel(path)

        self.index = 0

    def get_sample(self):

        if self.index >= len(self.data):
            self.index = 0

        sample = self.data.iloc[self.index]

        self.index += 1

        return sample.values