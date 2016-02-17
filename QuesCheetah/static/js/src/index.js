import {AjaxCall} from "../ajax_call.js";

export function Index() {
    $('#signup-form').on('submit', function(e){
        e.preventDefault();
        var email = $('#signup-email').val();
        var username = $('#signup-username').val();
        var password = $('#signup-password').val();
        var password2 = $('#signup-password2').val();

        if (password === password2 ){
            AjaxCall('signup', {email : email ,username:username, password : password}, function(json){
                if(json.status){
                    $('#tab-helper-msg').html("<div class='alert-box alert radius' data-alert>"+json.msg+"</div>");
                    $("#login-tab").tab('show');
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
        var email = $('#signin-email').val();
        var password = $('#signin-password').val();
        AjaxCall('login', {email : email, password : password}, function(json){
            if(json.status === 'success'){
                location.reload();
            }
        });
    });
}
