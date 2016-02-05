<img src="./QuesCheetah/static/images/quescheetah-logo.png" width="400">


<img src="http://acceleratingscience.com/wp-content/uploads/2015/02/istock_000013996600_medium.jpg" width="400">

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


##**Group**
###**1. create a group question**

Create many questions. These questions are grouped together as ```group_name```.

REST API URL = ```"groups"```

```javascript
    qs.createGroup(params, successCallback, errorCallback);
```

###**2. delete a group question**

Delete a group with all related question, answer and useranswer data.

REST API URL = ```"groups/{groupId}"```

```javascript
    qs.deleteGroup(params, successCallback, errorCallback);
```

##**Question**
###**1. make a question**

Make a single question.

REST API URL = ```"questions"```

```javascript
    qs.createQuestion(params, successCallback, errorCallback);
```

###**2. get a question**

get a question data.

REST API URL = ```"questions/{questionId}"```

```javascript
    qs.getQuestion(params, successCallback, errorCallback);
```

###**3. update a question**

update a question data.

REST API URL = ```"questions/{questionId}"```

```javascript
    qs.updateQuestion(params, successCallback, errorCallback);
```

###**4. delete a question**

delete a question data with all answer and useranswer data.

REST API URL = ```"questions/{questionId}"```

```javascript
    qs.deleteQuestion(params, successCallback, errorCallback);
```

##**Answer**
###**1. make a new answer of specific question**

Add a new answer to the question.

REST API URL = ```"questions/{questionId}/answers"```

```javascript
    qs.createAnswer(params, successCallback, errorCallback);
```

###**2. get one answer data of the question**

Get answer data of ```answerNum```.

REST API URL = ```"questions/{questionId}/answers/{answerNum}"```

```javascript
    qs.getAnswer(params, successCallback, errorCallback);
```

###**3. delete one answer data of the question**

Delete answer data of ```answerNum```.

REST API URL = ```"questions/{questionId}/answers/{answerNum}"```

```javascript
    qs.deleteAnswer(params, successCallback, errorCallback);
```

##**Useranswer**
###**1. create useranswer**

Used when new user answers the question. 

REST API URL = ```"questions/{questionId}/answers/{answerNum}/useranswers"```

```javascript
    qs.createUserAnswer(params, successCallback, errorCallback);
```

###**2. update useranswer**

Change the number which user answered.

REST API URL = ```"questions/{questionId}/answers/useranswers/{uniqueUser}"```

```javascript
    qs.updateUserAnswer(params, successCallback, errorCallback);
```

###**3. delete useranswer**

Delete the useranswer data of ```uniqueUser```.

REST API URL = ```"questions/{questionId}/answers/useranswers/{uniqueUser}"```

```javascript
    qs.deleteUserAnswer(params, successCallback, errorCallback);
```

