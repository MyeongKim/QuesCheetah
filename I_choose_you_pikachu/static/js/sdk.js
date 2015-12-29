// This javascript file must be inserted after the jQuery file.
function PKC(config){
    this.apiKey = config.apiKey;
    this.baseUrl = "http://localhost:8000/vote/";
    this.callBackUrl = config.callBackUrl;
}


PKC.prototype.createQuestion = function (params, success, error) {
    var url = this.baseUrl+'question/create';
    this.doPost(url, params, error, success)
};

PKC.prototype.createAnswer = function (params, success, error) {
    var url = this.baseUrl+'answer/create';
    this.doPost(url, params, error, success)
};

PKC.prototype.createMultipleQuestion = function (params, success, error) {
    if ( params['group_name'] === ""){
        this.createSingleQuestion(params, success, error);
    }else{
        var url = this.baseUrl+'multiple/create';
        this.doPost(url, params, error, success);
    }
};

PKC.prototype.createSingleQuestion = function (params, success, error) {
    var url = this.baseUrl+'single/create';
    this.doPost(url, params, error, success)
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
PKC.prototype.doPost = function (url, post_body, errorCallback, success) {
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
