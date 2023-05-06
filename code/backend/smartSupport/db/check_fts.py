import sqlite3

con = sqlite3.connect(':memory')
cur = con.cursor()
cur.execute('pragma compile_options;')
compile_options = cur.fetchall()
cur.execute('pragma module_list;')
module_list = cur.fetchall()
con.close()

if ('ENABLE_FTS5',) in compile_options:
    print('FTS5 is ENABLED')
else:
    print('NO FTS5')

