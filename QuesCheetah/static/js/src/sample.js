import "jquery";
import $ from "bootstrap";

import { qc } from "../quescheetah-init.js";

// This function is based on the site which has only one vote per pages.
// For using multiple votes in one page, getting ID(question / group) and
// cookie setting part should be changed.
export function Sample(){
    // Get id information from DOM element
    var qid = $('#systemjs-sample').attr('qid');
    var gid = $('#systemjs-sample').attr('gid');

    var params = {
        'group_id': gid,
        'question_id': qid
    };

    // Send request to API server
    if (gid){
        qc.getGroup(params, function(json){
            // Success callback function
            json = JSON.parse(json);
            // Transform DOM element for each question
            var questions_json = json['questions'];
            $.each(json['questions'], function(k,v){
                var value = questions_json[k];
                render_dom_element(k, value['id'], value['question_title'], json['answers'][k]);
            });
        })
    }else if (qid || !gid){
        qc.getQuestion(params, function(json){
            // Success callback function
            json = JSON.parse(json);
            // Transform DOM element for single question
            var questions_json = json['questions'];
            var value = questions_json[1];
            render_dom_element(1, value['id'], value['question_title'], json['answers'][1]);
        });
    }else {
        // Can't find any id info
        alert("Can't find any question info.");
    }

    // When user vote to your question, unique_user value is needed.
    // This value is used for identification between useranswer instances.
    function unique_set(myType){
        if (myType === "default"){
            // Use time value as unique user
            var d = new Date();
            return d.getTime();
        } else{
            // Set your site's user Id as unique user.
            // return your-site-user-id
        }
    }

    // Set JavaScript cookie after user vote.
    // This cookie is used when user visit your site again.
    // If browser has the cookie value, the user is only able to see results.
    // Default cookie Expiration date is 30 days.
    function check_cookie(q_id, exdays = 30){
        // Check user has our cookie.
        if (!document.cookie.match('(^|;)\\s*QuesCheetah'+q_id+'\\s*=\\s*([^;]+)')){
            // Set cookie for new user.
            var d = new Date();
            d.setTime(d.getTime() + (exdays*24*60*60*1000));
            var expires = "expires="+d.toUTCString();
            document.cookie = "QuesCheetah"+q_id+"=true; "+ expires;

            return false
        }else{
            // Show only results for already visited user.
            return true
        }
    }

    // Render DOM element with response data
    function render_dom_element(nth, q_id, title, answers){
        // Add nth question data to our tabs
        var tab_string = '<li tab='+nth+' role="presentation" q_id='+q_id+'>' +
            '<a href="#q'+q_id+'" aria-controls="q"'+q_id+' role="tab" data-toggle="tab">Q'+nth+'</a></li>';

        var answers_button_string = '';
        if (check_cookie(q_id)){
            // If user already answered this question, show result data in answer button
            $.each(answers, function(a_num,v){
                answers_button_string += '<button class="btn btn-default multi answerBtn" ' +
                    'type="button" disabled="disabled" a_num='+a_num+' q_id='+q_id+'>'+answers[a_num]['answer_text']+'<span class="badge">' +
                    answers[a_num]['answer_count']+'</span></button>';
            });
        }else{
            $.each(answers, function(a_num,v){
                answers_button_string += '<button class="btn btn-default multi answerBtn" ' +
                    'type="button" a_num='+a_num+' q_id='+q_id+'>'+answers[a_num]['answer_text']+'</button>';
            });
        }

        var tab_content_string = '<div role="tabpanel" class="tab-pane" id="q'+q_id+'">' +
            '<div class="panel panel-default">' +
            '<div class="panel-heading">' +
            '<h3 class="panel-title">'+title+'</h3></div>' +
            '<div class="panel-body">' +answers_button_string+
            '</div></div></div>';

        $('ul.nav-tabs').append(tab_string);
        $('.tab-content').append(tab_content_string);

        $('#systemjs-sample .nav-tabs li:first').addClass('active');
        $('#systemjs-sample .tab-pane:first').addClass('active');
        $('#systemjs-sample .nav-tabs a:first').tab('show');
    }

    // When user click the answer button
    $('#systemjs-sample').on("click", ".answerBtn", function(){
        var answer_num = $(this).attr('a_num');
        var question_id = $(this).attr('q_id');
        var unique_user = unique_set("default");
        var params = {
            "question_id": question_id,
            "answer_num": answer_num,
            "useranswer":{
                "unique_user": unique_user
            }
        };
        qc.createUserAnswer(params, function(){
            // Set cookie for answered question
            var d = new Date();
            d.setTime(d.getTime() + (30*24*60*60*1000));
            var expires = "expires="+d.toUTCString();
            document.cookie = "QuesCheetah"+params.question_id+"=true; "+ expires;

            $('.nav-tabs li[q_id="'+question_id+'"] a').html('<span class="glyphicon glyphicon-ok" aria-hidden="true"></span>');
            if(question_id == $('.answerBtn:last').attr('q_id')){
                // If this question is last question, show modal after finish.
                $('#systemjs-sample #resultModal').modal('show');
                setTimeout(function(){
                    location.reload();
                },2000);
            }else{
                var tab_num = $('.nav-tabs li[q_id="'+question_id+'"]').attr('tab');
                var next = parseInt(tab_num) + 1;
                $('.nav-tabs li[tab="'+next+'"] a').tab('show');
            }
        });
    });
}