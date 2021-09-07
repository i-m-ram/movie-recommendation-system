def clean_data(row):
    if isinstance(row, list):
        return [str.lower(i.replace(" ", "")) for i in row if isinstance(i,str)]
    else:
        if isinstance(row, str):
            return str.lower(row.replace(" ", ""))
        else:
            return ""