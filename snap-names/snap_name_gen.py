import csv

snapshot_names = []

for i in range(0, 100):
    if (i / 10 >= 1):
    	snapshot_names.append('0'+str(i))
    else:
        snapshot_names.append('00'+str(i))
    
print(snapshot_names)

csvfile = 'output/snapshot_names.txt'

with open(csvfile, "w") as output:
	writer = csv.writer(output, lineterminator='\n')
	for val in snapshot_names:
		writer.writerow([val])
