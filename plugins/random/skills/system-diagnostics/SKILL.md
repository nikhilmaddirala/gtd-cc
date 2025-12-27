---
name: system-diagnostics
description: Interactive system resource analysis and troubleshooting for memory, disk, CPU, and performance issues
version: 1.0.0
author: gtd-cc

# Skill metadata
domain: system-administration
category: diagnostics
tags: [system-resources, troubleshooting, performance, monitoring, linux, macos]

# Skill classification
type: domain-expertise
complexity: intermediate
scope: comprehensive

# Usage information
prerequisites:
  - "Unix-like operating system (Linux or macOS)"
  - "Basic familiarity with command line"
  - "System administrator or developer access"

provides:
  - "Cross-platform system diagnostics"
  - "Resource usage analysis"
  - "Performance troubleshooting workflows"
  - "Interactive problem-solving guidance"

# Integration notes
compatible_tools:
  - vmstat
  - top
  - htop
  - du
  - df
  - free
  - iostat
  - ps

# Learning objectives
objectives:
  - "Diagnose memory, disk, and CPU issues"
  - "Understand system resource patterns"
  - "Apply platform-specific troubleshooting"
  - "Identify and resolve resource bottlenecks"
---

# System Diagnostics and Resource Analysis Skill

An interactive skill for analyzing system resources and diagnosing performance issues across Linux and macOS platforms. This skill detects your operating system and guides you through appropriate diagnostic commands to identify and resolve memory, disk, CPU, and other resource problems.

## Quick Start

### 1. Detect Your System
```bash
# Identify your operating system
uname -s
# Output: Linux or Darwin (macOS)
```

### 2. Quick System Overview
```bash
# Linux
vmstat 1 5          # 5 seconds of VM statistics
free -h             # Memory usage (human-readable)
df -h               # Disk usage

# macOS
vm_stat             # Virtual memory statistics
df -h               # Disk usage
top -l 1 -n 10      # Top 10 processes snapshot
```

### 3. Identify Resource Pressure
```bash
# Check what's consuming resources
top -o %MEM -n 10   # Top memory consumers
top -o %CPU -n 10   # Top CPU consumers
du -sh /*           # Disk usage by directory
```

## What This Skill Covers

- **OS Detection**: Automatically identify Linux vs macOS for appropriate commands
- **Memory Analysis**: Diagnose memory leaks, high usage, and swap issues
- **Disk Analysis**: Find large files, identify disk hogs, analyze space usage
- **CPU Analysis**: Identify runaway processes and CPU bottlenecks
- **Interactive Troubleshooting**: Step-by-step guidance based on your specific issue

## Core Concepts

### System Resource Types

**Memory (RAM)**
- Physical RAM vs swap space
- Cache vs used vs available memory
- Memory leaks and gradual consumption
- OOM (Out of Memory) conditions

**Disk Space**
- Filesystem usage and inodes
- Large files and directories
- Log file accumulation
- Temporary file cleanup

**CPU**
- User vs system CPU time
- Load averages (1min, 5min, 15min)
- Process priorities and nice values
- CPU-bound vs I/O-bound processes

**I/O (Input/Output)**
- Disk read/write patterns
- I/O wait time
- Network I/O
- Filesystem performance

### Platform Differences

**Linux Commands**
- `free`: Memory usage (not available on macOS)
- `vmstat`: Virtual memory statistics
- `iostat`: I/O statistics
- `/proc` filesystem for detailed info

**macOS Commands**
- `vm_stat`: Virtual memory statistics
- `fs_usage`: Filesystem activity
- Activity Monitor (GUI)
- Different `top` flags and output format

## OS Detection Workflow

### Automatic Platform Detection

```bash
# Detect operating system
OS=$(uname -s)

if [[ "$OS" == "Linux" ]]; then
    echo "Running on Linux"
    # Use Linux-specific commands
elif [[ "$OS" == "Darwin" ]]; then
    echo "Running on macOS"
    # Use macOS-specific commands
else
    echo "Unsupported OS: $OS"
fi
```

