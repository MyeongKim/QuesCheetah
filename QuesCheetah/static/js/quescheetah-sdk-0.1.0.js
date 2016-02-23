// This javascript file must be inserted after the jQuery file.
function QuesCheetah(config){
    this.apiKey = config.apiKey;
    this.baseUrl = "http://127.0.0.1:8000/v1/";
    this.callBackUrl = config.callBackUrl;
}

QuesCheetah.prototype.createGroup = function (params, success, error) {
    if ( params['group_name'] === ""){
        this.createQuestion(params, success, error);
    }else{
        var url = this.baseUrl+'groups';
        this.doPost(url, "POST", params, success, error);
    }
};

QuesCheetah.prototype.createQuestion = function (params, success, error) {
    var url = this.baseUrl+'questions';
    this.doPost(url, "POST", params, success, error)
};

QuesCheetah.prototype.createAnswer = function (params, success, error) {
    var url = this.baseUrl+'questions/'+params.question_id+'/answers';
    this.doPost(url, "POST", params, success, error)
};

QuesCheetah.prototype.createUserAnswer = function (params, success, error) {
    var url = this.baseUrl+'questions/'+params.question_id+'/answers/'+params.answer_num+'/useranswers';
    this.doPost(url, "POST", params, success, error)
};

QuesCheetah.prototype.getQuestion = function (params, success, error) {
    var url = this.baseUrl+'questions/'+params.question_id;
    this.doPost(url, "GET", params, success, error)
};

QuesCheetah.prototype.getAnswer = function (params, success, error) {
    var url = this.baseUrl+'questions/'+params.question_id+'/answers/'+params.answer_num;
    this.doPost(url, "GET", params, success, error)
};

QuesCheetah.prototype.updateQuestion = function (params, success, error) {
    var url = this.baseUrl+'questions/'+params.question_id;
    this.doPost(url, "PUT", params, success, error)
};

QuesCheetah.prototype.deleteAnswer = function (params, success, error) {
    var url = this.baseUrl+'questions/'+params.question_id+'/answers/'+params.answer_num;
    this.doPost(url, "DELETE", params, success, error)
};

QuesCheetah.prototype.deleteUserAnswer = function (params, success, error) {
    var url = this.baseUrl+'questions/'+params.question_id+'/answers/useranswers/'+params.unique_user;
    this.doPost(url, "DELETE", params, success, error)
};

QuesCheetah.prototype.deleteQuestion = function (params, success, error) {
    var url = this.baseUrl+'questions/'+params.question_id;
    this.doPost(url, "DELETE", params, success, error)
};

QuesCheetah.prototype.deleteGroup = function (params, success, error) {
    var url = this.baseUrl+'groups/'+params.group_id;
    this.doPost(url, "DELETE", params, success, error)
};

QuesCheetah.prototype.updateUserAnswer = function (params, success, error) {
    var url = this.baseUrl+'questions/'+params.question_id+'/answers/useranswers/'+params.unique_user;
    this.doPost(url, "PUT", params, success, error)
};

QuesCheetah.prototype.doPost = function (url, type, post_body, success, errorCallback) {
    var request = new XMLHttpRequest();
    request.open(type, url, true);

    // you can use jwt with kid header instead of api-key header for more secure connection.
    //request.setRequestHeader("jwt", "your jwt value");
    //request.setRequestHeader("kid", "2");

    request.setRequestHeader("api-key", "a6a9bc92735ef12e8ba952265f334ba65739b5fc");
    request.setRequestHeader("Content-Type", "application/json");

    request.onreadystatechange = function () {
        if (request.status >= 200 && request.status < 400) {
            var json = request.responseText;
            if (json.error) {
                if (errorCallback) {
                    errorCallback()
                }
                console.log(json.description);
            } else {
                if (success) {
                    success(json);
                }
            }
        } else {
            alert('There was a problem with the request.');

        }
    };

    request.onerror = function (e) {
        alert("Error " + e.target.status + " occurred while receiving the document.");
    };
    request.send(JSON.stringify(post_body));
};