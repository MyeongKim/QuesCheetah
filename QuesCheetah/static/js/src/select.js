import "jquery";
//import $ from "bootstrap";

import { qc } from "../quescheetah-init.js";

export function Select(){
    function reload(){
        //location.reload();
    }

    $('.multi-delete-btn').click(function(){
        var choice = confirm("Are you sure?");
        if (choice){
            var params = {
                'group_id': $(this).attr('gid')
            };
            qc.deleteGroup(params, reload);
        }

    });

    $('.single-delete-btn').click(function(){
        var choice = confirm("Are you sure?");
        if (choice){
            var params = {
                'question_id': $(this).attr('qid'),
                'question_title': $(this).attr('qt')
            };
            qc.deleteQuestion(params, reload);
        }
    });
}