import sys
import pandas as pd

csv_file = sys.argv[1]

if len(sys.argv) > 2:
    out_file = sys.argv[2]
else:
    out_file = 'output.dta'

if csv_file.split('.')[1] == 'csv':
    df = pd.read_csv(csv_file)
    df.to_stata(out_file)
else:
    print('MUST BE CSV FILE')
    sys.exit()