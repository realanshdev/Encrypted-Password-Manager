import psycopg2
print("Connecting to the database...")
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="password_manager",
    user="postgres",
    password="postgres"
)
def init_db():
   cursor = conn.cursor()
   cursor.execute('''CREATE TABLE IF NOT EXISTS credentials(
   id serial primary key,
   website varchar(255) not null,
   username varchar(255) not null,
   password varchar(255) not null
)
''')
   conn.commit()
   cursor.close()
def create_vault():
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS vault(
     id serial primary key,
     salt varchar(255) not null,
     master_password_hash varchar(255) not null
    )
    ''')
    conn.commit()
    cursor.close()
    

def save_credential(website1, username1, password1):
     cursor = conn.cursor()
     cursor.execute('''INSERT INTO credentials (website, username, password) VALUES (%s, %s, %s)''', (website1, username1, password1))
     conn.commit()
def get_credentials():
     cursor = conn.cursor()
     cursor.execute('''SELECT * FROM credentials''')
     return cursor.fetchall()
def delete_credential_db(website1):
     cursor = conn.cursor()
     cursor.execute('''DELETE FROM credentials WHERE website = %s''', (website1,))
     conn.commit()
if __name__ == "__main__":
    init_db()
    create_vault()
