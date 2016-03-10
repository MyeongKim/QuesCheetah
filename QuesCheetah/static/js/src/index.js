import {AjaxCall} from "../ajax_call.js";

function escapeHtml(text) {
  return text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
}

export function Index() {
    $('#signup-form').on('submit', function(e){
        e.preventDefault();
        var email = escapeHtml($('#signup-email').val());
        var username = escapeHtml($('#signup-username').val());
        var password = escapeHtml($('#signup-password').val());
        var password2 = escapeHtml($('#signup-password2').val());

        if (password === password2 ){
            AjaxCall('signup', {email : email ,username:username, password : password}, function(json){
                if(json.status){
                    $('#tab-helper-msg').html("<div class='alert-box alert radius' data-alert>Welcome!</div>");
                    $("#login-tab a").click();
                    $('#signup-email').val('');
                    $('#signup-username').val('');
                    $('#signup-password').val('');
                    $('#signup-password2').val('');
                } else {
                    $('#tab-helper-msg').html("<div class='alert-box alert radius' data-alert>"+json.msg+
                        "</div>");
                }
            });
        } else {
            $('#tab-helper-msg').html("<div class='alert-box alert radius' data-alert>비밀번호가 일치하지 않습니다.</div>");
            $('#signup-password').val('');
            $('#signup-password2').val('');
        }
    });

    $('#login-form').on('submit', function(e){
        e.preventDefault();
        var email = escapeHtml($('#signin-email').val());
        var password = escapeHtml($('#signin-password').val());
        AjaxCall('login', {email : email, password : password}, function(json){
            if(json.status === 'success'){
                location.reload();
            }
        });
    });
}
