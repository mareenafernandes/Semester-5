import json
from collections import defaultdict

dirty_rec = defaultdict(lambda: 0)
trans_rec = defaultdict(lambda: 0)
page_rec = defaultdict(lambda: 0)

committed = []

undo_lsn = []
first_redo = float("inf")
last_undo = 0

with open('./aries.json') as f:
    log = json.load(f)["log"]

    print("Log: ")
    for data in log:
        print(data)
        if data["operation"] == "read" or data["operation"] == "write":
            trans_rec[data["transaction"]] = data["lsn"]
            if dirty_rec[data["page"]] == 0:
                dirty_rec[data["page"]] = data["lsn"]

        elif data["operation"] == "commit":
            if not data["transaction"] in committed:
                committed.append(data["transaction"])

        elif data["operation"] == "flush":
            dirty_rec[data["page"]] = 0
            page_rec[data["page"]] = data["lsn"]

        elif data["operation"] == "crash":
            break

        elif data["operation"] == "end":
            continue

        else:
            print("Invalid log file. Illegal operation type")
            break

    print("\nTransaction Table: ")
    print("TID\t|\tLSN\t|\tStatus")
    for key, val in trans_rec.items():
        print(key, "\t|\t", val, end="\t|\t")
        if key in committed:
            print("Committed")
        else:
            if val > last_undo:
                last_undo = val
            print("Running")

    print("\nDirty Page Table: ")
    print("PageID\t|\tRecLSN")
    for key, val in dirty_rec.items():
        if val != 0:
            print(key, "\t|\t", val)
            if val < first_redo:
                first_redo = val

    print("\nRedo starts at LSN", first_redo)

    for i in range(first_redo - 1, len(log)):
        data = log[i]
        if data["operation"] == "read" or data["operation"] == "write":
            if dirty_rec[data["page"]] > 0 and dirty_rec[data["page"]] <= data["lsn"] and page_rec[data["page"]] < data["lsn"]:
                print("LSN", data["lsn"], ": Redo")
            else:
                print("LSN", data["lsn"], ": No Redo")
        elif data["operation"] == "crash":
            continue
        else:
            print("LSN", data["lsn"], ": Skip")

    print("\nUndo starts up from LSN", last_undo,
          "for all Transaction IDs not in", committed)

    for i in range(last_undo - 1, -1, -1):
        data = log[i]
        if data["operation"] == "read" or data["operation"] == "write":
            if not data["transaction"] in committed:
                undo_lsn.append(data["lsn"])

    print("Undo LSN List: ", undo_lsn)

