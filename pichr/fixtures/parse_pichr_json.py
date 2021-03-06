import json
import csv


if __name__ == "__main__":
  with open("data.csv") as data_f:
    reader = csv.DictReader(data_f)
    print reader.fieldnames

    players = {}
    recoveries = []
    
    for row in reader:
      player = {
        "name": row['Name'].strip(),
        "pid": int(row['PlayerId']),
        "team": row['Team'].strip()
      }
      
      players[player["pid"]] = player

      date = row["On Date"].split('/')
      if len(date[0]) == 1:
        date[0] = "0%s" % date[0]
      if len(date[1]) == 1:
        date[1] = "0%s" % date[1]
      print date
      recovery = {
        "date": "%s-%s-%s" % (date[2], date[0], date[1]),
        "duration" : row['Days'],
        "sct_injury": row['InjurySCTID'],
        "player": player["pid"],
        "preERA": float(row['preERA']),
        "postERA": float(row['postERA']),
        "preFastball": float(row['preFB']),
        "postFastball": float(row['postFB'])
      }

      if "yes" in row['reinjury'].lower():
          recovery['reinjury'] = True
      if "yes" in row["offseason"].lower():
          recovery['offseason'] = True
      if "procedure" in row:
        recovery["ProcedureSCTID"] = row["ProcedureSCTID"]
      recoveries.append(recovery)

  players = [{ "model": "pichr.Player", "fields": players[pid] } for pid in players]
  recoveries = [{ "model": "pichr.Recovery", "pk": i, "fields": rec } for i, rec in enumerate(recoveries)]
  enc = json.JSONEncoder()

  with open("instances.json", "w+") as outF:
    outF.write(json.dumps(players + recoveries, sort_keys=False,
      indent=4, separators=(',', ': ')))







