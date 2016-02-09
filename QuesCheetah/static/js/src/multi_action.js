import "jquery";
import $ from "bootstrap";

import { qc } from "qc-init";

export function MultiAction(){
    function unique_set(myType){
        //if (myType === "default"){
        var d = new Date();
        return d.getTime();
        //}
    }
    var last_question_id = $('.answerBtn:last').attr('q_id');
    $('.multi.answerBtn').click(function () {
        var update_num = $(this).attr('a_num');
        var question_id = $(this).attr('q_id');
        var unique_user = unique_set("default");
        var params = {
            'question_id': question_id,
            'answer_num': update_num,
            'unique_user': unique_user
        };
        qc.createUserAnswer(params, function(){
            $('.nav-tabs li[q_id="'+question_id+'"] a').html('<span class="glyphicon glyphicon-ok" aria-hidden="true"></span>');
            if(question_id == last_question_id){
                $('#resultModal').modal('show');
                setTimeout(function(){
                    location.reload();
                },2000);
            }else{
                var next = parseInt(question_id) + 1;
                $('.nav-tabs li[q_id="'+next+'"] a').tab('show');
            }
        });
    });

    $('.nav-tabs li:first').addClass('active');
    $('.tab-pane:first').addClass('active');
    $('#myTabs a:first').tab('show');
}