# Ultimate Basic Python Course
Department of Mathematics and Computer Science
Rajamangala University of Technology Thanyaburi


## Python Practical Guide
A pythonista route to start a Python project

This guide summarizes the best practice and practical working progress for Python projects.
Save your time for spending it later for the creativity.

## Basic Tools

Follow the instructions for your OS:

### Windows

1. Open PowerShell (Admin):
    ```
    [WinKey] + x
    ```

1. Install Chocolatey (https://chocolatey.org/install),
    ```bash
    $ Set-ExecutionPolicy AllSigned
    $ Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
    ```
    
1. Install [pyenv-win]
    ```bash
    $ choco install pyenv-win
    ```


### macOS

1. Optional, but recommended: install Xcode Command Line Tools
    ```bash
    $ xcode-select --install
    ```

1. Install Homebrew (https://brew.sh)
    ```bash
    $ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    ``` 
1. Optional, but recommended:
    ```bash
    $ brew install openssl readline sqlite3 xz zlib
    $ brew cask install sublime-text
    ```
 

1. For macOS Mojave (10.14) or above, the following steps may be required:

    * When running Mojave (10.14), additionally install the SDK headers:
        ```bash
        $ sudo installer -pkg /Library/Developer/CommandLineTools/Packages/macOS_SDK_headers_for_macOS_10.14.pkg -target /
        ```
    
    * If you have Catalina (10.15), set the CPATH environment variable in your shell (e.g., put this in your .zshrc assuming you're using zsh):
        ```bash
        $ export CPATH=`xcrun --show-sdk-path`/usr/include
        ```

1. Install [pyenv](https://github.com/pyenv/pyenv) and [pyenv-vitualenv](https://github.com/pyenv/pyenv-virtualenv)
    ```bash
    $ brew install pyenv pyenv-virtualenv
    ```
    
1. Append these lines to your profile (`~/.bash_profile`, `~/.zshrc` or `~/.profile`):
    ```
     eval "$(pyenv init -)"
     eval "$(pyenv virtualenv-init -)"
    ```

## Usage of `pyenv`

 1. Install Python via `pyenv`:
    
    * List available Python versions:
        ```bash
        $ pyenv install --list
        ```
        
    * Install the selected version x.x.x :
        ```bash
        $ pyenv install x.x.x
        ```

    * After installtion or uninstallation of python in pyenv, run
        ```bash
        $ pyenv rehash
        ```
        
    * For `macOS`, in order to use modules like `matplotlib`, install Python with the following command instead:
        ```bash
        $ env PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install <x.x.x>
        ```

    * For `macOS`, to use `tkinter`, install `tcl-tk` via Homebrew and pay attention to its current version,

    	```bash
    	$ brew install tck-tk
    	```
    	this may give some information like:
    	```
    	...
    	...
    	Pouring tcl-tk-8.6.10.catalina.bottle.1.tar.gz
    	....
    	```
    	which is version 8.6.10. To install python use the following command instead:

    	```bash
    	$ env \
  		PATH="$(brew --prefix tcl-tk)/bin:$PATH" \
  		LDFLAGS="-L$(brew --prefix tcl-tk)/lib" \
  		CPPFLAGS="-I$(brew --prefix tcl-tk)/include" \
  		PKG_CONFIG_PATH="$(brew --prefix tcl-tk)/lib/pkgconfig" \
  		CFLAGS="-I$(brew --prefix tcl-tk)/include" \
  		PYTHON_CONFIGURE_OPTS="--with-tcltk-includes='-I$(brew --prefix tcl-tk)/include' --with-tcltk-libs='-L$(brew --prefix tcl-tk)/lib -ltcl8.6 -ltk8.6'" \
  		pyenv install x.x.x
    	```



1. To start a new project with an independent virtual environment:

    ```
    $ pyenv virtualenv <installed-pyenv-python-version> <prefered-environtment-name>
    ```
        
   When the enabled framework option required, use this instead:
   
   ```
   $ env PYTHON_CONFIGURE_OPTS="--enable-framework CC=clang" pyenv virtualenv <installed-pyenv-python-version> <prefered-environtment-name>
   ```
        
1. To select the created virtual environtment locally/globally:

    ```
    $ pyenv <local/global> <created-environtment-name>
    ```
        
1. Now you are in the created virtual environtment, feel free to work or install additional pacakges.

1. You may switch to any available virtual environment by the above command.
        
1. To remove an unwanted virtual environtment:
    * Switch to another available virtual environment, e.g.,
        
        ```
        $ pyenv <local/global> system
        ```
            
    * Remove the unwanted environment:
    
        ```
        $ pyenv uninstall <unwanted-environtment-name>
        ```
