import "jquery";

import { qc } from "qc-init";

export function Action() {
    function unique_set(myType) {
        //if (myType === "default"){
        var d = new Date();
        return d.getTime();
        //}
    }

    $('.single.answerBtn').click(function () {
        var update_num = $(this).attr('a_num');
        var question_title = "";
        var question_id = $(this).attr('q_id');
        var unique_user = unique_set("default");
        var params = {
            'question_title': question_title,
            'question_id': question_id,
            'answer_num': update_num,
            "useranswer":{
                "unique_user": unique_user
            }
        };
        qc.createUserAnswer(params, function () {
            location.reload();
        });
    });
}