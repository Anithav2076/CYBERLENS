import subprocess


# ============================================================
# GENERIC WINDOWS COUNTER READER
# ============================================================

def get_counter(counter_path: str) -> float:
    """
    Read one Windows Performance Counter.
    """

    command = [
        "powershell",
        "-Command",
        (
            f"(Get-Counter '{counter_path}')"
            f".CounterSamples[0].CookedValue"
        )
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Failed to collect counter:\n"
            f"{counter_path}\n"
            f"{result.stderr.strip()}"
        )

    return float(result.stdout.strip())


# ============================================================
# PROCESSOR
# ============================================================

PROCESSOR_COUNTERS = {

    "Processor_DPC_Rate":
        r"\Processor(_Total)\DPC Rate",

    "Processor_pct_ Idle_Time":
        r"\Processor(_Total)\% Idle Time",

    "Processor_pct_ C3_Time":
        r"\Processor(_Total)\% C3 Time",

    "Processor_pct_ Interrupt_Time":
        r"\Processor(_Total)\% Interrupt Time",

    "Processor_pct_ C2_Time":
        r"\Processor(_Total)\% C2 Time",

    "Processor_pct_ User_Time":
        r"\Processor(_Total)\% User Time",

    "Processor_pct_ C1_Time":
        r"\Processor(_Total)\% C1 Time",

    "Processor_pct_ Processor_Time":
        r"\Processor(_Total)\% Processor Time",

    "Processor_C1_ransitions_sec":
        r"\Processor(_Total)\C1 Transitions/sec",

    "Processor_pct_ DPC_Time":
        r"\Processor(_Total)\% DPC Time",

    "Processor_C2_ransitions_sec":
        r"\Processor(_Total)\C2 Transitions/sec",

    "Processor_pct_ Privileged_Time":
        r"\Processor(_Total)\% Privileged Time",

    "Processor_C3_ransitions_sec":
        r"\Processor(_Total)\C3 Transitions/sec",

    "Processor_DPCs_Queued_sec":
        r"\Processor(_Total)\DPCs Queued/sec",

    "Processor_Interrupts_sec":
        r"\Processor(_Total)\Interrupts/sec",
}


# ============================================================
# PROCESS
# ============================================================

PROCESS_COUNTERS = {

    "Process_Pool_Paged Bytes":
        r"\Process(_Total)\Pool Paged Bytes",

    "Process_IO Read_Operations_sec":
        r"\Process(_Total)\IO Read Operations/sec",

    "Process_Working_Set_ Private":
        r"\Process(_Total)\Working Set - Private",

    "Process_Working_Set_Peak":
        r"\Process(_Total)\Working Set Peak",

    "Process_IO_Write Operations_sec":
        r"\Process(_Total)\IO Write Operations/sec",

    "Process_Page_File Bytes":
        r"\Process(_Total)\Page File Bytes",

    "Process_pct_ User_Time":
        r"\Process(_Total)\% User Time",

    "Process_Virtual_Bytes Peak":
        r"\Process(_Total)\Virtual Bytes Peak",

    "Process_Page_File Bytes Peak":
        r"\Process(_Total)\Page File Bytes Peak",

    "Process_IO_Other_Bytes_sec":
        r"\Process(_Total)\IO Other Bytes/sec",

    "Process_Private_Bytes":
        r"\Process(_Total)\Private Bytes",

    "Process_IO_Write_Bytes_sec":
        r"\Process(_Total)\IO Write Bytes/sec",

    "Process_Elapsed_Time":
        r"\Process(_Total)\Elapsed Time",

    "Process_Virtual_Bytes":
        r"\Process(_Total)\Virtual Bytes",

    "Process_pct_ Processor_Time":
        r"\Process(_Total)\% Processor Time",

    "Process_Creating Process ID":
        r"\Process(_Total)\Creating Process ID",

    "Process_Pool Nonpaged Bytes":
        r"\Process(_Total)\Pool Nonpaged Bytes",

    "Process_Working Set":
        r"\Process(_Total)\Working Set",

    "Process_Page Faults_sec":
        r"\Process(_Total)\Page Faults/sec",

    "Process_ID Process":
        r"\Process(_Total)\ID Process",

    "Process_IO Other Operations_sec":
        r"\Process(_Total)\IO Other Operations/sec",

    "Process_IO Data Operations_sec":
        r"\Process(_Total)\IO Data Operations/sec",

    "Process_Thread Count":
        r"\Process(_Total)\Thread Count",

    "Process_pct_ Privileged_Time":
        r"\Process(_Total)\% Privileged Time",

    "Process_IO Data Bytes_sec":
        r"\Process(_Total)\IO Data Bytes/sec",

    "Process_IO Read Bytes_sec":
        r"\Process(_Total)\IO Read Bytes/sec",

    "Process_Priority Base":
        r"\Process(_Total)\Priority Base",

    "Process_Handle Count":
        r"\Process(_Total)\Handle Count",
}


