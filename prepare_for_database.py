import json
import logging

import psycopg2

try:
    # declare a new PostgreSQL connection object
    conn = psycopg2.connect(
        dbname="database",
        user="postgres",
        host="localhost",
        password="docker",
        port="5432",
        # attempt to connect for 3 seconds then raise exception
        connect_timeout=3
    )

    cur = conn.cursor()
    logging.info("\ncreated cursor object:", cur)

except (Exception, psycopg2.Error) as err:
    logging.info("\npsycopg2 connect error:", err)
    conn = None
    cur = None


def prepare_for_insert(file_path):
    table_name = "database"
    with open(file_path) as json_data:
        record_list = json.load(json_data)

    sql_string = 'INSERT INTO {} '.format(table_name)

    if type(record_list) == list:
        first_record = record_list[0]
        columns = list(first_record.keys())
    else:
        columns = []
        logging.warning("Needs to be an array of JSON objects")

    sql_string += "(" + ', '.join(columns) + ")\nVALUES "

    for i, record_dict in enumerate(record_list):
        # iterate over the values of each record dict object
        values = []
        for col_names, val in record_dict.items():
            # Postgres strings must be enclosed with single quotes
            if type(val) == str:
                # escape apostrophes with two single quotations
                val = val.replace("'", "''")
                val = "'" + val + "'"
            values += [str(val)]
        sql_string += "(" + ', '.join(values) + "),\n"
    sql_string = sql_string[:-2] + ";"

    with open("sql_sequence.sql", "w", encoding="utf-8") as outfile:
        outfile.write(sql_string)
        logging.info(f"Saved results to sql file sql_sequence.sql")

    return sql_string


def execute_insert(sql_string):
    if cur is not None:
        try:
            cur.executemany(sql_string)
            conn.commit()

            logging.info('\nfinished INSERT INTO execution')

        except (Exception, psycopg2.Error) as error:
            logging.info("\nexecute_sql() error:", error)
            conn.rollback()

        # close the cursor and connection
        cur.close()
        conn.close()


def create_database():
    sql_string = ''' CREATE database database '''
    # executing above query
    cur.execute(sql_string)
    logging.info("Database has been created successfully !!")
