import subprocess
from concurrent.futures import ThreadPoolExecutor

def execute_module(command: str):
    """Triggers shell command pipelines concurrently across sub-process allocation contexts."""
    subprocess.run(command, shell=True, check=True)

if __name__ == "__main__":
    # Segregates module splits to map features concurrently down across thread workers
    execution_tasks = [
        "pytest tests/test_ui/ -vs --alluredir=allure-results",
        "pytest tests/test_api/ -vs --alluredir=allure-results",
        "pytest tests/test_hybrid/ -vs --alluredir=allure-results"
    ]

    print("Launching programmatic concurrency pools across target modules...")
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(execute_module, execution_tasks)