# ============================================================
# MEMORY
# ============================================================

MEMORY_COUNTERS = {

    "Memory Pool Paged Bytes":
        r"\Memory\Pool Paged Bytes",

    "Memory Free & Zero Page List Bytes":
        r"\Memory\Free & Zero Page List Bytes",

    "Memory Cache Bytes Peak":
        r"\Memory\Cache Bytes Peak",

    "Memory System Code Resident Bytes":
        r"\Memory\System Code Resident Bytes",

    "Memory Available Bytes":
        r"\Memory\Available Bytes",

    "Memory Commit Limit":
        r"\Memory\Commit Limit",

    "Memory Transition Pages RePurposed sec":
        r"\Memory\Transition Pages RePurposed/sec",

    "Memory Pages Output sec":
        r"\Memory\Pages Output/sec",

    "Memory Page Reads sec":
        r"\Memory\Page Reads/sec",

    "Memory Demand Zero Faults sec":
        r"\Memory\Demand Zero Faults/sec",

    "Memory Available KBytes":
        r"\Memory\Available KBytes",

    "Memory Pages sec":
        r"\Memory\Pages/sec",

    "Memory Cache Bytes":
        r"\Memory\Cache Bytes",

    "Memory Pool Nonpaged Bytes":
        r"\Memory\Pool Nonpaged Bytes",

    "Memory Page Faults sec":
        r"\Memory\Page Faults/sec",

    "Memory Transition Faults sec":
        r"\Memory\Transition Faults/sec",

    "Memory System Cache Resident Bytes":
        r"\Memory\System Cache Resident Bytes",

    "Memory Long-Term Average Standby Cache Lifetime (s)":
        r"\Memory\Long-Term Average Standby Cache Lifetime (s)",

    "Memory Standby Cache Reserve Bytes":
        r"\Memory\Standby Cache Reserve Bytes",

    "Memory Page Writes sec":
        r"\Memory\Page Writes/sec",

    "Memory System Code Total Bytes":
        r"\Memory\System Code Total Bytes",

    "Memory Standby Cache Core Bytes":
        r"\Memory\Standby Cache Core Bytes",

    "Memory System Driver Resident Bytes":
        r"\Memory\System Driver Resident Bytes",

    "Memory Standby Cache Normal Priority Bytes":
        r"\Memory\Standby Cache Normal Priority Bytes",

    "Memory Pool Paged Allocs":
        r"\Memory\Pool Paged Allocs",

    "Memory Pool Nonpaged Allocs":
        r"\Memory\Pool Nonpaged Allocs",

    "Memory pct_ Committed Bytes In Use":
        r"\Memory\% Committed Bytes In Use",

    "Memory Free System Page Table Entries":
        r"\Memory\Free System Page Table Entries",

    "Memory Available MBytes":
        r"\Memory\Available MBytes",

    "Memory Modified Page List Bytes":
        r"\Memory\Modified Page List Bytes",

    "Memory Cache Faults sec":
        r"\Memory\Cache Faults/sec",

    "Memory Committed Bytes":
        r"\Memory\Committed Bytes",

    "Memory System Driver Total Bytes":
        r"\Memory\System Driver Total Bytes",

    "Memory Pages Input sec":
        r"\Memory\Pages Input/sec",

    "Memory Pool Paged Resident Bytes":
        r"\Memory\Pool Paged Resident Bytes",

    "Memory Write Copies sec":
        r"\Memory\Write Copies/sec",
}


# ============================================================
# NETWORK
# ============================================================

NETWORK_COUNTER_NAMES = {

    "Bytes Total/sec":
        "Bytes Total/sec",

    "Packets/sec":
        "Packets/sec",

    "Packets Received/sec":
        "Packets Received/sec",

    "Packets Sent/sec":
        "Packets Sent/sec",

    "Current Bandwidth":
        "Current Bandwidth",

    "Bytes Received/sec":
        "Bytes Received/sec",

    "Packets Received Unicast/sec":
        "Packets Received Unicast/sec",

    "Packets Received Non-Unicast/sec":
        "Packets Received Non-Unicast/sec",

    "Packets Received Discarded":
        "Packets Received Discarded",

    "Packets Received Errors":
        "Packets Received Errors",

    "Packets Received Unknown":
        "Packets Received Unknown",

    "Bytes Sent/sec":
        "Bytes Sent/sec",

    "Packets Sent Unicast/sec":
        "Packets Sent Unicast/sec",

    "Packets Sent Non-Unicast/sec":
        "Packets Sent Non-Unicast/sec",

    "Packets Outbound Discarded":
        "Packets Outbound Discarded",

    "Packets Outbound Errors":
        "Packets Outbound Errors",

    "Output Queue Length":
        "Output Queue Length",

    "Offloaded Connections":
        "Offloaded Connections",

    "TCP Active RSC Connections":
        "TCP Active RSC Connections",

    "TCP RSC Coalesced Packets/sec":
        "TCP RSC Coalesced Packets/sec",

    "TCP RSC Exceptions/sec":
        "TCP RSC Exceptions/sec",
}


