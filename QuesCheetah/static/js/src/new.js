import "jquery";
import $ from "bootstrap";

import { qc } from "../quescheetah-init.js";

function escapeHtml(text) {
  return text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
}

export function New(){
    var tabCount = 1;
    $(".nav-tabs").on("click", "a", function (e) {
        e.preventDefault();
        if (!$(this).hasClass('add-contact')) {
            $(this).tab('show');
        }
    })
        .on("click", "span", function () {
            var anchor = $(this).siblings('a');
            $(anchor.attr('href')).remove();
            anchor.parent().prev().children('a').click();
            $(this).parent().remove();


            $('.nav-tabs li').children('a').each(function(index){
                if(!$(this).is('.add-contact')){
                    $(this).text('question_'+(parseInt(index)+1));
                }
            });

            if ($(".nav-tabs").children().length < 11){
                $('.add-contact').show();
            }
            if ($(".nav-tabs").children().length < 3){
                $('.group-form').hide();
            }

        });

    $('.add-contact').click(function (e) {
        e.preventDefault();
        var id = tabCount+1;
        var tabLength = $(".nav-tabs").children().length;
        if(tabLength >= 2){
            $('.group-form').show();
        }
        if(tabLength > 10){
        }else {
            tabCount = tabCount+1;
            var tabId = 'question_' + id;
            $(this).closest('li').before('<li><a href="#question_' + id + '">question_' + tabLength + '</a> <span> x </span></li>');
            var append_string = '<div class="tab-pane" id="' + tabId + '">' +
                '<form class="form-horizontal" action="" method="post">\
                <input type="hidden" value="{{ api_key }}" name="api_key">\
                    <div class="form-group">\
                        <label for="question_title" class="col-sm-2 control-label">질문 제목</label>\
                        <div class="col-sm-10">\
                            <input type="text" class="form-control" id="question_title" name="question_title" placeholder="관리자가 보는 질문 제목을 입력하세요.(중복 불가)">\
                        </div>\
                    </div>\
                    <div class="form-group">\
                        <label for="question_text" class="col-sm-2 control-label">질문</label>\
                        <div class="col-sm-10">\
                            <input type="text" class="form-control" id="question_text" name="question_text" placeholder="질문을 입력하세요.">\
                        </div>\
                    </div>\
                    <hr>\
                    <div class="answer-wrapper">\
                        <div class="form-group answer">\
                            <label for="answer1" class="col-sm-2 control-label">보기1</label>\
                            <div class="col-sm-10">\
                                <input type="text" class="form-control" id="answer1" placeholder="answer1", name="answer1">\
                            </div>\
                        </div>\
                        <div class="form-group answer">\
                            <label for="answer2" class="col-sm-2 control-label">보기2</label>\
                            <div class="col-sm-10">\
                                <input type="text" class="form-control" id="answer2" placeholder="answer2", name="answer2">\
                            </div>\
                        </div>\
                    </div>\
                    <div>\
                        <button class="btn btn-info add-answer-btn" id="">보기 추가하기</button>\
                    </div>\
                    <hr>\
                </form></div>';
            $('.tab-content').append(append_string);
            $('.nav-tabs li:nth-child(' + id + ') a').click();
            if(tabLength == 10){
                $(this).hide();
            }
        }
    });

    $('.row').on('click', ".add-answer-btn",function (e) {
        e.preventDefault();
        var newNum = $('.tab-pane.active .answer-wrapper .answer').length + 1;
        if(newNum > 10){
        }else{
            $('.tab-pane.active .answer-wrapper').append('<div class="form-group answer">\
                    <label for="answer'+newNum+'" class="col-sm-2 control-label">보기'+newNum+'</label>\
                    <div class="col-sm-10">\
                        <input type="text" class="form-control" id="answer'+newNum+'" placeholder="answer'+newNum+'", name="answer'+newNum+'">\
                    </div>\
                </div>');
            if(newNum > 8){
                $('.add-answer-btn').hide()
            }
        }
    });

    $('#make-btn').click(function (e) {
        e.preventDefault();

        var group_name = escapeHtml($('#group_name').val());
        var questions = {};
        var answers = {};
        var q_length = $('.tab-pane').length;

        // check datetime conditions
        var start_dt = $('#start_dt').val();
        var end_dt = $('#end_dt').val();

        var start_dt_convert = new Date(start_dt);
        var end_dt_convert = new Date(end_dt);
        var curr_dt = new Date();

        if (start_dt_convert < curr_dt ){
            $('#new-error').html('<p class="alert alert-danger">start_dt value should be larger than current time.</p>');
            return false;
        } else if (start_dt_convert > end_dt_convert){
            $('#new-error').html('<p class="alert alert-danger">end_dt value shoudl be larger than start_dt value.</p>');
            return false;
        }

        if( ($('.group-form').css('display') !== 'none') && ($('.group-form input').val() == '') ){
            $('#new-error').html('<p class="alert alert-danger">Group name is needed to make multiple questions.</p>');
        }else {
            // set optional values
            var is_editable = $('input[name="is_editable"]').is(':checked');
            var is_private = $('input[name="is_private"]').is(':checked');

            for (var i = 1; i <= q_length || function () {
                console.log(questions);
                console.log(answers);
                var params = {
                    'group_name': group_name,
                    'questions': questions,
                    'answers': answers
                };
                qc.createGroup(params, function(){
                    location.reload();
                });
                location.reload();
                return false;
            }(); i++) {
                var question_title = escapeHtml($('#question_' + i + ' input[name="question_title"]').val());
                var question_text = escapeHtml($('#question_' + i + ' input[name="question_text"]').val());
                questions[i] = {
                    'question_title': question_title,
                    'question_text': question_text,
                    'question_num': i,
                    'start_dt': start_dt,
                    'end_dt': end_dt,
                    'is_editable': is_editable,
                    'is_private': is_private
                };

                answers[i] = {};
                for (var j = 1; j <= 9; j++) {
                    (function (new_j) {
                        var answer_text = escapeHtml($('#question_' + i + ' input[name="answer' + new_j + '"]').val());
                        if (answer_text) {
                            answers[i][new_j] = {
                                'answer_text': answer_text
                            };
                        }
                    })(j);
                }
            }
        }
    });
}