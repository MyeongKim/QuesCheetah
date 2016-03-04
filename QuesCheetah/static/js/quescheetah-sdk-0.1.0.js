function QuesCheetah(config){
    this.apiKey = config.apiKey;
    this.baseUrl = "http://127.0.0.1:8000/v1/";
    this.callBackUrl = config.callBackUrl;
    this.receiveRealtimeResponse = config.receiveRealtimeResponse;

    // If Realtime socket.io Response is used.
    if (this.receiveRealtimeResponse){
        socket = io('http://localhost:5000');
        socket.on('connect', function(){});
        socket.on('event', function(data){});
        socket.on('disconnect', function(){});
        socket.on('reply', function(data){
            alert(JSON.stringify(data));
        });
    }
}

var socket= "";

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
    var self = this;
    var url = this.baseUrl+'questions/'+params.question_id+'/answers/'+params.answer_num+'/useranswers';
    var successWithSend = function(){
        success();

        // If client realtime setting is true, send question_id to socket server.
        if (self.receiveRealtimeResponse){
            self.socketioAction($.extend({
                "api-key": self.apiKey
            },params));
        }
    };
    this.doPost(url, "POST", params, successWithSend, error)
};

QuesCheetah.prototype.getGroup = function (params, success, error) {
    var url = this.baseUrl+'groups/'+params.group_id;
    this.doPost(url, "GET", params, success, error)
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
    var self = this;
    var request = new XMLHttpRequest();
    request.open(type, url, true);

    // you can use jwt with kid header instead of api-key header for more secure connection.
    //request.setRequestHeader("jwt", "your jwt value");
    //request.setRequestHeader("kid", "2");

    request.setRequestHeader("api-key", self.apiKey);
    request.setRequestHeader("Content-Type", "application/json");

    request.onload = function () {
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

// Receiving realtime socket.io data
QuesCheetah.prototype.socketioAction = function(data){
    socket.emit('send', data);
};