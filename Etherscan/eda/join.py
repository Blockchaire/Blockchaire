import os
import pandas as pd

# provide path to data directory
directory = os.fsencode('data')

## dai

# initialize loop with an empty dataframe
dai = pd.DataFrame(columns=['to', 'from', 'value', 'gas', 'time', 'nonce'])

# loop through the files and iteratively build the full dataset
for file in os.listdir(directory):
    filename = os.path.join(os.fsdecode(directory), os.fsdecode(file))
    df = pd.read_feather(filename)
    dai = pd.concat([dai, df], axis=0, ignore_index=True)

# save to feather format
dai.to_feather('dai.feather')
print(dai.shape)