### Platform-Specific Command Selection

```bash
# Memory check - cross-platform
if [[ "$OS" == "Linux" ]]; then
    free -h
    cat /proc/meminfo
elif [[ "$OS" == "Darwin" ]]; then
    vm_stat
    top -l 1 | head -n 10
fi

# Disk usage - works on both
df -h

# Process listing - platform-aware flags
if [[ "$OS" == "Linux" ]]; then
    ps aux --sort=-%mem | head -n 11
elif [[ "$OS" == "Darwin" ]]; then
    ps aux -m | head -n 11
fi
```

## Memory Diagnostics

### Linux Memory Analysis

```bash
# Overall memory status
free -h

# Detailed memory info
cat /proc/meminfo

# Memory usage by process
ps aux --sort=-%mem | head -n 20

# Swap usage
swapon --show
cat /proc/swaps

# Monitor memory in real-time
vmstat 1 10

# Check for OOM killer activity
dmesg | grep -i "out of memory"
journalctl -k | grep -i "killed process"
```

### macOS Memory Analysis

```bash
# Virtual memory statistics
vm_stat

# Memory pressure
memory_pressure

# Top memory consumers
top -o MEM -n 20 -l 1

# Detailed process memory
ps aux -m | head -n 20

# Check swap usage
sysctl vm.swapusage
```

### Memory Problem Patterns

**High Memory Usage**
```bash
# Find memory hogs
if [[ "$OS" == "Linux" ]]; then
    ps aux --sort=-%mem | head -n 11
    # Check for memory leaks
    pmap -x $(pidof process_name)
elif [[ "$OS" == "Darwin" ]]; then
    top -o MEM -n 10 -l 1
    # Check specific process
    vmmap PID
fi
```

**Swap Thrashing**
```bash
# Linux: Monitor swap activity
vmstat 1 5
# High 'si' (swap in) and 'so' (swap out) indicates thrashing

# macOS: Check swap usage
sysctl vm.swapusage
# High swap usage with low free memory indicates pressure
```

**Memory Leaks**
```bash
# Monitor process memory over time
while true; do
    ps aux | grep process_name | awk '{print $6}'
    sleep 60
done

# Linux: Detailed process memory mapping
pmap -x PID

# macOS: Virtual memory map
vmmap PID
```

## Disk Diagnostics

### Cross-Platform Disk Analysis

```bash
# Filesystem usage
df -h

# Check inode usage (can fill up even with space available)
df -i

# Find large directories
du -sh /* 2>/dev/null | sort -hr | head -n 20

# Find large files
find / -type f -size +100M 2>/dev/null | xargs ls -lh | sort -k5 -hr

# Disk usage by directory depth
du -h --max-depth=1 / 2>/dev/null | sort -hr
```

### Linux Disk Diagnostics

```bash
# I/O statistics
iostat -x 1 5

# Disk activity by process
iotop -o

# Check for full filesystems
df -h | grep -E '^/dev/' | awk '$5+0 > 90'

# Find recently modified large files
find /var/log -type f -size +50M -mtime -7 -exec ls -lh {} \;

# Check disk health (if smartmontools installed)
smartctl -a /dev/sda
```

### macOS Disk Diagnostics

```bash
# Filesystem usage
df -h

# Find large files
find / -type f -size +100M 2>/dev/null -exec ls -lh {} \;

# Directory sizes
du -sh /* 2>/dev/null | sort -hr

# Disk activity
fs_usage -f filesys

# Check APFS snapshots (can consume space)
tmutil listlocalsnapshots /
```

### Common Disk Problems

**Full Filesystem**
```bash
# Find what's consuming space
du -sh /* 2>/dev/null | sort -hr | head -n 20

# Check log files
du -sh /var/log/*

# Find old log files
find /var/log -type f -name "*.log" -mtime +30

# Check temporary directories
du -sh /tmp /var/tmp
```

