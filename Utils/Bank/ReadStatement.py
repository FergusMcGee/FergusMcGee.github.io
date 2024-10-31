from multiprocessing import Value
import fitz
from pathlib import Path
import pandas as pd 
import re

def get_type(text):
    match text.upper():
        case text if  "DELIVEROO" in text:
            return "Take-away"
        case text if "SWEENEYS" in text:
            return "Booze"
        case text if "THE KINGS" in text:
            return "Booze"
        case text if "CONNOLLYS T" in text:
            return "Booze"
        case text if "GAFFNEY AND" in text:
            return "Booze"
        case text if "1884 BAR" in text:
            return "Booze"        
        case text if "PHYSIO" in text:
            return "Medical"
        case text if "SPORTS SURG" in text:
            return "Medical"
        case text if "TESCO" in text:
            return "Shopping"
        case text if "C+T SUPERMA" in text:
            return "Shopping"
        case _:
            return "Unknown"
        

def get_output_file_name(file: Path) -> Path:
    file_count = 1
    candidate = file
    
    while candidate.exists():
        candidate = file.with_stem(f"{file.stem}_{file_count}")
        file_count += 1
        
    return candidate

def is_date(string):
    # Regex pattern for "DD Mon YYYY" format
    pattern = r"^\d{2} [A-Za-z]{3} \d{4}$"
    return bool(re.match(pattern, string))
def parse_pdf_to_dataframe(pdf_path):
    data = []
    is_parsing = False
    with fitz.open(pdf_path) as pdf_document:
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            blocks = page.get_text("blocks")
            
            for block in blocks:
                line = block[4].strip()
                if "Transaction details" in line:
                    is_parsing = True
                    continue
                if "SUBTOTAL" in line:
                    is_parsing = False
                if is_parsing :
                    if line:
                        # Split on '\n' to separate description and value
                        parts = line.split('\n')
                        off_set = 0
                        if len(parts) > 1:
                            if is_date(parts[0]):
                                off_set = 1
                            description = parts[0 + off_set]
                            value = parts[1 + off_set]
                            type = get_type(description)
                        if 'OD' in value:
                            value = 0
                        try:
                            # Ensure value is a float, then format it to two decimal places
                            data.append({"Desc": description,"Type":type, "Value": f"{float(value):.2f}"})
                        except ValueError:
                            data.append({"Desc": description, "Value": ""})




    # Create DataFrame
    df = pd.DataFrame(data)
    return df
statement_path = Path.home()
statement_path = statement_path.joinpath(r"OneDrive - Autoaddress\Documents\Bank")
statement_file = statement_path.joinpath("downloadStatement (2).pdf")
df = parse_pdf_to_dataframe(statement_file)
print(df.head())
csv_file = statement_path.joinpath("downloadStatement.csv")
csv_file = get_output_file_name(csv_file)
    
df.to_csv(csv_file, index=False)
print ("Fin!")

