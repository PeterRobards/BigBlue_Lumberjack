# BigBlue Lumberjack

This repository contains a Python tool designed to aid in processing the RAW Access logs provided by
a popular webhosting company (BlueHost.com). WIth this program you can quickly search your log files for 
various events (e.g. all the POST requests to a specific URL on your site) and/or reformat them to a new 
format so that the data can be easily imported into other tools (currently both CSV and JSON formats are supported).
his tool: `process_logs.py`, accepts a directory path as input (this directory should contain your raw log files, all 
with a matching file extension - e.g. '.log'), cycles through all the log files in that directory, extracts the key data,
and loads that data into a python dictionary.


## Getting Started

This tool is optimized for Python 3.8x, and requires an up to date version of Python to properly function.

### Prerequisites

This program was built to process the RAW access logs supplied by BlueHost.com - these files all have the
same basic format (shown below), with each line representing a single event. If your log file has a different 
format, then this program may not work as intended. 
```
Log File Format:

IP - - [Date:Time -UTC] “REQUEST /url PROTOCOL/1.1” StatusCode# Bytes# “-“ “user/agent” website.com websiteIP
```
Note: This tool is designed process all files in a given directory with the same file extension.
 To set all files in the current working directory to the same file extension (i.e. '.log') via bash,
 you can run the following:
```
$ for f in *; do mv "$f" "$f.log"; done
```

## Python

Python 3 is essential for running this program and, while not required, I always suggest setting up a
python virtual environment (venv) or (pipenv) when running this tool in order to keep your workspace isolated.

