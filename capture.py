import os
import time
import subprocess
import sys

if len(sys.argv) < 3:
    print("USAGE: capture.py INTERFACE USERNAME")
    exit(0)
INTERFACE = sys.argv[1]
USERNAME = sys.argv[2]

print(f"{INTERFACE=}")
print(f"{USERNAME=}")

LOG_DIR = f"/ctf/logs/pcaps"
DEST_DIR = f"/ctf/logs/test_pcap"
EVE_FILE = "/var/log/suricata/eve.json"


def runner():
    pcaps = os.listdir(LOG_DIR)
    if len(pcaps) < 2:
        # print("Suricata is still writing!")
        return
    pcaps.sort()
    # clean up old pcaps already copied
    already_copied = os.listdir(DEST_DIR)
    if len(already_copied) > 30:
        for pcap in already_copied[:10]:
            # don't delete eve.json
            if pcap.endswith(".pcap"):
                os.remove(os.path.join(DEST_DIR, pcap))

    # copy all pcaps except the last one (still being written)
    # print("Not copying {}".format(pcaps[-1]))
    for pcap in pcaps[:-1]:
        # log, _, timestamp = pcap.split(".")
        log, timestamp, _ = pcap.split(".")
        # print("Copying {} to {}".format(pcap, log+timestamp+".pcap"))

        os.rename(
            os.path.join(LOG_DIR, pcap),
            os.path.join(DEST_DIR, log + timestamp + ".pcap"),
        )


if __name__ == "__main__":
    # TODO: TRY ME!
    subprocess.Popen(
        [
            "sudo",
            "tcpdump",
            "-i",
            INTERFACE,
            "-w",
            f"{LOG_DIR}/log.%FT%T.pcap",
            "-G",
            "30",
            "-Z",
            "root",
        ]
    )
    if not os.path.exists(os.path.join(DEST_DIR, "eve.json")):
        os.link(os.path.join(EVE_FILE), os.path.join(DEST_DIR, "eve.json"))
    while True:
        runner()
        time.sleep(5)
