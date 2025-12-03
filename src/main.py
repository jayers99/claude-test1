import json
from pathlib import Path


def read_json(filepath: Path) -> dict:
    """Read and parse a JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def write_json(filepath: Path, data: dict, indent: int = 2) -> None:
    """Write data to a JSON file."""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=indent)


def main():
    """Example usage."""
    example_data = {
        "name": "Example",
        "version": "1.0.0",
        "items": [1, 2, 3]
    }

    output_file = Path("example.json")
    write_json(output_file, example_data)
    print(f"Written to {output_file}")

    loaded_data = read_json(output_file)
    print(f"Loaded: {loaded_data}")


if __name__ == "__main__":
    main()
