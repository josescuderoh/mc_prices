import datetime
import psycopg2
import os
import numpy as np

CURRENT_YEAR = datetime.datetime.now().year


class Car():
    """
    Car class to perform calculations inside app
    Attributes:
        car_id (int): The car id of the car.
        kilometers (float): The kilometers of the car in units.
        state (float): The state of the car [1-5]. Default 4
        year (float): The year model of the car.
        survey (dict): The survey of the Car. Default {}
        fasecolda (float): The fasecolda price for the car.
        CURRENT_YEAR (int): The current year
    """

    # Car object
    def __init__(self, car_id, kilometers, model_year, year=None, month=None, state=4, survey={}):
        self.car_id = int(car_id)
        self.kilometers = float(kilometers)
        self.model_year = model_year
        self.year = year
        self.month = month
        self.state = int(state)
        self.survey = survey
        self.exists = self.find_car()
        if self.exists:
            self.variation = self.check_price_variation()
        # Connect to database
        try:
            self.conn = psycopg2.connect("""dbname={} user={} host={} password={}""".format(
                os.environ.get('MC_DB_NAME'),
                os.environ.get('DB_USER'),
                os.environ.get('DB_HOST'),
                os.environ.get('DB_PASSWORD')))
        except ConnectionError as e:
            print(e)

    def find_car(self):
        """Check if car exists in the database"""
        # Create cursor
        temp_cursor = self.conn.cursor()
        # Build query string
        sql_str = """
        select cars.model_id
        from cars
        where cars.id = {};
        """
        # Execute query
        temp_cursor.execute(sql_str.format(self.car_id))
        car_output = temp_cursor.fetchall()
        # Return boolean
        if car_output:
            return True
        else:
            return False
        # Close cursor
        temp_cursor.close()

    def get_car_name(self):
        """Returns model name and make"""
        if self.exists:
            # Create cursor
            temp_cursor = self.conn.cursor()
            # Build query string
            sql_str = """
            select models.name, makes.name from models
            join cars on cars.model_id = models.id
            join makes on makes.id = models.make_id
            where cars.id = {};
            """
            # Execute query
            temp_cursor.execute(sql_str.format(self.car_id))
            car_output = temp_cursor.fetchone()
            # Assign variables
            self.model = car_output[0]
            self.make = car_output[1]
            # Close cursor
            temp_cursor.close()

    def check_price_variation(self):
        """This method checks if the requested price_variation exists for a given month or year"""
        # Create cursor
        temp_cursor = self.conn.cursor()
        # Check if request contains month
        if self.month:
            # Build query
            sql_str = """
            select guides.reference
            from price_variations
            join guides on guides.id = price_variations.id_guide_pk
            join yearly_prices on price_variations.yearly_price_id = yearly_prices.id
            join cars on yearly_prices.car_id = cars.id
            where cars.id = {} and yearly_prices.year_model = {} and guides.month_sold = {};
            """
            # Execute query
            temp_cursor.execute(sql_str.format(self.car_id, self.year, self.month))
            car_output = temp_cursor.fetchall()
            # Return results
            if car_output:
                return "month"
            else:
                return "not_found"
        else:
            # Build query
            sql_str = """
            select guides.reference
            from price_variations
            join guides on guides.id = price_variations.id_guide_pk
            join yearly_prices on price_variations.yearly_price_id = yearly_prices.id
            join cars on yearly_prices.car_id = cars.id
            where cars.id = {} and yearly_prices.year_model = {};
            """
            # Execute query
            temp_cursor.execute(sql_str.format(self.car_id, self.year))
            car_output = temp_cursor.fetchall()
            # Return results
            if car_output:
                return "year"
            else:
                return "not_found"

    def get_buy_price(self):
        """Returns a response for the current POST request"""
        if self.exists:
            # Check price variation
            current_car = self.variation
            # If exact price variation exists
            if current_car == "month":
                # Create cursor
                temp_cursor = self.conn.cursor()
                # Build query string
                sql_str = """
                select price_variations.market_price,
                price_variations.min_price_percentage,
                price_variations.max_price_percentage,
                price_variations.med_price_percentage,
                price_variations.good_price_percentage
                from price_variations
                join guides on guides.id = price_variations.id_guide_pk
                join yearly_prices on price_variations.yearly_price_id = yearly_prices.id
                join cars on yearly_prices.car_id = cars.id
                where cars.id = {} and yearly_prices.year_model = {} and guides.month_sold = {};
                """
                # Execute query
                temp_cursor.execute(sql_str.format(self.car_id, self.model_year, self.month))
                car_output = temp_cursor.fetchone()
                self.market_price = car_output[0]
            # If exact price variation doesn't exist
            elif current_car == "year":
                # Create cursor
                temp_cursor = self.conn.cursor()
                # Build query string
                sql_str = """
                select price_variations.market_price,
                price_variations.min_price_percentage,
                price_variations.max_price_percentage,
                price_variations.med_price_percentage,
                price_variations.good_price_percentage
                from price_variations
                join guides on guides.id = price_variations.id_guide_pk
                join yearly_prices on price_variations.yearly_price_id = yearly_prices.id
                join cars on yearly_prices.car_id = cars.id
                where cars.id = {} and yearly_prices.year_model = {} and guides.month_sold = {};
                """
                # Execute query
                temp_cursor.execute(sql_str.format(self.car_id, self.model_year, self.month))
                car_output = temp_cursor.fetchall()
                self.market_price = np.mean([price[0] for price in car_output])
            elif current_car == "not_found":
                self.exists = False

    def get_max_price(self, buy_price):
        """
        Returns a max buy price for the car taking into account its current state
        Args:
            buy_price (float): The buy price of the car
        Returns:
            float: the max buy price of the car
        """
        delta = (0.01 * self.state) + 0.02
        max_price = (1 + delta) * buy_price
        return max_price

    def get_min_price(self, buy_price):
        """
        Returns a min buy price for the car taking into account its current state
        Args:
            buy_price (float): The buy price of the car
        Returns:
            float: the min buy price of the car
        """
        delta = ((0.01) * self.state) + 0.08
        min_price = (1 - delta) * buy_price
        return min_price
