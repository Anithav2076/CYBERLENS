import subprocess


def get_counter(counter_path):

    command = [
        "powershell",
        "-Command",
        f"(Get-Counter '{counter_path}').CounterSamples[0].CookedValue"
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            result.stderr.strip()
        )

    return float(
        result.stdout.strip()
    )


if __name__ == "__main__":

    print()
    print("========================================")
    print(" WINDOWS PERFORMANCE COUNTER TEST")
    print("========================================")
    print()

    counters = {

        "cpu":
            r"\Processor(_Total)\% Processor Time",

        "memory":
            r"\Memory\% Committed Bytes In Use",

        "disk":
            r"\LogicalDisk(_Total)\% Idle Time",

        "threads":
            r"\Process(_Total)\Thread Count"
    }

    for name, path in counters.items():

        value = get_counter(path)

        print(
            f"{name}: {value}"
        )

    print()
    print("========================================")
    print(" Counter collection successful")
    print("========================================")