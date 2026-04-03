from datetime import datetime

execution_log: list[str] = []

def step_callback(step_output):
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_entry = f"[{timestamp}] Step: {str(step_output)[:150]}"
    execution_log.append(log_entry)
    print(log_entry)

def task_callback(task_output):
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_entry = f"[{timestamp}] Task completed: {task_output.description[:80]}... | Output: {str(task_output.raw)[:100]}..."
    execution_log.append(log_entry)
    print(log_entry)

def get_execution_log() -> list[str]:
    return list(execution_log)

def clear_execution_log():
    execution_log.clear()
