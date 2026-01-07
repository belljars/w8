# w8 (Weight Tracker CLI)

A simple command-line tool to track your weight over time without any shame.

## Before usage

```bash
pip install matplotlib
```

## Usage

```bash
# Add weight (uses today's date)
python weight_tracker.py add 75.5

# Add weight for specific date
python weight_tracker.py add 74.8 2024-12-20

# View all entries
python weight_tracker.py list

# Generate graph
python weight_tracker.py graph

# Delete an entry
python weight_tracker.py delete 2024-12-20

# Clear all data
python weight_tracker.py clear
```

## Data Storage

Data is stored in `~/.weight_tracker_data.json`.
