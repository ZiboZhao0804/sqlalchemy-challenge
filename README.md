# SQLAlchemy Homework - Surfs Up!
## Step 1 - Climate Analysis and Exploration
[climate analysis notebook](https://github.com/ZiboZhao0804/sqlalchemy-challenge/blob/main/climate.ipynb)
### Station Analysis
### Precipitation Analysis
## Step 2 - Climate App
[climate app](https://github.com/ZiboZhao0804/sqlalchemy-challenge/blob/main/app.py)
### Routes

* `/`

  * Home page.

  * List all routes that are available.

* `/api/v1.0/precipitation`

  * Convert the query results to a dictionary using `date` as the key and `prcp` as the value.

  * Return the JSON representation of your dictionary.

* `/api/v1.0/stations`

  * Return a JSON list of stations from the dataset.

* `/api/v1.0/tobs`
  * Query the dates and temperature observations of the most active station for the last year of data.

  * Return a JSON list of temperature observations (TOBS) for the previous year.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

  * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

  * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
## Bonus: Other Recommended Analyses
### Temperature Analysis I
[Temperature Analysis I notebook](https://github.com/ZiboZhao0804/sqlalchemy-challenge/blob/main/temp_analysis_bonus_1.ipynb)
* Hawaii is reputed to enjoy mild weather all year. Is there a meaningful difference between the temperature in, for example, June and December?

* Use pandas to perform this portion.

  * Convert the date column format from string to datetime.

  * Set the date column as the DataFrame index

  * Drop the date column

* Identify the average temperature in June at all stations across all available years in the dataset. Do the same for December temperature.

* Use the t-test to determine whether the difference in the means, if any, is statistically significant. Will you use a paired t-test, or an unpaired t-test? Why?
### Temperature Analysis II
[Temperature Analysis II notebook](https://github.com/ZiboZhao0804/sqlalchemy-challenge/blob/main/temp_analysis_bonus_2.ipynb)
