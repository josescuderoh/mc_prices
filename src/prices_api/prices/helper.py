import datetime
import psycopg2
import os
import numpy as np
import math
from dateutil.relativedelta import relativedelta


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
        # Connect to database
        try:
            self.conn = psycopg2.connect("""dbname={} user={} host={} password={}""".format(
                'mc_db',
                # os.environ.get('MC_DB_NAME'),
                os.environ.get('DB_USER'),
                os.environ.get('DB_HOST'),
                # os.environ.get('DB_PASSWORD')))
                os.environ.get('DB_PASSWORD')))
        except ConnectionError as e:
            print(e)

        try:
            # Get market price
            self.market_price = self.get_price_variation()
            # Get price price_today
            self.price_today = self.mc_price()
            # Build response object
            self.output = self.create_response()
        except Exception:
            self.output = {
                "adjusted_max_price": None,
                "adjusted_min_price": None,
                "predicted_price": None,
                "status": "ERROR"
            }

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
            select models.name, makes.name, models.name from models
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

    def get_price_variation(self):
        """This method checks if the requested price_variation exists for a given month and year"""
        # Create cursor
        temp_cursor = self.conn.cursor()
        # Check if request contains month and year
        if self.month and self.year:
            # Build complete query if it does
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
            where cars.id = {} and yearly_prices.year_model = {} and guides.month_sold = {}
            and guides.year_guide = {};
            """
            # Execute query
            temp_cursor.execute(sql_str.format(self.car_id, self.model_year, self.month, self.year))
            car_output = temp_cursor.fetchone()
            # Check if month and year were found
            if car_output:
                temp_cursor.close()
                self.variation = "year_month"
                return float(car_output[0])

            # If exact price variation doesn't exist but year exists
            else:
                # Build partial query
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
                where cars.id = {} and yearly_prices.year_model = {} and guides.year_guide = {};
                """
                # Execute query
                temp_cursor.execute(sql_str.format(self.car_id, self.model_year, self.year))
                car_output = temp_cursor.fetchall()
                if car_output:
                    temp_cursor.close()
                    self.variation = "year"
                    return float(np.mean([price[0] for price in car_output]))

        # We get to this point if there are no variations for the year sent or if no year and
        # mont information is sent to the API

        # Build complete query
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
        where cars.id = {} and yearly_prices.year_model = {};
        """
        # Execute query
        temp_cursor.execute(sql_str.format(self.car_id, self.model_year))
        car_output = temp_cursor.fetchall()
        if car_output:
            temp_cursor.close()
            self.variation = "average"
            return float(np.mean([price[0] for price in car_output]))
        else:
            return None

    def get_max_price(self):
        """Returns a max buy price for the car taking into account its current state"""
        delta = (0.01 * self.state) + 0.02
        max_price = (1 + delta) * self.price_today
        return max_price

    def get_min_price(self):
        """Returns a min buy price for the car taking into account its current state"""
        delta = ((0.01) * self.state) + 0.08
        min_price = (1 - delta) * self.price_today
        return min_price

    def create_response(self):
        """This method creates the response object as form of dictionary to return to API"""

        # If price variation was found but state does not meet requirements
        if self.state == 1:
            obj = {
                "adjusted_max_price": None,
                "adjusted_min_price": None,
                "predicted_price": None,
                "status": "NOT_VALID"
            }
        elif self.price_today:
            obj = {
                "adjusted_max_price": round(self.get_max_price(), 3),
                "adjusted_min_price": round(self.get_min_price(), 3),
                "predicted_price": round(self.price_today, 3),
                "status": self.valify()
            }
        else:
            obj = {
                "adjusted_max_price": None,
                "adjusted_min_price": None,
                "predicted_price": None,
                "status": "NOT_FOUND"
            }
        return obj

    def valify(self):
        """This method checks validity of the car given MC standards"""
        # Constants
        monthly_mileage = 1600  # km
        today = datetime.datetime.today()
        # If month RUNT data is available
        if self.month and self.year:
            delta = relativedelta(today, datetime.datetime(self.year, self.month, 1))
            max_mileage = monthly_mileage * (delta.years * 12 + delta.months)
        # Otherwise
        else:
            delta = relativedelta(today, datetime.datetime(self.model_year, 1, 1))
            max_mileage = monthly_mileage * (delta.years * 12 + delta.months)
        # valify
        if (max_mileage < self.kilometers) or (self.state == 2):
            return "NOT_VALID"
        else:
            return "OK"

    def mc_price(self):
        """This method applies the model proposed by MatchCars"""
        # Set of parameters

        alpha = 0.01  # Curvature
        beta = 120  # Lateral displacement
        theta = 3.14  # Vertical displacement
        omega = 0.21  # Distance between asintotes (greater than zero)

        # Prediction for one car instance
        price_today = self.market_price * \
            (omega) * (theta - math.atan(alpha * (self.kilometers / 1000 - beta)))

        return price_today
