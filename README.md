<img src="./QuesCheetah/static/images/quescheetah-logo.png" width="400">

Web SDK for the easy Q&A of your site.


---

**Home page**
[On developing yet.]()

**Source code**

[https://github.com/mingkim/QuesCheetah](https://github.com/mingkim/QuesCheetah)

**REST API Documentation**

[https://mingkim.gitbooks.io/quescheetah-document/content/](https://mingkim.gitbooks.io/quescheetah-document/content/)

**Used open source projects**

[NOTICE.txt](./NOTICE.txt)

**Demo Video**

[https://youtu.be/BW8eLg8mp_E](https://youtu.be/BW8eLg8mp_E)

**Tutorial - Installation at your Jekyll blog in 3 minutes**

[https://youtu.be/4pEEbU2EPk4](https://youtu.be/4pEEbU2EPk4)

**slideshare**

[http://www.slideshare.net/ssuser0d8ba1/naver-d2-campus-fest-2015-quescheetah-56732325](http://www.slideshare.net/ssuser0d8ba1/naver-d2-campus-fest-2015-quescheetah-56732325)


---


# Download SDK
You can download QuesCheetah JavaScript file [here](https://raw.githubusercontent.com/mingkim/QuesCheetah/master/QuesCheetah/static/js/quescheetah-sdk-0.1.0.js)


# Installation

To start QuesCheetah, you need jQuery first. Put [jQuery](http://jquery.com/) script tag first and then put sdk script behind.


``` javascript
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <script src="libs/quescheetah-sdk-0.1.0.js"></script>
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

Following functions can be used inside of your JavaScript file. 

Check the parameter of the request and the response format in the REST API section.



###**make one question only**

Not making any related answers, make one question only.

REST API URL = ```"question/create"```

```javascript
    qs.createQuestion(params, successCallback, errorCallback);
```

###**make one answer only**

Make one answer

REST API URL = ```"answer/create"```

```javascript
    qs.createAnswer(params, successCallback, errorCallback);
```

###**create single question**

Create one question and related answers at once.

REST API URL = ```"single/create"```

```javascript
    qs.createSingleQuestion(params, successCallback, errorCallback);
```

###**create many question**

Create many questions. These questions are grouped together.
If the ```group_name```is empty in requested data, It's redirected to creating single question function.

REST API URL = ```"multiple/create"```


```javascript
    qs.createQuestion(params, successCallback, errorCallback);
```

###**create user answer**

Used when new user answers the question. 

REST API URL = ```"useranswer/create"```

```javascript
    qs.createUserAnswer(params, successCallback, errorCallback);
```

###**delete one question only**

Not removing any related answers, delete one question only.

REST API URL = ```"question/delete"```


```javascript
    qs.deleteQuestion(params, successCallback, errorCallback);
```

###**delete one answer only**

Delete one answer only.

REST API URL = ```"answer/delete"```


```javascript
    qs.deleteAnswer(params, successCallback, errorCallback);
```

###**delete an user's answer**

Delete specific user's answer.

REST API URL = ```"useranswer/delete"```


```javascript
    qs.deleteUserAnswer(params, successCallback, errorCallback);
```

###**delete an question and all related answers, useranswers.**

Delete an question with all related data.

REST API URL = ```"question/set/delete"```

```javascript
    qs.deleteQuestionSet(params, successCallback, errorCallback);
```

###**delete many question and all related answers, useranswers.**

Delete one group with all related data.

REST API URL = ```"multiple/delete"```

```javascript
    qs.deleteMultiQuestionSet(params, successCallback, errorCallback);
```

