<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/d05b3d02-f655-4fc1-bc68-1fe6e8f6089a" />

# 🍅 TimeFocus

**CLI Productivity Timer & Focus Manager**

A powerful yet simple command-line Pomodoro timer with productivity tracking. Zero dependencies, cross-platform, and designed for developers who live in the terminal.

---

## ✨ Features

- 🍅 **Pomodoro Technique** - Classic 25/5/15 intervals
- ⏰ **Custom Work Sessions** - Any duration you need
- ☕ **Smart Breaks** - Short breaks, long breaks, or custom
- 📊 **Productivity Tracking** - Daily and weekly statistics
- 📝 **Task Tracking** - Associate tasks with sessions
- 🔔 **Simple Notifications** - Terminal bell + messages
- ⏸️ **Keyboard Control** - Ctrl+C to pause anytime
- 💾 **Session History** - Track your productivity over time
- 🎯 **Zero Dependencies** - Pure Python, works everywhere

---

## 📦 Installation

### Option 1: Quick Install

```bash
# Clone the repository
git clone https://github.com/DonkRonk17/TimeFocus.git
cd TimeFocus

# Make executable (Linux/Mac)
chmod +x timefocus.py
ln -s $(pwd)/timefocus.py /usr/local/bin/timefocus

# Windows: Add to PATH or use python timefocus.py
```

### Option 2: Package Install

```bash
pip install -e .
```

**Requirements:** Python 3.6+

---

## 🚀 Quick Start

```bash
# Start a Pomodoro session (25 min)
timefocus pomodoro

# Pomodoro with task tracking
timefocus pomodoro --task "Write documentation"

# Custom work session (45 minutes)
timefocus work 45

# Take a short break (5 min)
timefocus break

# Take a long break (15 min)
timefocus break --long

# View today's productivity
timefocus stats

# View this week's stats
timefocus stats --week
```

---

## 📖 Usage Guide

### Pomodoro Sessions

The Pomodoro Technique uses 25-minute work intervals:

```bash
# Basic Pomodoro
timefocus pomodoro

# Track what you're working on
timefocus pomodoro --task "Fix bug #123"
timefocus pomo -t "Code review"  # Short alias
```

After each session, you'll be prompted to take a break.

### Custom Work Sessions

Need more or less time? Use custom sessions:

```bash
# 45-minute deep work session
timefocus work 45

# 90-minute sprint
timefocus work 90 --task "Feature implementation"

# Quick 10-minute task
timefocus work 10
```

### Break Management

```bash
# Short break (5 minutes)
timefocus break

# Long break (15 minutes)
timefocus break --long

# Custom break duration
timefocus break --minutes 10
```

### Productivity Statistics

Track your focus time and productivity:

```bash
# Today's stats
timefocus stats
# Output:
# 📊 Today's Productivity
# ⏰ Work time:       2h 30m
# ☕ Break time:      25m
# ✅ Sessions done:   6/7
# 📈 Completion rate: 86%

# This week's stats
timefocus stats --week
# Output:
# 📊 This Week's Productivity
# ⏰ Total work time:  12h 45m
# ✅ Sessions completed: 38
# 📈 Average per day:    2h 33m
# 📅 By Day:
#   Monday     2h 30m
#   Tuesday    2h 45m
#   Wednesday  3h 0m
```

### Data Management

```bash
# Reset all data (cannot be undone)
timefocus reset
```

---

## 🎯 Workflow Examples

### Classic Pomodoro Routine

```bash
# 1. Start work session
timefocus pomodoro --task "Write API endpoint"

# 2. Timer runs for 25 minutes
# ⏱️  Work time: 23:45

# 3. Break reminder
# ✅ Work session complete! Time for a break.
# Take break now? (y/n): y

# 4. Short break
# ☕ Break time: 5 minutes

# 5. Repeat 4 times, then take long break
timefocus break --long
```

### Deep Work Session

```bash
# Long focused session
timefocus work 90 --task "Architecture design"

# Review what you accomplished
timefocus stats
```

### Daily Wrap-up

```bash
# Check your productivity
timefocus stats

# 📊 Today's Productivity
# ⏰ Work time:       4h 15m
# ✅ Sessions done:   10/11
# 📈 Completion rate: 91%
```

---

## 🎨 Features in Detail

### Real-time Countdown

```
⏱️  Work time: 24:37   
```

Clean, updating countdown that shows exactly how much time remains.

### Smart Notifications

- **Terminal bell** - Audio notification (works in all terminals)
- **Visual message** - Clear completion message
- **Break prompts** - Automatic break reminders

### Session History

All sessions are saved to `~/.timefocus.json`:

```json
{
  "sessions": [
    {
      "type": "work",
      "duration": 25,
      "task": "Write docs",
      "completed": true,
      "timestamp": "2026-01-10T14:30:00"
    }
  ]
}
```

### Keyboard Control

Press `Ctrl+C` anytime to pause the timer. Your session will be recorded as incomplete, and you can review it in stats.

---

## 🔧 Configuration

### Default Pomodoro Settings

Edit `timefocus.py` to customize defaults:

```python
POMODORO_WORK = 25              # Work duration (minutes)
POMODORO_SHORT_BREAK = 5        # Short break (minutes)
POMODORO_LONG_BREAK = 15        # Long break (minutes)
POMODORO_CYCLES_BEFORE_LONG = 4 # Cycles before long break
```

### Data Location

Session data is stored in `~/.timefocus.json` (cross-platform).

---

## 🎓 The Pomodoro Technique

The Pomodoro Technique is a time management method:

1. **Choose a task** - Pick what you want to work on
2. **Set timer for 25 minutes** - Focus on the task
3. **Work until timer rings** - No distractions
4. **Take a short break (5 min)** - Relax and recharge
5. **Repeat 4 times** - Then take a longer break (15 min)

Benefits:
- ✅ Improved focus and concentration
- ✅ Reduced mental fatigue
- ✅ Better time awareness
- ✅ Increased productivity
- ✅ Less burnout

---

<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/d3f3f781-ce57-4167-858b-38cc13d5e195" />


## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

---

## 🏆 Why TimeFocus?

**Simple yet powerful:**
- No bloated GUI or web apps
- Works in any terminal
- Zero dependencies
- Cross-platform
- Fast and lightweight

**Designed for developers:**
- CLI-first interface
- Keyboard-driven workflow
- Git-friendly data storage
- Extensible Python code

**Actually helps productivity:**
- Real Pomodoro technique
- Smart break reminders
- Meaningful statistics
- Task tracking integration

---

## 📚 Resources

- [Pomodoro Technique Official Site](https://francescocirillo.com/pages/pomodoro-technique)
- [Time Management Best Practices](https://en.wikipedia.org/wiki/Time_management)

---

**Built with ❤️ for developers who value focus time**

Start your first session: `timefocus pomodoro`
