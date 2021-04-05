
Hi!

This is the task in the recruitment process for the position of Intern Python Developer at Profil Software. Read the instructions carefully. 

Good luck!

# Specification
API DOCS: https://api.coinpaprika.com

We would like you to build a script/CLI that will process historical data from external API about cryptocurrencies and give us desirable results. 

Default cryptocurrency for calculating results is bitcoin (**btc-bitcoin**). 

In the API response for historical values there are multiple fields available, but you can always use field **close** to get bitcoin value for that record. 


```
[

    {
        "time_open": "2018-03-01T00:00:00Z",
        "time_close": "2018-03-01T23:59:59Z",
        "open": 856.012,
        "high": 880.302,
        "low": 851.92,
        "close": 872.2,
        "volume": 1868520000,
        "market_cap": 83808161204
    }

]

```


## Calculate average price of currency by month for given period
Example input:

`python script.py average-price-by-month --start-date=2021-01 --end-date=2021-03`

Example output:

```
Date      Average price ($)

2021-01   1234.12

2021-02   1252.23

2021-03   1354.55
```

* this is just a sample data and should not be used to verify solutions
* watchout about current month ! 
* oldest date watchout 
* start cant be newer date than end



## Find longest consecutive period in which price was increasing

### Example input:

`python script.py consecutive-increase --start-date=2021-02-11 --end-date=2021-03-20`  


### Example output:  

`Longest consecutive period was from 2021-02-24 to 2021-02-28 with increase of $423.54`


* this is just a sample data and should not be used to verify solutions
* watchout about current month ! 
* oldest date watchout 
* start cant be newer date than end
* calculate avarage of close price for days by month

## Export data for given period in one of selected format csv or json

### Example input
`python script.py export --start-date=2021-01-01 --end-date=2021-01-03 --format=csv --file=exported_data.csv`
### CSV structure

You should use `,` as a delimiter (structure below is separated by spaces for better visual representation)

```
Date         Price
2021-01-01   1234.56
2021-01-02   1235.43
2021-01-03   1234.54
```


`python script.py --start-date=2021-01-01 --end-date=2021-01-03 --export --format=json --file=exported_data.json`

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
* this is just a sample data and should not be used to verify solutions
## Bonus tasks

- To prevent from too many requests to external API you can implement a caching mechanism (e.g. database or file). This way, if you execute the script again with the same parameters, you will get results directly from the database (or file) without calling API
- By default the program calculates results only for one cryptocurrency (btc-bitcoin). You can extend its functionality by passing optional parameter --coin in which we can specify other type of cryptocurrency

`python script.py consecutive-increase --start-date=2021-02-11 --end-date=2021-03-20 --coin=usdt-tether`

- Write at least one basic test for each functionality


## Rules & hints
- use Python 3.8
- use OOP paradigm
- You are free to use any third-party libraries
- Provide README with examples how to use your script
- Write Python code that conforms to PEP 8
- Remember about validating input data, e.g. if start_date is before end_date
- Please handle possible exceptions within script in a user-friendly way
- Please put your solution in a private repository on Github and invite `reviewer@profil-software.com` as collaborator (any role with at least read-only access to code) -> https://docs.github.com/en/github/setting-up-and-managing-your-github-user-account/inviting-collaborators-to-a-personal-repository



# Logika

# User daje zapytanie z startdata endData i coin. --> zapytanie trafia do rozdzielacza przez dateformater -->
# rozdzielacza przekazuje je do bazy danych--> baza zwraca rekordy pasujące do metod obliczających do rozdzielacza->
# rozdzielacz przekazuje listę rekordów do SPRAWDZENIA czy są wszystkie z zawartego przedziału, gdy ok - przekazuje do obliczeń!!!
# jesli nie zwraca listę przedziałów o które trzeba zapytać do API  -->
# odpowiedź przekazujedo zapisania w bazie danych następnie odczytujemy jeszcze raz metodą z bazy danych-->
# całośc trafia do obliczeń i zwraca odpowiedzi !!
