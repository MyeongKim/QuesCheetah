import "jquery";
//import $ from "bootstrap";

import { qc } from "../quescheetah-init.js";

export function Select(){
    function reload(){
        location.reload();
    }

    $('.multi-delete-btn').click(function(e){
        e.preventDefault();
        var choice = confirm("Are you sure?");
        if (choice){
            var params = {
                'group_id': $(this).attr('gid')
            };
            qc.apiKey = $('input[name="api_key"]').val();
            qc.deleteGroup(params, reload);
        }
    });

    $('.single-delete-btn').click(function(e){
        e.preventDefault();
        var choice = confirm("Are you sure?");
        if (choice){
            var params = {
                'question_id': $(this).attr('qid'),
                'question_title': $(this).attr('qt')
            };
            qc.apiKey = $('input[name="api_key"]').val();
            qc.deleteQuestion(params, reload);
        }
    });

    // Filter elements
    $('#group-filter').click(function(){
       if($(this).is(':checked')){
           $('.group-questions').show();
       }else{
           $('.group-questions').hide();
       }
    });

    $('#single-filter').click(function(){
       if($(this).is(':checked')){
           $('.single-question').show();
       }else{
           $('.single-question').hide();
       }
    });
}