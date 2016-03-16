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
            if (!value || value=='None'){
                $('#jwt-error').addClass('alert');
                $('#jwt-error').addClass('alert-danger');
                $('#jwt-error').html('You should create api key and secret key first.');
                empty = true
            }
            else{
                $('#jwt-error').removeClass('alert');
                $('#jwt-error').removeClass('alert-danger');
                $('#jwt-error').text('');
            }
        });

        if (!empty){
            AjaxCall('/jwt/new', post_data, function(data){
                alert(JSON.stringify(data));
            })
        }
    });

    // Delete enrolled domain instance
    $('.domain-delete-btn').click(function(){
        var domain_id = $(this).attr('d_id');

        AjaxCall('/domain/delete', {'d_id': domain_id}, function(json){
            if(json.status == 'success'){
                location.reload();
            }else{
                alert("Delete request failed.");
            }
        });
    });

}
