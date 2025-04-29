import sqlite3
import json
from pathlib import Path
from typing import List, Optional

class Database:
    def __init__(self):
        # Use pathlib to handle paths cross-platform
        self.db_dir = Path(__file__).parent / "database"
        self.db_dir.mkdir(parents=True, exist_ok=True)

    def save_combinations(self, base_filename: str, combinations: List[List[int]]) -> str:
        """
        Save combinations to a SQLite database file. Automatically increments run number
        based on existing files with the same parameters.
        """
        # Extract stem and split on '-' for robust parameter parsing
        base = Path(base_filename).stem
        parts = base.split('-')

        # Expect at least m,n,k,j,s
        if len(parts) >= 5:
            m, n, k, j, s = parts[:5]
            # Find existing DBs matching the first five parameters
            pattern = f"{m}-{n}-{k}-{j}-{s}-*.db"
            existing = list(self.db_dir.glob(pattern))

            # Collect run numbers from existing files
            run_nums = []  # type: List[int]
            for f in existing:
                stem_parts = f.stem.split('-')
                if len(stem_parts) >= 7:
                    try:
                        run_nums.append(int(stem_parts[5]))
                    except ValueError:
                        continue

            next_run = max(run_nums) + 1 if run_nums else 1
            new_filename = f"{m}-{n}-{k}-{j}-{s}-{next_run}-{len(combinations)}"
        else:
            # Fallback: use the provided base_filename stem
            new_filename = base

        db_path = self.db_dir / f"{new_filename}.db"

        # Use 'with' to ensure proper resource cleanup
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS combinations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    combination TEXT NOT NULL
                )
                """
            )
            # Insert all combinations as JSON strings
            cursor.executemany(
                "INSERT INTO combinations (combination) VALUES (?)",
                [(json.dumps(combo),) for combo in combinations]
            )
            conn.commit()

        return new_filename

    def load_combinations(self, filepath: str) -> List[List[int]]:
        """Load combinations from a given .db file path."""
        path = Path(filepath)
        combinations: List[List[int]] = []
        with sqlite3.connect(path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT combination FROM combinations")
            for (row,) in cursor.fetchall():
                combinations.append(json.loads(row))

        return combinations

    def delete_combinations(self, filepath: str) -> None:
        """Delete the specified database file."""
        path = Path(filepath)
        if path.exists():
            path.unlink()

    def get_db_files(
        self,
        m: Optional[int] = None,
        n: Optional[int] = None,
        k: Optional[int] = None,
        j: Optional[int] = None,
        s: Optional[int] = None,
    ) -> List[str]:
        """
        Return list of .db filenames filtered by provided parameters.
        If no parameters specified, returns all .db files.
        """
        all_files = [f.name for f in self.db_dir.glob("*.db")]
        if None in (m, n, k, j, s):
            return all_files

        # Filter by matching prefix
        prefix = f"{m}-{n}-{k}-{j}-{s}-"
        matching = [f for f in all_files if f.startswith(prefix)]
        return matching
