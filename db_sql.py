dados = [{'qt': '10', 'mlt': '2.22'}, {'qt': '3', 'mlt': '2.24'}, {'qt': '3', 'mlt': '1.69'}, {'qt': '1', 'mlt': '2.15'}, {'qt': '1', 'mlt': '2.11'}]
# 1.00
dados_mock = [{'qt': '25', 'mlt': '1.12'},
              {'qt': '15', 'mlt': '1.60'},
               {'qt': '10', 'mlt': '1.35'}, 
               {'qt': '5', 'mlt': '1.18'}, 
               {'qt': '5', 'mlt': '1.71'}, 
               {'qt': '2', 'mlt': '-'}, 
               {'qt': '2', 'mlt': '1.23'}]

import sqlite3

def gravando_player(dado):
    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    for linha in dado:
        # print(linha)
        # r_linha = linha != None
        r_linha_estorado = linha['mlt'] == "-"
        if r_linha_estorado:
            linha["mlt"] = "0"
        # if r_linha:
        cursor.execute("INSERT INTO player (qt, mlt)" + f"VALUES ({linha['qt']}, {linha['mlt']})")

        # cursor.execute("INSERT INTO player (qt, mlt)"+ "VALUES ("+ linha["qt"]+ ","+ linha["mlt"] + ")")
        conn.commit()
    conn.close()

def gravando_tempo(dado):
    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()

    cursor.execute(f"""
    INSERT INTO tempo (tempo)
    VALUES ({dado})
    """)
    
    conn.commit()
    conn.close()

def get_all_player_dados():
    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM player;
        """)
    for linha in cursor.fetchall():
        print(linha)
    conn.close()

def get_all_time_crash():
    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM tempo;
        """)
    for linha in cursor.fetchall():
        print(linha)
    conn.close()


if __name__ == "__main__":
    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE player (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            qt TEXT NOT NULL,
            mlt TEXT NOT NULL
    );
    """)

    cursor.execute("""
        CREATE TABLE tempo (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                tempo TEXT NOT NULL
        );
        """)
    conn.close()