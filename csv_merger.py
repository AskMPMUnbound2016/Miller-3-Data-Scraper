#!/usr/bin/env python3
"""
CSV FILE MERGER - Miller 3 Data Scraper
=======================================
Merge multiple downloaded CSV files into a single consolidated file
"""

import os
import sys
import csv
import pandas as pd
from datetime import datetime
import glob

class CSVMerger:
    def __init__(self, download_dir='downloads'):
        self.download_dir = download_dir
        print("\n=== CSV FILE MERGER ===")
        print("Merge multiple downloaded CSV files into one")
        
        # Ensure download directory exists
        if not os.path.exists(self.download_dir):
            print(f"❌ Download directory '{self.download_dir}' not found!")
            sys.exit(1)
    
    def find_csv_files(self):
        """Find all CSV files in the download directory"""
        csv_pattern = os.path.join(self.download_dir, "*.csv")
        csv_files = glob.glob(csv_pattern)
        
        if not csv_files:
            print(f"❌ No CSV files found in '{self.download_dir}' directory")
            return []
        
        # Sort files by modification time (newest first)
        csv_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        
        return csv_files
    
    def show_file_info(self, csv_files):
        """Display information about found CSV files"""
        print(f"\n📁 Found {len(csv_files)} CSV files in '{self.download_dir}':")
        print("=" * 80)
        
        total_size = 0
        total_records = 0
        
        for i, file_path in enumerate(csv_files, 1):
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            total_size += file_size
            
            # Try to count records
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    csv_reader = csv.reader(f)
                    next(csv_reader, None)  # Skip header
                    record_count = sum(1 for row in csv_reader)
                    total_records += record_count
            except Exception as e:
                record_count = "Unknown"
            
            # Get file modification time
            mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            
            print(f"{i:2d}. {filename}")
            print(f"    📊 Records: {record_count}")
            print(f"    📏 Size: {self.format_file_size(file_size)}")
            print(f"    📅 Modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print()
        
        print(f"📈 TOTALS:")
        print(f"   📁 Files: {len(csv_files)}")
        print(f"   📊 Total Records: {total_records:,}")
        print(f"   📏 Total Size: {self.format_file_size(total_size)}")
        
        return total_records
    
    def format_file_size(self, size_bytes):
        """Format file size in human readable format"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
    
    def select_files_to_merge(self, csv_files):
        """Let user select which files to merge"""
        print(f"\n🔄 MERGE OPTIONS:")
        print("=" * 40)
        print("1. 📥 Merge ALL files")
        print("2. 🎯 Select specific files")
        print("3. 📊 Merge by record count limit")
        print("4. 📅 Merge files from specific date range")
        print("5. ❌ Cancel")
        
        while True:
            choice = input("\n🔢 Choose option (1-5): ").strip()
            
            if choice == '1':
                return csv_files, "all_files"
            
            elif choice == '2':
                return self.select_specific_files(csv_files)
            
            elif choice == '3':
                return self.select_by_record_count(csv_files)
            
            elif choice == '4':
                return self.select_by_date_range(csv_files)
            
            elif choice == '5':
                return [], "cancelled"
            
            else:
                print("❌ Please choose 1-5")
                continue
    
    def select_specific_files(self, csv_files):
        """Let user select specific files by number"""
        print(f"\n🎯 SELECT SPECIFIC FILES:")
        print("Enter file numbers separated by commas (e.g., 1,3,5)")
        print("Or enter ranges (e.g., 1-5,7,9-12)")
        
        while True:
            selection = input("📝 Enter file numbers: ").strip()
            
            if not selection:
                print("❌ Please enter file numbers")
                continue
            
            try:
                selected_indices = self.parse_file_selection(selection, len(csv_files))
                selected_files = [csv_files[i-1] for i in selected_indices]
                
                print(f"\n✅ Selected {len(selected_files)} files:")
                for file_path in selected_files:
                    print(f"   • {os.path.basename(file_path)}")
                
                confirm = input(f"\n✅ Merge these {len(selected_files)} files? (y/n): ").lower().strip()
                if confirm in ['y', 'yes']:
                    return selected_files, "specific_files"
                else:
                    continue
                    
            except Exception as e:
                print(f"❌ Invalid selection: {e}")
                continue
    
    def parse_file_selection(self, selection, max_files):
        """Parse user file selection (e.g., '1,3,5-8')"""
        indices = set()
        
        for part in selection.split(','):
            part = part.strip()
            
            if '-' in part:
                # Handle ranges like '5-8'
                start, end = part.split('-', 1)
                start_idx = int(start.strip())
                end_idx = int(end.strip())
                
                if start_idx < 1 or end_idx > max_files:
                    raise ValueError(f"Range {start_idx}-{end_idx} is outside valid range 1-{max_files}")
                
                indices.update(range(start_idx, end_idx + 1))
            else:
                # Handle single numbers
                idx = int(part)
                if idx < 1 or idx > max_files:
                    raise ValueError(f"File number {idx} is outside valid range 1-{max_files}")
                indices.add(idx)
        
        return sorted(indices)
    
    def select_by_record_count(self, csv_files):
        """Select files up to a certain record count"""
        print(f"\n📊 MERGE BY RECORD COUNT:")
        
        while True:
            try:
                max_records = input("📝 Maximum records in merged file (e.g., 50000): ").strip()
                max_records = int(max_records.replace(',', ''))
                
                if max_records <= 0:
                    print("❌ Please enter a positive number")
                    continue
                
                break
            except ValueError:
                print("❌ Please enter a valid number")
                continue
        
        # Select files until we reach the record limit
        selected_files = []
        current_count = 0
        
        for file_path in csv_files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    csv_reader = csv.reader(f)
                    next(csv_reader, None)  # Skip header
                    file_records = sum(1 for row in csv_reader)
                
                if current_count + file_records <= max_records:
                    selected_files.append(file_path)
                    current_count += file_records
                    print(f"✅ Added: {os.path.basename(file_path)} ({file_records:,} records)")
                else:
                    print(f"⚠️ Skipped: {os.path.basename(file_path)} (would exceed limit)")
                    break
                    
            except Exception as e:
                print(f"⚠️ Error reading {os.path.basename(file_path)}: {e}")
                continue
        
        print(f"\n📊 Selected {len(selected_files)} files with {current_count:,} total records")
        
        if selected_files:
            return selected_files, "record_limit"
        else:
            print("❌ No files selected")
            return [], "cancelled"
    
    def select_by_date_range(self, csv_files):
        """Select files from a specific date range"""
        print(f"\n📅 MERGE BY DATE RANGE:")
        print("Enter dates in YYYY-MM-DD format (or press Enter for no limit)")
        
        start_date = input("📅 Start date (from): ").strip()
        end_date = input("📅 End date (to): ").strip()
        
        selected_files = []
        
        for file_path in csv_files:
            file_date = datetime.fromtimestamp(os.path.getmtime(file_path))
            file_date_str = file_date.strftime('%Y-%m-%d')
            
            include_file = True
            
            if start_date and file_date_str < start_date:
                include_file = False
            
            if end_date and file_date_str > end_date:
                include_file = False
            
            if include_file:
                selected_files.append(file_path)
                print(f"✅ Added: {os.path.basename(file_path)} ({file_date_str})")
            else:
                print(f"⚠️ Skipped: {os.path.basename(file_path)} ({file_date_str})")
        
        if selected_files:
            return selected_files, "date_range"
        else:
            print("❌ No files selected in date range")
            return [], "cancelled"
    
    def get_output_filename(self, selected_files, selection_type):
        """Get the output filename from user"""
        print(f"\n📝 OUTPUT FILE NAME:")
        
        # Suggest a default name based on selection type
        timestamp = datetime.now().strftime('%m%d%y_%H%M')
        
        if selection_type == "all_files":
            default_name = f"merged_all_files_{timestamp}.csv"
        elif selection_type == "specific_files":
            default_name = f"merged_selected_{len(selected_files)}files_{timestamp}.csv"
        elif selection_type == "record_limit":
            default_name = f"merged_limited_records_{timestamp}.csv"
        elif selection_type == "date_range":
            default_name = f"merged_date_range_{timestamp}.csv"
        else:
            default_name = f"merged_files_{timestamp}.csv"
        
        print(f"💡 Suggested: {default_name}")
        
        while True:
            filename = input("📁 Output filename (or press Enter for suggested): ").strip()
            
            if not filename:
                filename = default_name
            
            # Ensure .csv extension
            if not filename.lower().endswith('.csv'):
                filename += '.csv'
            
            # Check if file exists
            output_path = os.path.join(self.download_dir, filename)
            if os.path.exists(output_path):
                overwrite = input(f"⚠️ File '{filename}' exists. Overwrite? (y/n): ").lower().strip()
                if overwrite not in ['y', 'yes']:
                    continue
            
            return filename
    
    def merge_csv_files(self, selected_files, output_filename):
        """Merge the selected CSV files"""
        output_path = os.path.join(self.download_dir, output_filename)
        
        print(f"\n🔄 MERGING {len(selected_files)} FILES...")
        print("=" * 50)
        
        try:
            # Use pandas for efficient merging
            dataframes = []
            total_records = 0
            
            for i, file_path in enumerate(selected_files, 1):
                filename = os.path.basename(file_path)
                print(f"📖 Reading file {i}/{len(selected_files)}: {filename}")
                
                try:
                    # Read CSV with pandas
                    df = pd.read_csv(file_path, encoding='utf-8', low_memory=False)
                    records = len(df)
                    total_records += records
                    
                    # Add source file column
                    df['source_file'] = filename
                    
                    dataframes.append(df)
                    print(f"   ✅ {records:,} records loaded")
                    
                except Exception as e:
                    print(f"   ❌ Error reading file: {e}")
                    continue
            
            if not dataframes:
                print("❌ No files could be read successfully")
                return False
            
            # Merge all dataframes
            print(f"\n🔗 Combining {len(dataframes)} dataframes...")
            merged_df = pd.concat(dataframes, ignore_index=True, sort=False)
            
            # Remove duplicates if any
            initial_count = len(merged_df)
            merged_df = merged_df.drop_duplicates()
            final_count = len(merged_df)
            
            if initial_count != final_count:
                print(f"🧹 Removed {initial_count - final_count:,} duplicate records")
            
            # Save merged file
            print(f"💾 Saving merged file: {output_filename}")
            merged_df.to_csv(output_path, index=False, encoding='utf-8')
            
            # Show summary
            file_size = os.path.getsize(output_path)
            print(f"\n✅ MERGE COMPLETE!")
            print("=" * 40)
            print(f"📁 Output file: {output_filename}")
            print(f"📊 Total records: {final_count:,}")
            print(f"📏 File size: {self.format_file_size(file_size)}")
            print(f"📂 Location: {output_path}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error during merge: {e}")
            return False
    
    def run(self):
        """Main merger workflow"""
        try:
            # Find CSV files
            csv_files = self.find_csv_files()
            if not csv_files:
                return
            
            # Show file information
            total_records = self.show_file_info(csv_files)
            
            # Let user select files to merge
            selected_files, selection_type = self.select_files_to_merge(csv_files)
            
            if selection_type == "cancelled" or not selected_files:
                print("❌ Merge cancelled")
                return
            
            # Get output filename
            output_filename = self.get_output_filename(selected_files, selection_type)
            
            # Perform merge
            success = self.merge_csv_files(selected_files, output_filename)
            
            if success:
                print(f"\n🎉 Files successfully merged!")
                
                # Ask if user wants to open the folder
                open_folder = input(f"\n📂 Open download folder? (y/n): ").lower().strip()
                if open_folder in ['y', 'yes']:
                    import subprocess
                    import platform
                    
                    if platform.system() == "Darwin":  # macOS
                        subprocess.run(["open", self.download_dir])
                    elif platform.system() == "Windows":
                        subprocess.run(["explorer", self.download_dir])
                    else:  # Linux
                        subprocess.run(["xdg-open", self.download_dir])
            
        except KeyboardInterrupt:
            print("\n\n🛑 Merge cancelled by user")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
        
        finally:
            input("\n⏸️ Press Enter to exit...")


def main():
    """Main entry point"""
    print("🔗" + "="*60 + "🔗")
    print("           CSV FILE MERGER - MILLER 3 DATA SCRAPER")
    print("🔗" + "="*60 + "🔗")
    
    # Check if pandas is available
    try:
        import pandas as pd
    except ImportError:
        print("❌ Error: pandas library is required for CSV merging")
        print("📦 Install with: pip install pandas")
        input("⏸️ Press Enter to exit...")
        return
    
    merger = CSVMerger()
    merger.run()


if __name__ == "__main__":
    main()