**Large Files**
```bash
# Find files over 1GB
find / -type f -size +1G 2>/dev/null -exec ls -lh {} \;

# Find in specific directory
find /home -type f -size +500M 2>/dev/null -exec ls -lh {} \;

# Group by directory
find / -type f -size +100M 2>/dev/null | sed 's|/[^/]*$||' | sort | uniq -c | sort -rn
```

**Inode Exhaustion**
```bash
# Check inode usage
df -i

# Find directories with many files
find / -xdev -type d -exec bash -c 'echo "$(ls -a "$1" | wc -l) $1"' _ {} \; 2>/dev/null | sort -rn | head -n 20

# Count files in directory
find /var -type f | wc -l
```

## CPU Diagnostics

### Real-Time CPU Monitoring

```bash
# Linux: Interactive top
top
# Press 'P' to sort by CPU, 'M' for memory, '1' to show all cores

# macOS: Interactive top
top -o cpu
# Press 'o' to change sort order

# Both: Batch mode for scripting
if [[ "$OS" == "Linux" ]]; then
    top -b -n 1 | head -n 20
elif [[ "$OS" == "Darwin" ]]; then
    top -l 1 -n 20
fi
```

### Linux CPU Analysis

```bash
# CPU usage summary
vmstat 1 5

# Load averages
uptime

# Per-core CPU usage
mpstat -P ALL 1 5

# CPU hogs
ps aux --sort=-%cpu | head -n 20

# CPU time by process
ps -eo pid,ppid,cmd,%cpu,%mem --sort=-%cpu | head -n 20

# Check CPU frequency/throttling
cat /proc/cpuinfo | grep MHz
```

### macOS CPU Analysis

```bash
# Load averages
uptime

# CPU usage by process
top -o cpu -n 20 -l 1

# Detailed process info
ps aux | sort -k3 -r | head -n 20

# CPU time accumulation
ps -eo pid,ppid,command,%cpu,%mem | sort -k4 -r | head -n 20
```

### CPU Problem Patterns

**High Load Average**
```bash
# Check load average (1min, 5min, 15min)
uptime
# Rule of thumb: load > number of CPU cores indicates saturation

# Find number of CPUs
if [[ "$OS" == "Linux" ]]; then
    nproc
    lscpu
elif [[ "$OS" == "Darwin" ]]; then
    sysctl -n hw.ncpu
fi

# Identify CPU-bound processes
ps aux --sort=-%cpu | head -n 11
```

**Runaway Process**
```bash
# Find processes using > 50% CPU
ps aux | awk '$3 > 50.0 {print $0}'

# Monitor specific process
top -p PID  # Linux
top -pid PID  # macOS

# Check process tree
pstree -p PID  # Linux
ps -ef | grep -A 5 -B 5 PID  # macOS

# Kill runaway process (use with caution)
kill -TERM PID
# If not responding
kill -KILL PID
```

**I/O Wait**
```bash
# Linux: Check for high I/O wait
iostat -x 1 5
# High %iowait indicates disk bottleneck

vmstat 1 5
# 'wa' column shows I/O wait percentage

# Find processes causing I/O
iotop -o  # Requires iotop installed

# macOS: Monitor I/O
fs_usage -w
```

## Interactive Troubleshooting Workflows

### Memory Problem Workflow

**Step 1: Assess Memory State**
```bash
# What's the current memory situation?
if [[ "$OS" == "Linux" ]]; then
    echo "=== Memory Overview ==="
    free -h
    echo ""
    echo "=== Swap Usage ==="
    swapon --show
elif [[ "$OS" == "Darwin" ]]; then
    echo "=== Memory Statistics ==="
    vm_stat
    echo ""
    echo "=== Swap Usage ==="
    sysctl vm.swapusage
fi
```

