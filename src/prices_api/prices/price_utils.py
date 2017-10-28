import psycopg2
import os

# Connect to database
try:
    conn = psycopg2.connect("""dbname={} user={} host={} password={}""".format(
        os.environ.get('MC_DB_NAME'),
        os.environ.get('DB_USER'),
        os.environ.get('DB_HOST'),
        os.environ.get('DB_PASSWORD')))
except:
    print("Connection unsuccessful")


def get_car_name(car_data):
    """Returns model name and make"""
    # Create cursor
    temp_cursor = conn.cursor()
    # Build query string
    sql_str = """select models.name, makes.name from models
    join cars on cars.model_id = models.id
    join makes on makes.id = models.make_id
    where cars.id = {};"""
    # Execute query
    temp_cursor.execute(sql_str.format(car_data['car_id']))
    car_output = temp_cursor.fetchall()[0]
    # Build dictionary
    car_dict = {
        'model': car_output[0],
        'make': car_output[1]
    }
    return car_dict
