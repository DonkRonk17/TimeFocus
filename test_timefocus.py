#!/usr/bin/env python3
"""
Comprehensive test suite for TimeFocus
Tests all core functionality without user interaction
"""

import os
import sys
import io
import json
import time
from pathlib import Path
from datetime import datetime, timedelta

# Fix Unicode output
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Import TimeFocus
sys.path.insert(0, os.path.dirname(__file__))
from timefocus import TimeFocus, DATA_FILE


class TestTimeFocus:
    """Test suite for TimeFocus"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.test_data_file = Path.home() / ".timefocus_test.json"
    
    def setup(self):
        """Setup test environment"""
        # Backup real data if exists
        if DATA_FILE.exists():
            self.backup_file = DATA_FILE.with_suffix('.json.backup')
            DATA_FILE.rename(self.backup_file)
        
        # Clean test data
        if self.test_data_file.exists():
            self.test_data_file.unlink()
        
        # Monkey-patch DATA_FILE in timefocus module
        import timefocus
        timefocus.DATA_FILE = self.test_data_file
    
    def teardown(self):
        """Cleanup test environment"""
        # Restore DATA_FILE
        import timefocus
        timefocus.DATA_FILE = DATA_FILE
        
        # Remove test data
        if self.test_data_file.exists():
            self.test_data_file.unlink()
        
        # Restore real data
        if hasattr(self, 'backup_file') and self.backup_file.exists():
            self.backup_file.rename(DATA_FILE)
    
    def assert_equal(self, actual, expected, test_name):
        """Assert equality"""
        if actual == expected:
            print(f"✅ {test_name}")
            self.passed += 1
        else:
            print(f"❌ {test_name}")
            print(f"   Expected: {expected}")
            print(f"   Got: {actual}")
            self.failed += 1
    
    def assert_true(self, condition, test_name):
        """Assert true"""
        if condition:
            print(f"✅ {test_name}")
            self.passed += 1
        else:
            print(f"❌ {test_name}")
            self.failed += 1
    
    def test_initialization(self):
        """Test TimeFocus initialization"""
        print("\n📦 Test: Initialization")
        
        # Clean start
        if self.test_data_file.exists():
            self.test_data_file.unlink()
        
        tf = TimeFocus()
        self.assert_true(isinstance(tf.data, dict), "Creates data dictionary")
        self.assert_true("sessions" in tf.data, "Has sessions list")
        self.assert_true("settings" in tf.data, "Has settings dict")
    
    def test_record_session(self):
        """Test recording sessions"""
        print("\n📝 Test: Record Session")
        
        # Clean start
        if self.test_data_file.exists():
            self.test_data_file.unlink()
        
        tf = TimeFocus()
        initial_count = len(tf.data["sessions"])
        
        tf.record_session("work", 25, "Test task", True)
        
        self.assert_equal(
            len(tf.data["sessions"]),
            initial_count + 1,
            "Session recorded"
        )
        
        session = tf.data["sessions"][-1]
        self.assert_equal(session["type"], "work", "Correct session type")
        self.assert_equal(session["duration"], 25, "Correct duration")
        self.assert_equal(session["task"], "Test task", "Correct task")
        self.assert_equal(session["completed"], True, "Marked as completed")
        self.assert_true("timestamp" in session, "Has timestamp")
    
    def test_today_stats(self):
        """Test today's statistics"""
        print("\n📊 Test: Today's Statistics")
        
        # Clean start
        if self.test_data_file.exists():
            self.test_data_file.unlink()
        
        tf = TimeFocus()
        
        # Add some sessions
        tf.record_session("work", 25, "Task 1", True)
        tf.record_session("break", 5, None, True)
        tf.record_session("work", 25, "Task 2", True)
        tf.record_session("work", 25, "Task 3", False)
        
        stats = tf.get_today_stats()
        
        self.assert_equal(stats["work_minutes"], 50, "Correct work time")
        self.assert_equal(stats["break_minutes"], 5, "Correct break time")
        self.assert_equal(stats["sessions_completed"], 2, "Correct completed count")
        self.assert_equal(stats["total_sessions"], 3, "Correct total sessions")
    
    def test_week_stats(self):
        """Test week statistics"""
        print("\n📅 Test: Week Statistics")
        
        # Clean start
        if self.test_data_file.exists():
            self.test_data_file.unlink()
        
        tf = TimeFocus()
        
        # Add sessions across multiple days
        today = datetime.now()
        
        # Today
        tf.record_session("work", 50, "Today work", True)
        
        # Manually add older session
        yesterday = (today - timedelta(days=1)).isoformat()
        tf.data["sessions"].append({
            "type": "work",
            "duration": 25,
            "task": "Yesterday work",
            "completed": True,
            "timestamp": yesterday
        })
        tf.save_data()
        
        stats = tf.get_week_stats()
        
        self.assert_equal(stats["work_minutes"], 75, "Correct week work time")
        self.assert_equal(stats["sessions_completed"], 2, "Correct week sessions")
        self.assert_true(len(stats["by_day"]) > 0, "Has by-day breakdown")
    
    def test_format_time(self):
        """Test time formatting"""
        print("\n⏰ Test: Time Formatting")
        
        self.assert_equal(TimeFocus.format_time(45), "45m", "Minutes only")
        self.assert_equal(TimeFocus.format_time(90), "1h 30m", "Hours and minutes")
        self.assert_equal(TimeFocus.format_time(120), "2h 0m", "Exact hours")
    
    def test_data_persistence(self):
        """Test data saves and loads correctly"""
        print("\n💾 Test: Data Persistence")
        
        # Clean start
        if self.test_data_file.exists():
            self.test_data_file.unlink()
        
        # Create and save data
        tf1 = TimeFocus()
        tf1.record_session("work", 25, "Test", True)
        session_count = len(tf1.data["sessions"])
        
        # Load in new instance
        tf2 = TimeFocus()
        
        self.assert_equal(
            len(tf2.data["sessions"]),
            session_count,
            "Data persists across instances"
        )
    
    def test_incomplete_sessions(self):
        """Test incomplete session tracking"""
        print("\n⏸️  Test: Incomplete Sessions")
        
        # Clean start
        if self.test_data_file.exists():
            self.test_data_file.unlink()
        
        tf = TimeFocus()
        
        # Add completed and incomplete sessions
        tf.record_session("work", 25, "Completed", True)
        tf.record_session("work", 25, "Incomplete", False)
        
        stats = tf.get_today_stats()
        
        self.assert_equal(stats["sessions_completed"], 1, "Only counts completed")
        self.assert_equal(stats["total_sessions"], 2, "Counts all work sessions")
    
    def test_break_tracking(self):
        """Test break session tracking"""
        print("\n☕ Test: Break Tracking")
        
        # Clean start
        if self.test_data_file.exists():
            self.test_data_file.unlink()
        
        tf = TimeFocus()
        
        tf.record_session("work", 25, "Work", True)
        tf.record_session("break", 5, None, True)
        tf.record_session("work", 25, "Work", True)
        tf.record_session("break", 15, None, True)
        
        stats = tf.get_today_stats()
        
        self.assert_equal(stats["work_minutes"], 50, "Work time excludes breaks")
        self.assert_equal(stats["break_minutes"], 20, "Correct break time")
    
    def test_task_association(self):
        """Test task tracking"""
        print("\n📝 Test: Task Association")
        
        # Clean start
        if self.test_data_file.exists():
            self.test_data_file.unlink()
        
        tf = TimeFocus()
        
        tf.record_session("work", 25, "Fix bug #123", True)
        tf.record_session("work", 25, "Write docs", True)
        
        sessions = tf.data["sessions"]
        tasks = [s["task"] for s in sessions if s["task"]]
        
        self.assert_equal(len(tasks), 2, "Both tasks recorded")
        self.assert_true("Fix bug #123" in tasks, "First task found")
        self.assert_true("Write docs" in tasks, "Second task found")
    
    def test_empty_stats(self):
        """Test stats with no data"""
        print("\n📊 Test: Empty Statistics")
        
        # Clean start
        if self.test_data_file.exists():
            self.test_data_file.unlink()
        
        tf = TimeFocus()
        
        stats = tf.get_today_stats()
        
        self.assert_equal(stats["work_minutes"], 0, "Zero work time")
        self.assert_equal(stats["sessions_completed"], 0, "Zero sessions")
    
    def run_all(self):
        """Run all tests"""
        print("\n" + "="*60)
        print("🧪 TimeFocus Test Suite")
        print("="*60)
        
        self.setup()
        
        try:
            self.test_initialization()
            self.test_record_session()
            self.test_today_stats()
            self.test_week_stats()
            self.test_format_time()
            self.test_data_persistence()
            self.test_incomplete_sessions()
            self.test_break_tracking()
            self.test_task_association()
            self.test_empty_stats()
        finally:
            self.teardown()
        
        # Summary
        print("\n" + "="*60)
        print(f"📊 Test Results: {self.passed} passed, {self.failed} failed")
        print("="*60)
        
        if self.failed == 0:
            print("\n✅ All tests passed!\n")
            return 0
        else:
            print(f"\n❌ {self.failed} test(s) failed\n")
            return 1


if __name__ == "__main__":
    tester = TestTimeFocus()
    sys.exit(tester.run_all())
