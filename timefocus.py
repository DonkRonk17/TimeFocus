#!/usr/bin/env python3
"""
TimeFocus - CLI Productivity Timer & Focus Manager
Pomodoro technique, work sessions, break reminders, and productivity tracking. Zero dependencies!
"""

import os
import sys
import io
import time
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# Fix Unicode output on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# --- Config ---
DATA_FILE = Path.home() / ".timefocus.json"
POMODORO_WORK = 25  # minutes
POMODORO_SHORT_BREAK = 5  # minutes
POMODORO_LONG_BREAK = 15  # minutes
POMODORO_CYCLES_BEFORE_LONG = 4

class TimeFocus:
    """Productivity timer and tracker"""
    
    def __init__(self):
        self.data = self.load_data()
    
    def load_data(self) -> Dict:
        """Load session history"""
        if DATA_FILE.exists():
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {"sessions": [], "settings": {}}
    
    def save_data(self):
        """Save session history"""
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def record_session(self, session_type: str, duration: int, task: str = None, completed: bool = True):
        """Record a completed session"""
        session = {
            "type": session_type,
            "duration": duration,
            "task": task,
            "completed": completed,
            "timestamp": datetime.now().isoformat()
        }
        self.data["sessions"].append(session)
        self.save_data()
    
    def get_today_stats(self) -> Dict:
        """Get today's productivity stats"""
        today = datetime.now().date()
        today_sessions = [
            s for s in self.data["sessions"]
            if datetime.fromisoformat(s["timestamp"]).date() == today
        ]
        
        work_time = sum(s["duration"] for s in today_sessions if s["type"] == "work" and s["completed"])
        break_time = sum(s["duration"] for s in today_sessions if s["type"] == "break" and s["completed"])
        completed = sum(1 for s in today_sessions if s["type"] == "work" and s["completed"])
        
        return {
            "work_minutes": work_time,
            "break_minutes": break_time,
            "sessions_completed": completed,
            "total_sessions": len([s for s in today_sessions if s["type"] == "work"])
        }
    
    def get_week_stats(self) -> Dict:
        """Get this week's productivity stats"""
        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday())
        
        week_sessions = [
            s for s in self.data["sessions"]
            if datetime.fromisoformat(s["timestamp"]).date() >= week_start
        ]
        
        work_time = sum(s["duration"] for s in week_sessions if s["type"] == "work" and s["completed"])
        completed = sum(1 for s in week_sessions if s["type"] == "work" and s["completed"])
        
        # Count by day
        by_day = {}
        for s in week_sessions:
            if s["type"] == "work" and s["completed"]:
                day = datetime.fromisoformat(s["timestamp"]).strftime("%A")
                by_day[day] = by_day.get(day, 0) + s["duration"]
        
        return {
            "work_minutes": work_time,
            "sessions_completed": completed,
            "by_day": by_day
        }
    
    @staticmethod
    def format_time(minutes: int) -> str:
        """Format minutes as HH:MM"""
        hours = minutes // 60
        mins = minutes % 60
        if hours > 0:
            return f"{hours}h {mins}m"
        return f"{mins}m"
    
    @staticmethod
    def countdown(minutes: int, label: str = "Time remaining"):
        """Display countdown timer"""
        total_seconds = minutes * 60
        end_time = time.time() + total_seconds
        
        try:
            while time.time() < end_time:
                remaining = int(end_time - time.time())
                mins, secs = divmod(remaining, 60)
                
                # Clear line and print countdown
                print(f"\r⏱️  {label}: {mins:02d}:{secs:02d}   ", end='', flush=True)
                time.sleep(1)
            
            print(f"\r✅ {label}: Complete!     ")
            return True
        
        except KeyboardInterrupt:
            print(f"\n\n⏸️  Timer paused")
            return False
    
    def pomodoro_session(self, task: str = None):
        """Run a Pomodoro session"""
        print("\n🍅 Starting Pomodoro Session")
        if task:
            print(f"📝 Task: {task}")
        print(f"⏰ Work time: {POMODORO_WORK} minutes\n")
        
        # Work period
        completed = self.countdown(POMODORO_WORK, "Work time")
        
        if completed:
            self.record_session("work", POMODORO_WORK, task, True)
            self.show_notification("Work session complete! Time for a break.")
            
            # Ask about break
            print("\n💡 Time for a break!")
            response = input("Take break now? (y/n): ").lower().strip()
            
            if response == 'y':
                self.break_session(POMODORO_SHORT_BREAK)
        else:
            self.record_session("work", POMODORO_WORK, task, False)
    
    def break_session(self, minutes: int = POMODORO_SHORT_BREAK):
        """Run a break session"""
        print(f"\n☕ Break time: {minutes} minutes")
        print("💡 Step away from your computer!\n")
        
        completed = self.countdown(minutes, "Break time")
        
        if completed:
            self.record_session("break", minutes, None, True)
            self.show_notification("Break over! Back to work.")
        else:
            self.record_session("break", minutes, None, False)
    
    def custom_session(self, minutes: int, task: str = None):
        """Run a custom work session"""
        print(f"\n⏰ Starting {minutes}-minute session")
        if task:
            print(f"📝 Task: {task}")
        print()
        
        completed = self.countdown(minutes, "Work time")
        
        if completed:
            self.record_session("work", minutes, task, True)
            self.show_notification(f"{minutes}-minute session complete!")
        else:
            self.record_session("work", minutes, task, False)
    
    @staticmethod
    def show_notification(message: str):
        """Show simple terminal notification"""
        print(f"\n{'='*60}")
        print(f"🔔 {message}")
        print(f"{'='*60}\n")
        
        # Simple beep (cross-platform)
        print('\a', end='', flush=True)


