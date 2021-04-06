contact:
69910464
Marek.Demkowicz@wp.pl


# Specification
API DOCS: https://api.coinpaprika.com

That script is able to process historical data from external API about cryptocurrencies and give us desirable results. 

Default cryptocurrency for calculating results is bitcoin (**btc-bitcoin**). Here you can find all supported cryptocurrency(https://api.coinpaprika.com/v1/coins).   

To prevent from too many requests to external API it use caching mechanism (Sqlite-> Peewee). This way, if you execute the script again with the same parameters, you will get results directly from the database without calling API.

When database have data gaps, it will ask API only for missing data. Also it will complete the data in the local database. 

 
## Calculate average price of currency by month for given period
Example input:

`python ui.py average-price-by-month --start-date=2021-01 --end-date=2021-03`

Example output:

```
Date      Average price ($)

2021-01   1234.12

2021-02   1252.23

2021-03   1354.55
```

* this is just a sample data
* For current month it will calculate from beginning of month till current date. 
* if you will provide date older than cryptocurrency exists, it will start from first date accessible from API.
* when start is newer that end date, it will handle it. 
* when you will provide date containing days ( example: --end-date=2021-03-15) it will trim it, and return average for whole month.



## Find longest consecutive period in which price was increasing

### Example input:

`python ui.py consecutive-increase --start-date=2021-02-11 --end-date=2021-03-20`  


### Example output:  

`Longest consecutive period was from 2021-02-24 to 2021-02-28 with increase of $423.54`


* this is just a sample data.
* If you will provide date without days( example: --end-date=2021-03 --start-date=2021-03 ). it will end on last day of month, and start from first.


## Export data for given period in one of selected format csv or json

### Example input
`python ui.py export --start-date=2021-01-01 --end-date=2021-01-03 --format=csv --file=exported_data.csv`
### CSV structure

it uses `,` as a delimiter (structure below is separated by spaces for better visual representation)

```
Date         Price
2021-01-01   1234.56
2021-01-02   1235.43
2021-01-03   1234.54
```


`python ui.py export --start-date=2021-01-01 --end-date=2021-01-03  --format=json --file=exported_data.json`

### Json structure
```json
[
  {
    "date": "2021-01-01",
    "price": 1234.56
  },
  {
    "date": "2021-01-02",
    "price": 1234.56
  },
  {
    "date": "2021-01-03",
    "price": 1234.56
  }
]
```
* this is just a sample data
* when you will use same file name many times, it will handle it by adding number in the end of file name (example: ExampleName_5.csv).



