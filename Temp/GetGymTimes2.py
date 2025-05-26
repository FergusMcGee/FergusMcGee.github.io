import pandas as pd
from pathlib import Path

file_name = r"C:\Users\Fergu\source\FergusMcGee.github.io\Temp\Timetable.csv"

file_path = Path(file_name)

df = pd.read_csv(file_path, sep='|')

print(df.head())