**Step 2: Identify Memory Consumers**
```bash
# Who's using the memory?
echo "=== Top Memory Consumers ==="
if [[ "$OS" == "Linux" ]]; then
    ps aux --sort=-%mem | head -n 11
elif [[ "$OS" == "Darwin" ]]; then
    ps aux -m | head -n 11
fi
```

**Step 3: Investigate Suspicious Processes**
```bash
# Get details on high-memory process
PID=<identified_pid>

if [[ "$OS" == "Linux" ]]; then
    echo "=== Process Details ==="
    ps -p $PID -o pid,ppid,user,%cpu,%mem,vsz,rss,tty,stat,start,time,command
    echo ""
    echo "=== Memory Map ==="
    pmap -x $PID | tail -n 1
elif [[ "$OS" == "Darwin" ]]; then
    echo "=== Process Details ==="
    ps -p $PID -o pid,ppid,user,%cpu,%mem,vsz,rss,tty,stat,start,time,command
    echo ""
    echo "=== Virtual Memory Map ==="
    vmmap $PID | grep -A 5 "Physical footprint"
fi
```

**Step 4: Take Action**
- Normal high usage → Monitor or upgrade RAM
- Memory leak → Restart service or investigate code
- Cache bloat → May clear automatically, or clear caches
- Swap thrashing → Kill processes or add RAM

### Disk Problem Workflow

**Step 1: Check Overall Disk Usage**
```bash
echo "=== Filesystem Usage ==="
df -h

echo ""
echo "=== Filesystems > 80% Full ==="
df -h | awk '$5+0 > 80'
```

**Step 2: Find Large Directories**
```bash
echo "=== Top 20 Largest Directories ==="
du -sh /* 2>/dev/null | sort -hr | head -n 20
```

**Step 3: Drill Down into Problem Areas**
```bash
# Replace /var with your problem directory
PROBLEM_DIR="/var"

echo "=== Subdirectories in $PROBLEM_DIR ==="
du -sh $PROBLEM_DIR/* 2>/dev/null | sort -hr | head -n 20

echo ""
echo "=== Large Files in $PROBLEM_DIR ==="
find $PROBLEM_DIR -type f -size +100M 2>/dev/null -exec ls -lh {} \;
```

**Step 4: Take Action**
- Old logs → Compress or delete: `gzip /var/log/old.log`
- Large files → Archive or remove: `tar czf archive.tar.gz files/ && rm -rf files/`
- Full temp → Clean: `rm -rf /tmp/*` (with caution)
- Growth pattern → Set up log rotation or cleanup cron jobs

### CPU Problem Workflow

**Step 1: Check Load Average**
```bash
echo "=== System Load ==="
uptime

if [[ "$OS" == "Linux" ]]; then
    echo "Number of CPUs: $(nproc)"
elif [[ "$OS" == "Darwin" ]]; then
    echo "Number of CPUs: $(sysctl -n hw.ncpu)"
fi
```

**Step 2: Identify CPU Consumers**
```bash
echo "=== Top CPU Consumers ==="
if [[ "$OS" == "Linux" ]]; then
    ps aux --sort=-%cpu | head -n 11
elif [[ "$OS" == "Darwin" ]]; then
    ps aux | sort -k3 -r | head -n 11
fi
```

**Step 3: Analyze Specific Process**
```bash
PID=<identified_pid>

echo "=== Process Details ==="
ps -p $PID -o pid,ppid,user,%cpu,%mem,time,command

echo ""
echo "=== Process Threads (if supported) ==="
if [[ "$OS" == "Linux" ]]; then
    ps -T -p $PID
fi
```

**Step 4: Take Action**
- Expected high CPU → Monitor or optimize code
- Runaway process → Kill: `kill -TERM $PID`
- High I/O wait → Check disk performance
- Too many processes → Increase resources or optimize

## Advanced Diagnostic Commands

### Process Investigation

