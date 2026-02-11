"""
Refactored data update script using modular architecture.
This replaces the original update_data.py with a cleaner, more maintainable version.
"""
import os
import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))
from config import config
from data.fetcher import data_fetcher
from utils.logger import logger
from analysis.economic_insights import economic_analyzer
from visualization.components import viz_components
import yaml
import pandas as pd
import matplotlib.pyplot as plt
class EconomicDataUpdater:
    """Refactored economic data update system."""
    def __init__(self):
        """Initialize the data updater."""
        self.data_file = config.data_settings['cache_file']
        self.history_days = config.data_settings['history_days']
    def load_existing_data(self) -> list:
        """Load existing data from cache file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = yaml.safe_load(f) or []
                if isinstance(data, dict):
                    data = [data]
                logger.info(f"📂 Loaded {len(data)} existing records from {self.data_file}")
                return data
            except Exception as e:
                logger.error(f"Error loading existing data: {e}")
                return []
        logger.info(f"📂 No existing data file found at {self.data_file}")
        return []
    def save_data(self, records: list) -> None:
        """Save data to cache file."""
        try:
            with open(self.data_file, 'w') as f:
                yaml.safe_dump(records, f, sort_keys=False)
            logger.info(f"💾 Saved {len(records)} records to {self.data_file}")
        except Exception as e:
            logger.error(f"Error saving data: {e}")
            raise
    def trim_history(self, records: list) -> list:
        """Trim records to maintain configured history length."""
        cutoff_date = datetime.utcnow() - timedelta(days=self.history_days)
        trimmed = [
            record for record in records 
            if datetime.fromisoformat(record["timestamp"].replace("Z", "")) >= cutoff_date
        ]
        if len(trimmed) != len(records):
            logger.info(f"🗂️ Trimmed history: {len(records)} → {len(trimmed)} records")
        return trimmed
    def create_snapshot(self, fallback_data: dict = None) -> dict:
        """Create current data snapshot."""
        logger.info("📸 Creating data snapshot...")
        current_values = data_fetcher.fetch_all_current(fallback_data)
        timestamp = datetime.utcnow().isoformat() + "Z"
        snapshot = {**current_values, "timestamp": timestamp}
        logger.info(f"📸 Snapshot created with {len(current_values)} indicators")
        return snapshot
    def backfill_history(self) -> list:
        """Backfill complete historical data."""
        logger.info("🔄 Starting historical data backfill...")
        start_date = (datetime.utcnow() - timedelta(days=self.history_days)).date()
        df = data_fetcher.fetch_all_history(start_date)
        if df.empty:
            logger.error("❌ Backfill failed: No data retrieved")
            return []
        records = []
        for idx, row in df.iterrows():
            entry = {
                col: (None if pd.isna(val) else float(val)) 
                for col, val in row.items()
            }
            timestamp = datetime.combine(idx.date(), datetime.min.time()).isoformat() + "Z"
            entry["timestamp"] = timestamp
            records.append(entry)
        records = self.trim_history(records)
        logger.info(f"🔄 Backfill complete: {len(records)} records generated")
        return records
    def generate_visualizations(self, records: list) -> None:
        """Generate basic visualization (M2 area chart)."""
        if not records:
            logger.warning("⚠️ No data available for visualization")
            return
        try:
            df = pd.DataFrame(records)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df.set_index('timestamp', inplace=True)
            if 'M2SL' in df.columns:
                m2_data = df['M2SL'].dropna()
                if not m2_data.empty:
                    plt.figure(figsize=(10, 6))
                    plt.fill_between(m2_data.index, m2_data.values, 
                                   color='steelblue', alpha=0.5)
                    plt.plot(m2_data.index, m2_data.values, color='steelblue')
                    plt.title(f"M2SL (last {self.history_days // 365} years)")
                    plt.xlabel("Date")
                    plt.ylabel("M2SL")
                    plt.tight_layout()
                    plt.savefig("m2_area.png")
                    plt.close()
                    logger.visualization_complete("M2 Area Chart", "m2_area.png")
        except Exception as e:
            logger.error(f"Visualization generation failed: {e}")
    def run_update(self, backfill: bool = False) -> None:
        """Run the data update process."""
        logger.info("🚀 Starting economic data update...")
        if backfill:
            logger.info("🔄 Running full historical backfill...")
            records = self.backfill_history()
            if not records:
                logger.error("❌ Backfill failed, keeping existing data unchanged")
                return
        else:
            records = self.load_existing_data()
            fallback_data = records[-1] if records else {}
            snapshot = self.create_snapshot(fallback_data)
            records.append(snapshot)
            records = self.trim_history(records)
        self.save_data(records)
        self.generate_visualizations(records)
        logger.info("✅ Data update complete!")
def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Refactored Economic Data Updater",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python refactored_update_data.py
  python refactored_update_data.py --backfill
  python refactored_update_data.py --verbose
        """
    )
    parser.add_argument(
        '--backfill', 
        action='store_true',
        help='Rebuild complete 5-year historical dataset'
    )
    parser.add_argument(
        '--verbose',
        action='store_true', 
        help='Enable verbose debug logging'
    )
    args = parser.parse_args()
    if args.verbose:
        import logging
        logger.logger.setLevel(logging.DEBUG)
    updater = EconomicDataUpdater()
    try:
        updater.run_update(backfill=args.backfill)
    except KeyboardInterrupt:
        logger.info("⏹️ Update interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"💥 Update failed: {e}")
        sys.exit(1)
if __name__ == "__main__":
    main()