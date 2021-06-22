import json
from collections import defaultdict

file_map = {}
current_file = 0
files = []
transaction_map = {}
transactions = []

with open('./timestamp_log.json') as f:
    log = json.load(f)["log"]

    rts = [0] * len(log)
    wts = [0] * len(log)

    print("Timestamp Based Protocol Implementation: ")
    print("Op\t|\tFile\t|\tOutput")
    for data in log:
        if not data["file"] in files:
            file_map[data["file"]] = current_file
            current_file += 1
            files.append(data["file"])

        if not data["transaction"] in transactions:
            transaction_map[data["transaction"]] = data["timestamp"]
            transactions.append(data["transaction"])

        mapped_file_num = file_map[data["file"]]

        if data["operation"] == "read":
            if wts[mapped_file_num] > data["timestamp"]:
                transaction_num = list(transaction_map.keys())[list(
                    transaction_map.values()).index(wts[mapped_file_num])]

                print(
                    "Read\t|\t", data["file"], "\t|\tRollback and execute after Transaction", transaction_num)

            elif data["timestamp"] > rts[mapped_file_num]:
                rts[mapped_file_num] = data["timestamp"]

                print("Read\t|\t", data["file"], "\t|\tExecute operation")

        elif data["operation"] == "write":
            if rts[mapped_file_num] > data["timestamp"]:
                transaction_num = list(transaction_map.keys())[list(
                    transaction_map.values()).index(wts[mapped_file_num])]

                print(
                    "Write\t|\t", data["file"], "\t|\tRollback and execute after Transaction", transaction_num)

            elif wts[mapped_file_num] > data["timestamp"]:
                print(
                    "Write\t|\t", data["file"], "\t|\tReject and rollback (Obsolete write)")

            else:
                wts[mapped_file_num] = data["timestamp"]

                print(
                    "Write\t|\t", data["file"], "\t|\tExecute Operation")

        elif data["operation"] == "display":
            print("Display\t|\t", data["file"], "\t|\tExecute operation")

        else:
            print("Invalid operation type")
