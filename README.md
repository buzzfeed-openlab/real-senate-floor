# real-senate-floor

## Setup

**1. Install OS level dependencies**
- Python 3
- geckodriver (latest release [here](https://github.com/mozilla/geckodriver/releases))
- xvfb (only required if using ubuntu, `sudo apt-get install xvfb`)

**2. Clone this repo**
```
git clone https://github.com/buzzfeed-openlab/real-senate-floor.git
cd real-senate-floor
```

**3. Install required python libraries**

Optional but recommended: make a virtual environment using [virtualenv](https://virtualenv.readthedocs.io/en/latest/) and [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html).

Notes:
- Instructions for setting up virtualenv [here](http://docs.python-guide.org/en/latest/dev/virtualenvs/).
- `mkvirtualenv` will automatically activate the `rsf` environment; to activate it in the future, just use `workon rsf`
- if the virtualenv you make isn't python 3 (check w/ `python --version`), use `mkvirtualenv rsf -p /path/to/your/python3` (find your python3 path with `which python3`)
```
mkvirtualenv rsf
```

Install requirements:
```
pip install -r requirements.txt
```

**4. Create config file**

Copy the example config file:
```
cp config.py.example config.py
```
& then update `config.py` with the relevant twitter credentials
