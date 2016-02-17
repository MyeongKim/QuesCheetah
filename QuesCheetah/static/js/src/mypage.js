import {AjaxCall} from "../ajax_call.js";

export function Mypage(){
    $('#new-jwt-btn').click(function(e){
        e.preventDefault();
        var post_data = {
            "api-key": $('#key_value').attr('value'),
            "secret-key": $('#secret_value').attr('value')
        };

        if ($("#exp").val()){
            post_data["exp"] = Math.round(new Date($('#exp').val()).getTime()/1000)
        }

        if ($('#nbf').val()){
            post_data["nbf"] = Math.round(new Date($('#nbf').val()).getTime()/1000)
        }

        var empty = false;
        $.each(post_data, function(key, value){
            if (!value){
                alert("You should create api key and secret key first.");
                empty = true
            }
        });

        if (!empty){
            AjaxCall('/jwt/new', post_data, function(data){
                alert(JSON.stringify(data));
            })
        }
    });
}
