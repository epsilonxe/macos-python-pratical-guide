# macOS Python Pratical Guide
A route to start the Python project in macOS

This guide summarizes the best practice and practical working progress for Python projects.
Save your time to spend it more for the creativity.

## Installation
1. Xcode Command Line Tools

    ```sh
    xcode-select --install
    ```

1. Homebrew (https://brew.sh)

    ```sh
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    ``` 
1. Optional, but recommended:

    ```sh
    brew install openssl readline sqlite3 xz zlib
    ```
    
1. When running Mojave or higher (10.14+), install the additional SDK headers:

    ```sh
    sudo installer -pkg /Library/Developer/CommandLineTools/Packages/macOS_SDK_headers_for_macOS_10.14.pkg -target /
    ```
1. Install [pyenv](https://github.com/pyenv/pyenv) and [pyenv-vitualenv](https://github.com/pyenv/pyenv-virtualenv)

    ```sh
    brew install pyenv pyenv-virtualenv
    ```
