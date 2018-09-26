# weatherGetCitiesAPI
### Important! This API is for <a href="https://openweathermap.org" target="_blank">OpenWeatherMap</a> cities. :sunny:

### Usage

**URL:** 

   http:<span></span>//apis.mcwladkoe.ml/api?mode=**{mode_code}**&q=**{query_string}**   
   // You can pass some Additional params

#### Main params

* mode (type Integer)
    * mode = 0 "Start with" search
    * mode = 1 "Contains" search

* query (type String)

#### Additional params

* fields (type String)
    * name
    * id 
    * country 
    * coord

You can combine fields. Default fields=name,id

* limit (type Integer) - limit of cities in response, e.g you can get only 5 cities that contains 'ab'

#### Response

**items** - result array of objects // If cities were not found, **items** will be an empty array

**errors** - array of strings, where string is an error description  
* List of errors:    
   * <p>Invalid mode</p>       
   * <p>Empty Query</p>        
   * <p>Invalid limit</p>       
   * <p>Invalid field</p>    

**status** - status of request  
* List of statuses:  
    * <p>success</p> 
	* <p>error</p>   

**total_items** - count of found cities in cities.list.json by query (type Integer)

{"errors": [], "items": [{"name": "Oradell", "id": 5102208}], "status": "success", "total_items": 1}

### Examples

#### Examples without additional params

URL: http://apis.mcwladkoe.ml/api?mode=0&q=Kh

Response: {
    "errors": [],
    "items": [
        {
            "name": "Khaty",
            "id": 2021026
        },
        ... / a lot of objects
    ],
    "status": "success",
    "total_items": 502
}

URL: http://apis.mcwladkoe.ml/api?mode=0&q=Rio de janeiro

Response: {
    "errors": [],
    "items": [
        {
            "name": "Rio de Janeiro",
            "id": 3451190
        }
    ],
    "status": "success",
    "total_items": 1
}


#### Examples with additional parametres

URL: http://apis.mcwladkoe.ml/api?mode=0&q=Khark&fields=name

Response: {
    "errors": [],
    "items": [
        {
            "name": "Kharkiv"
        },
        {
            "name": "Kharkivs’ka Oblast’"
        },
        {
            "name": "Kharkhorin"
        },
        {
            "name": "Kharkhauda"
        },
        {
            "name": "Kharkhauda"
        }
    ],
    "status": "success",
    "total_items": 4
}

URL: http://apis.mcwladkoe.ml/api?mode=0&q=Khark&limit=2

Response: {
    "errors": [],
    "items": [
        {
            "name": "Kharkiv",
            "id": 706483
        },
        {
            "name": "Kharkivs’ka Oblast’",
            "id": 706482
        }
    ],
    "status": "success",
    "total_items": 4
}

URL: http://apis.mcwladkoe.ml/api?mode=1&q=ord&limit=2&fields=name,country

Response: {
    "errors": [],
    "items": [
        {
            "name": "Portman",
            "country": "ES"
        },
        {
            "name": "Groveport",
            "country": "US"
        },
        {
            "name": "East Porterville",
            "country": "US"
        },
        {
            "name": "Port Stephens",
            "country": "AU"
        },
        {
            "name": "Cotiporã",
            "country": "BR"
        }
    ],
    "status": "success",
    "total_items": 846
}









