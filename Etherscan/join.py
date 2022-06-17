import os
import pandas as pd

# provide path to data directory
directory = os.fsencode('data')

## dai

# initialize loop with an empty dataframe
dai = pd.DataFrame(columns=['to', 'from', 'value', 'gas', 'time', 'nonce'])

# loop through the files and iteratively build the full dataset
for file in os.listdir:
    filename = os.fsdecode(file)
    df = pd.DataFrame(filename)
    dai.append(df)

# save to feather format
dai.to_feather('dai.feather')

# ## maker

# # initialize loop with an empty dataframe
# mkr = pd.DataFrame(columns=['to', 'from', 'value', 'gas', 'time', 'nonce'])

# # loop through the files and riteratively build the full dataset
# for file in os.listdir:
#     df = pd.DataFrame(file + path)
#     mkr.append(df)

# mkr.to_feather('mkr.feather')