If you already know you have an appropriate version of Python installed on your system, you can skip to [Usage](#usage).

If you know you're missing Python3, you can find and download the appropriate package for your OS via the link below.
If you're unsure, or you have never installed Python before check out the next section about installing python.

* [Python.org](https://www.python.org/getit/) - Get Python 3.x here

## Installing Python

First check to see if Python is installed on your system and if so, what version is running. 
How that process works depends largely on your Operating System (OS).

### Linux

Note: Most Linux distributions come with Python preloaded, but it might not be with the latest version
 and you could only have Python 2 instead of Python 3 (which is what this program is written in).
 Double check your system's version by using the following commands:
```
# Check the system Python version
$ python --version

# Check the Python 2 version
$ python2 --version

# Check the Python 3 version
$ python3 --version
```

### Windows

In windows, open ‘cmd’ (Command Prompt) and type the following command.

```
C:\> python --version

```
Using the --version switch will show you the version that’s installed. Alternatively, you can use the -V switch:
```
C:\> python -V

```
Either of the above commands will give the version number of the Python interpreter installed or they will display an error if otherwise.

### Mac OSX

Starting with Catalina, Python no longer comes pre-installed on most Mac computers, and many older models only
have Python 2 pre-installed, not Python 3. In order to check the Python version currently installed on your Mac,
open a command-line application, i.e. Terminal, and type in any of the following commands:

```
# Check the system Python version
$ python --version

# Check the Python 2 version
$ python2 --version

# Check the Python 3 version
$ python3 --version
```
Note:
You’ll want to either download or upgrade to the latest version of Python if any of the following conditions are true:
* None of the above commands return a version number on your machine.
* The only versions you see listed when running the above commands are part of the Python 2.x series.
* Your version of Python 3 isn’t at least version 3.8x.

If Python is not already on your system, or it is not version 3.8x or above, you can find
detailed installation instructions for your particular OS, here:

Detailed instructions for installing Python3 on Linux, MacOS, and Windows, are available at link below:

* [Python 3 Installation & Setup Guide](https://realpython.com/installing-python/) - How to install Python3

## Package Management with pip

Once you have verified that you have Python 3.x installed and running on your system, you'll be using the built in
package manager 'pip' to handle the rest of the installations. 

pip is the reference Python package manager and is used to install and update packages. 
You’ll need to make sure you have the latest version of pip installed on your system.

### Linux

Note: Debian and most other distributions include a python-pip package. If, for some reason, you prefer to use 
one of the Linux distribution-provided versions of pip instead vist [https://packaging.python.org/guides/installing-using-linux-tools/].
 Double check your system's version by using the following commands:
```
# Check the system Python version
$ python -m pip --version

# Check the Python 3 version
$ python3 -m pip --version
```
You can also install pip yourself to ensure you have the latest version. It’s recommended to use the system pip to bootstrap a user installation of pip:
```
# Upgrade pip
$ python -m pip install --user --upgrade pip

# Upgrade pip python3
$ python3 -m pip install --user --upgrade pip
```

### Windows

The Python installers for Windows include pip. You should be able to see the version of pip by opening ‘cmd’ (the Command Prompt) and entering the following: 

```
C:\> python -m pip --version

```
You can make sure that pip is up-to-date by running:
```
C:\> python -m pip install --upgrade pip

```


### Mac OSX

 Double check your system's version by using the following commands:
```
# Check the system Python version
$ python -m pip --version

# Check the Python 3 version
$ python3 -m pip --version
```
You can also install pip yourself to ensure you have the latest version. It’s recommended to use the system pip to bootstrap a user installation of pip:
```
# Upgrade pip
$ python -m pip install --user --upgrade pip

# Upgrade pip python3
$ python3 -m pip install --user --upgrade pip
```

## Setting up a Virtual Environment in Python

It is recommended that you create a virtual environment in order to perform operations with this program on your system, 
this will need to be accomplished before installing any further dependencies this tool relies on.
The 'venv' module is the preferred way to create and manage virtual environments for this tool. 
Luckily since Python 3.3m venv is included in the Python standard library.
 Below are the steps needed to create a virtual environment and activate it in the working directory for this tool.

### Linux

To create a virtual environment, go to your project’s directory and run venv, as shown below:
```
# If you only have Python3 installed or Python3 is set as your default
$ python -m venv env

# If you have both Python2 and Python3 installed and want to specify Python3
$ python3 -m venv env
```

### Windows

To create a virtual environment, go to your project’s directory and run venv, as shown below: 

```
C:\> python -m venv env

```

### Mac OSX

To create a virtual environment, go to your project’s directory and run venv, as shown below: Double check your system's version by using the following commands:
```
# If you only have Python3 installed or Python3 is set as your default
$ python -m venv env

# If you have both Python2 and Python3 installed and want to specify Python3
$ python3 -m venv env
```

Note: The second argument is the location to create the virtual environment.
so accourding to the above commands: venv will create a virtual Python installation in the env folder.
In general, you can simply create this in your project yourself and call it env (or whatever you want).

Tip: You should be sure to exclude your virtual environment directory from your version control system using .gitignore or similar.

## Activating the Virtual Environment

Before you can start installing or using packages in your virtual environment you’ll need to activate it. Activating a virtual environment
erves to put the virtual environment-specific python and pip executables into your shell’s PATH.

### Linux

To create a virtual environment, go to your project’s directory and run venv, as shown below:
```
$ source env/bin/activate
```

### Windows

To create a virtual environment, go to your project’s directory and run venv, as shown below: 

```
C:\> .\env\Scripts\activate

```

### Mac OSX

To create a virtual environment, go to your project’s directory and run venv, as shown below: Double check your system's version by using the following commands:
```
$ source env/bin/activate
```
Now the development environment has been properly set up with and up to date version of Python 3 you should be ready
to go as all the libraries that this tool relies on are already included with Python.


## Usage

To begin you'll need to download the raw access logs from BlueHost (or if your logs come from another source, make sure
they are formatted correctly or be sure to modify the value extraction methods or the program might not perform correctly)
and make sure they are all saved in the same directory with a matchin file extension(e.g. '.log'). Instructions on one way to
accomplish this are included earlier in this document under [Prerequisites](#Prerequisites).
Once those conditions are met you are ready to begin using this tool.

Run `python process_logs.py` - as shown below there are also a set of optional arguments which are shown below:

```
usage: process_logs.py [-h] [-i [INPUT_PATH]] [-l [LOG_FILES]] [-o [OUTPUT_RESULTS]] [-e [{CSV,JSON}]] [-s] [-S]
                     [-D [DIR_OUT]]

Python tool designed to parse the RAW text Access Logs from a Webhosting provider

optional arguments:
  -h, --help            show this help message and exit
  -i [INPUT_PATH], --input_path [INPUT_PATH]
                        The path to the directory containing the log files you wish to add as input
  -l [LOG_FILES], --log_files [LOG_FILES]
                        Signal the file type (via its extension: 'txt', 'log', etc) to target
  -o [OUTPUT_RESULTS], --output_results [OUTPUT_RESULTS]
                        Output file name where you want to save the results from a search
  -e [{CSV,JSON}], --export_type [{CSV,JSON}]
                        Signal the type of file in the directory to target (default=CSV)
  -s, --search_for      Signal that you want to search for log events matching a certain pattern
  -S, --save_files      Signal that you wish to save the raw log files to a different format
  -D [DIR_OUT], --directory_out [DIR_OUT]
                        Set the name of the Directory to save the converted log files in
```

If no arguments are specified upon running this program, the program will display the help menu seen above automatically.
The optional arguments shown above allow the user to select the target input Directory (where all your log files are stored),
the file extension shared by your log files (e.g. if your files end in '.log', you enter '-l log'), whether you want to search
the log files for certain events or save the log files as a different format for later processing (note: you can do both at onece),
enter the file name to save your search results to, select the type of format (CSV or JSON) to convert your logs to (note: the files
wille be saved with an identical name to what they currently have, just the format and extension will be changed), and set the output
directory where you want all the results to be stored. 

### Examples
Upon the successful execution of the `process_logs.py` file, the results displayed to the
standard output should mimic what is shown below (with some differences based on the input supplied).

Below we're searching the logs and reformatting them to JSON files at the same time, while using the default output directory:

```
 $ python process_logs.py -i DIR_NAME/ -l log -o SearchResults -e JSON -sS

*** Running 'process_logs.py' ***
[+] Accessing Input Directory: 'DIR_NAME/'

[*] Processing Log File: DIR_NAME/YourWebsite.com-ssl_log-Jul-2019.log

[*] Search Function Selected...
	Note: search parameters consist of valid Key - Value pairs: 'ip':'127.0.0.1' 

[>] Valid Column Names: [ip, date, time, method, url, protocol, status, bytes, user_agent, website, dest_url]
	[->] Please enter the number of parameters (key:value pairs) to search for: 1

	[->] Please Enter a key matching a Column to search within: method
	[->] Please enter some corresponding value to search for: POST
[+] Searching for :
	'log_event["method"] == "POST"'
[+] Exporting data to: FormattedLogFiles/YourWebsite.com-ssl_log-Jul-2019.json

******* ******* *******

…

******* ******* *******

[*] Processing Log File: DIR_NAME/YourWebsite.com-ssl_log-Dec-2020.log
[+] Searching for :
	'log_event["method"] == "POST"'
[+] Exporting data to: FormattedLogFiles/YourWebsite.com-ssl_log-Dec-2020.json

******* ******* *******

[*] Saving Search Results to: FormattedLogFiles/SearchResults
[+] Exporting data to: FormattedLogFiles/SearchResults.json

******* ******* *******

```

Here we're signaling that we just want to search the logs for every entry containing matches to 
the both of the provided key:value pairs while relying on the default CSV format for our search 
results and setting SomeOtherDIR as the destination to save these results:


```
 $ python process_logs.py -i DIR_NAME/ -l log -o SearchResults -s -D SomeOtherDIR

*** Running 'process_logs.py' ***
[+] Accessing Input Directory: 'DIR_NAME/'

[*] Processing Log File: DIR_NAME/YourWebsite.com-ssl_log-Jul-2019.log

[*] Search Function Selected...
	Note: search parameters consist of valid Key - Value pairs: 'ip':'127.0.0.1' 

[>] Valid Column Names: [ip, date, time, method, url, protocol, status, bytes, user_agent, website, dest_url]
	[->] Please enter the number of parameters (key:value pairs) to search for: 2

	[->] Please Enter a key matching a Column to search within: method
	[->] Please enter some corresponding value to search for: POST
	
	[->] Please Enter a key Column to search within: url
	[->] Please enter some corresponding value to search for: /mail/contact_me.php
[+] Searching for :
	'log_event["method"] == "POST" and log_event["url"] == "/mail/contact_me.php"'

******* ******* *******

[*] Processing Log File: DIR_NAME/YourWebsite.com-ssl_log-May-2020.log
[+] Searching for :
	'log_event["method"] == "POST" and log_event["url"] == "/mail/contact_me.php"'

******* ******* *******

…

******* ******* *******

[*] Processing Log File: DIR_NAME/YourWebsite.com-ssl_log-Dec-2020.log
[+] Searching for :
	'log_event["method"] == "POST" and log_event["url"] == "/mail/contact_me.php"'

******* ******* *******

[*] Saving Search Results to: SomeOtherDIR/SearchResults
[+] Exporting data to: SomeOtherDIR/SearchResults.csv
******* ******* *******

```

Finally, below we're simply reformatting all the log files in the specified directory (i.e. 
all the files in the directory that end in '.log') to the default CSV format and saving them 
to 'OutputDIR'.

```
$ python process_logs.py -i DIR_NAME/ -l log -S -D OutputDIR

*** Running 'process_logs.py' ***
[+] Accessing Input Directory: 'DIR_NAME/'

[*] Processing Log File: DIR_NAME/YourWebsite.com-ssl_log-Jul-2019.log
[+] Exporting data to: OutputDIR/YourWebsite.com-ssl_log-Jul-2019.csv

******* ******* *******

...

******* ******* *******

[*] Processing Log File: DIR_NAME/YourWebsite.com-ssl_log-Dec-2020.log
[+] Exporting data to: OutputDIR/YourWebsite.com-ssl_log-Dec-2020.csv

******* ******* *******
```

Upon seeing output similar to the above, this program should be working as intended.


## Authors

* **Peter Robards** - *Initial work* - [PeterRobards](https://github.com/PeterRobards)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details



