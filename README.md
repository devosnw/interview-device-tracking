# interview-device-tracking

## Setup

You'll need a semi recent version of `python3` (likely >= 3.5 for `typing` support) installed on your machine. Then:

```sh
python3 -m venv .venv # make a virtualenv to not pollute your machine
source .venv/bin/activate # activate it
pip install -r requirements-dev.txt # install all dev dependencies
```

## Tests

To run the full test suite:

```sh
make test
```

## Solution

To run the "driver" code:

```sh
make solution
```

## Teardown

```sh
deactivate # deactivate the virualenv
```

## TODOs

Some other things I was thinking about but didn't want to spend the time:

* Add some useful comments here and there for more clarity
* Break out some of the classes/funcs into additional modules/packages
