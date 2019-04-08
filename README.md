# sharp-assist

Sharp-Assist is a set of utilities to assist in the prediction of game outcomes, both against-the-spread and over/under.

## Dependencies

### BeautifulSoup

Used for parsing HTML

    pip install beautifulsoup4

### libtidy

Used to correct issues with HTML before parsing

#### Ubuntu
    apt-get install libtidy
    pip install pytidylib

#### Windows

Download the binaries from [here](http://binaries.html-tidy.org/). Unzip and add directory with tidy.dll to system PATH variable.
