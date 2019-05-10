# macOS Python Pratical Guide
A route to start the Python project in macOS

This guide summarizes the best practice and practical working progress for Python projects.
Save your time to spend it more for the creativity.

## Installation
1. Install Xcode Command Line Tools
    ```bash
    xcode-select --install
    ```

1. Install Homebrew (https://brew.sh)
    ```bash
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    ``` 
1. Optional, but recommended:
    ```bash
    brew install openssl readline sqlite3 xz zlib
    ```
    
1. When running Mojave or higher (10.14+), install the additional SDK headers:
    ```bash
    sudo installer -pkg /Library/Developer/CommandLineTools/Packages/macOS_SDK_headers_for_macOS_10.14.pkg -target /
    ```
1. Install [pyenv](https://github.com/pyenv/pyenv) and [pyenv-vitualenv](https://github.com/pyenv/pyenv-virtualenv)
    ```bash
    brew install pyenv pyenv-virtualenv
    ```

1. Install Python via `pyenv`:
    * List available Python versions:
        ```bash
        pyenv install --list
        ```
        
    * Install the selected version <x.x.x>:
        ```bash
        pyenv install <x.x.x>
        ```
        
    * To enable `--framework-enable` option (package like `matplotlib` need this), use the following command instead:
        ```bash
        env PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install <x.x.x>
        ```
        
1. Append these lines to your profile (`~/.bash_profile`, `~/.zshrc` or `~/.profile`):
        ```
        eval "$(pyenv init -)"
        eval "$(pyenv virtualenv-init -)"
        ```
        
## Usgae

1. To start a new project with an independent virtual environment:
        ```
        pyenv virtualenv <installed-pyenv-python-version> <prefered-environtment-name>
        ```
        
   When the enabled framework option required, use this instead:
        ```
        env PYTHON_CONFIGURE_OPTS="--enable-framework CC=clang" pyenv virtualenv <installed-pyenv-python-version> <prefered-environtment-name>
        ```
        
1. To select the created virtual environtment locally/globally:
        ```
        pyenv <local/global> <created-environtment-name>
        ```
        
1. Now you are in the created virtual environtment, feel free to work or install additional pacakges.

1. You may switch to any available virtual environment by the above command.
        
1. To remove an unwanted virtual environtment:
    * Switch to another available virtual environment, e.g.,   
            ```
            pyenv <local/global> system
            ```
            
    * Remove the unwanted environment:   
            ```
            pyenv uninstall <unwanted-environtment-name>
            ```
