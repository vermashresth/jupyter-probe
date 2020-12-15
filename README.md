# Jupyter Probe
Jupyterprobe is a python package to monitor, manage, declare and analyse notebook resource usage on jupyter environments. 

## Compatibility

Jupyterprobe works with Linux, OSX. Wide variety of Jupyter environment flavours and configurations are supported:
- Jupyter Notebook, Jupyter Lab
- Authentication: None, Token, Password
- Hosted at: localhost, remote
- GPU is also supported (requires Nvidia Management Library (NVML)/ CUDA toolkit).

Jupyterprobe currently works with Python 3.6.1 or later.

## Installing

Install with `pip` or your favorite PyPi package manager.

```
pip install jupyter-probe
```
(For common troubleshooting, see here)

## Usage
Note: All these commands are to be run from within your jupyter notebooks.

#### Define Probe
First define a `Probe` object using host and port.

```python
from jupyterprobe import Probe
host = 'localhost'
port = 8888
pb = Probe(host, port)
```
If your jupyter environment is password authenticated, you can additionally pass the password argument
```python
pb = Probe(host, port, password='hobbit')
```

#### Monitor
To monitor resource usage of all notebooks in your session, call `Monitor`.

```python
pb.Monitor()
```
![Monitor](https://github.com/vermashresth/jupyter-probe/raw/master/img/monitorcell.png)
Top 5 results are shown sorted by memory usage. To see more, you can pass top_n as argument

```python
pb.Monitor(10)
```
#### Declare Experiment
To declare ownership 

```python
pb.Declare(owner='Gandalf', priority='10', project='Ring')
```
This will save the declaration for your current notebook in `~/.jupyterprobe/experiment_register.json`.

#### Monitor Team
By default, monitor only shows resource usage and PID of your notebooks. To see ownership and project related data, use `MonitorTeam` or `Monitor(team=true)`
```python
pb.MonitorTeam()
```
![Team](https://github.com/vermashresth/jupyter-probe/raw/master/img/teamcell.png)
This will show details based on your declarations as well as declarations from other teammates using the same Jupyter Session.

#### Custom Usage Analytics
If you want to do your own analytics on notebooks' usage, you can get Pandas Dataframe of all the results through `pb.results`.

Some more usefull methods:

`get_results_by_PID` : get all results of a notebook through PID

`get_results_by_name` : get all results of a notebook through name. Returns multiple notebooks if name isn't unique

`get_path_by_PID` : get absolute path of notebook through PID

`get_path_by_name` : get absolute path of notebook through name. Returns multiple paths if name isn't unique

## Troubleshooting

**Can't install psutil, python.h not found**: 
You need to install python-dev. For Unix like systems, you can do `sudo apt-get install python3.x-dev` where `python3.x` refers to your python version.


**INFO: GPU not found on your system, but you actually have GPU**: Install `py3nvml` and run 
```
import py3nvml
py3nvml.py3nvml.nvmlInit()
```
Most probably, your Nvidia libraries are missing due to which it will throw an error.


**Could not detect any jupyter servers from your kernel**: This can happen if you have multiple ipython kernels and you have only installed jupyterprobe in one of them.
The best way possible is to uninstall and install jupyter and jupyterlab packages.

```
python3.x -m pip uninstall jupyter jupyterlab
python3.x -m pip install jupyter jupyterlab
```

If this doesn't work either, you can try removing the ipython kernel, install it again and then repeat the above steps.

```
jupyter kernelspec list
jupyter kernelspec remove <kernel-name>
python3.x -m pip install ipykernel
python3.x -m ipykernel install --user
```

## Issues and Contributing
The project is still in active development. If you face any error or want to request a feature, feel free to open an issue. Additionally, if you want to contribute, a PR is always welcome.

