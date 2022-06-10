print("hey!!")


from torchvision import transforms
import netCDF4 as nc
import numpy as np
import random
import torch
import os

from config import get_config

config, _ = get_config()

print("waddup!!")

def get_munis(imagery_list, rank, worker_map):
    index = worker_map[rank]
    return imagery_list[index]


class Dataloader():

    def __init__(self, muni, imagery_dir, rank):

        self.muni = muni
        self.rank = rank
        self.split = config.tv_split
        self.num_train = int(5 * self.split)
        self.november_indices = [10, 22, 34, 46, 58]
        self.y_indices = {10: [12,24], 22: [24,36], 34: [36,48], 46: [48,60], 58: [60,72]}
        self.load_data()

    def load_data(self):

        ds = nc.Dataset(self.muni, "r")

        ims, migs = ds["ims"], ds["migrants"]

        x, y = [], []

        for index in self.november_indices:
            
            i1, i2 = self.y_indices[index][0], self.y_indices[index][1]
            
            x.append(np.array(ims[index]))
            y.append([migs[i1:i2].sum()])
            
        train_indices = random.sample([i for i in range(0, len(x))], self.num_train)
        val_indices = [i for i in range(0, len(x)) if i not in train_indices]
        
        x_train, y_train = [x[i] for i in train_indices], [y[i] for i in train_indices]
        x_val, y_val = [x[i] for i in val_indices], [y[i] for i in val_indices]
    
        self.x_train = torch.tensor(np.array(x_train), dtype = torch.float32)
        self.y_train = torch.tensor(np.array(y_train), dtype = torch.float32)
        self.x_val = torch.tensor(np.array(x_val), dtype = torch.float32)
        self.y_val = torch.tensor(np.array(y_val), dtype = torch.float32)
        
        # print(self.x_train.shape, self.y_train.shape, self.x_val.shape, self.y_val.shape)

        # with open(config.log_name, "a") as f:
        #     f.write(str(self.rank) + "  NUM TRAIN: " + str(len(self.x_train)) + "  NUM VAL: " + str(len(self.x_val)) + "\n")

if __name__ == "__main__":

    base_dir = config.imagery_dir

    for ncdf in os.listdir(base_dir):

        with open("./log.txt", "a") as f:
            f.write("NCDF: " + ncdf + "\n")

        try:

            Dataloader(base_dir + ncdf, base_dir, 1)

            with open("./log.txt", "a") as f:
                f.write(str(ncdf) + " worked!\n")

        except Exception as e:

            with open("./log.txt", "a") as f:
                f.write(str(ncdf) + " didn't work because: " + str(e) + "\n")