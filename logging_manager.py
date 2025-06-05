import os
import time
import datetime
import logging
from logging.handlers import RotatingFileHandler

class ScraperLogger:
    """Centralized logging manager for the Miller 3 Data Scraper"""
    
    def __init__(self, session_name=None):
        self.session_name = session_name or f"session_{int(time.time())}"
        self.session_start = datetime.datetime.now()
        
        # Create logs directory structure if it doesn't exist
        self.logs_dir = "logs"
        self.screenshots_dir = os.path.join(self.logs_dir, "screenshots")
        self.session_logs_dir = os.path.join(self.logs_dir, "session_logs")
        self.debug_dir = os.path.join(self.logs_dir, "debug")
        
        for directory in [self.logs_dir, self.screenshots_dir, self.session_logs_dir, self.debug_dir]:
            os.makedirs(directory, exist_ok=True)
        
        # Set up main session logger
        self.setup_session_logger()
        self.setup_debug_logger()
        
        # Log session start
        self.log_session_start()
    
    def setup_session_logger(self):
        """Set up the main session logger"""
        self.session_logger = logging.getLogger(f"session_{self.session_name}")
        self.session_logger.setLevel(logging.INFO)
        
        # Remove existing handlers to avoid duplicates
        for handler in self.session_logger.handlers[:]:
            self.session_logger.removeHandler(handler)
        
        # File handler for session logs
        session_log_file = os.path.join(
            self.session_logs_dir, 
            f"{self.session_name}_{self.session_start.strftime('%Y%m%d_%H%M%S')}.log"
        )
        
        file_handler = RotatingFileHandler(
            session_log_file, 
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.session_logger.addHandler(file_handler)
        self.session_logger.addHandler(console_handler)
        
        # Prevent propagation to root logger
        self.session_logger.propagate = False
    
    def setup_debug_logger(self):
        """Set up debug logger for detailed debugging"""
        self.debug_logger = logging.getLogger(f"debug_{self.session_name}")
        self.debug_logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers
        for handler in self.debug_logger.handlers[:]:
            self.debug_logger.removeHandler(handler)
        
        # Debug file handler
        debug_log_file = os.path.join(
            self.debug_dir,
            f"debug_{self.session_name}_{self.session_start.strftime('%Y%m%d_%H%M%S')}.log"
        )
        
        debug_handler = RotatingFileHandler(
            debug_log_file,
            maxBytes=50*1024*1024,  # 50MB
            backupCount=3
        )
        debug_handler.setLevel(logging.DEBUG)
        
        debug_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        debug_handler.setFormatter(debug_formatter)
        
        self.debug_logger.addHandler(debug_handler)
        self.debug_logger.propagate = False
    
    def log_session_start(self):
        """Log the start of a new scraping session"""
        self.session_logger.info("="*60)
        self.session_logger.info(f"🚀 MILLER 3 DATA SCRAPER SESSION STARTED")
        self.session_logger.info(f"📅 Session: {self.session_name}")
        self.session_logger.info(f"🕐 Start Time: {self.session_start.strftime('%Y-%m-%d %H:%M:%S')}")
        self.session_logger.info("="*60)
    
    def log_session_end(self, stats=None):
        """Log the end of a scraping session"""
        session_end = datetime.datetime.now()
        duration = session_end - self.session_start
        
        self.session_logger.info("="*60)
        self.session_logger.info(f"🏁 MILLER 3 DATA SCRAPER SESSION ENDED")
        self.session_logger.info(f"🕐 End Time: {session_end.strftime('%Y-%m-%d %H:%M:%S')}")
        self.session_logger.info(f"⏱️  Total Duration: {duration}")
        
        if stats:
            self.session_logger.info(f"📊 SESSION STATISTICS:")
            for key, value in stats.items():
                self.session_logger.info(f"   {key}: {value}")
        
        self.session_logger.info("="*60)
    
    def log_batch_start(self, batch_num, start_page, end_page):
        """Log the start of a batch"""
        self.session_logger.info(f"📦 BATCH {batch_num} STARTED")
        self.session_logger.info(f"   📄 Pages: {start_page} to {end_page}")
    
    def log_batch_end(self, batch_num, success, filename=None):
        """Log the end of a batch"""
        status = "✅ SUCCESS" if success else "❌ FAILED"
        self.session_logger.info(f"📦 BATCH {batch_num} {status}")
        if filename:
            self.session_logger.info(f"   📁 File: {filename}")
    
    def log_download_start(self, batch_num):
        """Log download initiation"""
        self.session_logger.info(f"⬇️  Initiating download for batch {batch_num}")
    
    def log_download_success(self, batch_num, filename):
        """Log successful download"""
        self.session_logger.info(f"✅ Download completed for batch {batch_num}")
        self.session_logger.info(f"   📁 File saved: {filename}")
    
    def log_download_failure(self, batch_num, error):
        """Log download failure"""
        self.session_logger.error(f"❌ Download failed for batch {batch_num}")
        self.session_logger.error(f"   🚫 Error: {error}")
    
    def log_button_detection(self, strategy_num, success, button_info=None):
        """Log button detection attempts"""
        if success:
            self.debug_logger.info(f"🎯 Button found using Strategy {strategy_num}")
            if button_info:
                self.debug_logger.info(f"   Button info: {button_info}")
        else:
            self.debug_logger.debug(f"❌ Strategy {strategy_num} failed")
    
    def log_page_navigation(self, page_num, success):
        """Log page navigation"""
        status = "✅" if success else "❌"
        self.session_logger.info(f"{status} Navigated to page {page_num}")
    
    def log_selection_clearing(self, count):
        """Log selection clearing"""
        if count > 0:
            self.session_logger.info(f"🧹 Cleared {count} existing selections")
        else:
            self.debug_logger.debug("🧹 No existing selections to clear")
    
    def log_error(self, component, error, details=None):
        """Log errors with context"""
        self.session_logger.error(f"🚫 ERROR in {component}: {error}")
        if details:
            self.session_logger.error(f"   Details: {details}")
        
        # Also log to debug with full traceback
        import traceback
        self.debug_logger.error(f"ERROR in {component}: {error}")
        self.debug_logger.error(f"Full traceback:\n{traceback.format_exc()}")
    
    def save_screenshot(self, name, driver, context=""):
        """Save screenshot with organized naming"""
        timestamp = int(time.time())
        filename = f"{name}_{timestamp}.png"
        filepath = os.path.join(self.screenshots_dir, filename)
        
        try:
            driver.save_screenshot(filepath)
            self.debug_logger.info(f"📸 Screenshot saved: {filename}")
            if context:
                self.debug_logger.info(f"   Context: {context}")
            return filepath
        except Exception as e:
            self.debug_logger.error(f"Failed to save screenshot {filename}: {e}")
            return None
    
    def log_manual_intervention(self, reason):
        """Log when manual intervention is required"""
        self.session_logger.warning(f"🔧 MANUAL INTERVENTION REQUIRED")
        self.session_logger.warning(f"   Reason: {reason}")
    
    def log_config(self, config):
        """Log configuration at session start"""
        self.session_logger.info("⚙️  CONFIGURATION:")
        for key, value in config.items():
            # Don't log sensitive information
            if 'password' in key.lower() or 'secret' in key.lower():
                value = "***hidden***"
            self.session_logger.info(f"   {key}: {value}")
    
    def get_session_summary(self):
        """Get summary of current session for logging"""
        duration = datetime.datetime.now() - self.session_start
        return {
            "session_name": self.session_name,
            "start_time": self.session_start.strftime('%Y-%m-%d %H:%M:%S'),
            "duration": str(duration),
            "logs_directory": self.logs_dir
        }

# Global logger instance
_global_logger = None

def get_logger(session_name=None):
    """Get or create the global logger instance"""
    global _global_logger
    if _global_logger is None:
        _global_logger = ScraperLogger(session_name)
    return _global_logger

def set_logger(logger):
    """Set the global logger instance"""
    global _global_logger
    _global_logger = logger
