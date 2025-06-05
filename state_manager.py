import json
import os

class StateManager:
    def __init__(self, state_file):
        self.state_file = state_file
        self.state = self._load_state()
    
    def _load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {
            "last_batch": 0,
            "total_batches": 0,
            "completed_batches": [],
            "search_url": "",
            "results_url": "",
            "downloaded_files": [],
            "geography_filter": {
                "type": "",  # Can be state, city, county, msa, city_state
                "value": ""
            }
        }
    
    def save_state(self):
        # Make sure the directory exists
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f)
    
    def update_last_batch(self, batch_num):
        self.state["last_batch"] = batch_num
        self.save_state()
    
    def add_completed_batch(self, batch_num):
        if batch_num not in self.state["completed_batches"]:
            self.state["completed_batches"].append(batch_num)
        self.save_state()
    
    def update_urls(self, search_url=None, results_url=None):
        if search_url:
            self.state["search_url"] = search_url
        if results_url:
            self.state["results_url"] = results_url
        self.save_state()
    
    def update_geography_filter(self, filter_type, filter_value):
        """Update the geography filter information
        
        Args:
            filter_type (str): Type of filter (state, city, county, msa, city_state)
            filter_value (str): Value of the filter
        """
        self.state["geography_filter"]["type"] = filter_type
        self.state["geography_filter"]["value"] = filter_value
        self.save_state()
    
    def add_downloaded_file(self, batch_num, filename, pages):
        import datetime
        timestamp = datetime.datetime.now().strftime('%d%m%y_%H%M')
        
        self.state["downloaded_files"].append({
            "batch": batch_num,
            "filename": filename,
            "timestamp": timestamp,
            "pages": pages
        })
        self.save_state()
    
    def remove_batch_data(self, batch_num):
        self.state["downloaded_files"] = [
            f for f in self.state["downloaded_files"] 
            if f["batch"] != batch_num
        ]
        self.state["completed_batches"] = [
            b for b in self.state["completed_batches"]
            if b != batch_num
        ]
        self.save_state()
    
    def set_total_batches(self, total_batches):
        self.state["total_batches"] = total_batches
        self.save_state()
    
    def is_batch_completed(self, batch_num):
        return batch_num in self.state["completed_batches"]