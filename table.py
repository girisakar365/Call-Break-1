from prettytable import PrettyTable

table = PrettyTable()
table.field_names = ['Player','Bid', 'Total Point','Cards']

def show_table(data:tuple):
    table.add_rows(data)
    print(table)
    table.clear_rows()