```bash
# Full process tree
pstree -p  # Linux
ps -ef | less  # macOS

# Process open files
lsof -p PID

# Process network connections
lsof -i -n -P | grep PID
netstat -anp | grep PID  # Linux
lsof -iTCP -sTCP:ESTABLISHED -n -P | grep PID  # macOS

# Process system calls
strace -p PID  # Linux
dtruss -p PID  # macOS (requires sudo)
```

### System-Wide Monitoring

```bash
# All-in-one system view
if [[ "$OS" == "Linux" ]]; then
    # Install htop for better experience
    htop

    # Or use vmstat for overview
    vmstat 1 5
elif [[ "$OS" == "Darwin" ]]; then
    # Use top with good defaults
    top -o cpu -O +rsize -s 1 -n 20
fi

# Network connections
netstat -tulpn  # Linux
lsof -i -n -P  # macOS

# Logged in users
who
w
```

### Historical Analysis

```bash
# Linux: System logs
journalctl -xe
journalctl --since "1 hour ago"
dmesg | tail -n 50

# Check for OOM kills
dmesg | grep -i "out of memory"

# macOS: System logs
log show --predicate 'eventMessage contains "error"' --info --last 1h
log show --predicate 'processImagePath contains "kernel"' --last 1h
```

## Troubleshooting Cheat Sheet

### Quick Commands by Problem

**"My system is slow"**
```bash
# Check all resources at once
uptime && df -h && free -h  # Linux
uptime && df -h && vm_stat  # macOS
```

**"Out of memory"**
```bash
# Linux
free -h
ps aux --sort=-%mem | head -n 11

# macOS
vm_stat
ps aux -m | head -n 11
```

**"Out of disk space"**
```bash
df -h
du -sh /* 2>/dev/null | sort -hr | head -n 10
```

**"High CPU usage"**
```bash
uptime
top -o cpu -n 10  # Then 'q' to quit
```

**"What's using my disk I/O?"**
```bash
# Linux
iostat -x 1 5
iotop -o

# macOS
fs_usage -w
```

### Emergency Commands

```bash
# Kill all processes by name (use with extreme caution)
pkill -9 process_name

# Clear disk space quickly
# Clean package manager cache
apt clean  # Debian/Ubuntu
yum clean all  # RHEL/CentOS
brew cleanup  # macOS Homebrew

# Clear temp files
sudo rm -rf /tmp/*
sudo rm -rf /var/tmp/*

# Compress old logs
find /var/log -name "*.log" -mtime +7 -exec gzip {} \;

# Free up memory cache (Linux only, generally not needed)
sync && echo 3 | sudo tee /proc/sys/vm/drop_caches
```

## Best Practices

### Regular Monitoring

- Check disk usage weekly: `df -h`
- Monitor load average: `uptime`
- Review top consumers: `top` or `htop`
- Check system logs for errors

### Prevention

- Set up log rotation
- Configure monitoring/alerting
- Regular cleanup of temp files
- Capacity planning based on trends

### Safe Investigation

- Always use `2>/dev/null` to suppress permission errors in find commands
- Test commands in read-only mode first
- Backup before deleting large files
- Use `-i` flag for interactive confirmation: `rm -i file`

### Documentation

- Record baseline metrics when system is healthy
- Document normal resource patterns
- Keep notes on problem resolution
- Track capacity growth over time

## Platform-Specific Tips

### Linux-Specific

- Use `/proc` filesystem for detailed system info: `/proc/meminfo`, `/proc/cpuinfo`
- Check `dmesg` for kernel messages and OOM killer activity
- Use `systemctl` to manage and troubleshoot services
- Review logs with `journalctl`

### macOS-Specific

- Use Activity Monitor GUI for visual investigation
- DTrace-based tools require SIP adjustment on newer versions
- APFS snapshots can consume significant space
- Time Machine local snapshots: `tmutil listlocalsnapshots /`

This skill provides comprehensive guidance for diagnosing and resolving system resource issues across Linux and macOS platforms, with interactive workflows that adapt to your specific situation.