def get_active_network_interface():

    command = [
        "powershell",
        "-Command",
        """
        $counters = Get-Counter '\\Network Interface(*)\\Bytes Total/sec'

        $sample = $counters.CounterSamples |
            Sort-Object CookedValue -Descending |
            Select-Object -First 1

        if ($sample) {
            $sample.InstanceName
        }
        """
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Could not determine active network interface."
        )

    interface_name = result.stdout.strip()

    if not interface_name:
        raise RuntimeError(
            "No active network interface found."
        )

    return interface_name


def collect_network_counters():

    interface_name = get_active_network_interface()

    network_data = {}

    for counter_name in NETWORK_COUNTER_NAMES.values():

        counter_path = (
            f"\\Network Interface"
            f"({interface_name})"
            f"\\{counter_name}"
        )

        try:

            value = get_counter(counter_path)

            network_data[counter_name] = value

        except Exception as error:

            print(
                f"Warning: Network counter failed: "
                f"{counter_name}"
            )

            print(error)

            network_data[counter_name] = None

    return interface_name, network_data


# ============================================================
# LOGICAL DISK
# ============================================================

LOGICAL_DISK_COUNTERS = {

    "LogicalDisk(_Total) Avg  Disk Bytes Write":
        r"\LogicalDisk(_Total)\Avg. Disk Bytes/Write",

    "LogicalDisk(_Total) pct_ Idle Time":
        r"\LogicalDisk(_Total)\% Idle Time",

    "LogicalDisk(_Total) Disk Reads sec":
        r"\LogicalDisk(_Total)\Disk Reads/sec",

    "LogicalDisk(_Total) pct_ Free Space":
        r"\LogicalDisk(_Total)\% Free Space",

    "LogicalDisk(_Total) Disk Read Bytes sec":
        r"\LogicalDisk(_Total)\Disk Read Bytes/sec",

    "LogicalDisk(_Total) Avg  Disk sec Read":
        r"\LogicalDisk(_Total)\Avg. Disk sec/Read",

    "LogicalDisk(_Total) Disk Writes sec":
        r"\LogicalDisk(_Total)\Disk Writes/sec",

    "LogicalDisk(_Total) Current Disk Queue Length":
        r"\LogicalDisk(_Total)\Current Disk Queue Length",

    "LogicalDisk(_Total) Split IO Sec":
        r"\LogicalDisk(_Total)\Split IO/Sec",

    "LogicalDisk(_Total) Free Megabytes":
        r"\LogicalDisk(_Total)\Free Megabytes",

    "LogicalDisk(_Total) Avg  Disk sec Write":
        r"\LogicalDisk(_Total)\Avg. Disk sec/Write",

    "LogicalDisk(_Total) Disk Bytes sec":
        r"\LogicalDisk(_Total)\Disk Bytes/sec",

    "LogicalDisk(_Total) Avg  Disk Read Queue Length":
        r"\LogicalDisk(_Total)\Avg. Disk Read Queue Length",

    "LogicalDisk(_Total) pct_ Disk Time":
        r"\LogicalDisk(_Total)\% Disk Time",

    "LogicalDisk(_Total) Avg  Disk Bytes Read":
        r"\LogicalDisk(_Total)\Avg. Disk Bytes/Read",

    "LogicalDisk(_Total) Avg  Disk Write Queue Length":
        r"\LogicalDisk(_Total)\Avg. Disk Write Queue Length",

    "LogicalDisk(_Total) Avg  Disk Queue Length":
        r"\LogicalDisk(_Total)\Avg. Disk Queue Length",

    "LogicalDisk(_Total) pct_ Disk Read Time":
        r"\LogicalDisk(_Total)\% Disk Read Time",

    "LogicalDisk(_Total) Disk Write Bytes sec":
        r"\LogicalDisk(_Total)\Disk Write Bytes/sec",

    "LogicalDisk(_Total) Disk Transfers sec":
        r"\LogicalDisk(_Total)\Disk Transfers/sec",

    "LogicalDisk(_Total) Avg  Disk Bytes Transfer":
        r"\LogicalDisk(_Total)\Avg. Disk Bytes/Transfer",

    "LogicalDisk(_Total) pct_ Disk Write Time":
        r"\LogicalDisk(_Total)\% Disk Write Time",

    "LogicalDisk(_Total) Avg  Disk sec Transfer":
        r"\LogicalDisk(_Total)\Avg. Disk sec/Transfer",
}


