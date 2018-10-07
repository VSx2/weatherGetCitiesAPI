# weatherGetCitiesAPI
### Important! This API is for <a href="https://openweathermap.org" target="_blank">OpenWeatherMap</a> cities. :sunny:

### Introduction

_When our team decided to develop this API, the problem was in the point , that OpenWeartherMap API hasn't provided a possibility to get all cities by request. They propose to get cities only from the big 29mbs json file called city.list.json . If you use their's API  for web or desktop apps - it's ok, you can store this file.In other cases, e.g. when you develop a mobile app, it isn't a good idea to store 29mbs file on a mobile device.So you need to have an API, that can give you some cities by request. Using weatherGetCitiesAPI you can get all cities, get cities by name in some different ways and control fields & count of requested cities._

_We hope that this API will help you )_

### Usage

**URL:**
```markdown
    http://apis.mcwladkoe.ml/api?mode={mode_code}&q={query_string}
```
   You can pass some Additional params

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
```json
{"errors": [], "items": [{"name": "Oradell", "id": 5102208}], "status": "success", "total_items": 1}
```

### Examples

#### Examples without additional params

URL:
```json
http://apis.mcwladkoe.ml/api?mode=0&q=Rio De J
```

Response:
```json
{
    "errors": [],
    "items": [
        {
            "name": "Rio de Janeiro",
            "id": 3451190
        },
        {
            "name": "Rio de Jesus",
            "id": 3701882
        }
    ],
    "status": "success",
    "total_items": 1
}
```


Response:
```json
{
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
```

#### Examples with additional parametres

URL:
```json
http://apis.mcwladkoe.ml/api?mode=0&q=Khark&fields=name
```

Response:
```json
{
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
```

URL:
```json
http://apis.mcwladkoe.ml/api?mode=0&q=Khark&limit=2
```
Response:
```json
{
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
```

URL:
```json
http://apis.mcwladkoe.ml/api?mode=1&q=ord&limit=2&fields=name,country
```

Response: 
```json
{
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
```








