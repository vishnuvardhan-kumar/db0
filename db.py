from collections import defaultdict
from tabulate import tabulate
import operator, re, sys, socket

ID_PTR, table, mapping = 1, [], {'=':'eq','<':'lt','>':'gt','<=':'le','>=':'ge','!=':'ne'}

def custom_tabl(table): return tabulate(table, headers={'id':'id','key':'key','value':'value'}, tablefmt='psql')

def filter_col(table, cols): return [{col: row[col] for col in cols} for row in table] if cols != ['*'] else table

def sel(cols, condition=None): # SELECT STATEMENT
    if not condition: return custom_tabl(filter_col(table, cols.split(','))) if table else "0 rows selected."
    col, op, val = re.split(r'(\W+)', condition)
    subtable, reqd_cols = [], cols.split(',')
    for row in table:
        if getattr(operator, mapping[op])(str(row[col]), str(val)):
            subtable.append(row)
    if subtable: return custom_tabl(filter_col(subtable, reqd_cols))
    return "0 rows selected."

def ins(data): # INSERT STATEMENT
    try:
        global ID_PTR
        table.append(defaultdict(lambda:'', {'id': ID_PTR, 'key': data.split(',')[0], 'value': data.split(',')[1]}))
        ID_PTR += 1
        return "Inserted 1 row."
    except: return "Insert failed, please check syntax/conflicting entries"

def upd(col, condition): # UPDATE STATEMENT
    key_to_set, value_to_set = col.split('=')
    col, op, val = re.split(r'(\W+)', condition)
    upd_count = 0
    for row in table:
        if getattr(operator, mapping[op])(str(row[col]), str(val)):
            row[key_to_set], upd_count = value_to_set, upd_count+1
    return f"Updated {upd_count} row(s)."

def delt(condition): # DELETE STATEMENT
    col, op, val = re.split(r'(\W+)', condition)
    for row in table:
        if getattr(operator, mapping[op])(str(row[col]), str(val)):
            table.remove(row)
            return "Deleted 1 row."
    else:
        return "No rows matched condition"

def exec_cmd(cmd):  # SQL COMMAND PARSER
    accepted = ['select', 'insert', 'update', 'delete']
    cmdc = cmd.split()
    if not cmdc: return ''
    if cmdc[0] not in accepted:
        return f'Unknown command: {cmdc[0]}'
    if cmdc[0] == 'select': 
        if len(cmdc) == 4: return sel(cmdc[1])
        return sel(cmdc[1], cmdc[5])
    if cmdc[0] == 'insert': return ins(cmdc[4])
    if cmdc[0] == 'update': return upd(cmdc[3], cmdc[5])
    else: return delt(cmdc[4])

if __name__ == '__main__': # MAIN EVENT LOOP
    if len(sys.argv) == 1:
        while True:
            try: result = exec_cmd(input('db0 > '))
            except KeyboardInterrupt: sys.exit()
            except: print("There was an error with the SQL syntax.")
            else: devnull = print(result) if result else None
    else:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(('127.0.0.1', int(sys.argv[1])))
            sock.listen()
            connection, address = sock.accept()
            with connection:
                while True:
                    connection.send('db0 > '.encode())
                    connection.send(f"{exec_cmd(connection.recv(1024).decode('utf-8'))}\n".encode())
                