# ROS Workspace

This is the ros/catkin workspace. Developed nodes should all have a folder in `./src`.

**You need to activate this on your computer.** See Setup Instructions below.

## Adding existing modules

To add an existing module, use a git submodule inside or `src`.

## Setup Instructions

1. Start in this folder! `cd catkin_ws`
2. Source your global ROS setup file: `source /opt/ros/melodic/setup.bash`
3. Setup for Python3: `alias catkin_make="catkin_make -DPYTHON_EXECUTABLE=/usr/bin/python3 -DPYTHON_INCLUDE_DIR=/usr/include/python3.7m -DPYTHON_LIBRARY=/usr/lib/libpython3.so"`
4. Create the workspace: `catkin_make`
5. This should have no errors!
6. A `build` and `devel` folder should have appeared.
7. Source `devel/setup.bash`
8. `export ROS_HOSTNAME=$(hostname -i | cut -f1 -d' ')`
9. `export ROS_MASTER_URI="http://rospi.dns.dries007.net:11311"`

The steps you need to do **every time** are 1, 2, 3, and 7. 
It's best to put them in a file and source that from your own bashrc.
For an example: see `dries_setup_env`.

