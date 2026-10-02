import psutil
import socket
from datetime import datetime, timezone


# ============================================================
# SYSTEM INFORMATION
# ============================================================

def collect_system_info():

    return {
        "hostname": socket.gethostname(),

        "operating_system": "Windows",

        "cpu_count": psutil.cpu_count(),

        "memory_total": psutil.virtual_memory().total,

        "memory_available": psutil.virtual_memory().available,

        "timestamp": datetime.now(
            timezone.utc
        ).isoformat()
    }


# ============================================================
# CPU INFORMATION
# ============================================================

def collect_cpu_info():

    cpu = psutil.cpu_times_percent(
        interval=1
    )

    return {
        "cpu_user_percent":
            cpu.user,

        "cpu_system_percent":
            cpu.system,

        "cpu_idle_percent":
            cpu.idle
    }


# ============================================================
# MEMORY INFORMATION
# ============================================================

def collect_memory_info():

    memory = psutil.virtual_memory()

    return {
        "memory_total":
            memory.total,

        "memory_available":
            memory.available,

        "memory_used":
            memory.used,

        "memory_percent":
            memory.percent
    }


# ============================================================
# DISK INFORMATION
# ============================================================

def collect_disk_info():

    disk = psutil.disk_usage("C:\\")

    return {
        "disk_total":
            disk.total,

        "disk_used":
            disk.used,

        "disk_free":
            disk.free,

        "disk_percent":
            disk.percent
    }


# ============================================================
# NETWORK INFORMATION
# ============================================================

def collect_network_info():

    network = psutil.net_io_counters()

    return {
        "bytes_sent":
            network.bytes_sent,

        "bytes_received":
            network.bytes_recv,

        "packets_sent":
            network.packets_sent,

        "packets_received":
            network.packets_recv,

        "errors_in":
            network.errin,

        "errors_out":
            network.errout,

        "drops_in":
            network.dropin,

        "drops_out":
            network.dropout
    }


# ============================================================
# PROCESS INFORMATION
# ============================================================

def collect_process_info():

    process_count = 0

    total_threads = 0

    total_handles = 0

    total_memory = 0

    for process in psutil.process_iter(
        [
            "pid",
            "num_threads",
            "memory_info"
        ]
    ):

        try:

            process_count += 1

            info = process.info

            total_threads += (
                info["num_threads"] or 0
            )

            memory_info = info[
                "memory_info"
            ]

            if memory_info:

                total_memory += (
                    memory_info.rss
                )

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied
        ):

            continue

    return {

        "process_count":
            process_count,

        "total_threads":
            total_threads,

        "total_memory":
            total_memory
    }


# ============================================================
# COMPLETE TELEMETRY COLLECTION
# ============================================================

def collect_telemetry():

    telemetry = {

        "system":
            collect_system_info(),

        "cpu":
            collect_cpu_info(),

        "memory":
            collect_memory_info(),

        "disk":
            collect_disk_info(),

        "network":
            collect_network_info(),

        "process":
            collect_process_info()
    }

    return telemetry


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print()
    print("========================================")
    print(" AI CYBER SECURITY ENDPOINT AGENT")
    print("========================================")
    print()

    telemetry = collect_telemetry()

    print("SYSTEM")
    print("----------------------------------------")

    for key, value in telemetry["system"].items():

        print(f"{key}: {value}")

    print()

    print("CPU")
    print("----------------------------------------")

    for key, value in telemetry["cpu"].items():

        print(f"{key}: {value}")

    print()

    print("MEMORY")
    print("----------------------------------------")

    for key, value in telemetry["memory"].items():

        print(f"{key}: {value}")

    print()

    print("DISK")
    print("----------------------------------------")

    for key, value in telemetry["disk"].items():

        print(f"{key}: {value}")

    print()

    print("NETWORK")
    print("----------------------------------------")

    for key, value in telemetry["network"].items():

        print(f"{key}: {value}")

    print()

    print("PROCESS")
    print("----------------------------------------")

    for key, value in telemetry["process"].items():

        print(f"{key}: {value}")

    print()

    print("========================================")
    print(" Collection completed successfully")
    print("========================================")