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

Create many questions. These questions are group together.
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

###**delete an question and all related answers, useranswers. **

Delete an question with all related data.

REST API URL = ```"question/set/delete"```

```javascript
    qs.deleteQuestionSet(params, successCallback, errorCallback);
```

###**delete many question and all related answers, useranswers. **

Delete one group with all related data.

REST API URL = ```"multiple/delete"```

```javascript
    qs.deleteMultiQuestionSet(params, successCallback, errorCallback);
```


# REST API

All request to QuesCheetah are processed with REST API.

You send the request data in JSON format. you should set ```content-type: application/json``` in the request header.

The response will be always JSON object. It depends on the context.


###**Error response**

``` json
    {
        'error'      : True,
        'description': desc     // this data depends on the context.
    }
```

###**to_private**


POST - (http://quescheetah.com/v1/question/private)

Change question state to private.

**request**
``` json
    {
        'api_key'       : "Your api key",
        'question_title': "Your question title",
        'question_id'   : "Your question id"    // Either question_title and question_id is required.
    }

```

**return**
``` json
    {}
```
    
###**to_public**


POST - (http://quescheetah.com/v1/question/public)

Change question state to public.

**request**
``` json
    {
        'api_key'       : "Your api key",
        'question_title': "Your question title",
        'question_id'   : "Your question id"    // Either question_title and question_id is required.
    }

```

**return**
``` json
    {}
```
    
###**get_url_list**


POST - (http://quescheetah.com/v1/question/url/list)

Get authenticated urls of the question.

**request**
``` json
    {
        'api_key'       : "Your api key",
        'question_title': "Your question title",
        'question_id'   : "Your question id"    // Either question_title and question_id is required.
    }

```

**return**
``` json
    {
        'urls': {0:{"https://naver.com"},
                 1:{"https://google.com"},
                 2:{"https://daum.net"},
                 ...
                 }
    }
```
    
###**add_url**


POST - (http://quescheetah.com/v1/question/url/add)

Add an authenticated url.

**request**
``` json
    {
        'api_key'       : "Your api key",
        'question_title': "Your question title",
        'question_id'   : "Your question id",    // Either question_title and question_id is required.
        'url'           : "New url"
    }

```

**return**
``` json
    {
        'urls': {0:{"https://naver.com"},
                 1:{"https://google.com"},
                 2:{"https://daum.net"},
                 ...
                 }
    }
```
    
###**create_question**


POST - (http://quescheetah.com/v1/question/create)

Create one question. Not any related answers.

**request**
``` json
    {
        'api_key'           : "Your api key",
        'question_title'    : "Your question title",
        'question_text'     : "Your question text",
        'start_dt'          : "",                   // optional
        'end_dt'            : "",                   // optional
        'is_editable'       : "True",               // optional
        'is_private'        : "True",               // optional
    }

```

**return**
``` json
    {
        'api_key'           : "Your api key",
        'question_title'    : "Your question title",
        'question_text'     : "Your question text",
        'start_dt'          : "",                   
        'end_dt'            : "",                   
        'is_editable'       : "True",               
        'is_private'        : "True",               
    }
```
    
###**create_answer**


POST - (http://quescheetah.com/v1/answer/create)

Create answers related to one question.

**request**
``` json
    {
        'api_key'       : "Your api key",
        'question_title': "Your question title",
        'question_id'   : "Your question id",    // Either question_title and question_id is required.
        'answers': {
                        1:{'answer_num':"1", 'answer_text': "answer1"},
                        2:{'answer_num':"2", 'answer_text': "answer2"},
                        3:{'answer_num':"3", 'answer_text': "answer3"},
                        4:{'answer_num':"4", 'answer_text': "answer4"}
                    }
    }

```

**return**
``` json
    {
        'answers': {
                        1:{'answer_num':"1", 'answer_text': "answer1"},
                        2:{'answer_num':"2", 'answer_text': "answer2"},
                        3:{'answer_num':"3", 'answer_text': "answer3"},
                        4:{'answer_num':"4", 'answer_text': "answer4"}
                    }             
    }
```

###**get_question**


POST - (http://quescheetah.com/v1/question/get)

Get question data. Not related answers.

**request**
``` json
    {
        'api_key'       : "Your api key",
        'question_title': "Your question title",
        'question_id'   : "Your question id",    // Either question_title and question_id is required.
    }

```

**return**
``` json
    {
        'api_key'           : "Your api key",
        'question_title'    : "Your question title",
        'question_text'     : "Your question text",
        'start_dt'          : "",                   
        'end_dt'            : "",                   
        'is_editable'       : "True",               
        'is_private'        : "True",           
    }
```

###**get_answer**


POST - (http://quescheetah.com/v1/answer/get)

Get all answer data related with one question.

**request**
``` json
    {
        'api_key'       : "Your api key",
        'question_title': "Your question title",
        'question_id'   : "Your question id",    // Either question_title and question_id is required.
    }

```

**return**
``` json
    {
        'answers': {
                        1:{'answer_num':"1", 'answer_text': "answer1"},
                        2:{'answer_num':"2", 'answer_text': "answer2"},
                        3:{'answer_num':"3", 'answer_text': "answer3"},
                        4:{'answer_num':"4", 'answer_text': "answer4"}
                    }          
    }
```

###**create_useranswer**


POST - (http://quescheetah.com/v1/useranswer/create)

Make a new useranswer.

**request**
``` json
    {
        'api_key'       : "Your api key",
        'question_title': "Your question title",
        'question_id'   : "Your question id",    // Either question_title and question_id is required.
        'update_num'    : "1",                    // The answer_num of answer
        'unique_user'   : "Unique Id"            // For the distiction between useranswers.
    }

```

**return**
``` json
    {
        'useranswer':  {
                            'update_num' : "1",
                            'unique_user': "Unique Id"
                        }       
    }
```

###**simple_view_answer**


POST - (http://quescheetah.com/v1/answer/view/simple)

Provide the main information of question.

**request**
```
    {
        'api_key'       : "Your api key",
        'question_title': "Your question title",
        'question_id'   : "Your question id",    // Either question_title and question_id is required.
    }

```

**return**
``` json
    {
        'answer'
    }
```
