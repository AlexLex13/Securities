def parse_bonds_df(df):
    bonds = []
    for lst in df.values:
        field_list = lst[1:-1]
        for i, f in enumerate(field_list):
           if i in (6, 7, 9, 11):
               field_list[i] = float(f.strip('$'))
           if i in range(12, 16):
               field_list[i] = f.date()

        bonds.append(field_list)

    return bonds