def print_today_stats(stats: Dict):
    """Pretty print today's stats"""
    print("\n📊 Today's Productivity\n")
    print(f"⏰ Work time:       {TimeFocus.format_time(stats['work_minutes'])}")
    print(f"☕ Break time:      {TimeFocus.format_time(stats['break_minutes'])}")
    print(f"✅ Sessions done:   {stats['sessions_completed']}/{stats['total_sessions']}")
    
    if stats['work_minutes'] > 0:
        efficiency = (stats['sessions_completed'] / stats['total_sessions'] * 100) if stats['total_sessions'] > 0 else 0
        print(f"📈 Completion rate: {efficiency:.0f}%")
    
    print()


def print_week_stats(stats: Dict):
    """Pretty print week's stats"""
    print("\n📊 This Week's Productivity\n")
    print(f"⏰ Total work time:  {TimeFocus.format_time(stats['work_minutes'])}")
    print(f"✅ Sessions completed: {stats['sessions_completed']}")
    
    if stats['work_minutes'] > 0:
        avg_per_day = stats['work_minutes'] / len(stats['by_day']) if stats['by_day'] else 0
        print(f"📈 Average per day:    {TimeFocus.format_time(int(avg_per_day))}")
    
    if stats['by_day']:
        print(f"\n📅 By Day:\n")
        days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for day in days_order:
            if day in stats['by_day']:
                print(f"  {day:10} {TimeFocus.format_time(stats['by_day'][day])}")
    
    print()


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="TimeFocus - CLI Productivity Timer & Focus Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  timefocus pomodoro                           # 25-min Pomodoro session
  timefocus pomodoro --task "Write docs"       # Pomodoro with task
  timefocus work 45                            # 45-minute work session
  timefocus break                              # 5-minute break
  timefocus break --long                       # 15-minute break
  timefocus stats                              # Today's productivity
  timefocus stats --week                       # This week's stats
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Pomodoro command
    pomo_parser = subparsers.add_parser('pomodoro', aliases=['pomo'], help='Start Pomodoro session (25 min)')
    pomo_parser.add_argument('--task', '-t', help='Task description')
    
    # Work command
    work_parser = subparsers.add_parser('work', help='Start custom work session')
    work_parser.add_argument('minutes', type=int, help='Session duration in minutes')
    work_parser.add_argument('--task', '-t', help='Task description')
    
    # Break command
    break_parser = subparsers.add_parser('break', help='Start break')
    break_parser.add_argument('--long', action='store_true', help='Long break (15 min)')
    break_parser.add_argument('--minutes', '-m', type=int, help='Custom break duration')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show productivity statistics')
    stats_parser.add_argument('--week', '-w', action='store_true', help='Show week stats')
    
    # Reset command
    reset_parser = subparsers.add_parser('reset', help='Reset all data')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    tf = TimeFocus()
    
    # Execute command
    if args.command in ['pomodoro', 'pomo']:
        tf.pomodoro_session(args.task)
    
    elif args.command == 'work':
        if args.minutes < 1:
            print("❌ Duration must be at least 1 minute")
            return
        tf.custom_session(args.minutes, args.task)
    
    elif args.command == 'break':
        if args.minutes:
            duration = args.minutes
        elif args.long:
            duration = POMODORO_LONG_BREAK
        else:
            duration = POMODORO_SHORT_BREAK
        
        tf.break_session(duration)
    
    elif args.command == 'stats':
        if args.week:
            stats = tf.get_week_stats()
            print_week_stats(stats)
        else:
            stats = tf.get_today_stats()
            print_today_stats(stats)
    
    elif args.command == 'reset':
        confirm = input("⚠️  Reset all data? This cannot be undone. (yes/no): ")
        if confirm.lower() == 'yes':
            if DATA_FILE.exists():
                DATA_FILE.unlink()
            print("✅ All data reset")
        else:
            print("❌ Reset cancelled")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 TimeFocus closed")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