# ============================================================
# COLLECT A COUNTER GROUP
# ============================================================

def collect_counter_group(counter_map):

    data = {}

    for feature_name, counter_path in counter_map.items():

        try:

            data[feature_name] = get_counter(
                counter_path
            )

        except Exception as error:

            print(
                f"Warning: Could not collect "
                f"{feature_name}"
            )

            print(error)

            data[feature_name] = None

    return data


# ============================================================
# COMPLETE TON_IoT TELEMETRY
# ============================================================

def collect_toniot_features():

    print("Collecting Processor counters...")

    processor_data = collect_counter_group(
        PROCESSOR_COUNTERS
    )

    print("Collecting Process counters...")

    process_data = collect_counter_group(
        PROCESS_COUNTERS
    )

    print("Collecting Memory counters...")

    memory_data = collect_counter_group(
        MEMORY_COUNTERS
    )

    print("Collecting Network counters...")

    interface_name, network_raw = (
        collect_network_counters()
    )

    print(
        f"Active network interface: "
        f"{interface_name}"
    )

    print("Collecting LogicalDisk counters...")

    disk_data = collect_counter_group(
        LOGICAL_DISK_COUNTERS
    )

    # --------------------------------------------------------
    # Convert network counters to TON_IoT feature names
    # --------------------------------------------------------

    network_data = {}

    # This is ONLY the feature-name schema used by the
    # trained TON_IoT model.
    #
    # The actual measurements still come from the
    # active Realtek/Windows network interface.
    TONIOT_NETWORK_PREFIX = (
        "Network_I(Intel R _82574L_GNC)"
    )

    network_mapping = {

        "Bytes Total/sec":
            "Bytes Total sec",

        "Packets/sec":
            "Packets sec",

        "Packets Received/sec":
            "Packets Received sec",

        "Packets Sent/sec":
            "Packets Sent sec",

        "Current Bandwidth":
            "Current Bandwidth",

        "Bytes Received/sec":
            "Bytes Received sec",

        "Packets Received Unicast/sec":
            "Packets Received Unicast sec",

        "Packets Received Non-Unicast/sec":
            "Packets Received Non-Unicast sec",

        "Packets Received Discarded":
            "Packets Received Discarded",

        "Packets Received Errors":
            "Packets Received Errors",

        "Packets Received Unknown":
            "Packets Received Unknown",

        "Bytes Sent/sec":
            "Bytes Sent sec",

        "Packets Sent Unicast/sec":
            "Packets Sent Unicast sec",

        "Packets Sent Non-Unicast/sec":
            "Packets Sent Non-Unicast sec",

        "Packets Outbound Discarded":
            "Packets Outbound Discarded",

        "Packets Outbound Errors":
            "Packets Outbound Errors",

        "Output Queue Length":
            "Output Queue Length",

        "Offloaded Connections":
            "Offloaded Connections",

        "TCP Active RSC Connections":
            "TCP Active RSC Connections",

        "TCP RSC Coalesced Packets/sec":
            "TCP RSC Coalesced Packets sec",

        "TCP RSC Exceptions/sec":
            "TCP RSC Exceptions sec",
    }

    for raw_name, ton_iot_name in network_mapping.items():

        # The TON_IoT network feature names contain a
        # space after the adapter name.
        feature_name = (
            f"{TONIOT_NETWORK_PREFIX} "
            f"{ton_iot_name}"
        )

        network_data[feature_name] = (
            network_raw.get(raw_name)
        )

    # --------------------------------------------------------
    # Missing TCP_APS
    # --------------------------------------------------------
    #
    # The current Windows network adapter does not expose
    # the exact TCP_APS counter used in the TON_IoT dataset.
    #
    # Keep the expected model feature name and use None.
    # The ML preprocessing/imputer can handle the missing
    # value.

    network_data[
        "Network_I(Intel R _82574L_GNC)TCP_APS"
    ] = None

    # --------------------------------------------------------
    # Combine everything
    # --------------------------------------------------------

    observation = {}

    observation.update(processor_data)

    observation.update(process_data)

    observation.update(memory_data)

    observation.update(network_data)

    observation.update(disk_data)

    return observation


# ============================================================
# MAIN TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("========================================")
    print(" TON_IoT WINDOWS FEATURE COLLECTOR")
    print("========================================")
    print()

    observation = collect_toniot_features()

    print()
    print("========================================")
    print(" COLLECTION SUMMARY")
    print("========================================")

    print(
        f"Total features collected: "
        f"{len(observation)}"
    )

    missing = [
        feature
        for feature, value in observation.items()
        if value is None
    ]

    print(
        f"Missing features: "
        f"{len(missing)}"
    )

    if missing:

        print()
        print("Missing:")

        for feature in missing:

            print(
                f"  - {feature}"
            )

    print()
    print("========================================")