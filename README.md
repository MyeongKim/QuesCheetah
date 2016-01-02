# QuesCheetah
Web SDK for the Q&A

# Installation

To start QuesCheetah, you need jQuery first. Put jQuery script tag first and then put sdk script behind.

``` javascript
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
<script src="libs/sdk.js"></script>
```


# Sample

Sample project for QuesCheetah is [here](https://github.com/mingkim/QuesCheetah_sample)(https://github.com/mingkim/QuesCheetah_sample)

You can test creating questions, making answers, direct voting and delete questions.
No additional server needed.

# Usage

You should get a api key to use the API. You can get it from [here](http://quescheetah.com)(http://quescheetah.com)

```javascript
    //Callback functions
    var error = function (err, response, body) {
        console.log(err);
    };
    var success = function (data) {
        console.log(data);
    };

    //Get this data from your twitter apps dashboard
    var config = {
        "apiKey": "XXX",
        "callBackUrl": "XXX"
    }

    var qc = new QuesCheetah(config);

```

# Functions




# REST API

All request to QuesCheetah are processed with REST API.

You send the request data in JSON format. you should set ```content-type: application/json``` in the request header.

The response will be always JSON object. It depends on the context.


**Error response**

``` json
{
    'error'      : True,
    'description': desc     // this data depends on the context.
}
```

**Make one Question only**



