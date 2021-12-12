When we originally collected the Uniswap data we forgot to include an extra value that we wanted, the jupyter file was created to go though each line of our database and get that missing piece of data line by line. It is inefficient and extremely slow, yet we used it since we only cared about getting specific data at a time and the code being correct. The way I have the filestructure for saving the queries set up is the following:

C:.
├───.ipynb_checkpoints
├───burns
│   ├───burns_output
│   └───burns_split
├───mints
│   ├───mints_output
│   └───mints_split
└───swaps
    ├───swaps_output
    └───swaps_split


Where the original files were in the swaps/burns/mints subdirectories. The saved output from the queries is saved into the "_output" files. It is not necessary to have the same filestructure, and one can change the directories by editing the jupyter notebook.

Working on cleaning up the code and collecting the data in a more efficient manner
