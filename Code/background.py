import psutil
import time
import os
import logging

# Set up logging
log_file = "resource_monitor.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(message)s")

# Monitor the process (replace this with your process ID, or use this in conjunction with a process list)
def monitor_process(process_pid):
    try:
        process = psutil.Process(process_pid)
        
        while process.is_running():
            # Get current memory and CPU usage
            memory_info = process.memory_info()
            cpu_percent = process.cpu_percent(interval=1)
            
            # Log resource usage every 2 seconds
            logging.info(f"Memory Usage (RSS): {memory_info.rss / 1024 / 1024:.2f} MB, "
                         f"CPU Usage: {cpu_percent}%, "
                         f"Virtual Memory: {memory_info.vms / 1024 / 1024:.2f} MB")
            
            # Check if memory usage is growing exponentially (sign of memory leak)
            if memory_info.rss > 64 * 1024 * 1024 * 1024:  # If using > 64 GB RAM
                logging.warning("Memory usage is very high (>64 GB). Potential memory leak detected!")

            # Check if the process is using too much CPU
            if cpu_percent > 90:
                logging.warning(f"High CPU usage: {cpu_percent}%")

            # Sleep for 2 seconds before checking again
            time.sleep(20)
    
    except psutil.NoSuchProcess:
        logging.error(f"Process with PID {process_pid} does not exist anymore.")
    except psutil.AccessDenied:
        logging.error(f"Access to the process with PID {process_pid} was denied.")
    except Exception as e:
        logging.error(f"An error occurred while monitoring the process: {e}")


# Function to find the process ID (PID) of your running script
def get_current_pid():
    return os.getpid()


if __name__ == "__main__":
    pid = get_current_pid()
    logging.info(f"Starting resource monitoring for process PID: {pid}")
    
    # Start monitoring the process in the background
    monitor_process(pid)
