# w8 (Weight Tracker CLI)

A simple command-line tool to track your weight over time without any shame.

## Before usage

```bash
pip install matplotlib
```

## Usage

```bash
# Add weight (uses today's date)
python w8.py add 75.5

# Add weight for specific date
python w8.py add 74.8 2024-12-20

# View all entries
python w8.py list

# Generate graph
python w8.py graph

# Delete an entry
python w8.py delete 2024-12-20

# Clear all data
python w8.py clear
```

## Data Storage

Data is stored in `~/.weight_tracker_data.json`.
