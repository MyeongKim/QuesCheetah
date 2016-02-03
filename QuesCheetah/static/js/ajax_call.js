import $ from "jquery";

export function AjaxCall(url, params, successCallback) {
    //from index
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
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // from mypage
    $.ajax({
        url: url,
        contentType: "application/json",
        type: "POST",
        dataType: 'json',
        data: JSON.stringify(params),
        success: successCallback,
        error : function(xhr, errmsg, err){
            $('#tab-helper-msg').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                "</div>");
            console.log(xhr.status + ": " + xhr.responseText);
            console.log('---------------');
            console.log(xhr);
            console.log('---------------');
            console.log(err);
        }
    });
}