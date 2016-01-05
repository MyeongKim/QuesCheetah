// This javascript file must be inserted after the jQuery file.
function PKC(config){
    this.apiKey = config.apiKey;
    this.baseUrl = "http://localhost:8000/vote/";
    this.callBackUrl = config.callBackUrl;
}

PKC.prototype.createMultipleQuestion = function (params, success, error) {
    if ( params['group_name'] === ""){
        this.createSingleQuestion(params, success, error);
    }else{
        var url = this.baseUrl+'multiple/create';
        this.doPost(url, params, success, error);
    }
};

PKC.prototype.createSingleQuestion = function (params, success, error) {
    var url = this.baseUrl+'single/create';
    this.doPost(url, params, success, error)
};

PKC.prototype.createQuestion = function (params, success, error) {
    var url = this.baseUrl+'question/create';
    this.doPost(url, params, success, error)
};

PKC.prototype.createAnswer = function (params, success, error) {
    var url = this.baseUrl+'answer/create';
    this.doPost(url, params, success, error)
};

PKC.prototype.createUserAnswer = function (params, success, error) {
    var url = this.baseUrl+'useranswer/create';
    this.doPost(url, params, success, error)
};

PKC.prototype.getQuestion = function (params, success, error) {
    var url = this.baseUrl+'question/get';
    this.doPost(url, params, success, error)
};

PKC.prototype.getAnswer = function (params, success, error) {
    var url = this.baseUrl+'answer/get';
    this.doPost(url, params, success, error)
};

PKC.prototype.deleteQuestion = function (params, success, error) {
    var url = this.baseUrl+'question/delete';
    this.doPost(url, params, success, error)
};

PKC.prototype.deleteAnswer = function (params, success, error) {
    var url = this.baseUrl+'answer/delete';
    this.doPost(url, params, success, error)
};

PKC.prototype.deleteUserAnswer = function (params, success, error) {
    var url = this.baseUrl+'useranswer/delete';
    this.doPost(url, params, success, error)
};

PKC.prototype.deleteQuestionSet = function (params, success, error) {
    var url = this.baseUrl+'question/set/delete';
    this.doPost(url, params, success, error)
};

PKC.prototype.deleteMultiQuestionSet = function (params, success, error) {
    var url = this.baseUrl+'multiple/delete';
    this.doPost(url, params, success, error)
};


PKC.prototype.doRequest = function (url, success, errorCallback) {
    $.ajax({
        url : url,
        contentType: "application/json",
        type : "GET",
        dataType: 'json',
        success : function(json){
            console.log(json);
            if(success){
                success(json);
            }
        },
        error : function(xhr, errmsg, err){
            $('#helper-msg').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    "</div>");
            console.log(xhr.status + ": " + xhr.responseText);
            console.log('---------------');
            console.log(xhr);
            console.log('---------------');
            console.log(err);
            if(errorCallback){
                errorCallback(err, errmsg);
            }
        }
    });
};

// todo error 함수 실행시 error json body 받아서 처리
PKC.prototype.doPost = function (url, post_body, success, errorCallback) {
    $.ajax({
        url : url,
        contentType: "application/json",
        type : "POST",
        dataType: 'json',
        data : JSON.stringify(post_body),
        success : function(json){
            console.log(json);
            if(success){
                success(json);
            }
        },
        error : function(xhr, errmsg, err){
            $('#helper-msg').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    "</div>");
            console.log(xhr.status + ": " + xhr.responseText);
            console.log('---------------');
            console.log(xhr);
            console.log('---------------');
            console.log(err);
            if(errorCallback){
                errorCallback(err, errmsg);
            }
        }
    });
};

// from here ajax request start
function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
