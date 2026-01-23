# w8 (Weight Tracker CLI)

A simple command-line tool to track your weight over time without any shame.

## Before usage

```bash
pip install matplotlib
```

## Usage

```bash
python w8.py add 75.5 # add weight for today's date

python w8.py add 74.8 2024-12-20 # add weight for a specific date

python w8.py list # list all entries

python w8.py graph # generate an graph with matplotlib

python w8.py delete 2024-12-20 # delete an entry

python w8.py clear # clear all data
```

## Data Storage

Data is stored in `~/.weight_tracker_data.json`.
