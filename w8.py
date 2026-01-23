import json
import os
from datetime import datetime
from pathlib import Path

# Data file path
DATA_FILE = Path.home() / ".weight_tracker_data.json"


def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"entries": []}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def add_weight(weight, date=None):
    data = load_data()
    
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("Error: Invalid date format. Please use YYYY-MM-DD.")
            return
    
    for entry in data["entries"]:
        if entry["date"] == date:
            entry["weight"] = weight
            save_data(data)
            print(f"Updated weight for {date}: {weight} kg")
            return
    
    data["entries"].append({"date": date, "weight": weight})
    # sort entries by date
    data["entries"].sort(key=lambda x: x["date"])
    save_data(data)
    print(f"Added weight for {date}: {weight} kg")


def list_entries():
    data = load_data()
    entries = data["entries"]
    
    if not entries:
        print("No weight entries found. Use 'add' command to add your first entry.")
        return
    
    print("\n" + "=" * 60)
    print(f"{'Date':<15} {'Weight (kg)':<15} {'Change':<15} {'% Change':<15}")
    print("=" * 60)
    
    first_weight = entries[0]["weight"]
    prev_weight = None
    
    for entry in entries:
        date = entry["date"]
        weight = entry["weight"]
        
        if prev_weight is None:
            change_str = "-"
            percent_str = "-"
        else:
            change = weight - prev_weight
            percent_change = ((weight - prev_weight) / prev_weight) * 100
            sign = "+" if change >= 0 else ""
            change_str = f"{sign}{change:.2f} kg"
            percent_str = f"{sign}{percent_change:.2f}%"
        
        print(f"{date:<15} {weight:<15.2f} {change_str:<15} {percent_str:<15}")
        prev_weight = weight
    
    print("=" * 60)
    
    if len(entries) > 1:
        last_weight = entries[-1]["weight"]
        total_change = last_weight - first_weight
        total_percent = ((last_weight - first_weight) / first_weight) * 100
        sign = "+" if total_change >= 0 else ""
        
        print(f"\nSummary:")
        print(f"  Starting weight: {first_weight:.2f} kg ({entries[0]['date']})")
        print(f"  Current weight:  {last_weight:.2f} kg ({entries[-1]['date']})")
        print(f"  Total change:    {sign}{total_change:.2f} kg ({sign}{total_percent:.2f}%)")
        print(f"  Total entries:   {len(entries)}")
    print()


def delete_entry(date):
    data = load_data()
    
    for i, entry in enumerate(data["entries"]):
        if entry["date"] == date:
            removed = data["entries"].pop(i)
            save_data(data)
            print(f"Deleted entry: {removed['date']} - {removed['weight']} kg")
            return
    
    print(f"No entry found for date: {date}")


def generate_graph(output_file="weight_graph.png"):
    try:
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
    except ImportError:
        print("Error: matplotlib is required for graph generation.")
        print("Install it with: pip install matplotlib")
        return
    
    data = load_data()
    entries = data["entries"]
    
    if not entries:
        print("No weight entries found. Add some entries first.")
        return
    
    if len(entries) < 2:
        print("Need at least 2 entries to generate a graph.")
        return
    
    dates = [datetime.strptime(e["date"], "%Y-%m-%d") for e in entries]
    weights = [e["weight"] for e in entries]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(dates, weights, marker='o', linewidth=2, markersize=8, 
            color='#2563eb', markerfacecolor='#3b82f6', markeredgecolor='white',
            markeredgewidth=2)
    
    ax.fill_between(dates, weights, alpha=0.3, color='#3b82f6')
    
    for i, (date, weight) in enumerate(zip(dates, weights)):
        ax.annotate(f'{weight:.1f}', (date, weight), 
                   textcoords="offset points", xytext=(0, 10),
                   ha='center', fontsize=9, fontweight='bold')
    
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Weight (kg)', fontsize=12, fontweight='bold')
    ax.set_title('Weight Tracker Progress', fontsize=16, fontweight='bold', pad=20)
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45, ha='right')
    
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)
    
    min_weight = min(weights)
    max_weight = max(weights)
    min_idx = weights.index(min_weight)
    max_idx = weights.index(max_weight)
    
    ax.axhline(y=min_weight, color='green', linestyle=':', alpha=0.5)
    ax.axhline(y=max_weight, color='red', linestyle=':', alpha=0.5)
    
    first_weight = weights[0]
    last_weight = weights[-1]
    total_change = last_weight - first_weight
    total_percent = ((last_weight - first_weight) / first_weight) * 100
    sign = "+" if total_change >= 0 else ""
    
    stats_text = f"Start: {first_weight:.1f} kg → Current: {last_weight:.1f} kg | Change: {sign}{total_change:.1f} kg ({sign}{total_percent:.1f}%)"
    ax.text(0.5, -0.18, stats_text, transform=ax.transAxes, 
            ha='center', fontsize=10, style='italic')
    
    plt.tight_layout()
    
    plt.savefig(output_file, dpi=150, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"Graph saved to: {os.path.abspath(output_file)}")


def clear_all():
    """Clear all weight data."""
    confirm = input("Are you sure you want to delete all data? (yes/no): ")
    if confirm.lower() == "yes":
        save_data({"entries": []})
        print("All data cleared.")
    else:
        print("Operation cancelled.")


def print_help():
    """Print help message."""
    help_text = """
Weight Tracker CLI - Track your weight over time

Usage:
  python weight_tracker.py <command> [arguments]

Commands:
  add <weight> [date]    Add a weight entry (date format: YYYY-MM-DD)
                         If no date is provided, today's date is used.
                         Example: python weight_tracker.py add 75.5
                         Example: python weight_tracker.py add 75.5 2024-01-15

  list                   List all weight entries with percentage changes
                         Example: python weight_tracker.py list

  delete <date>          Delete an entry by date
                         Example: python weight_tracker.py delete 2024-01-15

  graph [filename]       Generate a visual graph of weight changes
                         Default filename: weight_graph.png
                         Example: python weight_tracker.py graph
                         Example: python weight_tracker.py graph my_progress.png

  clear                  Clear all weight data

  help                   Show this help message

Data is stored in: ~/.weight_tracker_data.json
"""
    print(help_text)


def main():
    import sys
    
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "add":
        if len(sys.argv) < 3:
            print("Error: Please provide a weight value.")
            print("Usage: python weight_tracker.py add <weight> [date]")
            return
        try:
            weight = float(sys.argv[2])
        except ValueError:
            print("Error: Weight must be a number.")
            return
        
        date = sys.argv[3] if len(sys.argv) > 3 else None
        add_weight(weight, date)
    
    elif command == "list":
        list_entries()
    
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Error: Please provide a date to delete.")
            print("Usage: python weight_tracker.py delete <date>")
            return
        delete_entry(sys.argv[2])
    
    elif command == "graph":
        output_file = sys.argv[2] if len(sys.argv) > 2 else "weight_graph.png"
        generate_graph(output_file)
    
    elif command == "clear":
        clear_all()
    
    elif command == "help":
        print_help()
    
    else:
        print(f"Unknown command: {command}")
        print("Use 'help' to see available commands.")


if __name__ == "__main__":
    main()
