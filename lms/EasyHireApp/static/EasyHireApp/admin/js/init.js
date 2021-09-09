(function($) {
    $(function() {
        $('.sidenav').sidenav();
        $('.dropdown-trigger').dropdown({
            constrainWidth: false,
            alignment: 'left'
        });
        $('.collapsible').collapsible();
        $('.modal').modal();
        $('.tabs').tabs();
        $('select').select2({
            width: "100%"
        });
        $('.slider').slider();
        $('.tooltipped').tooltip({
            position: 'top'
        });
        $('.datepicker').datepicker({
            format: "dd/mm/yyyy"
        });
        $('.fixed-action-btn').floatingActionButton();
        $(".readable-pro-tooltipped").tooltip({
            position: "top"
        });
    }); // end of document ready
})(jQuery); // end of jQuery name space

$(window).keyup(function(e){
      if(e.keyCode == 44){
        $("body").hide();
      }

});

/*--------------------------
    preloader
---------------------------- */
$(window).on('load', function() {
    var pre_loader = $('#global-preloader');
    pre_loader.fadeOut('slow', function() {
        $(this).remove();
    });
});

function showGlobalPreloader() {
    $("#global-preloader").show(500);
}

function hideGlobalPreloader() {
    $("#global-preloader").hide(500);
}

function getCsrfToken() {
    var CSRF_TOKEN = $('input[name="csrfmiddlewaretoken"]').val();
    return CSRF_TOKEN;
}

function validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

function showToast(message, duration) {
    M.toast({
        "html": message
    }, duration);
}

function hideChoiceDiv() {
    $("#div-problem-choices").hide();
    $("#div-problem-correct-choices").hide();
}

function showChoiceDiv() {
    $("#div-problem-choices").show();
    $("#div-problem-correct-choices").show();
    hideDescriptiveDiv();
}

function showDescriptiveDiv() {
    $("#div-problem-solution").show();
    $("#div-problem-hint").show();
    hideChoiceDiv();
}

function hideDescriptiveDiv() {
    $("#div-problem-solution").hide();
    $("#div-problem-hint").hide();
}

function getEmbedVideoURL(url) {
    var regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
    var match = url.match(regExp);

    if (match && match[2].length == 11) {
        return "https://www.youtube.com/embed/" + match[2];
    } else {
        return url;
    }
}

function scrollToGivenElementId(element_id) {
    $('html, body').animate({
        scrollTop: $("#" + element_id).offset().top - 100
    }, 500);
}

function focusAtGivenElementID(element_id) {
    $("#" + element_id).focus();
}

function isCanvasBlank(canvas) {
    var blank = document.createElement('canvas');
    blank.width = canvas.width;
    blank.height = canvas.height;

    return canvas.toDataURL() == blank.toDataURL();
}

function showProfileRegisterCardPanel() {
    $("#profile-register-card-panel").show();
    $("#profile-verification-card-panel").hide();
    capturePictureInit();
}

function showProfileVerificationCardPanel() {
    $("#profile-register-card-panel").hide();
    $("#profile-verification-card-panel").show();
}

if(window.location.pathname=="/master-list/create-administrator/"){
  $(document).ready(function(){
      var table = $('#table-coordinator-details').DataTable();
      setTimeout(function(){
          window.location.reload();
      }, 300000);
  });
}

if(window.location.pathname=="/administrator/manage-applicants/"){
  $(document).ready(function(){
      var table = $('#manage-applicants-table').DataTable({
        "aLengthMenu": [[100,200,500, -1], [100,200,500, "All"]],
        "iDisplayLength": 100
        //"pageLength": 200
      });
      $('select').select2({
            width: "100%"
        });
      setTimeout(function(){
          window.location.reload();
      }, 300000);
  });
}
if(window.location.pathname=="/master-list/institutes/"){
  $(document).ready(function(){
      var table = $('#table-group-discussion-details').DataTable();
      setTimeout(function(){
          window.location.reload();
      }, 300000);
  });
}
$(document).on("click", "#btn-search-applicant", function(e) {

    var search_parameter_list = $("#multiple-select-applicant-search").val();
    var date = document.getElementById("startdate").value;
    if (search_parameter_list.length > 0)
    {
        search_url = "/administrator/manage-applicants?";
        /*if(date != ""){
              search_url += "date=" + date;
        }
        search_url += "&"*/
        for (var i = 0; i < search_parameter_list.length; i++)
        {
            var variable_list = search_parameter_list[i].split("_");
            var value = variable_list[variable_list.length - 1];

            if(variable_list.indexOf("institute") != -1)
            {
                search_url += "institute=" + value;
            }
            else if(variable_list.indexOf("department") != -1)
            {
                search_url += "department=" + value;
            }
            else if(variable_list.indexOf("stream") != -1)
            {
                search_url += "stream=" + value;
            }
            else if(variable_list.indexOf("event") != -1)
            {
                search_url += "event=" + value;
            }
            else if(variable_list.indexOf("group") != -1)
            {
                search_url += "group=" + value;
            }
            else if(variable_list.indexOf("quiz")!=-1){
                search_url += "quiz=" + value;
            }
            else if(value == "1")
            {
                search_url += "is_rejected=" + "True";
            }
            else if(value == "2")
            {
                search_url += "is_selected=" + "True";
            }
            else if(value == "3")
            {
                search_url += "is_nonapproved=" + "True";
            }
            else if(value == "4")
            {
                search_url += "is_campus=" + "True";
            }
            else if(value == "5")
            {
                search_url += "is_walkin=" + "True";
            }
            else if(value == "6")
            {
                search_url += "is_posting=" + "True";
            }
            else if(value == "7")
            {
                search_url += "is_male=" + "True";
            }
            else if(value == "8")
            {
                search_url += "is_female=" + "True";
            }
            else if(value == "9")
            {
                search_url += "is_others=" + "True";
            }
            else if(value == "10")
            {
                search_url += "all=" + "True";
            }
            else if(value == "11"){
                search_url += "quiz_not_assigned"
            }
            else if(value == "12"){
                search_url += "quiz_assigned"
            }
            else if(value == "13"){
                search_url += "quiz_assigned_between"
                let range_start_date = $('#quiz-assigned-start-date').val();
                let range_end_date = $('#quiz-assigned-end-date').val();
                let date1 = new Date(range_start_date);
                let date2 = new Date(range_end_date);

                console.log(date1, date2);

                if(date1 == "Invalid Date" || date2 == "Invalid Date" || date1>date2){
                    showToast("Enter valid date range for quiz assigned", 2000);
                    return;
                }

                search_url+="&qa_start="+range_start_date + "&qa_end=" + range_end_date;
            }
            else if(value == "14"){
                search_url += "quiz_completed"
            }
            else if(value == "15"){
                search_url += "quiz_completed_between"
                let range_start_date = $('#quiz-completed-start-date').val();
                let range_end_date = $('#quiz-completed-end-date').val();
                let date1 = new Date(range_start_date);
                let date2 = new Date(range_end_date);

                console.log(date1, date2);

                if(date1 == "Invalid Date" || date2 == "Invalid Date" || date1>date2){
                    showToast("Enter valid date range for quiz completed", 2000);
                    return;
                }

                search_url+="&qc_start="+range_start_date + "&qc_end=" + range_end_date;
            }
            else if(value == "16"){
                search_url += "registered_between"
                let range_start_date = $('#registered-between-start-date').val();
                let range_end_date = $('#registered-between-end-date').val();
                let date1 = new Date(range_start_date);
                let date2 = new Date(range_end_date);

                console.log(date1, date2);

                if(date1 == "Invalid Date" || date2 == "Invalid Date" || date1>date2){
                    showToast("Enter valid date range registration filter", 2000);
                    return;
                }

                search_url+="&r_start="+range_start_date + "&r_end=" + range_end_date;
            }
            if (i != search_parameter_list.length - 1) {
                search_url += "&"
            }
        }
        window.location = search_url;
    }
    else
    {
        window.location = "/administrator/manage-applicants/";
    }
});

$(document).on("change", "#global-selected-applicants", function(e) {
    is_checked = document.getElementById("global-selected-applicants").checked;
    selected_problem_list = document.getElementsByClassName("selected-applicant");
    for (var i = 0; i < selected_problem_list.length; i++) {
        id = selected_problem_list[i].id;
        document.getElementById(id).checked = is_checked;
    }

    $(".selected-applicant").change();
});

$(document).on("change", ".selected-applicant", function(e){
    selected_applicant_list = document.getElementsByClassName("selected-applicant");
    show_add_next_round_button = false;
    for (var i = 0; i < selected_applicant_list.length; i++) {
        id = selected_applicant_list[i].id;
        if (document.getElementById(id).checked == true) {
            show_add_next_round_button = true;
            break;
        }
    }

    if (show_add_next_round_button == true) {
        $("#btn-assign-task").removeAttr('disabled');
        $("#btn-applicant-status").removeAttr('disabled');
        $("#btn-save-applicant-irecruit").removeAttr('disabled');
        $('#btn-assign-tag').removeAttr('disabled');
    } else {
        $("#btn-assign-task").attr('disabled','disabled');
        $("#btn-applicant-status").attr('disabled','disabled');
        $("#btn-save-applicant-irecruit").attr('disabled','disabled');
        $('#btn-assign-tag').attr('disabled', 'disabled');
    }
});

function get_list_of_selected_applicants(){
    selected_applicant_list = document.getElementsByClassName("selected-applicant");
    applicant_id_list = [];
    for (var i = 0; i < selected_applicant_list.length; i++) {
        id = selected_applicant_list[i].id;
        if(document.getElementById(id).checked){
            id_item_list = id.split("-");
            applicant_id_list.push(id_item_list[id_item_list.length-1]);            
        }
    }        
    return applicant_id_list;
}
function save_applicants_at_irecruit(element){
    selected_applicant_id_list = get_list_of_selected_applicants();
    if(selected_applicant_id_list == ""){
      showToast("Please select a candidate.", 2000);
      return;
    }
    json_string = JSON.stringify({
        selected_applicant_id_list:selected_applicant_id_list
    });
    var CSRF_TOKEN = getCsrfToken();
    element.innerHTML = "Saving...";
    $.ajax({
       url: '/administrator/save-applicant-at-irecruit/',
       type: 'POST',
       headers: {
           'X-CSRFToken': CSRF_TOKEN
       },
       data: {
           data: json_string
       },
       success: function(response) {
           if (response["status_code"] == 200) {
            window.location.reload();
           } else if(response["status_code"]==101) {
               showToast(response["status_message"], 2000);
               console.log("Please report this. ", response["status_message"]);
           }else{
               showToast("Unable to push due to some internal server error. Kindly report the same", 2000);
               console.log("Please report this. ", response["status_message"]);            
           }
            element.innerHTML = "iRecruit";
       },
       error: function(xhr, textstatus, errorthrown){
           console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
            element.innerHTML = "iRecruit";
       }
   });
}

//function assign_task_applicants(element){
//    selected_next_round = document.getElementById("selected-next-round").value;
//    selected_quiz_for_next_round = document.getElementById("selected-quiz-for-next-round").value;
//    selected_group_for_next_round = document.getElementById("selected-group-for-next-round").value;
//    selected_bot_for_next_round = document.getElementById("selected-bot-for-next-round").value;
//    quiz_start_date = document.getElementById("input-quiz-start-date").value;
//    quiz_start_time = document.getElementById("input-quiz-start-time").value;
//    quiz_end_date = document.getElementById("input-quiz-end-date").value;
//    quiz_end_time = document.getElementById("input-quiz-end-time").value;
//    selected_applicant_id_list = get_list_of_selected_applicants();
//
//    json_string = JSON.stringify({
//        selected_next_round:selected_next_round,
//        selected_quiz_for_next_round:selected_quiz_for_next_round,
//        selected_group_for_next_round:selected_group_for_next_round,
//        selected_bot_for_next_round:selected_bot_for_next_round,
//        quiz_start_time:quiz_start_time,
//        quiz_start_date:quiz_start_date,
//        quiz_end_date:quiz_end_date,
//        quiz_end_time:quiz_end_time,
//        selected_applicant_id_list:selected_applicant_id_list
//    });
//
//    var CSRF_TOKEN = getCsrfToken();
//    element.innerHTML = "Assigning...";
//    $.ajax({
//       url: '/administrator/assign-task/',
//       type: 'POST',
//       headers: {
//           'X-CSRFToken': CSRF_TOKEN
//       },
//       data: {
//           data: json_string
//       },
//       success: function(response) {
//           if (response["status_code"] == 200) {
//               console.log(response)
//               showToast(response["status_message"], 2000)
//               window.location.reload();
//           } else if(response["status_code"]==101) {
//               showToast(response["status_message"], 2000);
//               console.log("Please report this. ", response["status_message"]);
//           }else{
//               showToast("Unable to schedule due to some internal server error. Kindly report the same", 2000);
//               console.log("Please report this. ", response["status_message"]);            
//           }
//            element.innerHTML = "Assign Task";
//       },
//       error: function(xhr, textstatus, errorthrown){
//           console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
//            element.innerHTML = "Assign Task";
//       }
//   });
//}


function assign_task_applicants(element){
    selected_next_round = document.getElementById("selected-next-round").value;
    selected_quiz_for_next_round = document.getElementById("selected-quiz-for-next-round").value;
    selected_group_for_next_round = document.getElementById("selected-group-for-next-round").value;
    selected_bot_for_next_round = document.getElementById("selected-bot-for-next-round").value;
    quiz_start_date = document.getElementById("input-quiz-start-date").value;
    quiz_start_time = document.getElementById("input-quiz-start-time").value;
    quiz_end_date = document.getElementById("input-quiz-end-date").value;
    quiz_end_time = document.getElementById("input-quiz-end-time").value;
    selected_applicant_id_list = get_list_of_selected_applicants();

    json_string = JSON.stringify({
        selected_next_round:selected_next_round,
        selected_quiz_for_next_round:selected_quiz_for_next_round,
        selected_group_for_next_round:selected_group_for_next_round,
        selected_bot_for_next_round:selected_bot_for_next_round,
        quiz_start_time:quiz_start_time,
        quiz_start_date:quiz_start_date,
        quiz_end_date:quiz_end_date,
        quiz_end_time:quiz_end_time,
        selected_applicant_id_list:selected_applicant_id_list
    });

    var CSRF_TOKEN = getCsrfToken();
    element.innerHTML = "Assigning...";
    $.ajax({
       url: '/administrator/assign-task/',
       type: 'POST',
       headers: {
           'X-CSRFToken': CSRF_TOKEN
       },
       data: {
           data: json_string
       },
       success: function(response) {
           console.log("s")
           if (response["status_code"] == 200) {
               console.log(response)
               showToast(response["status_message"], 2000)
               window.location.reload();
           } else if(response["status_code"]==101) {

                //M.toast({html: 'Please note down the error page will be refreshed <button class="btn-flat toast-action" onclick="window.location.reload()">Reload</button>'})
                response.errors.map(error =>{
                    showToast(error, 50000)
                })
           }else{
               showToast("Unable to schedule due to some internal server error. Kindly report the same", 2000);
               console.log("Please report this. ", response["status_message"]);            
           }
            element.innerHTML = "Assign Task";
       },
       error: function(xhr, textstatus, errorthrown){
           console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
            element.innerHTML = "Assign Task";
       }
   });
}

function download_applicant_report(element){
    showToast("Creating candidate report. Please wait.", 200000);
    selected_applicant_id_list = get_list_of_selected_applicants();
    if(selected_applicant_id_list == ""){
      showToast("Please select a candidate.", 2000);
      return;
    }
    json_string = JSON.stringify({
        selected_applicant_id_list:selected_applicant_id_list
    });
    var CSRF_TOKEN = getCsrfToken();
    //element.innerHTML = "Downloading...";
    $.ajax({
       url: '/administrator/download-applicant-report/',
       type: 'POST',
       headers: {
           'X-CSRFToken': CSRF_TOKEN
       },
       data: {
           data: json_string
       },
       success: function(response) {
           if (response["status_code"] == 200) {
               var file_url = response["file_url"];
              url = window.location.origin + file_url
            window.open(url)
           } else if(response["status_code"]==101) {
               showToast(response["status_message"], 2000);
               console.log("Please report this. ", response["status_message"]);
           }else{
               showToast("Unable to download due to some internal server error. Kindly report the same", 2000);
               console.log("Please report this. ", response["status_message"]);            
           }
            //element.innerHTML = "Download Report";
       },
       error: function(xhr, textstatus, errorthrown){
           console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
            element.innerHTML = "Download Report";
       }
   });
}

function accepted_applicants(element){

    selected_applicant_id_list = get_list_of_selected_applicants();

    json_string = JSON.stringify({
        selected_applicant_id_list:selected_applicant_id_list
    });

    var CSRF_TOKEN = getCsrfToken();
    element.innerHTML = "Changing status...";
    $.ajax({
       url: '/administrator/accepted-applicant/',
       type: 'POST',
       headers: {
           'X-CSRFToken': CSRF_TOKEN
       },
       data: {
           data: json_string
       },
       success: function(response) {
           if (response["status_code"] == 200) {
               window.location.reload();
           } else if(response["status_code"]==101) {
               showToast(response["status_message"], 2000);
               console.log("Please report this. ", response["status_message"]);
           }else{
               showToast("Unable to schedule due to some internal server error. Kindly report the same", 2000);
               console.log("Please report this. ", response["status_message"]);            
           }
            element.innerHTML = "Accept";
       },
       error: function(xhr, textstatus, errorthrown){
           console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
            element.innerHTML = "Accept";
       }
   });
}

function rejected_applicants(element){

    selected_applicant_id_list = get_list_of_selected_applicants();

    json_string = JSON.stringify({
        selected_applicant_id_list:selected_applicant_id_list
    });

    var CSRF_TOKEN = getCsrfToken();
    element.innerHTML = "Changing status...";
    $.ajax({
       url: '/administrator/rejected-applicant/',
       type: 'POST',
       headers: {
           'X-CSRFToken': CSRF_TOKEN
       },
       data: {
           data: json_string
       },
       success: function(response) {
           if (response["status_code"] == 200) {
               window.location.reload();
           } else if(response["status_code"]==101) {
               showToast(response["status_message"], 2000);
               console.log("Please report this. ", response["status_message"]);
           }else{
               showToast("Unable to schedule due to some internal server error. Kindly report the same", 2000);
               console.log("Please report this. ", response["status_message"]);            
           }
            element.innerHTML = "Reject";
       },
       error: function(xhr, textstatus, errorthrown){
           console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
            element.innerHTML = "Reject";
       }
   });
}

function reset_profile_applicants(element){

    selected_applicant_id_list = get_list_of_selected_applicants();

    json_string = JSON.stringify({
        selected_applicant_id_list:selected_applicant_id_list
    });

    var CSRF_TOKEN = getCsrfToken();
    element.innerHTML = "Changing status...";
    $.ajax({
       url: '/administrator/reset-applicant-account/',
       type: 'POST',
       headers: {
           'X-CSRFToken': CSRF_TOKEN
       },
       data: {
           data: json_string
       },
       success: function(response) {
           if (response["status_code"] == 200) {
               window.location.reload();
           } else if(response["status_code"]==101) {
               showToast(response["status_message"], 2000);
               console.log("Please report this. ", response["status_message"]);
           }else{
               showToast("Unable to schedule due to some internal server error. Kindly report the same", 2000);
               console.log("Please report this. ", response["status_message"]);            
           }
            element.innerHTML = "Reset Account";
       },
       error: function(xhr, textstatus, errorthrown){
           console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
            element.innerHTML = "Reset Account";
       }
   });
}

$(document).on("click", "#btn-add-institute", function(e) 
{
    var institute_name = $("#input-institute-name").val();
    if (institute_name == "") {
        showToast("Institute name can not be empty.");
        return;
    }
    json_string = JSON.stringify({
           "name": institute_name,
       });

       var CSRF_TOKEN = getCsrfToken();
       $.ajax({
           url: '/master-list/add-institutes/',
           type: 'POST',
           headers: {
               'X-CSRFToken': CSRF_TOKEN
           },
           data: {
               data: json_string
           },
           success: function(response) {
               if (response["status_code"] == 200) {
                   window.location.reload();
               } else {
                   showToast("Unable to add new institute. Make sure institute name is unique.", 2000);
                   console.log("Please report this. ", response["status_message"]);
               }
           },
           error: function(xhr, textstatus, errorthrown) {
               console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
           }
       });
});

function deactivate_institute(institute_name)
{
  console.log(institute_name)
    json_string = JSON.stringify({
           "institute": institute_name,
       });

       var CSRF_TOKEN = getCsrfToken();
       $.ajax({
           url: '/administrator/deactivate-institute/',
           type: 'POST',
           headers: {
               'X-CSRFToken': CSRF_TOKEN
           },
           data: {
               data: json_string
           },
           success: function(response) {
               if (response["status_code"] == 200) {
                   window.location.reload();
               } else {
                   showToast("Unable to deactivate institute. Try again later.", 2000);
                   console.log("Please report this. ", response["status_message"]);
               }
           },
           error: function(xhr, textstatus, errorthrown) {
               console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
           }
       });
}

function activate_institute(institute_name)
{
  console.log(institute_name)
    json_string = JSON.stringify({
           "institute": institute_name,
       });

       var CSRF_TOKEN = getCsrfToken();
       $.ajax({
           url: '/administrator/activate-institute/',
           type: 'POST',
           headers: {
               'X-CSRFToken': CSRF_TOKEN
           },
           data: {
               data: json_string
           },
           success: function(response) {
               if (response["status_code"] == 200) {
                   window.location.reload();
               } else {
                   showToast("Unable to activate institute. Try again later.", 2000);
                   console.log("Please report this. ", response["status_message"]);
               }
           },
           error: function(xhr, textstatus, errorthrown) {
               console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
           }
       });
}

$(document).on("click", "#btn-add-stream", function(e) 
{
    var stream_name = $("#input-stream-name").val();
    if (stream_name == "") {
        showToast("Stream name can not be empty.");
        return;
    }
    json_string = JSON.stringify({
           "name": stream_name,
       });

       var CSRF_TOKEN = getCsrfToken();
       $.ajax({
           url: '/master-list/add-streams/',
           type: 'POST',
           headers: {
               'X-CSRFToken': CSRF_TOKEN
           },
           data: {
               data: json_string
           },
           success: function(response) {
               if (response["status_code"] == 200) {
                   window.location.reload();
               } else {
                   showToast("Unable to add new stream. Make sure stream name is unique.", 2000);
                   console.log("Please report this. ", response["status_message"]);
               }
           },
           error: function(xhr, textstatus, errorthrown) {
               console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
           }
       });
});
function delete_stream(stream_id)
{
    json_string = JSON.stringify({
           "stream_id": stream_id,
       });

       var CSRF_TOKEN = getCsrfToken();
       $.ajax({
           url: '/master-list/delete-stream/',
           type: 'POST',
           headers: {
               'X-CSRFToken': CSRF_TOKEN
           },
           data: {
               data: json_string
           },
           success: function(response) {
               if (response["status_code"] == 200) {
                   window.location.reload();
               } else {
                   showToast("Unable to delete stream. Try again later.", 2000);
                   console.log("Please report this. ", response["status_message"]);
               }
           },
           error: function(xhr, textstatus, errorthrown) {
               console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
           }
       });
}

if(window.location.pathname=="/master-list/streams/"){
  $(document).ready(function(){
      var table = $('#table-streams-details').DataTable();
  });
}


/////////////////////QUIZ////////////////////////////


if(window.location.pathname=="/manage-quiz/"){
  $(document).ready(function(){
      var table = $('#table-manage-quiz').DataTable();
  });
}

if(window.location.pathname=="/manage-quiz/topics/"){
  $(document).ready(function(){
      var table = $('#table-manage-quiz-topics').DataTable();
  });
}


$(document).on("click", "#btn-add-topic", function(e) {
    var topicName = $("#topic-name").val();
    if (topicName == "") {
        showToast("Topic Name can not be empty.", 2000);
        return;
    }

//    json_string = JSON.stringify({
//       "topic_name": topicName
//    });

    var category = $('#select-topic-category').val();

    json_string = JSON.stringify({
        "topic_name": topicName,
        'category': category,
    });

    var CSRF_TOKEN = getCsrfToken()
    $.ajax({
        url: "/manage-quiz/add-topic/",
        type: "POST",
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        },
        data: {
            data: json_string
        },
        success: function(response) {
            window.location.reload();
        },
        error: function(xhr, textstatus, errorthrown) {
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
        }
    });
});


function delete_selected_urls_from_problem(option_id){
    document.getElementById("li-collection-item-"+option_id).remove();
}

if(window.location.pathname.indexOf("/problem/edit")!=-1 || window.location.pathname.indexOf("/problem/add")!=-1){
    document.getElementById('input-url-value').onkeypress=function(e){
        if(e.keyCode==13){
            document.getElementById('btn-add-url').click();
        }
    }
}

$(document).on("click", "#btn-add-url", function(e) {
    number_of_urls = document.getElementsByClassName("url-collection").length;
    var url_value = $("#input-url-value").val();
    if (url_value == "") {
        showToast("URL can not be empty.", 2000);
        return;
    }
    number_of_urls = number_of_urls + 1;
    html = '<li class="collection-item" id="li-collection-item-'+number_of_urls+'">\
                <div class="row">\
                    <div class="col s10">\
                        <input value="'+url_value+'" class="url-collection" id="input-url-'+number_of_urls+'"></input>\
                    </div>\
                    <div class="col s2">\
                        <i class="material-icons right" onclick="delete_selected_urls_from_problem('+number_of_urls+')">delete</i>\
                    </div>\
                </div>\
            </li>';
    $("#ul-url-collection").append(html);
    document.getElementById("input-url-value").value = "";
});


if(window.location.pathname.indexOf("/problem/edit")!=-1 || window.location.pathname.indexOf("/problem/add")!=-1){
    document.getElementById('input-choice-value').onkeypress=function(e){
        if(e.keyCode==13){
            document.getElementById('btn-add-choice').click();
        }
    }
}

$(document).on("click", "#btn-add-choice", function(e) {
    number_of_choices = document.getElementsByClassName("choice-collection").length;
    var choice_value = $("#input-choice-value").val();
    if (choice_value == "") {
        showToast("Choice value can not be empty.", 2000);
        return;
    }
    if(checkChoices(choice_value)){
        showToast("Choice already exists.", 2000);
        return;
    }
    number_of_choices = number_of_choices + 1;
    html = '<li class="collection-item" id="li-collection-item-'+number_of_choices+'">\
        <div class="row">\
          <div class="col s10">\
            <input value="'+choice_value+'" class="choice-collection" id="input-choice-'+number_of_choices+'"></input>\
          </div>\
          <div class="col s2">\
            <i class="material-icons right" onclick="delete_selected_option_from_problem('+number_of_choices+')">delete</i>\
          </div>\
        </div>\
      </li>';
    $("#ul-choice-collection").append(html);
    document.getElementById("input-choice-value").value = "";
});


function checkChoices(choice_value)
{
    choice_length = document.getElementsByClassName("choice-collection").length;
    found = false;
    for(var i=0;i<choice_length;i++)
    {
        if(choice_value == document.getElementsByClassName("choice-collection")[i].value)
        {
            found = true;
            break;
        }
    }
    return found;
}
function checkRepeatedChoices(choice_value)
{
    choice_length = document.getElementsByClassName("choice-correct-collection").length;
    found = false;
    for(var i=0;i<choice_length;i++)
    {
        if(choice_value == document.getElementsByClassName("choice-correct-collection")[i].value)
        {
            found = true;
            break;
        }
    }
    return found;
}

if(window.location.pathname.indexOf("/problem/edit")!=-1 || window.location.pathname.indexOf("/problem/add")!=-1){
    document.getElementById('input-choice-correct-value').onkeypress=function(e){
        if(e.keyCode==13){
            document.getElementById('btn-add-correct-choice').click();
        }
    }
}

$(document).on("click", "#btn-add-correct-choice", function(e) {

    number_of_choices = document.getElementsByClassName("choice-correct-collection").length;
    var choice_value = $("#input-choice-correct-value").val();
    if (choice_value == "") {
        showToast("Correct choice value can not be empty.", 2000);
        return;
    }
    found = checkChoices(choice_value);
    if(found == false)
    {
        showToast("Correct choice value should exist in choices.", 2000);
        return;
    }
    repeat = checkRepeatedChoices(choice_value);
    if(repeat == true)
    {
        showToast("This option already exists.", 2000);
        return;
    }
    number_of_choices = number_of_choices + 1;
    html = '<li class="collection-item" id="li-collection-correct-item-'+number_of_choices+'">\
        <div class="row">\
          <div class="col s10">\
            <input value="'+choice_value+'" class="choice-correct-collection" id="input-choice-correct-'+number_of_choices+'"></input>\
          </div>\
          <div class="col s2">\
            <i class="material-icons right" onclick="delete_selected_correct_option_from_problem('+number_of_choices+')">delete</i>\
          </div>\
        </div>\
      </li>';
    $("#ul-choice-correct-collection").append(html);

    document.getElementById("input-choice-correct-value").value = "";

});

function delete_selected_option_from_problem(option_id){
    document.getElementById("li-collection-item-"+option_id).remove();
}

function delete_selected_correct_option_from_problem(option_id){
    document.getElementById("li-collection-correct-item-"+option_id).remove();
}

$(document).on("click", ".delete-topic", function(e) {
    var topicId = this.id.split("-")[3];

    json_string = JSON.stringify({
        "topic_id": topicId
    });

    var CSRF_TOKEN = getCsrfToken();
    $.ajax({
        url: "/manage-quiz/delete-topic/",
        type: "POST",
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        },
        data: {
            data: json_string
        },
        success: function(response) {
            window.location.reload();
        },
        error: function(xhr, textstatus, errorthrown) {
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
        }
    });
});


$(document).on("click", ".rename-topic", function(e) {

    var topicId = this.id.split("-")[3];
    var topicName = document.getElementById("input-topic-new-name-" + topicId).value;

    if (topicName == "") {
        showToast("Topic name can not be empty!");
        return;
    }

    json_string = JSON.stringify({
        "topic_id": topicId,
        "topic_name": topicName
    });

    var CSRF_TOKEN = getCsrfToken();
    $.ajax({
        url: "/manage-quiz/rename-topic/",
        type: "POST",
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        },
        data: {
            data: json_string
        },
        success: function(response) {
            window.location.reload();
        },
        error: function(xhr, textstatus, errorthrown) {
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
        }
    });
});


$(document).on("change", "#problem-category", function(e) {
    var problemCategory = $("#problem-category").val();
    if (problemCategory == "1" || problemCategory == "2") {
        showChoiceDiv();
    } else if (problemCategory == "3") {
        showDescriptiveDiv();
    } else if (problemCategory == "4" || problemCategory == "5") {
        hideChoiceDiv();
        hideDescriptiveDiv();
    }
});

if (window.location.pathname.indexOf("/problem/edit") != -1) {
    $("#problem-category").change();
    $("#multiple-select-choices").change();
}

$(document).on("click", ".save-problem", function(e) {

    var problemID = "None";
    if (window.location.pathname.indexOf("/problem/edit") != -1) {
        problemID = window.location.pathname.split("/")[4];
    }

    var problemCategory = $("#problem-category").val();
    if (problemCategory == undefined || problemCategory == "" || problemCategory == null) {
        showToast("Please select problem category.", 2000);
        return;
    }

    var problemDifficulty = $("#problem-difficulty").val();
    if (problemDifficulty == undefined || problemDifficulty == "" || problemDifficulty == null) {
        showToast("Please select problem difficulty.", 2000);
        return;
    }

    //var problemTopics = $("#multiple-select-problem-topics").val();
    //if (problemTopics.length == 0) {
    //    showToast("Please select topic for problem", 2000);
    //    return;
    // }

       if(problemCategory == "2"){
        temp_category = "1"
    }
    else{
        temp_category = problemCategory
    }

    var problemTopics = $("#multiple-select-problem-topics-"+temp_category).val();
    if (problemTopics.length == 0) {
        showToast("Please select topic for problem", 2000);
        return;
    }


    var problem_description = CKEDITOR.instances['problem-description'].getData();
    // var problem_solution = CKEDITOR.instances['problem-solution'].getData();
    var problem_solution = $("#problem-solution").val();
    var problem_hint = CKEDITOR.instances['problem-hint'].getData();

    if (problem_description == null || problem_description == undefined || problem_description == "") {
        showToast("Problem description can not be empty.", 2000);
        return;
    }


    var selected_urls = "";
    var selected_urls_length = document.getElementsByClassName("url-collection").length;
    if(selected_urls_length>0){
        selected_urls += document.getElementsByClassName("url-collection")[0].value;
        for(var i=1; i<selected_urls_length; i++)
        {
            selected_urls += ",";
            selected_urls += document.getElementsByClassName("url-collection")[i].value;
        }        
    }


    var selected_choices = "";
    correct_choices = "";
    if(problemCategory == "1" || problemCategory == "2"){
        var selected_choices_length = document.getElementsByClassName("choice-collection").length;
//        selected_choices += document.getElementsByClassName("choice-collection")[0].value;
//        for(var i=1; i<selected_choices_length; i++)
//        {
//            selected_choices += "|";
//            selected_choices += document.getElementsByClassName("choice-collection")[i].value;
//        }
//        correct_choices_length = document.getElementsByClassName("choice-correct-collection").length;
//        correct_choices += document.getElementsByClassName("choice-correct-collection")[0].value;
//        for(i=1;i<correct_choices_length;i++)
//        {
//            correct_choices += "|";
//            correct_choices += document.getElementsByClassName("choice-correct-collection")[i].value
//        }
	selected_choices_dict = {};
	selected_choices = "";
        if(selected_choices_length == 0){
            showToast('Please provide atleast one option', 2000);
            return;
        }
        for(var i=0; i<selected_choices_length; i++)
        {
            selected_choices += document.getElementsByClassName("choice-collection")[i].value.trim();
            selected_choices += "|";
            selected_choices_dict[document.getElementsByClassName("choice-collection")[i].value.trim()] = true;
        }
        correct_choices_length = document.getElementsByClassName("choice-correct-collection").length;

        if(correct_choices_length == 0){
            showToast('Please provide an answer', 2000);
            return;
        }
        correct_choices = '';
        for(i=0;i<correct_choices_length;i++)
        {
            correct_choices += document.getElementsByClassName("choice-correct-collection")[i].value.trim();
            correct_choices += "|";

            if(!(document.getElementsByClassName("choice-correct-collection")[i].value in selected_choices_dict)){
                showToast('Answer doesn\'t exist in choices', 2000);
                return;
            }
        }
    }

    var selected_video_urls = "";
    var selected_video_urls_length = document.getElementsByClassName("video-url-collection").length;
    if(selected_video_urls_length>0){
        selected_video_urls += document.getElementsByClassName("video-url-collection")[0].value;
        for(var i=1; i<selected_video_urls_length; i++)
        {
            selected_video_urls += ",";
            selected_video_urls += document.getElementsByClassName("video-url-collection")[i].value;
        }        
    }

    var pdf_url = "";
    pdf_url = document.getElementById("input-pdf-url-value").value;

    var text_to_speech = document.getElementById("checkbox-text-to-speech").checked;
    json_string = JSON.stringify({
        "problem_id": problemID,
        "problem_category": problemCategory,
        "problem_difficulty": problemDifficulty,
        "problem_topics": problemTopics,
        "problem_description": problem_description,
        "problem_solution": problem_solution,
        "problem_hint": problem_hint,
        "selected_choices": selected_choices,
        "correct_choices": correct_choices,
        "video_url": selected_video_urls,
        "text_to_speech": text_to_speech,
        "pdf_url":pdf_url,
        "selected_urls":selected_urls
    });

    problemImage = ($("#input_upload_image"))[0].files[0];
    formdata = new FormData();
    formdata.append('file', problemImage);
    formdata.append('data', json_string);

    var CSRF_TOKEN = getCsrfToken();
    showToast("Saving problem...");
    $.ajax({
        url: '/manage-quiz/save-problem/',
        type: 'POST',
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        },
        data: formdata,
        processData: false,
        contentType: false,
        success: function(response) {
            if (response["status_code"] == 200) {
                window.location = "/manage-quiz/problem/edit/" + response["problem_id"];
            } else {
                showToast("Unable to save the problem. Kindly report the same.");
            }
        },
        error: function(xhr, textstatus, errorthrown) {
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
        }
    });
});

$(document).on("click", "#btn-add-video", function(e) {
    var video_url = $("#input-video-url").val();
    var video_url = getEmbedVideoURL(video_url);
    $("#problem-video-url").val(video_url);
});

$(document).on("click", "#btn-add-quiz-config", function(e) {
    var quizTitle = $("#quiz-title").val();
    if (quizTitle == "") {
        showToast("Quiz title can not be empty.", 2000);
        return;
    }

    json_string = JSON.stringify({
        "quiz_title": quizTitle
    });

    var CSRF_TOKEN = getCsrfToken()
    $.ajax({
        url: "/manage-quiz/add-quiz/",
        type: "POST",
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        },
        data: {
            data: json_string
        },
        success: function(response) {
            window.location.reload();
        },
        error: function(xhr, textstatus, errorthrown) {
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
        }
    });
});

$(document).on("click", ".delete-quiz-config", function(e) {
    var quizId = this.id.split("-")[3];

    json_string = JSON.stringify({
        "quiz_id": quizId
    });

    var CSRF_TOKEN = getCsrfToken();
    $.ajax({
        url: "/manage-quiz/delete-quiz/",
        type: "POST",
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        },
        data: {
            data: json_string
        },
        success: function(response) {
            window.location.reload();
        },
        error: function(xhr, textstatus, errorthrown) {
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
        }
    });
});

if(window.location.pathname.indexOf("/quiz-config/edit")!=-1){
    $(document).ready(function(e){
        $("#select-quiz-section-topic").select2({
            dropdownParent: $("#modal-add-quiz-section"),
            width:"100%",
        });
    });
}

$(document).on("click", ".save-quiz-config", function(e) {

    var quizConfigID = "None";
    if (window.location.pathname.indexOf("/manage-quiz/quiz/edit") != -1) {
        quizConfigID = window.location.pathname.split("/")[4];
    }

    var quiz_title = $("#quiz-config-title").val();
    if (quiz_title == "") {
        showToast("Quiz title can not be empty.", 2000);
        return;
    }

    var quiz_instruction = CKEDITOR.instances['quiz-config-instruction'].getData();

    if (quiz_instruction == "") {
        showToast("Quiz instruction can not be empty.", 2000);
        return;
    }

    include_personality_profiler = document.getElementById("checkbox-include-personality-profiler").checked;
    is_sectional_timed = document.getElementById("checkbox-sectional-timer").checked;
    buffer_time = $('#quiz-buffer-time').val();

    if(is_sectional_timed){
        if(buffer_time == null || parseInt(buffer_time) == NaN || parseInt(buffer_time) < 1 || parseInt(buffer_time)>180){
            showToast("Buffer timer can not be greater than 180 minutes", 2000);
            return;
        }
    }

    tag_pk = $('#select-quiz-tag').val();

    var json_string = JSON.stringify({
        quiz_id: quizConfigID,
        quiz_title: quiz_title,
        quiz_instruction: quiz_instruction,
        include_personality_profiler: include_personality_profiler,
        is_sectional_timed: is_sectional_timed,
        buffer_time: buffer_time,
        tag_pk: tag_pk,
    });

    var CSRF_TOKEN = getCsrfToken();
    showToast('Request Submitted. Please wait...',500);
    $.ajax({
        url: '/manage-quiz/save-quiz-config/',
        type: 'POST',
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        },
        data: {
            data: json_string
        },
        success: function(response) {
            //window.location.reload();
        if(response['status_code']==200){
            showToast('Quiz Updated Successfully',2000);
        }    
	    if(response['status_code']==201){
            showToast('This name has already been taken up in another quiz',1000);
            showToast('All other information has been saved',2000);
        }
        setTimeout(function(){
            window.location.reload();
        },2000);
        },
        error: function(xhr, textstatus, errorthrown) {
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
        }
    });
});

function scrollToGivenElementId(element_id) {
    $('html, body').animate({
        scrollTop: $("#" + element_id).offset().top - 100
    }, 500);
}

function focusAtGivenElementID(element_id) {
    $("#" + element_id).focus();
}

$(document).on("click", ".remove-problem-image", function(e) {
    problem_id = this.id.split("-")[4];
    var CSRF_TOKEN = getCsrfToken();

    json_string = JSON.stringify({
        "problem_id": problem_id,
        "remove_image": true,
        "remove_video": false
    });

    $.ajax({
        url: "/problem/remove-media",
        type: "POST",
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        },
        data: {
            data: json_string
        },
        success: function(response) {
            window.location.reload();
        },
        error: function(xhr, textstatus, errorthrown) {
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
        }
    });
});

$(document).on("click", ".remove-problem-video", function(e) {
    problem_id = this.id.split("-")[4];
    var CSRF_TOKEN = getCsrfToken();

    json_string = JSON.stringify({
        "problem_id": problem_id,
        "remove_image": false,
        "remove_video": true
    });

    $.ajax({
        url: "/problem/remove-media",
        type: "POST",
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        },
        data: {
            data: json_string
        },
        success: function(response) {
            window.location.reload();
        },
        error: function(xhr, textstatus, errorthrown) {
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
        }

    });
});
/*
$(document).on("click", "#btn-add-quiz-section", function(e) {

    quiz_config_id = window.location.pathname.split("/")[4];
    quiz_section_topic_id = $("#select-quiz-section-topic").val();
    quiz_section_weightage = $("#quiz-section-weightage").val();
    quiz_section_no_questions = $("#quiz-section-no-questions").val();
    quiz_section_time = $("#quiz-section-time").val();

    if (quiz_section_topic_id == "") {
        showToast("Please select Topic to add section", 2000);
        focusAtGivenElementID("select-quiz-section-topic");
        $("#modal-add-quiz-section").modal('open');
        return;
    }

    if (quiz_section_weightage == "") {
        showToast("Please assign weightage to quiz section", 2000);
        focusAtGivenElementID("quiz-section-weightage");
        $("#quiz-section-weightage").modal('open');
        return;
    }

    if (quiz_section_no_questions == "") {
        showToast("Please add no of questions", 2000);
        focusAtGivenElementID("quiz-section-no-questions");
        $("#modal-add-quiz-section").modal('open');
        return;
    }

    if (quiz_section_time == "") {
        showToast("Please add time for section in minutes", 2000);
        focusAtGivenElementID("quiz-section-time");
        $("#modal-add-quiz-section").modal('open');
        return;
    }

    var CSRF_TOKEN = getCsrfToken();

    json_string = JSON.stringify({
        "quiz_config_id": quiz_config_id,
        "quiz_section_weightage": quiz_section_weightage,
        "quiz_section_topic_id": quiz_section_topic_id,
        "quiz_section_no_questions": quiz_section_no_questions,
        "quiz_section_time": quiz_section_time
    });

    $.ajax({
        url: "/manage-quiz/add-quiz-section/",
        type: "POST",
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        },
        data: {
            data: json_string
        },
        success: function(response) {
            if (response["status_code"] == 200) {
                window.location.reload();
            } else {
                showToast(response["status_message"], 2000);
            }
        },
        error: function(xhr, textstatus, errorthrown) {
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
        }

    });
});*/

$(document).on("click", "#btn-add-quiz-section", function(e) {

    quiz_config_id = window.location.pathname.split("/")[4];
    quiz_section_topic_id = $("#select-quiz-section-topic").val();
    quiz_section_weightage = $("#quiz-section-weightage").val();
    quiz_section_no_questions = $("#quiz-section-no-questions").val();
    quiz_section_time = $("#quiz-section-time").val();


    if($('#btn-add-quiz-section').html()=="Add" && topic_already_added(quiz_section_topic_id)){
       showToast("Topic already added, use edit button to modify it",2000);
       return;
    }
    type = document.getElementById("select-quiz-section-type").value;
    if(type == ""){
      showToast("Please choose a quiz type.", 2000);
      $("#modal-add-quiz-section").modal('open');
      return;
    }
    quiz_easy_question = ""
    quiz_medium_question = ""
    quiz_hard_question = ""

    if(type == "2"){
      quiz_easy_question = document.getElementById("quiz-easy-question").value;
      if(quiz_easy_question == ""){
        showToast("Please enter the number of easy questions.", 2000);
        $("#quiz-section-weightage").modal('open');
        return;
      }
      quiz_medium_question = document.getElementById("quiz-medium-question").value;
      if(quiz_medium_question == ""){
        showToast("Please enter the number of medium questions.", 2000);
        $("#quiz-section-weightage").modal('open');
        return;
      }
      quiz_hard_question = document.getElementById("quiz-hard-question").value;
      if(quiz_hard_question == ""){
        showToast("Please enter the number of hard questions.", 2000);
        $("#quiz-section-weightage").modal('open');
        return;
      }
    }

    if (quiz_section_topic_id == "") {
        showToast("Please select Topic to add section", 2000);
        focusAtGivenElementID("select-quiz-section-topic");
        $("#modal-add-quiz-section").modal('open');
        return;
    }

    if (quiz_section_weightage == "") {
        showToast("Please assign weightage to quiz section", 2000);
        focusAtGivenElementID("quiz-section-weightage");
        $("#quiz-section-weightage").modal('open');
        return;
    }

    if (quiz_section_no_questions == "") {
        showToast("Please add no of questions", 2000);
        focusAtGivenElementID("quiz-section-no-questions");
        $("#modal-add-quiz-section").modal('open');
        return;
    }

    if (quiz_section_time == "") {
        showToast("Please add time for section in minutes", 2000);
        focusAtGivenElementID("quiz-section-time");
        $("#modal-add-quiz-section").modal('open');
        return;
    }
    if(type == "2"){
      total_questions = parseInt(quiz_easy_question) + parseInt(quiz_medium_question) + parseInt(quiz_hard_question)
      if(total_questions != quiz_section_no_questions){
        showToast("Total number of questions should be equal to sum of easy, medium and hard.")
        return;
      }
    }

    var CSRF_TOKEN = getCsrfToken();

    json_string = JSON.stringify({
        "quiz_config_id": quiz_config_id,
        "quiz_section_weightage": quiz_section_weightage,
        "quiz_section_topic_id": quiz_section_topic_id,
        "quiz_section_no_questions": quiz_section_no_questions,
        "quiz_section_time": quiz_section_time,
        "type":type,
        "quiz_easy_question":quiz_easy_question,
        "quiz_medium_question":quiz_medium_question,
        "quiz_hard_question":quiz_hard_question
    });

    $.ajax({
        url: "/manage-quiz/add-quiz-section/",
        type: "POST",
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        },
        data: {
            data: json_string
        },
        success: function(response) {
            if (response["status_code"] == 200) {
                window.location.reload();
            } else {
                showToast(response["status_message"], 2000);
            }
        },
        error: function(xhr, textstatus, errorthrown) {
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
        }

    });
});

function delete_selected_video_urls_from_problem(option_id){
    document.getElementById("li-collection-video-item-"+option_id).remove();
}

if(window.location.pathname.indexOf("/problem/edit")!=-1 || window.location.pathname.indexOf("/problem/add")!=-1){
    document.getElementById('input-video-url-value').onkeypress=function(e){
        if(e.keyCode==13){
            document.getElementById('btn-add-video-url').click();
        }
    }
}

var frequency_count_section_id = {}
 var frequency_count_problem_id = {}

//function expandSectionProblemResult(section_id) {
//     console.log(section_id);
//     if (section_id in frequency_count_problem_id) {
//         frequency_count_problem_id[section_id] += 1;
//         if (frequency_count_problem_id[section_id] % 2 == 0) {
//             $("#section-problem-table-" + section_id).hide();
//             $("#section-problem-table-icon-" + section_id).html("expand_more");
//         } else {
//             $("#section-problem-table-" + section_id).show(1000);
//             $("#section-problem-table-icon-" + section_id).html("expand_less");
//         }
//     } else {
//         frequency_count_problem_id[section_id] = 1;
//         $("#section-problem-table-" + section_id).show(1000);
//         $("#section-problem-table-icon-" + section_id).html("expand_less");
//     }
// }

function expandSectionProblemResult(section_id) {
     console.log(section_id);
     if (section_id in frequency_count_problem_id) {
         frequency_count_problem_id[section_id] += 1;
         if (frequency_count_problem_id[section_id] % 2 == 0) {
             $("#section-problem-table-" + section_id).hide();
             $('#canvas-'+section_id).hide();
             $('#canvas-'+section_id).html('<div class="col s6 m6 l6">\
                                                <canvas id="canvas-bar-chart-'+section_id+'"></canvas>\
                                                </div>\
                                                <div class="col s6 m6 l6">\
                                                <canvas id="canvas-pie-chart-'+section_id+'"></canvas>\
                                                </div>');
             $("#section-problem-table-icon-" + section_id).html("expand_more");
         } else {
            show_charts(section_id);
            $("#section-problem-table-" + section_id).show(1000);

             $("#section-problem-table-icon-" + section_id).html("expand_less");
         }
     } else {
         frequency_count_problem_id[section_id] = 1;
        show_charts(section_id);
        $("#section-problem-table-" + section_id).show(1000);
        $("#section-problem-table-icon-" + section_id).html("expand_less");
     }
 }

function show_charts(section_id){

        if ($('#easy-allotted-'+section_id).html() ==  "NA*" || $('#easy-allotted-'+section_id).html() == "N/A" )
            {return}

        $('#canvas-'+section_id).show();
        var barchartdata ={
            labels: ['Easy', 'Medium', 'Hard'],
            datasets: [{
                label: 'Correct',
                backgroundColor: '#9fcd7e',
                data: [parseInt($('#easy-correct-'+section_id).html()), parseInt($('#medium-correct-'+section_id).html()), parseInt($('#hard-correct-'+section_id).html())]
            }, {
                label: 'Incorrect',
                backgroundColor: '#e6654e',
                data: [parseInt($('#easy-attempted-'+section_id).html()) - parseInt($('#easy-correct-'+section_id).html()), parseInt($('#medium-attempted-'+section_id).html()) - parseInt($('#medium-correct-'+section_id).html()), parseInt($('#hard-attempted-'+section_id).html()) - parseInt($('#hard-correct-'+section_id).html())]
            }, {
                label: 'Unattempted',
                backgroundColor: '#e2e2e2',
                data: [parseInt($('#easy-allotted-'+section_id).html()) - parseInt($('#easy-attempted-'+section_id).html()), parseInt($('#medium-allotted-'+section_id).html()) - parseInt($('#medium-attempted-'+section_id).html()), parseInt($('#hard-allotted-'+section_id).html()) - parseInt($('#hard-attempted-'+section_id).html())]
            }]

        };

        var ctx = document.getElementById('canvas-bar-chart-'+section_id).getContext('2d');
        var chart = new Chart(ctx, {
            // The type of chart we want to create
            type: 'bar',

            // The data for our dataset
            data: barchartdata,

            // Configuration options go here
            options: {
                scales: {
                    xAxes: [{ stacked: true }],
                    yAxes: [{ stacked: true }],
                }
            }
        });

        var ctx = document.getElementById('canvas-pie-chart-'+section_id).getContext('2d');
        var chart = new Chart(ctx, {
            // The type of chart we want to create
            type: 'doughnut',

            // The data for our dataset
            data: {
                labels: ['Easy', 'Medium', 'Hard'],
                datasets: [{
                    data: [parseInt($('#easy-allotted-'+section_id).html()),parseInt($('#medium-allotted-'+section_id).html()),parseInt($('#hard-allotted-'+section_id).html())],
                    backgroundColor: ["#46BFBD","#FDB45C","#F7464A"]
                    }]

            },

        });

}

function load_video_player(player_id, is_consolidated) {

      if (is_consolidated) {
         video_link = document.getElementById('div-consolidated-video-player-' + player_id).getElementsByClassName('video-link')[0];
         video_player = document.getElementById('div-consolidated-video-player-' + player_id).getElementsByTagName('video')[0];
     }
     else {
         video_link = document.getElementById('div-video-player-' + player_id).getElementsByClassName('video-link')[0];
         video_player = document.getElementById('div-video-player-' + player_id).getElementsByTagName('video')[0];
     }

      console.log(video_player.src);

      if (video_player.src != "") {
         return;
     }

      // console.log(video_links,video_players);

      var req = new XMLHttpRequest();

      req.open('GET', video_link.href, true);
     req.responseType = 'blob';

      console.log(video_player);

      req.onload = function () {
         // Onload is triggered even on 404
         // so we need to check the status code
         if (this.status === 200) {
             var videoBlob = this.response;
             var vid = URL.createObjectURL(videoBlob); // IE10+
             // Video is now downloaded
             // and we can set it as source on the video element
             console.log(video_player);
             video_player.src = vid;
         }
     }
     req.onerror = function () {
         // Error
     }
     req.send();
 }
$(document).on("click", "#btn-add-video-url", function(e) {
    number_of_urls = document.getElementsByClassName("video-url-collection").length;
    var url_value = $("#input-video-url-value").val();
    if (url_value == "") {
        showToast("URL can not be empty.", 2000);
        return;
    }
    number_of_urls = number_of_urls + 1;
    url_value = getEmbedVideoURL(url_value);
    html = '<li class="collection-item" id="li-collection-video-item-'+number_of_urls+'">\
                <div class="row">\
                    <div class="col s10">\
                        <input value="'+url_value+'" class="video-url-collection" id="input-video-url-'+number_of_urls+'"></input>\
                    </div>\
                    <div class="col s2">\
                        <i class="material-icons right" onclick="delete_selected_video_urls_from_problem('+number_of_urls+')">delete</i>\
                    </div>\
                </div>\
            </li>';
    $("#ul-video-url-collection").append(html);
    document.getElementById("input-video-url-value").value = "";
});

function hideChoiceDiv() {
    $("#div-problem-choices").hide();
    $("#div-problem-correct-choices").hide();
}

function showChoiceDiv() {
    $("#div-problem-choices").show();
    $("#div-problem-correct-choices").show();
    hideDescriptiveDiv();
}

function showDescriptiveDiv() {
    $("#div-problem-solution").show();
    $("#div-problem-hint").show();
    hideChoiceDiv();
}

function hideDescriptiveDiv() {
    $("#div-problem-solution").hide();
    $("#div-problem-hint").hide();
}

$(document).on("change", "#global-selected-problem", function(e) {
    is_checked = document.getElementById("global-selected-problem").checked;
    selected_problem_list = document.getElementsByClassName("selected-problem");
    for (var i = 0; i < selected_problem_list.length; i++) {
        id = selected_problem_list[i].id;
        document.getElementById(id).checked = is_checked;
    }

    $(".selected-problem").change();
});

$(document).on("change", ".selected-problem", function(e) {
    selected_problem_list = document.getElementsByClassName("selected-problem");
    is_delete_button_show = false;
    for (var i = 0; i < selected_problem_list.length; i++) {
        id = selected_problem_list[i].id;
        if (document.getElementById(id).checked == true) {
            is_delete_button_show = true;
            break;
        }
    }

    delete_button_element = document.getElementById("delete-selected-problem");
    if (is_delete_button_show == true) {
        delete_button_element.style.display = "block";
    } else {
        delete_button_element.style.display = "none";
    }
});

$(document).on("click", "#btn-delete-selected-problem", function(e) {
    var topicId = document.location.pathname.split("/")[3];
    var url = "/manage-quiz/delete-problem/" + topicId + "?";
    selected_problem_list = document.getElementsByClassName("selected-problem");
    for (var i = 0; i < selected_problem_list.length; i++) {
        id = selected_problem_list[i].id;
        if (document.getElementById(id).checked) {
            url += "problem_id=" + id.split("-")[4] + "&";
        }
    }

    $.ajax({
        url: url,
        type: "GET",
        data: {},
        success: function(response) {
            window.location.reload();
        },
        error: function(xhr, textstatus, errorthrown) {
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
        }
    })
});

$(document).on("click", "#btn-upload-questions-excel", function(e) {

    e.preventDefault();

    var selected_question_type_to_upload = $("#selected-question-type-excel-upload").val();
    if (selected_question_type_to_upload == "") {
        showToast("Please select type of questions which you want to upload through excel.");
        return;
    }

    var files = ($("#input-upload-questions-excel"))[0].files
    if (files.length == 0) {
        showToast("Kindly select an excel file to upload.", 2000);
        return;
    }
    file = files[0];

    var formData = new FormData();
    fname = file['name'].split('.');
    fname = fname[fname.length - 1].toLowerCase();
    if (fname == "xlsx" || fname == "xls") {
        formData.append("file", file);
    } else {
        showToast("Kindly select an excel file to upload.", 2000);
        return;
    }

    url = window.location.pathname.split('/')
    formData.append("topic_pk", url[url.length - 1]);
    formData.append("type_of_questions", selected_question_type_to_upload);

    btn_element = document.getElementById("btn-upload-questions-excel");
    btn_element.disabled = true;
    var CSRF_TOKEN = getCsrfToken();
    $("#preloader_div").show();
    $.ajax({
        url: "upload-questions-excel/",
        type: "POST",
        headers: {
           'X-CSRFToken': CSRF_TOKEN
        },
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            $("#preloader_div").hide();
            if (response["status"] == 200) {
                showToast("Questions Added Successfully.", 2000);
                setTimeout(function() {
                    console.log("success reloading")
                    window.location.reload();
                }, 2100);
            } else if (response["status"] == 301) {
                showToast("File Extension Error. Please Upload Valid File", 2000);
            } else if (response["status"] == 302) {
                error_div = document.getElementById("upload-questions-excel-error");
                error_div.style.display = "block";
                error_div.innerHTML = response["message"];
                showToast("An Error Occuredselected-problem.", 6000);
            } else {
                showToast("Internal Server Error. Please try again later.", 2000);
            }
            document.getElementById("input-upload-questions-excel").value = "";
            document.getElementById("input-upload-questions-excel-v").value = "";
            btn_element.disabled = false;
        },
        error: function(xhr, textstatus, errorthrown) {
            $("#preloader_div").hide();
            showToast("Internal Server Error. Please try again later.", 2000);
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
            document.getElementById("#input-upload-questions-excel").val("");
            btn_element.disabled = false;
        }
    });
});

var frequency_count_section_id = {}

function expandQuizSectionResult(section_id) {
    if (section_id in frequency_count_section_id) {
        frequency_count_section_id[section_id] += 1;
        if (frequency_count_section_id[section_id] % 2 == 0) {
            $("#expand-quiz-section-result-" + section_id).hide();
            $("#quiz-section-result-expand-icon-" + section_id).html("expand_more");
        } else {
            $("#expand-quiz-section-result-" + section_id).show(1000);
            $("#quiz-section-result-expand-icon-" + section_id).html("expand_less");
        }
    } else {
        frequency_count_section_id[section_id] = 1;
        $("#expand-quiz-section-result-" + section_id).show(1000);
        $("#quiz-section-result-expand-icon-" + section_id).html("expand_less");
    }
}

function expandAllQuizSectionResult() {
    $(".expand-quiz-section-result").show(1000);
    $(".quiz-section-result-expand-icon").html("expand_less");
}

function hideAllQuizSectionResult() {
    $(".expand-quiz-section-result").hide();
    $(".quiz-section-result-expand-icon").html("expand_more");
}

function showApplicantDetails(applicant_id) {
    window.location = "/administrator/applicant-details/" + applicant_id;
}

//function load_quiz_result(student_id, hiring_round_id) {
//
//    $("#attempted-quiz-result-content-" + hiring_round_id).hide();
//    $("#attempted-quiz-preloader-" + hiring_round_id).show();
//
//    authkey = "";
//    if (window.location.pathname.indexOf("/applicant/report-card") != -1) {
//        authkey = getUrlVars()["authkey"];
//    }
//
//    $.ajax({
//        url: "/administrator/quiz-result/",
//        type: "POST",
//        headers: {
//            "X-CSRFToken": getCsrfToken()
//        },
//        data: {
//            student_id: student_id,
//            quiz_config_id: hiring_round_id,
//            hiring_round_id: hiring_round_id,
//            authkey: authkey
//        },
//        success: function(response) {
//            if (response["status_code"] == 200) {
//                quiz_result = "";
//                 if (response["recruiter_remark"] != -1) {
//                     console.log("herer");
//                     quiz_result += '\
//                     <div class="row">\
//                         <div class="col s12 m3" style="padding-top:1em;">\
//                             <b>Recruiter\'s Remarks:</b>\
//                         </div>\
//                         <div class="col s12 m9">\
//                         <textarea id="recruiters-remark-' + hiring_round_id + '" placeholder="Reqruiter\'s remark" class="materialize-textarea" readonly="readonly">' + response["recruiter_remark"] + '</textarea>\
//                         </div>\
//                     </div>';
//                     quiz_result += '<a class="btn one right" id="edit-remark-'+hiring_round_id+'" onclick="save_remarks(' + hiring_round_id + ',' + student_id + ', this);">Edit Remarks</a>';
//                     document.getElementById("attempted-quiz-remark-content-" + hiring_round_id).innerHTML = quiz_result;
//                     $('#quiz-video-list-' + hiring_round_id).show();
//                 }
//                else if (response["quiz_result"].length == 0) {
//                    quiz_result += "<div class='col s12'><p style='padding:1em;' class='green lighten-3 center'>Applicant haven't attempted quiz yet.</p></div>";
//                } else {
//                    quiz_result_list = response["quiz_result"]["quiz_section_result_list"];
//                      if(quiz_result_list.length > 0){
//                      quiz_result += '\
//                      <div class="col s12 m6 l6">\
//                          <table>\
//                              <tbody>\
//                                  <tr>\
//                                      <td><b>Applicant Percentage</b></td>\
//                                      <td>' + response["quiz_result"]["applicant_total_score"] + ' %</td>\
//                                  </tr>\
//                              </tbody>\
//                          </table>\
//                      </div>\
//                      <div class="col s12 m6 l6">\
//                          <table>\
//                              <tbody>\
//                                  <tr>\
//                                      <td><b>Applicant Percentile</b></td>\
//                                      <td>' + response["quiz_result"]["applicant_percentile"] + ' %</td>\
//                                  </tr>\
//                              </tbody>\
//                          </table>\
//                      </div>\
//                      <div class="col s12">\
//                          <table>\
//                              <thead>\
//                                <tr>\
//                                    <th>Quiz Section</th>\
//                                    <th>Pass score</th>\
//                                    <th>Correct score</th>\
//                                    <th>Adjusted difficulty score</th>\
//                                    <th>Norm Rasch Score</th>\
//                                </tr>\
//                              </thead>\
//                              <tbody>';
//
//                      for (var i = 0; i < quiz_result_list.length; i++) {
//                          quiz_result += '\
//                                        <tr onmouseover="" style="cursor: pointer;" onclick="expandQuizSectionResult(' + quiz_result_list[i]["id"] + ')">\
//                                          <td>\
//                                              <i class="material-icons inline-icon quiz-section-result-expand-icon" \
//                                              id="quiz-section-result-expand-icon-' + quiz_result_list[i]["id"] + '">expand_more</i> \
//                                              ' + quiz_result_list[i]["section_name"] + '\
//                                          </td>\
//                                          <!-- <td>';
//
//                          if (quiz_result_list[i]["is_completed"] == true) {
//                              quiz_result += '<i class="material-icons green-text">check</i>';
//                          } else {
//                              quiz_result += '<i class="material-icons red-text">cancel</i>';
//                          }
//
//                          quiz_result += '</td>--><!-- <td>';
//
//                          if (quiz_result_list[i]["is_cleared"] == true) {
//                              quiz_result += '<i class="material-icons green-text">check</i>';
//                          } else {
//                              quiz_result += '<i class="material-icons red-text">cancel</i>';
//                          }
//
//                          quiz_result += '</td>-->';
//
//                          quiz_result += '<td>' + quiz_result_list[i]["pass_score"] + '</td>\
//                                          <td>' + quiz_result_list[i]["right_answers"] + '</td>\
//                                          <td>' + quiz_result_list[i]["adjusted_diff_score"] + '</td>\
//                                          <td>' + quiz_result_list[i]["diff_score"] + ' %</td>\
//                                        </tr>\
//                                        <!-- Detailed Quiz Section Result Report -->\
//                                        <tr class="expand-quiz-section-result"\
//                                        id="expand-quiz-section-result-' + quiz_result_list[i]["id"] + '"\
//                                        style="display:none;">\
//                                          <td colspan="6">        \
//                                              <div class="row">\
//                                                  <div class="col s12 m8 l8">\
//                                                      <table class="highlight centered" style="border:0.1em solid black;border-radius:1em;">\
//                                                          <thead>\
//                                                            <tr>\
//                                                                <th></th>\
//                                                                <th>Easy</th>\
//                                                                <th>Medium</th>\
//                                                                <th>Hard</th>\
//                                                                <th>Total</th>\
//                                                            </tr>\
//                                                          </thead>\
//                                                          <tbody>\
//                                                            <tr>\
//                                                              <td>Attempt</td>\
//                                                              <td>' + quiz_result_list[i]["attempts"]["easy"] + '</td>\
//                                                              <td>' + quiz_result_list[i]["attempts"]["medium"] + '</td>\
//                                                              <td>' + quiz_result_list[i]["attempts"]["hard"] + '</td>\
//                                                              <td>' + quiz_result_list[i]["attempts"]["total"] + '</td>\
//                                                            </tr>\
//                                                            <tr>\
//                                                              <td>Correct</td>\
//                                                              <td>' + quiz_result_list[i]["correct"]["easy"] + '</td>\
//                                                              <td>' + quiz_result_list[i]["correct"]["medium"] + '</td>\
//                                                              <td>' + quiz_result_list[i]["correct"]["hard"] + '</td>\
//                                                              <td>' + quiz_result_list[i]["correct"]["total"] + '</td>\
//                                                            </tr>\
//                                                            <tr>\
//                                                              <td>%</td>\
//                                                              <td>' + quiz_result_list[i]["abs_per"]["easy"] + ' %</td>\
//                                                              <td>' + quiz_result_list[i]["abs_per"]["medium"] + ' %</td>\
//                                                              <td>' + quiz_result_list[i]["abs_per"]["hard"] + ' %</td>\
//                                                              <td>' + quiz_result_list[i]["abs_per"]["total"] + ' %</td>\
//                                                            </tr>\
//                                                          </tbody>\
//                                                       </table>\
//                                                  </div>\
//                                                  <div class="col s12 m4 l4">\
//                                                      <table class="highlight centered" style="border:0.1em solid black;border-radius:1em;">\
//                                                          <thead>\
//                                                          </thead>\
//                                                          <tbody>\
//                                                            <tr>\
//                                                              <td>Abs Score</td>\
//                                                              <td>\
//                                                              ' + quiz_result_list[i]["total_abs_per"] + ' %</td>\
//                                                            </tr>\
//                                                            <!-- <tr>\
//                                                              <td>Rasch Score</td>\
//                                                              <td>\
//                                                              ' + quiz_result_list[i]["rasch_score"] + '</td>\
//                                                            </tr> -->\
//                                                            <tr>\
//                                                              <td>Norm Rasch Score</td>\
//                                                              <td>\
//                                                                  ' + quiz_result_list[i]["diff_score"] + ' %</td>\
//                                                            </tr>\
//                                                          </tbody>\
//                                                       </table>\
//                                                  </div>\
//                                              </div>'
//
//                  		/*	if (response['problems_list'][quiz_result_list[i]["section_name"]].length > 1) {
//       						pro = response['problems_list'][quiz_result_list[i]["section_name"]];
//						quiz_result += '<div class="col s12"\
//                                             onmouseover="" style="cursor: pointer;" onclick="expandSectionProblemResult(' + quiz_result_list[i]["id"] + ')"">\
//                                             <i class="material-icons inline-icon quiz-section-result-expand-icon" \
//                                               id="section-problem-table-icon-' + quiz_result_list[i]["id"] + '">expand_more</i>\
//                                             Detailed Problem Result\
//                                             </div>';
//                                 quiz_result += '<div class="col s12" >\
//                                                 <table style="display:none;" id = "section-problem-table-'+ quiz_result_list[i]["id"] + '">\
//                                                     <thead>\
//                                                     <tr >\
//                                                         <th>'+ pro[0]['no'] + '</th>\
//                                                         <th>'+ pro[0]['difficulty'] + '</th>\
//                                                         <th style="width:50%">'+ pro[0]['question'] + '</th>\
//                                                         <th>'+ pro[0]['attempted_options'] + '</th>\
//                                                         <th>'+ pro[0]['correct_options'] + '</th>\
//                                                         <th>'+ pro[0]['result'] + '</th>\
//                                                     </tr>\
//                                                     </thead><tbody>';
//                                 for (let j = 1; j < pro.length; j++) {
//                                     quiz_result += '<tr>\
//                                     <td>'+ pro[j]['no'] + '</td>\
//                                     <td>'+ pro[j]['difficulty'] + '</td>\
//                                     <td style="width:50%">'+ pro[j]['question'] + '</td>\
//                                     <td>'+ pro[j]['attempted_options'] + '</td>\
//                                     <td>'+ pro[j]['correct_options'] + '</td>\
//                                     <td>'+ pro[j]['result'] + '</td>\
//                                     </tr>';
//                                 }
//
// 
// 
//                                  quiz_result += '</tbody></table>\
//                                                 </div>';
//
//                              }*/
//                             quiz_result += '</td>\
//                             </tr>';
//			}
//                      }
//
//                      quiz_result += '</tbody>\
//                              </table>\
//                          </div>\
//                          <div class="col s12">\
//                              <br>\
//                              <a class="btn one right" onclick="expandAllQuizSectionResult()">Expand</a>\
//                              <a class="btn one right" onclick="hideAllQuizSectionResult()">Hide</a>\
//                          </div>';
//                  }
//                  console.log(hiring_round_id)
//
//                  document.getElementById("attempted-quiz-result-content-" + hiring_round_id).innerHTML = quiz_result;
//                }
//            else {
//                document.getElementById("attempted-quiz-result-content-" + hiring_round_id).innerHTML = "<div class='col s12'><p style='padding:1em;' class='red lighten-3 center'>Unable to load the result.</p></div>";
//            }
//
//            $("#attempted-quiz-result-content-" + hiring_round_id).show();
//            $("#attempted-quiz-preloader-" + hiring_round_id).hide();
//            $('#quiz-question-list-' + hiring_round_id).show();
//        },
//        error: function(xhr, textstatus, errorthrown) {
//            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
//        }
//    });
//}



function load_deassgined_result(hiring_round_id){
    $("#attempted-quiz-result-content-" + hiring_round_id).hide();
    $("#attempted-quiz-preloader-" + hiring_round_id).show();
    $('#hidden-attempted-quiz-result-content-'+hiring_round_id).html("");
    authkey = "";
    if (window.location.pathname.indexOf("/applicant/report-card") != -1) {
        authkey = getUrlVars()["authkey"];
    }

    $.ajax({
        url: "/administrator/deassigned-quiz-result/",
        type: "POST",
        headers: {
            "X-CSRFToken": getCsrfToken()
        },
        data: {
            hiring_round_id: hiring_round_id,
            authkey: authkey,
            
        },
        success: function (response) {
            console.log(response);
            if (response["status_code"] == 200) {

                section_timing_html = '<div class="col s12 m12 row">\
                <div class="col s12"\
                onmouseover="" style="cursor: pointer;" onclick="expandTimeSpentTable(' + hiring_round_id+ ')"">\
                <i class="material-icons inline-icon quiz-section-result-expand-icon" \
                  id="time-spent-table-icon-' + hiring_round_id + '">expand_more</i>\
                Quiz Timing Info\
                </div>\
                <div class="col s12 m6 l6">\
                <table id="time-info-table-'+hiring_round_id+'" class="highlight centered" style="display:none;border:0.1em solid black;border-radius:1em;"">\
                    <tbody>\
                        <tr>\
                            <td><b>Quiz assign time:</b></td>\
                            <td>'+response['quiz_assign_time']+'</td>\
                        </tr>\
                        <tr>\
                            <td><b>Quiz start time:</b></td>\
                            <td>'+response['quiz_start_time']+'</td>\
                        </tr>\
                        <tr>\
                            <td><b>Quiz end time:</b></td>\
                            <td>'+response['quiz_end_time']+'</td>\
                        </tr>\
                        <tr>\
                            <td><b>Session frequencies:</b></td>';

                if(response['sessions'].length){
                    section_timing_html += '<td><a class="modal-trigger tooltipped" data-tooltip="Click for more info" href="#modal-session-info-'+hiring_round_id+'">'+response['sessions'].length+'</a></td>'
                }
                else{
                    section_timing_html += '<td>No records</td>'
                }
                section_timing_html += '</tr></tbody></table></div>';
                section_timing_html+='<div class="col s12 m6 l6">\
                <table id="time-spent-table-'+hiring_round_id+'" class="highlight centered" style="display:none;border:0.1em solid black;border-radius:1em;"">\
                    <thead>\
                        <tr>\
                        <th>Section Name</th>\
                        <th>Time spent</th>\
                        </tr>\
                    </thead>\
                    <tbody>';

                for(let i=0; i<response['section_timing'].length; i++){
                   
                    section_timing_html+='<tr>\
                        <td><b>'+response['section_timing'][i]['section_name']+'</b></td>\
                        <td>'+response['section_timing'][i]['time_spent']+'</td>\
                        </tr>';
                    
                }
                section_timing_html += '</tbody></table></div>';

                // if(response['sessions'].length)


                section_timing_html+='</div><br>';

                session_html = '<div class="modal-content">\
                <table id="sessions-table-'+hiring_round_id+'" class="highlight centered" style="border:0.1em solid black;border-radius:1em;"">\
                    <thead>\
                        <tr>\
                        <th></th>\
                        <th>Login time</th>\
                        <th>Logout time</th>\
                        </tr>\
                    </thead>\
                    <tbody>';

                for(let i=0; i<response['sessions'].length; i++){
                    session_html+='<tr>\
                        <td>'+(i+1)+'</td>\
                        <td>'+response['sessions'][i]['login']+'</td>\
                        <td>'+response['sessions'][i]['logout']+'</td>\
                        </tr>';
                }
                session_html += '</tbody></table></div>\
                <div class="modal-footer">\
                <a class="btn grey modal-close">Close</a>\
                </div>';

                $('#modal-session-info-'+hiring_round_id).html(session_html);

                document.getElementById("attempted-quiz-timings-content-" + hiring_round_id).innerHTML = section_timing_html;

                quiz_result = "";
                if (response["recruiter_remark"] != -1) {
                    console.log("herer");
                    temp_quiz_result = '\
                    <div class="row">\
                        <div class="col s12 m3" style="padding-top:1em;">\
                            <b>Recruiter\'s Remarks:</b>\
                        </div>\
                        <div class="col s12 m9">\
                        <textarea id="recruiters-remark-' + hiring_round_id + '" placeholder="Recruiter\'s remark" class="materialize-textarea" style="display:none;">' + response["recruiter_remark"] + '</textarea>\
                        <h6 id="recruiters-remark-text-' + hiring_round_id + '" style="padding-top:0.3em;">' + response["recruiter_remark"] + '</h6>\
                        </div>\
                    </div>';
                   
                   
                    temp_quiz_result += '<a class="btn one right disabled  tooltipped"  data-position="bottom" data-tooltip="Quiz is deassigned you cannot modify" >Edit Remarks</a>';
                  

                    $('#quiz-video-list-' + hiring_round_id).show();
		    if(!$('#recruiters-remark-text-' + hiring_round_id).html() || $('#recruiters-remark-text-' + hiring_round_id).html()==""){
                        $('#recruiters-remark-text-' + hiring_round_id).html("No Recruiters Remarks Added Yet");
                    }
                }
                if (response["quiz_result"].length == 0) {
                    quiz_result += "<div class='col s12'><p style='padding:1em;' class='green lighten-3 center'>Applicant haven't attempted quiz yet.</p></div>";
                } else {
                    quiz_result_list = response["quiz_result"]["quiz_section_result_list"];
                    has_objective = false;
                    for(i=0;i<quiz_result_list.length;i++){
                        if(quiz_result_list[i]['type']=="OBJ"){
                            has_objective = true;
                            break;
                        }
                    }
            
            console.log(quiz_result_list)
		     if (quiz_result_list.length > 0) {
		      if (has_objective) {
                     $('#tbody-brief-result-objective-'+hiring_round_id).html('\
                            <tr>\
                                <th colspan="2">Objective Section</th>\
                            </tr>\
                            <tr>\
                                <th>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Section Name</th>\
                                <th>Applicant Norm Rash Score</th>\
                            </tr>'); 
		     quiz_result += '\
                      <div class="col s12 m6 l6">\
                          <table>\
                              <tbody>\
                                  <tr>\
                                      <td><b>Applicant Percentage</b></td>\
                                      <td>' + response["quiz_result"]["applicant_total_score"] + ' %</td>\
                                  </tr>\
                              </tbody>\
                          </table>\
                      </div>\
                      <div class="col s12 m6 l6">\
                          <table>\
                              <tbody>\
                                  <tr>\
                                      <td><b>Applicant Percentile</b></td>\
                                      <td>' + response["quiz_result"]["applicant_percentile"] + ' %</td>\
                                  </tr>\
                              </tbody>\
                          </table>\
                      </div>\
                      <div class="col s12">\
                          <table>\
                              <thead>\
                                <tr>\
                                    <th>Quiz Section</th>\
                                    <th>Pass score</th>\
                                    <th>Correct score</th>\
                                    <th>Adjusted difficulty score</th>\
                                    <th>Norm Rasch Score</th>\
                                </tr>\
                              </thead>\
                              <tbody>';
			}
                        for (var i = 0; i < quiz_result_list.length; i++) {
                            	if(quiz_result_list[i]['type']!="OBJ")
                                continue;
				quiz_result += '\
                                        <tr onmouseover="" style="cursor: pointer;" onclick="expandQuizSectionResult(' + quiz_result_list[i]["id"] + ')">\
                                          <td>\
                                              <i class="material-icons inline-icon quiz-section-result-expand-icon" \
                                              id="quiz-section-result-expand-icon-' + quiz_result_list[i]["id"] + '">expand_more</i> \
                                              ' + quiz_result_list[i]["section_name"] + '\
                                          </td>\
                                          <!-- <td>';

                            if (quiz_result_list[i]["is_completed"] == true) {
                                quiz_result += '<i class="material-icons green-text">check</i>';
                            } else {
                                quiz_result += '<i class="material-icons red-text">cancel</i>';
                            }

                            quiz_result += '</td>--><!-- <td>';

                            if (quiz_result_list[i]["is_cleared"] == true) {
                                quiz_result += '<i class="material-icons green-text">check</i>';
                            } else {
                                quiz_result += '<i class="material-icons red-text">cancel</i>';
                            }

                            quiz_result += '</td>-->';
			    $('#tbody-brief-result-objective-'+hiring_round_id).append('\
                                <tr>\
                                <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+quiz_result_list[i]['section_name']+'</td>\
                                <td>'+quiz_result_list[i]["diff_score"]+'&nbsp;%</td>\
                                </tr>');

                            quiz_result += '<td>' + quiz_result_list[i]["pass_score"] + '</td>\
                                          <td>' + quiz_result_list[i]["right_answers"] + '</td>\
                                          <td>' + quiz_result_list[i]["adjusted_diff_score"] + '</td>\
                                          <td>' + quiz_result_list[i]["diff_score"] + ' %</td>\
                                        </tr>\
                                        <!-- Detailed Quiz Section Result Report -->\
                                        <tr class="expand-quiz-section-result"\
                                        id="expand-quiz-section-result-' + quiz_result_list[i]["id"] + '"\
                                        style="display:none;">\
                                          <td colspan="6">        \
                                              <div class="row">\
                                                  <div class="col s12 m8 l8">\
                                                      <table class="highlight centered" style="border:0.1em solid black;border-radius:1em;">\
                                                          <thead>\
                                                            <tr>\
                                                                <th></th>\
                                                                <th>Easy</th>\
                                                                <th>Medium</th>\
                                                                <th>Hard</th>\
                                                                <th>Total</th>\
                                                            </tr>\
                                                          </thead>\
                                                          <tbody>\
                                                            <tr>\
						                <td>Allotted</td>\
							        <td id="easy-allotted-'+quiz_result_list[i]['id']+'">' + quiz_result_list[i]["allotted"]["easy"] + '</td>\
							        <td id="medium-allotted-'+quiz_result_list[i]['id']+'">' + quiz_result_list[i]["allotted"]["medium"] + '</td>\
							        <td id="hard-allotted-'+quiz_result_list[i]['id']+'">' + quiz_result_list[i]["allotted"]["hard"] + '</td>\
							        <td id="total-allotted-'+quiz_result_list[i]['id']+'">' + quiz_result_list[i]["allotted"]["total"] + '</td>\
							    </tr>\
							    <tr>\
                                                              <td>Attempt</td>\
                                                              <td id="easy-attempted-'+quiz_result_list[i]['id']  +'">' + quiz_result_list[i]["attempts"]["easy"] + '</td>\
                                                              <td id="medium-attempted-'+quiz_result_list[i]['id']+'">' + quiz_result_list[i]["attempts"]["medium"] + '</td>\
                                                              <td id="hard-attempted-'+quiz_result_list[i]['id']  +'" >' + quiz_result_list[i]["attempts"]["hard"] + '</td>\
                                                              <td id="total-attempted-'+quiz_result_list[i]['id'] +'">' + quiz_result_list[i]["attempts"]["total"] + '</td>\
                                                            </tr>\
                                                            <tr>\
                                                              <td>Correct</td>\
                                                              <td id="easy-correct-'+quiz_result_list[i]['id']  +'">' + quiz_result_list[i]["correct"]["easy"] + '</td>\
                                                              <td id="medium-correct-'+quiz_result_list[i]['id']+'">' + quiz_result_list[i]["correct"]["medium"] + '</td>\
                                                              <td id="hard-correct-'+quiz_result_list[i]['id']  +'">' + quiz_result_list[i]["correct"]["hard"] + '</td>\
                                                              <td id="total-correct-'+quiz_result_list[i]['id'] +'">' + quiz_result_list[i]["correct"]["total"] + '</td>\
                                                            </tr>\
                                                            <tr>\
                                                              <td>%</td>\
                                                              <td>' + quiz_result_list[i]["abs_per"]["easy"] + ' %</td>\
                                                              <td>' + quiz_result_list[i]["abs_per"]["medium"] + ' %</td>\
                                                              <td>' + quiz_result_list[i]["abs_per"]["hard"] + ' %</td>\
                                                              <td>' + quiz_result_list[i]["abs_per"]["total"] + ' %</td>\
                                                            </tr>\
                                                          </tbody>\
                                                       </table>';
                                                  if(quiz_result_list[i]["allotted"]["easy"] == "NA*" || quiz_result_list[i]["allotted"]["easy"] == "N/A"){
                                                        quiz_result+='<p>* Adaptive Quiz section has variable difficulty level questions.</p>';
                                                    }
                                                  quiz_result+='</div>\
                                                  <div class="col s12 m4 l4">\
                                                      <table class="highlight centered" style="border:0.1em solid black;border-radius:1em;">\
                                                          <thead>\
                                                          </thead>\
                                                          <tbody>\
                                                            <tr>\
                                                              <td>Abs Score</td>\
                                                              <td>\
                                                              ' + quiz_result_list[i]["total_abs_per"] + ' %</td>\
                                                            </tr>\
                                                            <!-- <tr>\
                                                              <td>Rasch Score</td>\
                                                              <td>\
                                                              ' + quiz_result_list[i]["rasch_score"] + '</td>\
                                                            </tr> -->\
                                                            <tr>\
                                                              <td>Norm Rasch Score</td>\
                                                              <td>\
                                                                  ' + quiz_result_list[i]["diff_score"] + ' %\
                                                              </td>\
                                                            </tr>\
                                                          </tbody>\
                                                       </table>\
                                                       </div>\
                                                   </div>';
                            //console.log(response['problems_list'][quiz_result_list[i]["section_name"]].length);
                            if (response['problems_list'][quiz_result_list[i]["section_name"]].length > 1) {
                                pro = response['problems_list'][quiz_result_list[i]["section_name"]];
                                //console.log("yes");
				pdf_objective_table_html = '\
                                <table class="objective-table" id="table-'+quiz_result_list[i]["id"]+'" style="display:none;">\
                                <thead>\
                                <tr><th colspan="6">'+quiz_result_list[i]["section_name"]+'</th></tr>\
                                <tr >\
                                <th>'+ pro[0]['no'] + '</th>\
                                <th>'+ pro[0]['difficulty'] + '</th>\
                                <th>'+ pro[0]['question'] + '</th>\
                                <th>'+ pro[0]['attempted_options'] + '</th>\
                                <th>'+ pro[0]['correct_options'] + '</th>\
                                <th>'+ pro[0]['result'] + '</th>\
                                </tr>\
                                </thead>\
                                <tbody>';
                                quiz_result += '<div class="col s12"\
                                            onmouseover="" style="cursor: pointer;" onclick="expandSectionProblemResult(' + quiz_result_list[i]["id"] + ')"">\
                                            <i class="material-icons inline-icon quiz-section-result-expand-icon" \
                                              id="section-problem-table-icon-' + quiz_result_list[i]["id"] + '">expand_more</i>\
                                            Detailed Problem Result\
                                            </div>';


                                quiz_result += '<div id="canvas-'+quiz_result_list[i]["id"]+'" class="row" style="display:none;">\
                                                <div class="col s6 m6 l6">\
                                                <canvas id="canvas-bar-chart-'+quiz_result_list[i]["id"]+'"></canvas>\
                                                </div>\
                                                <div class="col s6 m6 l6">\
                                                <canvas id="canvas-pie-chart-'+quiz_result_list[i]["id"]+'"></canvas>\
                                                </div>\
                                                </div>';

                                quiz_result += '<div class="col s12" >\
                                                <table style="display:none;" id = "section-problem-table-'+ quiz_result_list[i]["id"] + '">\
                                                    <thead>\
                                                    <tr >\
                                                        <th>'+ pro[0]['no'] + '</th>\
                                                        <th>'+ pro[0]['difficulty'] + '</th>\
                                                        <th style="width:50%">'+ pro[0]['question'] + '</th>\
                                                        <th>'+ pro[0]['attempted_options'] + '</th>\
                                                        <th>'+ pro[0]['correct_options'] + '</th>\
                                                        <th>'+ pro[0]['result'] + '</th>\
                                                    </tr>\
                                                    </thead><tbody>';
//                                for (let j = 1; j < pro.length; j++) {
//                                    quiz_result += '<tr>\
//                                    <td>'+ pro[j]['no'] + '</td>\
//                                    <td>'+ pro[j]['difficulty'] + '</td>\
//                                    <td style="width:50%">'+ pro[j]['question'] + '</td>\
//                                    <td>'+ pro[j]['attempted_options'] + '</td>\
//                                    <td>'+ pro[j]['correct_options'] + '</td>\
//                                    <td>'+ pro[j]['result'] + '</td>\
//                                    </tr>';
//                                }

				for (let j = 1; j < pro.length; j++) {
                                    quiz_result += '<tr>\
                                    <td>'+ pro[j]['no'] + '</td>\
                                    <td>'+ pro[j]['difficulty'] + '</td>\
                                    <td style="width:50%">'+ pro[j]['question'] + '</td>\
                                    <td>'+ pro[j]['attempted_options'] + '</td>\
                                    <td>'+ pro[j]['correct_options'] + '</td>';
				    if(pro[j]['result'] == "Correct"){
					quiz_result += '<td><i class="material-icons green-text ">check</i></td>';}
				    else{
					quiz_result += '<td><i class="material-icons red-text ">close</i></td>';}
                                    //<td>'+ pro[j]['result'] + '</td>\
                                    quiz_result += '</tr>';

                                    pdf_objective_table_html+='\
                                    <tr>\
                                    <th>'+ pro[j]['no'] + '</th>\
                                    <th>'+ pro[j]['difficulty'] + '</th>\
                                    <th>'+ pro[j]['question'] + '</th>\
                                    <th>'+ pro[j]['attempted_options'] + '</th>\
                                    <th>'+ pro[j]['correct_options'] + '</th>\
                                    <th>'+ pro[j]['result'] + '</th>\
                                    </tr>';
                                }

                                quiz_result += '</tbody></table>\
                                                </div>';
				pdf_objective_table_html+='</tbody></table>';
                                $('#hidden-attempted-quiz-result-content-'+hiring_round_id).append(pdf_objective_table_html);

                            }
                            quiz_result += '</td>\
                            </tr>';
                        }
			if (has_objective) {
                        quiz_result += '</tbody>\
                              </table>\
                          </div>\
			 <div class="col s12">\
                              <br>\
                              <a class="btn one right" onclick="expandAllQuizSectionResult()">Expand</a>\
                              <a class="btn one right" onclick="hideAllQuizSectionResult()">Hide</a>\
                          </div>';
			}
                    }
                    document.getElementById("attempted-quiz-result-content-" + hiring_round_id).innerHTML = quiz_result;
                }
            } else if(response['status_code'] == 201){
                document.getElementById("attempted-quiz-result-content-" + hiring_round_id).innerHTML = "<div class='col s12'><p style='padding:1em;' class='yellow lighten-3 center'>Quiz is yet to be attempted.</p></div>";
            }
            else {
                document.getElementById("attempted-quiz-result-content-" + hiring_round_id).innerHTML = "<div class='col s12'><p style='padding:1em;' class='red lighten-3 center'>Unable to load the result.</p></div>";
            }
            $('#quiz-question-list-' + hiring_round_id).show();
            $('#btn-download-quiz-report-'+hiring_round_id).show();
	    $("#attempted-quiz-result-content-" + hiring_round_id).show();
            $("#attempted-quiz-preloader-" + hiring_round_id).hide();
        },
        error: function (xhr, textstatus, errorthrown) {
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
        }
    });
}



function load_quiz_result(student_id, hiring_round_id) {

    $("#attempted-quiz-result-content-" + hiring_round_id).hide();
    $("#attempted-quiz-preloader-" + hiring_round_id).show();
    $('#hidden-attempted-quiz-result-content-'+hiring_round_id).html("");
    authkey = "";
    if (window.location.pathname.indexOf("/applicant/report-card") != -1) {
        authkey = getUrlVars()["authkey"];
    }

    $.ajax({
        url: "/administrator/quiz-result/",
        type: "POST",
        headers: {
            "X-CSRFToken": getCsrfToken()
        },
        data: {
            student_id: student_id,
            quiz_config_id: hiring_round_id,
            hiring_round_id: hiring_round_id,
            authkey: authkey
        },
        success: function (response) {
            console.log(response);
            if (response["status_code"] == 200) {

                section_timing_html = '<div class="col s12 m12 row">\
                <div class="col s12"\
                onmouseover="" style="cursor: pointer;" onclick="expandTimeSpentTable(' + hiring_round_id+ ')"">\
                <i class="material-icons inline-icon quiz-section-result-expand-icon" \
                  id="time-spent-table-icon-' + hiring_round_id + '">expand_more</i>\
                Quiz Timing Info\
                </div>\
                <div class="col s12 m6 l6">\
                <table id="time-info-table-'+hiring_round_id+'" class="highlight centered" style="display:none;border:0.1em solid black;border-radius:1em;"">\
                    <tbody>\
                        <tr>\
                            <td><b>Quiz assign time:</b></td>\
                            <td>'+response['quiz_assign_time']+'</td>\
                        </tr>\
                        <tr>\
                            <td><b>Quiz start time:</b></td>\
                            <td>'+response['quiz_start_time']+'</td>\
                        </tr>\
                        <tr>\
                            <td><b>Quiz end time:</b></td>\
                            <td>'+response['quiz_end_time']+'</td>\
                        </tr>\
                        <tr>\
                            <td><b>Session frequencies:</b></td>';

                if(response['sessions'].length){
                    section_timing_html += '<td><a class="modal-trigger tooltipped" data-tooltip="Click for more info" href="#modal-session-info-'+hiring_round_id+'">'+response['sessions'].length+'</a></td>'
                }
                else{
                    section_timing_html += '<td>No records</td>'
                }
                section_timing_html += '</tr></tbody></table></div>';
                section_timing_html+='<div class="col s12 m6 l6">\
                <table id="time-spent-table-'+hiring_round_id+'" class="highlight centered" style="display:none;border:0.1em solid black;border-radius:1em;"">\
                    <thead>\
                        <tr>\
                        <th>Section Name</th>\
                        <th>Time spent</th>\
                        </tr>\
                    </thead>\
                    <tbody>';

                for(let i=0; i<response['section_timing'].length; i++){
                    //if(response['is_deleted']){
                        //section_timing_html+='<tr>\
                        //<td><b>'+response['section_timing'][i]['section_name']+'</b></td>\
                        //<td>-</td>\
                        //</tr>';
                    //}else{
                    //section_timing_html+='<tr>\
                    //    <td><b>'+response['section_timing'][i]['section_name']+'</b></td>\
                    //    <td>'+response['section_timing'][i]['time_spent']+'</td>\
                    //     </tr>';
                    //}

                    section_timing_html+='<tr>\
                        <td><b>'+response['section_timing'][i]['section_name']+'</b></td>\
                        <td>'+response['section_timing'][i]['time_spent']+'</td>\
                       </tr>';
                }
                section_timing_html += '</tbody></table></div>';

                // if(response['sessions'].length)


                section_timing_html+='</div><br>';

                session_html = '<div class="modal-content">\
                <table id="sessions-table-'+hiring_round_id+'" class="highlight centered" style="border:0.1em solid black;border-radius:1em;"">\
                    <thead>\
                        <tr>\
                        <th></th>\
                        <th>Login time</th>\
                        <th>Logout time</th>\
                        </tr>\
                    </thead>\
                    <tbody>';

                for(let i=0; i<response['sessions'].length; i++){
                    session_html+='<tr>\
                        <td>'+(i+1)+'</td>\
                        <td>'+response['sessions'][i]['login']+'</td>\
                        <td>'+response['sessions'][i]['logout']+'</td>\
                        </tr>';
                }
                session_html += '</tbody></table></div>\
                <div class="modal-footer">\
                <a class="btn grey modal-close">Close</a>\
                </div>';

                $('#modal-session-info-'+hiring_round_id).html(session_html);

                document.getElementById("attempted-quiz-timings-content-" + hiring_round_id).innerHTML = section_timing_html;

                quiz_result = "";
                if (response["recruiter_remark"] != -1) {
                    console.log("herer");
                    temp_quiz_result = '\
                    <div class="row">\
                        <div class="col s12 m3" style="padding-top:1em;">\
                            <b>Recruiter\'s Remarks:</b>\
                        </div>\
                        <div class="col s12 m9">\
                        <textarea id="recruiters-remark-' + hiring_round_id + '" placeholder="Recruiter\'s remark" class="materialize-textarea" style="display:none;">' + response["recruiter_remark"] + '</textarea>\
                        <h6 id="recruiters-remark-text-' + hiring_round_id + '" style="padding-top:0.3em;">' + response["recruiter_remark"] + '</h6>\
                        </div>\
                    </div>';
                    //temp_quiz_result += '<a class="btn one right" id="edit-remark-' + hiring_round_id + '" onclick="save_remarks(' + hiring_round_id + ',' + student_id + ', this);">Edit Remarks</a>';

                    if(response.is_deleted){
                    temp_quiz_result += '<a class="btn one right disabled  tooltipped"  data-position="bottom" data-tooltip="Quiz is deassigned you cannot modify" id="edit-remark-' + hiring_round_id + '" onclick="save_remarks(' + hiring_round_id + ',' + student_id + ', this);">Edit Remarks</a>';
                    }else{
                    temp_quiz_result += '<a class="btn one right "  id="edit-remark-' + hiring_round_id + '" onclick="save_remarks(' + hiring_round_id + ',' + student_id + ', this);">Edit Remarks</a>';
                    }


                    document.getElementById("attempted-quiz-remark-content-" + hiring_round_id).innerHTML = temp_quiz_result;
                    $('#quiz-video-list-' + hiring_round_id).show();
		    if(!$('#recruiters-remark-text-' + hiring_round_id).html() || $('#recruiters-remark-text-' + hiring_round_id).html()==""){
                        $('#recruiters-remark-text-' + hiring_round_id).html("No Recruiters Remarks Added Yet");
                    }
                }
                if (response["quiz_result"].length == 0) {
                    quiz_result += "<div class='col s12'><p style='padding:1em;' class='green lighten-3 center'>Applicant haven't attempted quiz yet.</p></div>";
                } else {
                    quiz_result_list = response["quiz_result"]["quiz_section_result_list"];
                    has_objective = false;
                    for(i=0;i<quiz_result_list.length;i++){
                        if(quiz_result_list[i]['type']=="OBJ"){
                            has_objective = true;
                            break;
                        }
                    }
		     if (quiz_result_list.length > 0) {
		      if (has_objective) {
                     $('#tbody-brief-result-objective-'+hiring_round_id).html('\
                            <tr>\
                                <th colspan="2">Objective Section</th>\
                            </tr>\
                            <tr>\
                                <th>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Section Name</th>\
                                <th>Applicant Norm Rash Score</th>\
                            </tr>'); 
		     quiz_result += '\
                      <div class="col s12 m6 l6">\
                          <table>\
                              <tbody>\
                                  <tr>\
                                      <td><b>Applicant Percentage</b></td>\
                                      <td>' + response["quiz_result"]["applicant_total_score"] + ' %</td>\
                                  </tr>\
                              </tbody>\
                          </table>\
                      </div>\
                      <div class="col s12 m6 l6">\
                          <table>\
                              <tbody>\
                                  <tr>\
                                      <td><b>Applicant Percentile</b></td>\
                                      <td>' + response["quiz_result"]["applicant_percentile"] + ' %</td>\
                                  </tr>\
                              </tbody>\
                          </table>\
                      </div>\
                      <div class="col s12">\
                          <table>\
                              <thead>\
                                <tr>\
                                    <th>Quiz Section</th>\
                                    <th>Pass score</th>\
                                    <th>Correct score</th>\
                                    <th>Adjusted difficulty score</th>\
                                    <th>Norm Rasch Score</th>\
                                </tr>\
                              </thead>\
                              <tbody>';
			}
                        for (var i = 0; i < quiz_result_list.length; i++) {
                            	if(quiz_result_list[i]['type']!="OBJ")
                                continue;
				quiz_result += '\
                                        <tr onmouseover="" style="cursor: pointer;" onclick="expandQuizSectionResult(' + quiz_result_list[i]["id"] + ')">\
                                          <td>\
                                              <i class="material-icons inline-icon quiz-section-result-expand-icon" \
                                              id="quiz-section-result-expand-icon-' + quiz_result_list[i]["id"] + '">expand_more</i> \
                                              ' + quiz_result_list[i]["section_name"] + '\
                                          </td>\
                                          <!-- <td>';

                            if (quiz_result_list[i]["is_completed"] == true) {
                                quiz_result += '<i class="material-icons green-text">check</i>';
                            } else {
                                quiz_result += '<i class="material-icons red-text">cancel</i>';
                            }

                            quiz_result += '</td>--><!-- <td>';

                            if (quiz_result_list[i]["is_cleared"] == true) {
                                quiz_result += '<i class="material-icons green-text">check</i>';
                            } else {
                                quiz_result += '<i class="material-icons red-text">cancel</i>';
                            }

                            quiz_result += '</td>-->';
			    $('#tbody-brief-result-objective-'+hiring_round_id).append('\
                                <tr>\
                                <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+quiz_result_list[i]['section_name']+'</td>\
                                <td>'+quiz_result_list[i]["diff_score"]+'&nbsp;%</td>\
                                </tr>');

                            quiz_result += '<td>' + quiz_result_list[i]["pass_score"] + '</td>\
                                          <td>' + quiz_result_list[i]["right_answers"] + '</td>\
                                          <td>' + quiz_result_list[i]["adjusted_diff_score"] + '</td>\
                                          <td>' + quiz_result_list[i]["diff_score"] + ' %</td>\
                                        </tr>\
                                        <!-- Detailed Quiz Section Result Report -->\
                                        <tr class="expand-quiz-section-result"\
                                        id="expand-quiz-section-result-' + quiz_result_list[i]["id"] + '"\
                                        style="display:none;">\
                                          <td colspan="6">        \
                                              <div class="row">\
                                                  <div class="col s12 m8 l8">\
                                                      <table class="highlight centered" style="border:0.1em solid black;border-radius:1em;">\
                                                          <thead>\
                                                            <tr>\
                                                                <th></th>\
                                                                <th>Easy</th>\
                                                                <th>Medium</th>\
                                                                <th>Hard</th>\
                                                                <th>Total</th>\
                                                            </tr>\
                                                          </thead>\
                                                          <tbody>\
                                                            <tr>\
						                <td>Allotted</td>\
							        <td id="easy-allotted-'+quiz_result_list[i]['id']+'">' + quiz_result_list[i]["allotted"]["easy"] + '</td>\
							        <td id="medium-allotted-'+quiz_result_list[i]['id']+'">' + quiz_result_list[i]["allotted"]["medium"] + '</td>\
							        <td id="hard-allotted-'+quiz_result_list[i]['id']+'">' + quiz_result_list[i]["allotted"]["hard"] + '</td>\
							        <td id="total-allotted-'+quiz_result_list[i]['id']+'">' + quiz_result_list[i]["allotted"]["total"] + '</td>\
							    </tr>\
							    <tr>\
                                                              <td>Attempt</td>\
                                                              <td id="easy-attempted-'+quiz_result_list[i]['id']  +'">' + quiz_result_list[i]["attempts"]["easy"] + '</td>\
                                                              <td id="medium-attempted-'+quiz_result_list[i]['id']+'">' + quiz_result_list[i]["attempts"]["medium"] + '</td>\
                                                              <td id="hard-attempted-'+quiz_result_list[i]['id']  +'" >' + quiz_result_list[i]["attempts"]["hard"] + '</td>\
                                                              <td id="total-attempted-'+quiz_result_list[i]['id'] +'">' + quiz_result_list[i]["attempts"]["total"] + '</td>\
                                                            </tr>\
                                                            <tr>\
                                                              <td>Correct</td>\
                                                              <td id="easy-correct-'+quiz_result_list[i]['id']  +'">' + quiz_result_list[i]["correct"]["easy"] + '</td>\
                                                              <td id="medium-correct-'+quiz_result_list[i]['id']+'">' + quiz_result_list[i]["correct"]["medium"] + '</td>\
                                                              <td id="hard-correct-'+quiz_result_list[i]['id']  +'">' + quiz_result_list[i]["correct"]["hard"] + '</td>\
                                                              <td id="total-correct-'+quiz_result_list[i]['id'] +'">' + quiz_result_list[i]["correct"]["total"] + '</td>\
                                                            </tr>\
                                                            <tr>\
                                                              <td>%</td>\
                                                              <td>' + quiz_result_list[i]["abs_per"]["easy"] + ' %</td>\
                                                              <td>' + quiz_result_list[i]["abs_per"]["medium"] + ' %</td>\
                                                              <td>' + quiz_result_list[i]["abs_per"]["hard"] + ' %</td>\
                                                              <td>' + quiz_result_list[i]["abs_per"]["total"] + ' %</td>\
                                                            </tr>\
                                                          </tbody>\
                                                       </table>';
                                                  if(quiz_result_list[i]["allotted"]["easy"] == "NA*" || quiz_result_list[i]["allotted"]["easy"] == "N/A"){
                                                        quiz_result+='<p>* Adaptive Quiz section has variable difficulty level questions.</p>';
                                                    }
                                                  quiz_result+='</div>\
                                                  <div class="col s12 m4 l4">\
                                                      <table class="highlight centered" style="border:0.1em solid black;border-radius:1em;">\
                                                          <thead>\
                                                          </thead>\
                                                          <tbody>\
                                                            <tr>\
                                                              <td>Abs Score</td>\
                                                              <td>\
                                                              ' + quiz_result_list[i]["total_abs_per"] + ' %</td>\
                                                            </tr>\
                                                            <!-- <tr>\
                                                              <td>Rasch Score</td>\
                                                              <td>\
                                                              ' + quiz_result_list[i]["rasch_score"] + '</td>\
                                                            </tr> -->\
                                                            <tr>\
                                                              <td>Norm Rasch Score</td>\
                                                              <td>\
                                                                  ' + quiz_result_list[i]["diff_score"] + ' %\
                                                              </td>\
                                                            </tr>\
                                                          </tbody>\
                                                       </table>\
                                                       </div>\
                                                   </div>';
                            //console.log(response['problems_list'][quiz_result_list[i]["section_name"]].length);
                            if (response['problems_list'][quiz_result_list[i]["section_name"]].length > 1) {
                                pro = response['problems_list'][quiz_result_list[i]["section_name"]];
                                //console.log("yes");
				pdf_objective_table_html = '\
                                <table class="objective-table" id="table-'+quiz_result_list[i]["id"]+'" style="display:none;">\
                                <thead>\
                                <tr><th colspan="6">'+quiz_result_list[i]["section_name"]+'</th></tr>\
                                <tr >\
                                <th>'+ pro[0]['no'] + '</th>\
                                <th>'+ pro[0]['difficulty'] + '</th>\
                                <th>'+ pro[0]['question'] + '</th>\
                                <th>'+ pro[0]['attempted_options'] + '</th>\
                                <th>'+ pro[0]['correct_options'] + '</th>\
                                <th>'+ pro[0]['result'] + '</th>\
                                </tr>\
                                </thead>\
                                <tbody>';
                                quiz_result += '<div class="col s12"\
                                            onmouseover="" style="cursor: pointer;" onclick="expandSectionProblemResult(' + quiz_result_list[i]["id"] + ')"">\
                                            <i class="material-icons inline-icon quiz-section-result-expand-icon" \
                                              id="section-problem-table-icon-' + quiz_result_list[i]["id"] + '">expand_more</i>\
                                            Detailed Problem Result\
                                            </div>';


                                quiz_result += '<div id="canvas-'+quiz_result_list[i]["id"]+'" class="row" style="display:none;">\
                                                <div class="col s6 m6 l6">\
                                                <canvas id="canvas-bar-chart-'+quiz_result_list[i]["id"]+'"></canvas>\
                                                </div>\
                                                <div class="col s6 m6 l6">\
                                                <canvas id="canvas-pie-chart-'+quiz_result_list[i]["id"]+'"></canvas>\
                                                </div>\
                                                </div>';

                                quiz_result += '<div class="col s12" >\
                                                <table style="display:none;" id = "section-problem-table-'+ quiz_result_list[i]["id"] + '">\
                                                    <thead>\
                                                    <tr >\
                                                        <th>'+ pro[0]['no'] + '</th>\
                                                        <th>'+ pro[0]['difficulty'] + '</th>\
                                                        <th style="width:50%">'+ pro[0]['question'] + '</th>\
                                                        <th>'+ pro[0]['attempted_options'] + '</th>\
                                                        <th>'+ pro[0]['correct_options'] + '</th>\
                                                        <th>'+ pro[0]['result'] + '</th>\
                                                    </tr>\
                                                    </thead><tbody>';
//                                for (let j = 1; j < pro.length; j++) {
//                                    quiz_result += '<tr>\
//                                    <td>'+ pro[j]['no'] + '</td>\
//                                    <td>'+ pro[j]['difficulty'] + '</td>\
//                                    <td style="width:50%">'+ pro[j]['question'] + '</td>\
//                                    <td>'+ pro[j]['attempted_options'] + '</td>\
//                                    <td>'+ pro[j]['correct_options'] + '</td>\
//                                    <td>'+ pro[j]['result'] + '</td>\
//                                    </tr>';
//                                }

				for (let j = 1; j < pro.length; j++) {
                                    quiz_result += '<tr>\
                                    <td>'+ pro[j]['no'] + '</td>\
                                    <td>'+ pro[j]['difficulty'] + '</td>\
                                    <td style="width:50%">'+ pro[j]['question'] + '</td>\
                                    <td>'+ pro[j]['attempted_options'] + '</td>\
                                    <td>'+ pro[j]['correct_options'] + '</td>';
				    if(pro[j]['result'] == "Correct"){
					quiz_result += '<td><i class="material-icons green-text ">check</i></td>';}
				    else{
					quiz_result += '<td><i class="material-icons red-text ">close</i></td>';}
                                    //<td>'+ pro[j]['result'] + '</td>\
                                    quiz_result += '</tr>';

                                    pdf_objective_table_html+='\
                                    <tr>\
                                    <th>'+ pro[j]['no'] + '</th>\
                                    <th>'+ pro[j]['difficulty'] + '</th>\
                                    <th>'+ pro[j]['question'] + '</th>\
                                    <th>'+ pro[j]['attempted_options'] + '</th>\
                                    <th>'+ pro[j]['correct_options'] + '</th>\
                                    <th>'+ pro[j]['result'] + '</th>\
                                    </tr>';
                                }

                                quiz_result += '</tbody></table>\
                                                </div>';
				pdf_objective_table_html+='</tbody></table>';
                                $('#hidden-attempted-quiz-result-content-'+hiring_round_id).append(pdf_objective_table_html);

                            }
                            quiz_result += '</td>\
                            </tr>';
                        }
			if (has_objective) {
                        quiz_result += '</tbody>\
                              </table>\
                          </div>\
			 <div class="col s12">\
                              <br>\
                              <a class="btn one right" onclick="expandAllQuizSectionResult()">Expand</a>\
                              <a class="btn one right" onclick="hideAllQuizSectionResult()">Hide</a>\
                          </div>';
			}
                    }
                    document.getElementById("attempted-quiz-result-content-" + hiring_round_id).innerHTML = quiz_result;
                }
            } else if(response['status_code'] == 201){
                document.getElementById("attempted-quiz-result-content-" + hiring_round_id).innerHTML = "<div class='col s12'><p style='padding:1em;' class='yellow lighten-3 center'>Quiz is yet to be attempted.</p></div>";
            }
            else {
                document.getElementById("attempted-quiz-result-content-" + hiring_round_id).innerHTML = "<div class='col s12'><p style='padding:1em;' class='red lighten-3 center'>Unable to load the result.</p></div>";
            }
            $('#quiz-question-list-' + hiring_round_id).show();
            $('#btn-download-quiz-report-'+hiring_round_id).show();
	    $("#attempted-quiz-result-content-" + hiring_round_id).show();
            $("#attempted-quiz-preloader-" + hiring_round_id).hide();
        },
        error: function (xhr, textstatus, errorthrown) {
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
        }
    });
}

//function save_remarks(hiring_round_id, student_id) {
//
//      console.log($('#edit-remark-'+hiring_round_id).html());
//
//      if ($('#edit-remark-'+hiring_round_id).html() == "Edit Remarks") {
//         $('#recruiters-remark-' + hiring_round_id).attr("readonly", false);
//         $('#recruiters-remark-' + hiring_round_id).focus();
//         $('#edit-remark-'+hiring_round_id).html("Save Remarks");
//         return;
//     }
//
//      var CSRF_TOKEN = getCsrfToken();
//     console.log($('#recruiters-remark-' + hiring_round_id).val());
//     $.ajax({
//         url: "/administrator/save-remarks/",
//         type: "POST",
//         headers: {
//             'X-CSRFToken': CSRF_TOKEN
//         },
//         data: {
//             'quiz_config_id': hiring_round_id,
//             'student_id': student_id,
//             'remarks': $('#recruiters-remark-' + hiring_round_id).val()
//         },
//         success: function (response) {
//             if (response["status_code"] == 200) {
//                 showToast("Remarks saved", 2000);
//             }
//             else {
//                 showToast("Internal Server Error. Please try again later.", 2000);
//             }
//         },
//         error: function (xhr, textstatus, errorthrown) {
//             showToast("Internal Server Error. Please try again later.", 2000);
//             console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
//         }
//     });
//     $('#recruiters-remark-' + hiring_round_id).attr("readonly", true);
//     // $('#recruiters-remark-' + hiring_round_id).focus();
//     $('#edit-remark-'+hiring_round_id).html("Edit Remarks");
// }


function save_remarks(hiring_round_id, student_id) {

    console.log($('#edit-remark-' + hiring_round_id).html());

    if ($('#edit-remark-' + hiring_round_id).html() == "Edit Remarks") {
        $('#recruiters-remark-' + hiring_round_id).show();
        $('#recruiters-remark-text-' + hiring_round_id).hide();
        $('#recruiters-remark-' + hiring_round_id).focus();
        $('#edit-remark-' + hiring_round_id).html("Save Remarks");
        return;
    }

    var CSRF_TOKEN = getCsrfToken();
    console.log($('#recruiters-remark-' + hiring_round_id).val());
    $.ajax({
        url: "/administrator/save-remarks/",
        type: "POST",
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        },
        data: {
            'quiz_config_id': hiring_round_id,
            'student_id': student_id,
            'remarks': $('#recruiters-remark-' + hiring_round_id).val()
        },
        success: function (response) {
            if (response["status_code"] == 200) {
                showToast("Remarks saved", 2000);
		$('#recruiters-remark-' + hiring_round_id).val(response["remarks"]);
                if($('#recruiters-remark-' + hiring_round_id).val() === ""){
                    $('#recruiters-remark-text-' + hiring_round_id).html("No Recreuiters Remarks Added Yet");
                }
                else{
                    $('#recruiters-remark-text-' + hiring_round_id).html($('#recruiters-remark-' + hiring_round_id).val());
                }
                $('#recruiters-remark-text-' + hiring_round_id).show();
                $('#recruiters-remark-' + hiring_round_id).hide();
            }
            else {
                showToast("Internal Server Error. Please try again later.", 2000);
            }
        },
        error: function (xhr, textstatus, errorthrown) {
            showToast("Internal Server Error. Please try again later.", 2000);
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
        }
    });
    //$('#recruiters-remark-text-' + hiring_round_id).html($('#recruiters-remark-' + hiring_round_id).val());
    //$('#recruiters-remark-text-' + hiring_round_id).show();
    //$('#recruiters-remark-' + hiring_round_id).hide();
    
    // $('#recruiters-remark-' + hiring_round_id).focus();
    $('#edit-remark-' + hiring_round_id).html("Edit Remarks");
}

//function edit_save_descriptive_score(attempted_problem_id, quiz_status_id) {
//     console.log(attempted_problem_id);
//     if ($("#edit-save-descriptive-score-" + attempted_problem_id).html() == "edit") {
//         $("#attempted-descriptive-problem-score-"+attempted_problem_id).removeAttr('disabled');
//         // $("#attempted-descriptive-problem-score-"+attempted_problem_id).focus();
//         // $("#attempted-descriptive-problem-score-"+attempted_problem_id).css("border-bottom","2px solid green");
//         $("#edit-save-descriptive-score-" + attempted_problem_id).html("save");
//     }
//     else {
//
//          // float_regex = /^(?:100|\d{1,2})(?:\.\d*)?$/;
//         inp = $("#attempted-descriptive-problem-score-" + attempted_problem_id).val();
//         // console.log(float_regex.test(inp));
//         // if(float_regex.test(inp)==false){
//         //     showToast("Enter Valid Percentage",1);
//         //     // $("#attempted-descriptive-problem-score-"+attempted_problem_id).focus();
//         // }
//         // else
//         {
//             $.ajax({
//                 url: "/manage-quiz/save-modified-descriptive-score/",
//                 type: "POST",
//                 headers: {
//                     "X-CSRFToken": getCsrfToken()
//                 },
//                 data: {
//                     "attempted_problem_id": attempted_problem_id,
//                     "quiz_status_id": quiz_status_id,
//                     "score": inp,
//                 },
//                 success: function (response) {
//                     showToast("Percentage Updated Successfully");
//                     console.log(response['applicant_percentage']);
//                     if (response['applicant_percentage'] == -1) {
//                         $("#div-descriptive-section-" + quiz_status_id).html('Applicant Percentage:&nbsp;\
//                         <i class="material-icons tooltipped" style="color: red;" data-position="bottom"\
// 									data-tooltip="Evaluate all the questions of the section to get final percentage">error_outline</i>\
//                         ');
//                     }
//                     else {
//                         $("#div-descriptive-section-" + quiz_status_id).html("Applicant Percentage:&nbsp;" + response['applicant_percentage'] + " %")
//                     }
//                 },
//                 error: function (xhr, textstatus, errorthrown) {
//                     console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
//                 }
//             });
//             // $("#attempted-descriptive-problem-score-"+attempted_problem_id).val(parseFloat(inp).toFixed(2));
//             $("#attempted-descriptive-problem-score-"+attempted_problem_id).attr('disabled', 'disabled'); ;
//             // $("#attempted-descriptive-problem-score-"+attempted_problem_id).css("border-bottom","");
//             // $("#edit-save-descriptive-score-" + attempted_problem_id).html("edit");
//         }
//     }
// }

function edit_save_descriptive_score(attempted_problem_id, quiz_status_id) {
    console.log(attempted_problem_id);
    if ($("#edit-save-descriptive-score-" + attempted_problem_id).html() == "edit") {
        $("#div-attempted-descriptive-problem-score-" + attempted_problem_id).show();
        $("#attempted-descriptive-problem-score-text-" + attempted_problem_id).hide();
        // $("#attempted-descriptive-problem-score-"+attempted_problem_id).focus();
        // $("#attempted-descriptive-problem-score-"+attempted_problem_id).css("border-bottom","2px solid green");
        $("#edit-save-descriptive-score-" + attempted_problem_id).html("save");
    }
    else {

        // float_regex = /^(?:100|\d{1,2})(?:\.\d*)?$/;
        inp = $("#attempted-descriptive-problem-score-" + attempted_problem_id).val();
        // console.log(float_regex.test(inp));
        // if(float_regex.test(inp)==false){
        //     showToast("Enter Valid Percentage",1);
        //     // $("#attempted-descriptive-problem-score-"+attempted_problem_id).focus();
        // }
        // else
        {
            $.ajax({
                url: "/manage-quiz/save-modified-descriptive-score/",
                type: "POST",
                headers: {
                    "X-CSRFToken": getCsrfToken()
                },
                data: {
                    "attempted_problem_id": attempted_problem_id,
                    "quiz_status_id": quiz_status_id,
                    "score": inp,
                },
                success: function (response) {
                    showToast("Percentage Updated Successfully");
                    console.log(response['applicant_percentage']);
                    if (response['applicant_percentage'] == -1) {
                        $('#applicant-descriptive-percentage-'+quiz_status_id).html('Evaluation Pending');
			$("#div-descriptive-section-" + quiz_status_id).html('Applicant Percentage:&nbsp;\
                        <i class="material-icons tooltipped" style="color: red;" data-position="bottom"\
									data-tooltip="Evaluate all the questions of the section to get final percentage">error_outline</i>\
                        ');
                    }
                    else {
			$('#applicant-descriptive-percentage-'+quiz_status_id).html(response['applicant_percentage'] + " %");
                        $("#div-descriptive-section-" + quiz_status_id).html("Applicant Percentage:&nbsp;" + response['applicant_percentage'] + " %")
                    }
		    $('#problem-percentage-'+attempted_problem_id).html(response['score']);
                },
                error: function (xhr, textstatus, errorthrown) {
                    console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
                }
            });
            // $("#attempted-descriptive-problem-score-"+attempted_problem_id).val(parseFloat(inp).toFixed(2));
            $("#div-attempted-descriptive-problem-score-" + attempted_problem_id).hide();
            if ($("#attempted-descriptive-problem-score-" + attempted_problem_id).val() != "-1")
                $("#attempted-descriptive-problem-score-text-" + attempted_problem_id).html(parseInt($("#attempted-descriptive-problem-score-" + attempted_problem_id).val()) / 20);
            else
                $("#attempted-descriptive-problem-score-text-" + attempted_problem_id).html("Not Evaluated");
            $("#attempted-descriptive-problem-score-text-" + attempted_problem_id).show();
            // $("#attempted-descriptive-problem-score-"+attempted_problem_id).css("border-bottom","");
            $("#edit-save-descriptive-score-" + attempted_problem_id).html("edit");
        }
    }
}

/*
$(document).on("click", "#btn-upload-applicant-excel", function(e) {

    e.preventDefault();

    var selected_insititute_upload = $("#select-institute-excel-upload").val();
    console.log(selected_insititute_upload)
    if (selected_insititute_upload == "") {
        showToast("Please select the institute for which you want to create applicants through excel.");
        return;
    }

    var selected_stream_upload = $("#select-stream-excel-upload").val();
    if (selected_stream_upload == "") {
        showToast("Please select the stream for which you want to create applicants through excel.");
        return;
    }

    var files = ($("#input-upload-applicant-excel"))[0].files
    if (files.length == 0) {
        showToast("Kindly select an excel file to upload.", 2000);
        return;
    }
    file = files[0];

    var formData = new FormData();
    fname = file['name'].split('.');
    fname = fname[fname.length - 1].toLowerCase();
    if (fname == "xlsx" || fname == "xlx") {
        formData.append("file", file);
    } else {
        showToast("Kindly select an excel file to upload.", 2000);
        return;
    }

    formData.append("institute", selected_insititute_upload);
    formData.append("stream", selected_stream_upload);

    btn_element = document.getElementById("btn-upload-applicant-excel");
    btn_element.disabled = true;

    var CSRF_TOKEN = getCsrfToken();

    $("#preloader_div").show();
    $.ajax({
        url: "/master-list/create-applicants-excel/",
        type: "POST",
        headers: {
           'X-CSRFToken': CSRF_TOKEN
       },
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            $("#preloader_div").hide();
            if (response["status"] == 200) {
                showToast("Applicants Created Successfully.", 2000);
                setTimeout(function() {
                    console.log("success reloading")
                    window.location.reload();
                }, 2100);
            } else if (response["status"] == 301) {
                showToast("File Extension Error. Please Upload Valid File", 2000);
            } else if (response["status"] == 302) {
                error_div = document.getElementById("upload-applicant-excel-error");
                error_div.style.display = "block";
                error_div.innerHTML = response["message"];
                showToast("An Error Occured.", 6000);
            } else {
                showToast("Internal Server Error. Please try again later.", 2000);
            }
            document.getElementById("input-upload-applicant-excel").value = "";
            document.getElementById("input-upload-applicant-excel-v").value = "";
            btn_element.disabled = false;
        },
        error: function(xhr, textstatus, errorthrown) {
            $("#preloader_div").hide();
            showToast("Internal Server Error. Please try again later.", 2000);
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
            document.getElementById("#input-upload-applicant-excel").val("");
            btn_element.disabled = false;
        }
    });
});*/

//$(document).on("click", "#btn-upload-applicant-excel", function(e) {
//
//    e.preventDefault();
//
//    var selected_event_upload = $("#select-event-excel-upload").val();
//    console.log(selected_event_upload)
//    if (selected_event_upload == "") {
//        showToast("Please select the event for which you want to create applicants through excel.");
//        return;
//    }
//
//    var selected_stream_upload = $("#select-stream-excel-upload").val();
//    if (selected_stream_upload == "") {
//        showToast("Please select the stream for which you want to create applicants through excel.");
//        return;
//    }
//
//    var files = ($("#input-upload-applicant-excel"))[0].files
//    if (files.length == 0) {
//        showToast("Kindly select an excel file to upload.", 2000);
//        return;
//    }
//    file = files[0];
//
//    var formData = new FormData();
//    fname = file['name'].split('.');
//    fname = fname[fname.length - 1].toLowerCase();
//    if (fname == "xlsx" || fname == "xls") {
//        formData.append("file", file);
//    } else {
//        showToast("Kindly select an excel file to upload.", 2000);
//        return;
//    }
//
//    formData.append("event", selected_event_upload);
//    formData.append("stream", selected_stream_upload);
//
//    btn_element = document.getElementById("btn-upload-applicant-excel");
//    btn_element.disabled = true;
//
//    var CSRF_TOKEN = getCsrfToken();
//
//    $("#preloader_div").show();
//    $.ajax({
//        url: "/master-list/create-applicants-excel/",
//        type: "POST",
//        headers: {
//           'X-CSRFToken': CSRF_TOKEN
//       },
//        data: formData,
//        processData: false,
//        contentType: false,
//        success: function(response) {
//            $("#preloader_div").hide();
//            if (response["status"] == 200) {
//                showToast("Applicants Created Successfully.", 2000);
//                setTimeout(function() {
//                    console.log("success reloading")
//                    window.location.reload();
//                }, 2100);
//            } else if (response["status"] == 301) {
//                showToast("File Extension Error. Please Upload Valid File", 2000);
//            } else if (response["status"] == 302) {
//                error_div = document.getElementById("upload-applicant-excel-error");
//                error_div.style.display = "block";
//                error_div.innerHTML = response["message"];
//                showToast("An Error Occured.", 6000);
//            } else {
//                showToast("Internal Server Error. Please try again later.", 2000);
//            }
//            document.getElementById("input-upload-applicant-excel").value = "";
//            document.getElementById("input-upload-applicant-excel-v").value = "";
//            btn_element.disabled = false;
//        },
//        error: function(xhr, textstatus, errorthrown) {
//            $("#preloader_div").hide();
//            showToast("Internal Server Error. Please try again later.", 2000);
//            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
//            document.getElementById("#input-upload-applicant-excel").val("");
//            btn_element.disabled = false;
//        }
//    });
//});



$(document).on("click", "#btn-upload-applicant-excel", function(e) {


    var elems = document.querySelector('#modal1');
    var instance = M.Modal.init(elems, {'dismissible' :false});
    instance.open()

    e.preventDefault();

    var selected_event_upload = $("#select-event-excel-upload").val();
    var errors_div = document.getElementById('errors')
    console.log(selected_event_upload)
    if (selected_event_upload == "") {
        showToast("Please select the event for which you want to create applicants through excel.");
        return;
    }

    var selected_stream_upload = $("#select-stream-excel-upload").val();
    if (selected_stream_upload == "") {
        showToast("Please select the stream for which you want to create applicants through excel.");
        return;
    }

    var files = ($("#input-upload-applicant-excel"))[0].files
    if (files.length == 0) {
        showToast("Kindly select an excel file to upload.", 2000);
        return;
    }
    file = files[0];

    var formData = new FormData();
    fname = file['name'].split('.');
    fname = fname[fname.length - 1].toLowerCase();
    if (fname == "xlsx" || fname == "xlx") {
        formData.append("file", file);
    } else {
        showToast("Kindly select an excel file to upload.", 2000);
        return;
    }

    formData.append("event", selected_event_upload);
    formData.append("stream", selected_stream_upload);

    btn_element = document.getElementById("btn-upload-applicant-excel");
    btn_element.disabled = true;

    var CSRF_TOKEN = getCsrfToken();

    $("#preloader_div").show();
    $.ajax({
        url: "/master-list/create-applicants-excel/",
        type: "POST",
        headers: {
           'X-CSRFToken': CSRF_TOKEN
       },
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            console.log(response)
            $("#preloader_div").hide();
            if (response["status"] == 200) {
                showToast("File uploaded successfully .", 2000);

                


            } else if (response["status"] == 301) {
                showToast("File Extension Error. Please Upload Valid File", 2000);
            } else if (response["status"] == 302) {
                error_div = document.getElementById("upload-applicant-excel-error");
                error_div.style.display = "block";
                error_div.innerHTML = response["message"];
                if (response.errors.length){
                    var html = ''
                    response.errors.map(error =>{
                       html  += `<li >${error} </li>`
                    })
                errors_div.innerHTML += html
                }
                response.errors.map(error =>{
                    showToast(error, 2000);
                })
                showToast("An Error Occured.", 6000);
            } else {
                showToast("Internal Server Error. Please try again later.", 2000);
            }
            document.getElementById("input-upload-applicant-excel").value = "";
            document.getElementById("input-upload-applicant-excel-v").value = "";
            btn_element.disabled = false;
        },
        error: function(xhr, textstatus, errorthrown) {
            $("#preloader_div").hide();
            showToast("Internal Server Error. Please try again later.", 2000);
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
            document.getElementById("#input-upload-applicant-excel").val("");
            btn_element.disabled = false;
        }
    });
});







//function load_descriptive_section_text_analysis(attempted_problem_id, quiz_status_id,applicant_id){
//    // document.getElementById("div-text-analysis-descriptive-section-"+attempted_problem_id).innerHTML="1";
//    $.ajax({
//        url:"/manage-quiz/get-text-analysis-attempted-problem/",
//        type:"POST",
//        headers:{
//            "X-CSRFToken":getCsrfToken()
//        },
//        data:{
//            "attempted_problem_id":attempted_problem_id,
//            "quiz_status_id":quiz_status_id,
//            "applicant_id":applicant_id
//        },
//        success: function(response){
//            console.log(response)
//            text_analysis_html = '';
//            if(response["status_code"]==200){
//                //text_analysis_html += '<div class="center"><p>Applicant Percentage: '+response["total_score"]+'%</p></div><hr>';
//                //document.getElementById("div-descriptive-section-"+attempted_problem_id).innerHTML=text_analysis_html;
//                //text_analysis_html = ''
//                text_analysis_html += '<div class="row"><p><b>Applicant Answer: &nbsp; </b> '+response["answer"]+'</p>';
//                text_analysis_html += '<p><b>Solution:</b> '+response["solution"]+'</p><hr>';
//                text_analysis_html += '<!-- <input style = "all:unset;" readonly="readonly" size="3"\
//                 id = "attempted-descriptive-problem-score-'+ attempted_problem_id + '" "type="text"\
//                  value="'+ response["score"].toFixed(2) + '">% --!>\
//                 <div class="row">\
//                  <div class="col s6 m2">\
//                  <b style="padding-top:1rem;">Percentage:</b>\
//                  </div>\
//                  <div class="col s6 m2">\
//                  <select id = "attempted-descriptive-problem-score-'+ attempted_problem_id + '">\
//                      <option value="-1" selected>Not Evaluated</option>\
//                      <option value="0">0</option>\
//                      <option value="20">1</option>\
//                      <option value="40">2</option>\
//                      <option value="60">3</option>\
//                      <option value="80">4</option>\
//                      <option value="100">5</option>\
//                  </select>\
//                  </div>\
//                  <i style="margin-left:50px; cursor: pointer;" class="material-icons inline-icon"\
//                   onclick="edit_save_descriptive_score('+ attempted_problem_id + ',' + quiz_status_id + ')"\
//                  id = "edit-save-descriptive-score-'+ attempted_problem_id + '">save</i>\
//                 </div>\
//                  <!-- <div class="input-field col s12 m2" style="display:inline-block;">\
//                     <select>\
//                     <option value="-1" selected>Not Evaluated</option>\
//                     <option value="0">0 %</option>\
//                     <option value="20">20 %</option>\
//                     <option value="40">40 %</option>\
//                     <option value="60">60 %</option>\
//                     <option value="80">80 %</option>\
//                     <option value="100">100 %</option>\
//                     </select>\
//                 </div> --!>\
//                 </div>';
//                //text_analysis_html += '<p><b>Total Maching Words:</b> '+response["common_words"]+'</p><p><b>Percentage:</b> '+response["score"]+'%</p></div>';
//                //text_analysis_html += '<div class="row"><p><b>Applicant Answer:</b> '+response["answer"]+'</p></div>';
//                // tone_analysis = response["text_analysis"]["tone_analysis"];
//                // document_tone = JSON.parse(tone_analysis)["document_tone"]["tones"];
//                // type_of_tones = {
//                //     "Anger":0,
//                //     "Fear":0,
//                //     "Joy":0,
//                //     "Sadness":0,
//                //     "Analytical":0,
//                //     "Confident":0,
//                //     "Tentative":0
//                // }
//                // for(var i=0;i<document_tone.length;i++){
//                //     tone_details = document_tone[i];
//                //     type_of_tones[tone_details["tone_name"]]=Math.round(tone_details["score"]*100);
//                // }
//
//                // tone_analysis_html = "<div class='row'><h6>Tones</h6><hr><br>";
//                // for(var tone in type_of_tones){
//                //     if(type_of_tones[tone]==0){
//                //         tone_analysis_html+='<span style="margin:0em 1em 0em 1em;">'+tone+'&nbsp;&nbsp;<i class="material-icons inline-icon">cancel</i></span>';
//                //     }else{
//                //         tone_analysis_html+='<span style="margin:0em 1em 0em 1em;">'+tone+'&nbsp;&nbsp;<i class="material-icons inline-icon green-text text-darken-4 tooltipped" data-position="bottom" data-tooltip="'+type_of_tones[tone]+' %">check_circle</i></span>';
//                //     }
//                // }
//                // tone_analysis_html += "</div>";
//
//                // personality_insights = {"personality":[], "needs":[], "values":[]};
//                // try{
//                //     personality_insights = JSON.parse(response["text_analysis"]["personality_insights"]);
//                // }catch{
//                //     console.log("unable to get personality_insights");
//                // }
//                // personality_insights_html = '<div class="row"><br><h6>Personality Portrait</h6><hr><br>';
//                // personality_insights_html += '<div class="col s4">\
//                //                         <table>\
//                //                             <thead>\
//                //                                 <tr>\
//                //                                     <th>Personality</th>\
//                //                                     <th></th>\
//                //                                 </tr>\
//                //                             </thead><tbody>';
//                // for(var i=0;i<personality_insights["personality"].length;i++){
//                //     score = Math.round(personality_insights["personality"][i]["raw_score"]*100);
//                //     personality_insights_html += '<tr>\
//                //         <td>'+personality_insights["personality"][i]["name"]+'</td>\
//                //         <td>'+score+' %</td>\
//                //     </tr>';
//                // }
//
//                // personality_insights_html += '</tbody></table></div>';
//                // personality_insights_html += '<div class="col s4">\
//                //                         <table>\
//                //                             <thead>\
//                //                                 <th>Consumer Needs</th>\
//                //                                 <th></th>\
//                //                             </thead><tbody>';
//
//                // for(var i=0;i<personality_insights["needs"].length;i++){
//                //     score = Math.round(personality_insights["needs"][i]["raw_score"]*100);
//                //     personality_insights_html += '<tr>\
//                //                                     <td>'+personality_insights["needs"][i]["name"]+'</td>\
//                //                                     <td>'+score+' %</td>\
//                //                                 </tr>';                    
//                // }
//                
//                // personality_insights_html +='</tbody></table></div>';
//                // personality_insights_html += '<div class="col s4">\
//                //                         <table>\
//                //                             <thead>\
//                //                                 <th>Values</th>\
//                //                                 <th></th>\
//                //                             </thead><tbody>';
//
//                // for(var i=0;i<personality_insights["values"].length;i++){
//                //     score = Math.round(personality_insights["values"][i]["raw_score"]*100);
//                //     personality_insights_html += '<tr>\
//                //                                     <td>'+personality_insights["values"][i]["name"]+'</td>\
//                //                                     <td>'+score+' %</td>\
//                //                                 </tr>';                    
//                // }
//                // personality_insights_html +='</tbody></table></div></div>';
//                // text_analysis_html += tone_analysis_html + personality_insights_html + get_readable_text_analysis_html(response["text_analysis"]["text_analysis"]);
//            }
//            console.log(text_analysis_html)
//            console.log(attempted_problem_id)
//            document.getElementById("div-text-analysis-descriptive-section-"+attempted_problem_id).innerHTML=text_analysis_html;
//            $('.tooltipped').tooltip();
//            $('#attempted-descriptive-problem-score-' + attempted_problem_id).val(response["score"])
//             $('select').formSelect();
//             $('#attempted-descriptive-problem-score-'+ attempted_problem_id).attr('disabled','disabled'); 
//        },
//        error: function(xhr, textstatus, errorthrown){
//           console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
//        }        
//    });
//}

function load_descriptive_section_text_analysis(attempted_problem_id, quiz_status_id, applicant_id) {
    // document.getElementById("div-text-analysis-descriptive-section-"+attempted_problem_id).innerHTML="1";
    $.ajax({
        url: "/manage-quiz/get-text-analysis-attempted-problem/",
        type: "POST",
        headers: {
            "X-CSRFToken": getCsrfToken()
        },
        data: {
            "attempted_problem_id": attempted_problem_id,
            "quiz_status_id": quiz_status_id,
            "applicant_id": applicant_id
        },
        success: function (response) {
            console.log(response);
            text_analysis_html = '';
            if (response["status_code"] == 200) {
                // text_analysis_html += '<div class="center"><p>Applicant Percentage: '+response["total_score"]+'%</p></div><hr>';
                // document.getElementById("div-descriptive-section-"+attempted_problem_id).innerHTML=text_analysis_html;
                // text_analysis_html = ''
                text_analysis_html += '<div class="row"><p><b>Applicant Answer:&nbsp;</b> ' + response["answer"] + '</p>';
                text_analysis_html += '<p><b>Solution:</b> ' + response["solution"] + '</p><hr>';
                text_analysis_html += '<!-- <input style = "all:unset;" readonly="readonly" size="3"\
                id = "attempted-descriptive-problem-score-'+ attempted_problem_id + '" "type="text"\
                 value="'+ response["score"].toFixed(2) + '">% --!>\
                <div class="row">\
                 <div class="col s6 m2">\
                 <b style="padding-top:1rem;">Percentage:</b>\
                 </div>\
                 <div class="col s6 m2" style="display:none;" id = "div-attempted-descriptive-problem-score-'+ attempted_problem_id + '">\
                 <select id = "attempted-descriptive-problem-score-'+ attempted_problem_id + '">\
                     <option value="-1" selected>Not Evaluated</option>\
                     <option value="0">0</option>\
                     <option value="20">1</option>\
                     <option value="40">2</option>\
                     <option value="60">3</option>\
                     <option value="80">4</option>\
                     <option value="100">5</option>\
                 </select>\
                 </div>\
                 <h6 class="col s6 m2" id = "attempted-descriptive-problem-score-text-'+ attempted_problem_id + '"></h6>'

                 if(response.is_deleted){
                    text_analysis_html   += '<i style="margin-left:50px; cursor: pointer;" class="material-icons tooltipped disabled inline-icon"\
                    data-position="bottom" data-tooltip="Quiz is deassigned you cannot modify"\
                   id = "edit-save-descriptive-score-'+ attempted_problem_id + '">edit</i>\
                  </div> </div>'
                 }else{
                    text_analysis_html   += '<i style="margin-left:50px; cursor: pointer;" class="material-icons  inline-icon"\
                    onclick="edit_save_descriptive_score('+ attempted_problem_id + ',' + quiz_status_id + ')"\
                   id = "edit-save-descriptive-score-'+ attempted_problem_id + '">edit</i>\
                  </div> </div>'
                 }

                //text_analysis_html += '<div class="row"><p><b>Applicant Answer:</b> '+response["answer"]+'</p></div>';
                // tone_analysis = response["text_analysis"]["tone_analysis"];
                // document_tone = JSON.parse(tone_analysis)["document_tone"]["tones"];
                // type_of_tones = {
                //     "Anger":0,
                //     "Fear":0,
                //     "Joy":0,
                //     "Sadness":0,
                //     "Analytical":0,
                //     "Confident":0,
                //     "Tentative":0
                // }
                // for(var i=0;i<document_tone.length;i++){
                //     tone_details = document_tone[i];
                //     type_of_tones[tone_details["tone_name"]]=Math.round(tone_details["score"]*100);
                // }

                // tone_analysis_html = "<div class='row'><h6>Tones</h6><hr><br>";
                // for(var tone in type_of_tones){
                //     if(type_of_tones[tone]==0){
                //         tone_analysis_html+='<span style="margin:0em 1em 0em 1em;">'+tone+'&nbsp;&nbsp;<i class="material-icons inline-icon">cancel</i></span>';
                //     }else{
                //         tone_analysis_html+='<span style="margin:0em 1em 0em 1em;">'+tone+'&nbsp;&nbsp;<i class="material-icons inline-icon green-text text-darken-4 tooltipped" data-position="bottom" data-tooltip="'+type_of_tones[tone]+' %">check_circle</i></span>';
                //     }
                // }
                // tone_analysis_html += "</div>";

                // personality_insights = {"personality":[], "needs":[], "values":[]};
                // try{
                //     personality_insights = JSON.parse(response["text_analysis"]["personality_insights"]);
                // }catch{
                //     console.log("unable to get personality_insights");
                // }
                // personality_insights_html = '<div class="row"><br><h6>Personality Portrait</h6><hr><br>';
                // personality_insights_html += '<div class="col s4">\
                //                         <table>\
                //                             <thead>\
                //                                 <tr>\
                //                                     <th>Personality</th>\
                //                                     <th></th>\
                //                                 </tr>\
                //                             </thead><tbody>';
                // for(var i=0;i<personality_insights["personality"].length;i++){
                //     score = Math.round(personality_insights["personality"][i]["raw_score"]*100);
                //     personality_insights_html += '<tr>\
                //         <td>'+personality_insights["personality"][i]["name"]+'</td>\
                //         <td>'+score+' %</td>\
                //     </tr>';
                // }

                // personality_insights_html += '</tbody></table></div>';
                // personality_insights_html += '<div class="col s4">\
                //                         <table>\
                //                             <thead>\
                //                                 <th>Consumer Needs</th>\
                //                                 <th></th>\
                //                             </thead><tbody>';

                // for(var i=0;i<personality_insights["needs"].length;i++){
                //     score = Math.round(personality_insights["needs"][i]["raw_score"]*100);
                //     personality_insights_html += '<tr>\
                //                                     <td>'+personality_insights["needs"][i]["name"]+'</td>\
                //                                     <td>'+score+' %</td>\
                //                                 </tr>';                    
                // }

                // personality_insights_html +='</tbody></table></div>';
                // personality_insights_html += '<div class="col s4">\
                //                         <table>\
                //                             <thead>\
                //                                 <th>Values</th>\
                //                                 <th></th>\
                //                             </thead><tbody>';

                // for(var i=0;i<personality_insights["values"].length;i++){
                //     score = Math.round(personality_insights["values"][i]["raw_score"]*100);
                //     personality_insights_html += '<tr>\
                //                                     <td>'+personality_insights["values"][i]["name"]+'</td>\
                //                                     <td>'+score+' %</td>\
                //                                 </tr>';                    
                // }
                // personality_insights_html +='</tbody></table></div></div>';
                // text_analysis_html += tone_analysis_html + personality_insights_html + get_readable_text_analysis_html(response["text_analysis"]["text_analysis"]);
            }
            document.getElementById("div-text-analysis-descriptive-section-" + attempted_problem_id).innerHTML = text_analysis_html;
            $('.tooltipped').tooltip();
            $('#attempted-descriptive-problem-score-' + attempted_problem_id).val(response["score"]);
            if ($("#attempted-descriptive-problem-score-" + attempted_problem_id).val() != "-1")
                $("#attempted-descriptive-problem-score-text-" + attempted_problem_id).html(parseInt($("#attempted-descriptive-problem-score-" + attempted_problem_id).val()) / 20);
            else
                $("#attempted-descriptive-problem-score-text-" + attempted_problem_id).html("Not Evaluated");
            $('select').formSelect();
            // $('#attempted-descriptive-problem-score-' + attempted_problem_id).attr('disabled', 'disabled');
            // document.getElementById('attempted-descriptive-problem-score-'+ attempted_problem_id).disabled=true;

        },
        error: function (xhr, textstatus, errorthrown) {
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
        }
    });
}


$(document).on("click", "#old-btn-add-administrator", function(e) 
{
    var username = document.getElementById("input-administrator-username").value;
    if(username == ""){
      showToast("Please enter a unique username.", 2000);
      return;
    }
    var name = document.getElementById("input-administrator-name").value;
    if(!/^[a-zA-Z ]*$/.test(name) || name == ""){
      showToast("Please enter a valid name.");
      return;
    }
    var email = document.getElementById("input-administrator-email").value;
    if(email == ""){
      showToast("Please enter a valid email.");
      return;
    }
    if(!/^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/.test(email)){
     showToast("Please enter a valid email.");
      return; 
    }
    var password = document.getElementById("input-administrator-password").value;
    if(password == ""){
       showToast("Please enter the password.");
      return; 
    }
    json_string = JSON.stringify({
           "username": username,
           "name":name,
           "email":email,
           "password":password
       });

       var CSRF_TOKEN = getCsrfToken();
       $.ajax({
           url: '/master-list/create-new-administrator/',
           type: 'POST',
           headers: {
               'X-CSRFToken': CSRF_TOKEN
           },
           data: {
               data: json_string
           },
           success: function(response) {
               if (response["status_code"] == 200) {
                   showToast("Coordinator created successfully.", 2000);
                   window.location.reload();
               }else if(response["status_code"] == 301){
                showToast("Coordinator already exist. Try another username.", 2000);
               } else if(response['status_code'] == 400){
                showToast("Coordinator already exist. Try another username.", 2000);
               }
               else {
                   showToast("Unable to create new Coordinator. Make sure institute name is unique.", 2000);
                   console.log("Please report this. ", response["status_message"]);
               }
           },
           error: function(xhr, textstatus, errorthrown) {
               console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
           }
       });
});

function deactivate_administrator(administrator_id)
{
    json_string = JSON.stringify({
           "administrator_id": administrator_id,
       });

       var CSRF_TOKEN = getCsrfToken();
       $.ajax({
           url: '/administrator/deactivate-administrator/',
           type: 'POST',
           headers: {
               'X-CSRFToken': CSRF_TOKEN
           },
           data: {
               data: json_string
           },
           success: function(response) {
               if (response["status_code"] == 200) {
                   window.location.reload();
               } else {
                   showToast("Unable to deactivate coordinator. Try again later.", 2000);
                   console.log("Please report this. ", response["status_message"]);
               }
           },
           error: function(xhr, textstatus, errorthrown) {
               console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
           }
       });
}

function activate_adminstrator(administrator_id)
{
    json_string = JSON.stringify({
           "administrator_id": administrator_id,
       });

       var CSRF_TOKEN = getCsrfToken();
       $.ajax({
           url: '/administrator/activate-administrator/',
           type: 'POST',
           headers: {
               'X-CSRFToken': CSRF_TOKEN
           },
           data: {
               data: json_string
           },
           success: function(response) {
               if (response["status_code"] == 200) {
                   window.location.reload();
               }
               else if(response['status_code'] == 400){
                   showToast("Atmost " + response['max_admin'] + " coordinators can be active at a time.", 2000);
               }
               else {
                   showToast("Unable to activate coordinator. Try again later.", 2000);
                   console.log("Please report this. ", response["status_message"]);
               }
           },
           error: function(xhr, textstatus, errorthrown) {
               console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
           }
       });
}


$(document).on("click", "#btn-add-event", function(e)
{

    let category = $('#selected-event-category').val();
    var event_name = $("#input-event-name").val();
    if (event_name == "") {
        showToast("Event name can not be empty.");
        return;
    }
    //var event_quiz = document.getElementById("select-event-quiz").value;
    var event_quiz = $('#multiple-select-event-quiz').val();
    if(event_quiz == ""){
      showToast("Please select a valid quiz");
      return;
    }
    json_string = JSON.stringify({
           "name": event_name,
           "event_quiz":event_quiz,
           "category":category
       });

       var CSRF_TOKEN = getCsrfToken();
       $.ajax({
           url: '/master-list/add-events/',
           type: 'POST',
           headers: {
               'X-CSRFToken': CSRF_TOKEN
           },
           data: {
               data: json_string
           },
           success: function(response) {
               if (response["status_code"] == 200) {
                   showToast("Event Added Successfully", 2000);
                   window.location.reload();
               } else {
                   showToast("Unable to add new event. Make sure event name is unique.", 2000);
                   console.log("Please report this. ", response["status_message"]);
               }
           },
           error: function(xhr, textstatus, errorthrown) {
               console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
           }
       });
});
function delete_event(event_id)
{
    json_string = JSON.stringify({
           "event_id": event_id,
       });

       var CSRF_TOKEN = getCsrfToken();
       $.ajax({
           url: '/master-list/delete-events/',
           type: 'POST',
           headers: {
               'X-CSRFToken': CSRF_TOKEN
           },
           data: {
               data: json_string
           },
           success: function(response) {
               if (response["status_code"] == 200) {
                   window.location.reload();
               } else {
                   showToast("Unable to delete event. Try again later.", 2000);
                   console.log("Please report this. ", response["status_message"]);
               }
           },
           error: function(xhr, textstatus, errorthrown) {
               console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
           }
       });
}

function edit_event(event_id)
{
  //var event_quiz = document.getElementById("select-event-quiz-edit-"+event_id).value;

    let category = $('#selected-event-category-'+event_id).val();
    var event_quiz = $('#multiple-select-event-quiz-edit-'+event_id).val();
    if(event_quiz == ""){
      showToast("Please select a valid quiz");
      return;
    }
    json_string = JSON.stringify({
           "event_id": event_id,
           "event_quiz":event_quiz,
           "category":category
       });

       var CSRF_TOKEN = getCsrfToken();
       $.ajax({
           url: '/master-list/edit-events/',
           type: 'POST',
           headers: {
               'X-CSRFToken': CSRF_TOKEN
           },
           data: {
               data: json_string
           },
           success: function(response) {
               if (response["status_code"] == 200) {
                   showToast("Event Edited Successfully", 2000);
                   window.location.reload();
               } else {
                   showToast("Unable to edit event. Try again later.", 2000);
                   console.log("Please report this. ", response["status_message"]);
               }
           },
           error: function(xhr, textstatus, errorthrown) {
               console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
           }
       });
}

if(window.location.pathname=="/master-list/events/"){
  $(document).ready(function(){
      var table = $('#table-events-details').DataTable();
  });
}



$(document).on("click", "#btn-add-department", function(e) 
{
    var department = $("#input-department-name").val();
    if (department == "") {
        showToast("Department name can not be empty.");
        return;
    }
    json_string = JSON.stringify({
           "name": department,
       });

       var CSRF_TOKEN = getCsrfToken();
       $.ajax({
           url: '/master-list/add-departments/',
           type: 'POST',
           headers: {
               'X-CSRFToken': CSRF_TOKEN
           },
           data: {
               data: json_string
           },
           success: function(response) {
               if (response["status_code"] == 200) {
                   window.location.reload();
               } else {
                   showToast("Unable to add new department. Make sure department name is unique.", 2000);
                   console.log("Please report this. ", response["status_message"]);
               }
           },
           error: function(xhr, textstatus, errorthrown) {
               console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
           }
       });
});
function delete_department(department_id)
{
    json_string = JSON.stringify({
           "department_id": department_id,
       });

       var CSRF_TOKEN = getCsrfToken();
       $.ajax({
           url: '/master-list/delete-departments/',
           type: 'POST',
           headers: {
               'X-CSRFToken': CSRF_TOKEN
           },
           data: {
               data: json_string
           },
           success: function(response) {
               if (response["status_code"] == 200) {
                   window.location.reload();
               } else {
                   showToast("Unable to delete department. Try again later.", 2000);
                   console.log("Please report this. ", response["status_message"]);
               }
           },
           error: function(xhr, textstatus, errorthrown) {
               console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
           }
       });
}

if(window.location.pathname=="/master-list/departments/"){
  $(document).ready(function(){
      var table = $('#table-departments-details').DataTable();
  });
}






$(document).on("click", "#btn-search-applicant-date", function(e) {
  search_url = "/administrator/manage-applicants?";
  date = document.getElementById("startdate").value;
  console.log(date)
  if(date == ""){
    showToast("Please enter a date.", 2000);
    return;
  }
  search_url += "date=" + date 
  window.location = search_url;
});

// new search by name, mobile, emailid filter
$(document).on("click", "#btn-search-applicant-info", function(e) {
    search_url = "/administrator/manage-applicants?";
    applicant_info = $("#applicant-search-info").val();
    console.log(applicant_info);
    if(applicant_info.trim() == ""){
      showToast("Please enter some Name / Email / Contact to Filter", 2000);
      return;
    }
    search_url += "applicant-info=" + applicant_info;
    window.location = search_url;
});

function activate_event(event_id)
{
    json_string = JSON.stringify({
           "event_id": event_id,
       });

       var CSRF_TOKEN = getCsrfToken();
       $.ajax({
           url: '/administrator/activate-event/',
           type: 'POST',
           headers: {
               'X-CSRFToken': CSRF_TOKEN
           },
           data: {
               data: json_string
           },
           success: function(response) {
               if (response["status_code"] == 200) {
                   window.location.reload();
               } else {
                   showToast("Unable to activate event. Try again later.", 2000);
                   console.log("Please report this. ", response["status_message"]);
               }
           },
           error: function(xhr, textstatus, errorthrown) {
               console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
           }
       });
}

function deactivate_event(event_id)
{
    json_string = JSON.stringify({
           "event_id": event_id,
       });

       var CSRF_TOKEN = getCsrfToken();
       $.ajax({
           url: '/administrator/deactivate-event/',
           type: 'POST',
           headers: {
               'X-CSRFToken': CSRF_TOKEN
           },
           data: {
               data: json_string
           },
           success: function(response) {
               if (response["status_code"] == 200) {
                   window.location.reload();
               } else {
                   showToast("Unable to deactivate institute. Try again later.", 2000);
                   console.log("Please report this. ", response["status_message"]);
               }
           },
           error: function(xhr, textstatus, errorthrown) {
               console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
           }
       });
}






function download_event_excel(event_id){
    showToast("Creating report. Please wait.", 200000);
    console.log(event_id)
    json_string = JSON.stringify({
        "event_id":event_id
    });
    var CSRF_TOKEN = getCsrfToken();
    $.ajax({
       url: '/administrator/download-event-excel/',
       type: 'POST',
       headers: {
           'X-CSRFToken': CSRF_TOKEN
       },
       data: {
           data: json_string
       },
       success: function(response) {
        console.log(response)
           if (response["status_code"] == 200) {
               var file_url = response["file_url"];
              url = window.location.origin + file_url
            window.open(url)
           } else if(response["status_code"]==101) {
               showToast(response["status_message"], 2000);
               console.log("Please report this. ", response["status_message"]);
           }else{
               showToast("Unable to download due to some internal server error. Kindly report the same", 2000);
               console.log("Please report this. ", response["status_message"]);            
           }
            //element.innerHTML = "Download Report";
       },
       error: function(xhr, textstatus, errorthrown){
           console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
       }
   });
}





/// JS for Coordinator


function edit_coordinator_modal(administrator_id){

    $('#input-administrator-id').val(administrator_id);
    $('#input-administrator-username').val($('#administrator-username-'+administrator_id).html());
    $('#input-administrator-name').val($('#administrator-name-'+administrator_id).html());
    $('#input-administrator-email').val($('#administrator-email-'+administrator_id).html());
    var rights = $('#administrator-rights-'+administrator_id).html().trim();
    rights = JSON.parse(rights);
    console.log(rights);
    $('#select-administrator-rights').val(rights).trigger('change');

    var events = $('#administrator-events-'+administrator_id).html().trim();
    console.log(events);
    if(events == "None")
        events = "[]";
    events = JSON.parse(events);
    $('#select-administrator-events').val(events).trigger('change');

    $('#btn-add-administrator').html("Update");
    $('#modal-add-new-administrator').modal('open');
}

function add_coordinator_modal(){
    $('#input-administrator-id').val("-1");
    $('#input-administrator-username').val("");
    $('#input-administrator-name').val("");
    $('#input-administrator-email').val("");
    $('#select-administrator-rights').val(["can_create_applicants"]).trigger('change');
    $('#select-administrator-events').val([]);
    $('#btn-add-administrator').html("Create");
    $('#modal-add-new-administrator').modal('open');
}

$(document).on("click", "#btn-add-administrator", function(e)
{

    administrator_id = $('#input-administrator-id').val();

    var username = document.getElementById("input-administrator-username").value;
    if(username == ""){
      showToast("Please enter a unique username.", 2000);
      return;
    }
    var name = document.getElementById("input-administrator-name").value;
    if(!/^[a-zA-Z ]*$/.test(name) || name == ""){
      showToast("Please enter a valid name.");
      return;
    }
    var email = document.getElementById("input-administrator-email").value;
    if(email == ""){
      showToast("Please enter a valid email.");
      return;
    }
    if(!/^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/.test(email)){
     showToast("Please enter a valid email.");
      return;
    }
    var password = document.getElementById("input-administrator-password").value;
    if(password == "" && administrator_id==-1){
       showToast("Please enter the password.");
      return;
    }
    // feature admin rights
    var rights = $('#select-administrator-rights').val();

    var events = $('#select-administrator-events').val();

    json_string = JSON.stringify({
            "administrator_id": administrator_id,
           "username": username,
           "name":name,
           "email":email,
           "password":password,
           "rights":rights,
           "events":events,
       });

       var CSRF_TOKEN = getCsrfToken();
       $.ajax({
           url: '/master-list/create-new-administrator/',
           type: 'POST',
           headers: {
               'X-CSRFToken': CSRF_TOKEN
           },
           data: {
               data: json_string
           },
           success: function(response) {
               console.log(response);
               if (response["status_code"] == 200) {
                if(administrator_id==-1)
                    showToast("Coordinator created successfully.", 2000);
                else{
                    showToast("Coordinator updated successfully.", 2000);
                }
                   window.location.reload();
               }else if(response["status_code"] == 301){
                showToast("Coordinator already exist. Try another username.", 2000);
               }else if(response["status_code"] == 400){
                   showToast("Atmost " + response['max_admin'] + " coordinators can be active at a time.", 2000);
               }
               else {
                   showToast("Unable to create new Coordinator. Make sure institute name is unique.", 2000);
                   console.log("Please report this. ", response["status_message"]);
               }
           },
           error: function(xhr, textstatus, errorthrown) {
               console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
           }
       });
});



function save_topic_category(topic_pk){

    category = $('#select-topic-category').val()

    json_string = JSON.stringify({
        'topic_pk': topic_pk,
        'category': category,
    })

    $.ajax({
       url: '/manage-quiz/save-topic-category/',
       type: 'POST',
       headers: {
           'X-CSRFToken': getCsrfToken()
       },
       data: {
           data: json_string
       },
       success: function(response) {
           if (response["status_code"] == 200) {
               showToast("Category saved successfully", 2000);
               location.reload();
           }
           else if(response['status_code'] == 400){
               showToast(response['status_message'], 2000);
           }
           else{
               showToast("Unable to save due to some internal server error. Kindly report the same", 2000);
               console.log("Please report this. ", response["status_message"]);
           }
       },
       error: function(xhr, textstatus, errorthrown){
           console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
       }
    });
}






function change_topic_list(){
    let category = $('#problem-category').val();

    $('#div-select-topic-1').hide();
    $('#div-select-topic-3').hide();
    $('#div-select-topic-4').hide();
    $('#div-select-topic-5').hide();

    if(category == "1" || category == "2"){
        $('#div-select-topic-1').show();
    }

    if(category == "3"){
        $('#div-select-topic-3').show();
    }

    if(category == "4"){
        $('#div-select-topic-4').show();
    }

    if(category == "5"){
        $('#div-select-topic-5').show();
    }
}





// feature edit task
function open_edit_task_modal(applicant_id){

    CSRF_TOKEN = getCsrfToken();

    $.ajax({
        url: '/master-list/get-applicant-quiz/',
        type: 'POST',
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        },
        data: {
            'applicant_id': applicant_id
        },
        success: function(response) {
            console.log(response);
            if (response["status_code"] == 200) {
                event_list = response['event_list']
                assigned_event = response['assigned_event']
                assigned_quizzes = response['assigned_quizzes']

                $('#edit-title').html('Change the event assigned to '+response['applicant_name']);

                div_edit_event_html = '<option disabled selected>Change the event assigned to '+response['applicant_name'] +'</option>';

                for(let i=0; i<event_list.length; i++){
                    if(event_list[i]['pk'] == assigned_event){
                        div_edit_event_html += '<option value="'+event_list[i]['pk']+'" selected>'+event_list[i]['name']+'</option>';
                    }
                    else{
                        div_edit_event_html += '<option value="'+event_list[i]['pk']+'">'+event_list[i]['name']+'</option>';
                    }
                }
                quiz_table = '';
                if(assigned_quizzes.length){
                    quiz_table = '<table id="assigned-quiz-table">\
                    <thead>\
                    <tr>\
                        <th class="center">Quiz Name</th>\
                        <th class="center">Check to deassign</th>\
                    </tr>\
                    </thead>\
                    <tbody>';
                    for(let i=0; i<assigned_quizzes.length; i++){
                        quiz_table += '<tr>\
                        <td class="center">'+assigned_quizzes[i]['name']+'</td>\
                        <td class="center">\
                        <label>\
                              <input type="checkbox" value="'+assigned_quizzes[i]['pk']+'" name="delete-quiz-status-checkbox"\
                              class="filled-in">\
                              <span></span>\
                            </label>\
                        </td>';
                    }
                    quiz_table+='</tbody></table>';
                }
                else{
                    quiz_table+='<h6>No Quizzes assigned </h6>';
                }
                $('#edit-applicant-id').html(applicant_id);
                $('#div-quiz-table').html(quiz_table);
                // div_edit_event_html+='</select>'
                $('#select-edit-event').html(div_edit_event_html);
                // $('#selected-edit-event').trigger('change');
            } else if(response["status_code"]==101) {
                showToast(response["status_message"], 2000);
                console.log("Please report this. ", response["status_message"]);
            }else{
                // showToast("Unable to schedule due to some internal server error. Kindly report the same", 2000);
                console.log("Please report this. ", response["status_message"]);
            }

            $('#modal-edit-task').modal('open')
            $('#modal-edit-task').removeAttr('tabindex');
        },
        error: function(xhr, textstatus, errorthrown){
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
        }
    });

}


function update_applicant_tasks(update_event){
    var deassigned_quiz_list = [];
    $.each($("input[name='delete-quiz-status-checkbox']:checked"), function(){
        deassigned_quiz_list.push($(this).val())
    });
    console.log(deassigned_quiz_list);
    var event_pk = $('#select-edit-event').val();
    console.log(event_pk);

    CSRF_TOKEN = getCsrfToken();

    $.ajax({
        url: '/master-list/update-applicant-task/',
        type: 'POST',
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        },
        data: {
            'event_pk': event_pk,
            'deassigned_quiz_list': JSON.stringify(deassigned_quiz_list),
            'applicant_id': $('#edit-applicant-id').html(),
            'update_event': update_event,
        },
        success: function(response) {
            console.log(response);
            if (response["status_code"] == 200) {
                if(update_event == 1){
                    showToast('Event Updated Successfully', 2000);
                }
                else{
                    showToast('Tasks Updated Successfully', 2000);
                }
                location.reload();
            } else if(response["status_code"]==101) {
                showToast(response["status_message"], 2000);
                console.log("Please report this. ", response["status_message"]);
            }else{
                // showToast("Unable to schedule due to some internal server error. Kindly report the same", 2000);
                console.log("Please report this. ", response["status_message"]);
            }
        },
        error: function(xhr, textstatus, errorthrown){
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
        }
    });

}



$(document).on("click", "#btn-search-applicant-date-edit", function(e) {
    search_url = "/master-list/edit-applicants?";
    date = document.getElementById("startdate").value;
    console.log(date)
    if(date == ""){
      showToast("Please enter a date.", 2000);
      return;
    }
    search_url += "date=" + date
    window.location = search_url;
  });



$(document).on("click", "#btn-search-applicant-info-edit", function(e) {
    search_url = "/master-list/edit-applicants?";
    applicant_info = $("#applicant-search-info").val();
    console.log(applicant_info);
    if(applicant_info.trim() == ""){
      showToast("Please enter some Name / Email / Contact to Filter", 2000);
      return;
    }
    search_url += "applicant-info=" + applicant_info;
    window.location = search_url;
});



// Updating Applicant Profile
function update_applicant_profile(applicant_pk){

    name = $('#applicant-name-'+applicant_pk).val();
    email_id = $('#applicant-email-'+ applicant_pk ).val();
    phone_number = $('#applicant-phone-'+applicant_pk).val();
    // location = $()
    adhaar = $('#applicant-adhaar-'+applicant_pk).val();
    pan = $('#applicant-pan-'+applicant_pk).val();
    password = $('#applicant-password-'+applicant_pk).val();

    if(invalid_input(name)){
        showToast("Enter valid name", 2000);
        return;
    }
    if(invalid_input(email_id)){
        showToast("Enter valid email id", 2000);
        return;;
    }
    if(invalid_input(phone_number)){
        showToast("Enter valid contact number", 2000);
        return;
    }
    if(invalid_input(adhaar)){
        showToast("Enter valid adhaar number", 2000);
        return;
    }
    if(invalid_input(pan)){
        showToast("Enter valid pan number", 2000);
        return;
    }
    if(invalid_input(password)){
        password = "";
    }

    json_string = JSON.stringify({
        applicant_pk: applicant_pk,
        name: name,
        email_id: email_id,
        phone_number: phone_number,
        adhaar: adhaar,
        pan: pan,
        password: password,
    });
    var CSRF_TOKEN = getCsrfToken();
    $.ajax({
       url: '/administrator/update-applicant-profile/',
       type: 'POST',
       headers: {
           'X-CSRFToken': CSRF_TOKEN
       },
       data: {
           data: json_string
       },
       success: function(response) {
           console.log(response)
           if (response["status"] == 200) {
               showToast("Profile Updated Successfully", 2000)
               setTimeout(function(){window.location.reload();}, 2000);
           }else{
               showToast(response['message'], 2000);
           }
       },
       error: function(xhr, textstatus, errorthrown){
           console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
       }
   });

}


function invalid_input(input){
    if(input === "" || input == null)
        return true
    return false
}





function expandTimeSpentTable(hiring_round_id) {
    if ($("#time-spent-table-icon-" + hiring_round_id).html() == "expand_less") {
        $("#time-spent-table-" + hiring_round_id).hide();
        $("#time-info-table-" + hiring_round_id).hide();
        // $("#sessions-table-" + hiring_round_id).hide();
        // console.log("1")
        $("#time-spent-table-icon-" + hiring_round_id).html("expand_more");
    } else {
        // console.log("2")
        $("#time-spent-table-" + hiring_round_id).show(1000);
        $("#time-info-table-" + hiring_round_id).show(1000);
        // $("#sessions-table-" + hiring_round_id).show(1000);
        $("#time-spent-table-icon-" + hiring_round_id).html("expand_less");
    }
}




///// Download Excel Dump of the Database



function download_database(option){

    var CSRF_TOKEN = getCsrfToken();
    json_string = JSON.stringify({
        'option': option,
        'start_date': $('#input-start-date-'+option).val(),
        'end_date': $('#input-end-date-'+option).val(),
    });
    showToast("Preparing Requested File...");
    $.ajax({
       url: '/administrator/download-database/',
       type: 'POST',
       headers: {
           'X-CSRFToken': CSRF_TOKEN
       },
       data: {
           data: json_string
       },
       success: function(response) {
           if (response["status_code"] == 200 && response['file_path'] != null) {
                showToast("File Ready to Download");
                var file_path = response["file_path"];
                url = window.location.origin + file_path
                window.open(url);
           }else if(response["status_code"] == 300){
               showToast("No Consolidated Video files in the specified date-range.", 2000);
               //console.log("Please report this.");
           }else{
               showToast("Unable to generate file due to some internal server error. Kindly report the same", 2000);
               console.log("Please report this.");
           }
       },
       error: function(xhr, textstatus, errorthrown){
           console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
       }
   });
}



/// Download Excel Dump of Question Bank


function download_topic_problems(topic_pk){

    var CSRF_TOKEN = getCsrfToken();
    json_string = JSON.stringify({
        'topic_pk': topic_pk
    });
    showToast("Preparing Excel File...");
    $.ajax({
       url: '/manage-quiz/get-topic-problem-excel/',
       type: 'POST',
       headers: {
           'X-CSRFToken': CSRF_TOKEN
       },
       data: {
           data: json_string
       },
       success: function(response) {
           if (response["status_code"] == 200 && response['file_path'] != null) {
                showToast("File Ready to Download");
                var file_path = response["file_path"];
                url = window.location.origin + file_path
                window.open(url);
           }else{
               showToast("Unable to generate file due to some internal server error. Kindly report the same", 2000);
               console.log("Please report this.");
           }
       },
       error: function(xhr, textstatus, errorthrown){
           console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
       }
   });
}


function toggle_problem_visibility(problem_pk){

    json_string = JSON.stringify({
        problem_pk: problem_pk,
    })

    $.ajax({
        url: "/manage-quiz/toggle-problem-visibility/",
        type: "POST",
        headers: {
            'X-CSRFToken': getCsrfToken()
        },
        data: {
            data: json_string
        },
        success: function(response) {
            if (response["status"] == 200) {
                if(response['message']=="active"){
                    $('#td-problem-status-'+problem_pk).html('<a class="btn green tooltipped" href="javascript:void(0)" ' +
                        'onclick="toggle_problem_visibility('+problem_pk+')" data-tooltip="Deactivate Problem">Active</a>');
                    showToast("Problem activated successfully (in all topics)", 2000);
                }
                else{
                    $('#td-problem-status-'+problem_pk).html('<a class="btn red tooltipped" href="javascript:void(0)" ' +
                        'onclick="toggle_problem_visibility('+problem_pk+')" data-tooltip="Activate Problem">Inactive</a>');
                    showToast("Problem deactivated successfully (in all topics)", 2000);
                }
                $('.tooltipped').tooltip();
            } else {
                showToast("Some error occurred", 2000);
            }
        },
        error: function(xhr, textstatus, errorthrown) {
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
        }
    });
}


function activate_quiz(quiz_id){

    var CSRF_TOKEN = getCsrfToken();
    $.ajax({
        url: "/manage-quiz/activate-quiz/",
        type: "POST",
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        },
        data: {
            'quiz_id': quiz_id,
        },
        success: function(response) {
            window.location.reload();
        },
        error: function(xhr, textstatus, errorthrown) {
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
        }
    });
}


function deactivate_quiz(quiz_id){

    var CSRF_TOKEN = getCsrfToken();
    $.ajax({
        url: "/manage-quiz/deactivate-quiz/",
        type: "POST",
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        },
        data: {
            'quiz_id': quiz_id,
        },
        success: function(response) {
            window.location.reload();
        },
        error: function(xhr, textstatus, errorthrown) {
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
        }
    });
}


function activate_topic(topic_id){

    var CSRF_TOKEN = getCsrfToken();
    $.ajax({
        url: "/manage-quiz/activate-topic/",
        type: "POST",
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        },
        data: {
            'topic_id': topic_id,
        },
        success: function(response) {
            console.log("Successfully activated")
            window.location.reload();
        },
        error: function(xhr, textstatus, errorthrown) {
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
        }
    });
}


function deactivate_topic(topic_id){

    var CSRF_TOKEN = getCsrfToken();
    $.ajax({
        url: "/manage-quiz/deactivate-topic/",
        type: "POST",
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        },
        data: {
            'topic_id': topic_id,
        },
        success: function(response) {
            console.log("Successfully deactivated")
            window.location.reload();
        },
        error: function(xhr, textstatus, errorthrown) {
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
        }
    });
}


function copy_quiz_content(destination_quiz_pk){

    source_quiz_pk = $('#select-copy-quiz').val();

    var CSRF_TOKEN = getCsrfToken();
    $.ajax({
        url: "/manage-quiz/copy-quiz/",
        type: "POST",
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        },
        data: {
            'source_quiz_pk': source_quiz_pk,
            'destination_quiz_pk': destination_quiz_pk,
        },
        success: function(response) {
            window.location.reload();
        },
        error: function(xhr, textstatus, errorthrown) {
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
        }
    });
}


function import_question_from_topic(delete_and_import=false, destination_topic_pk){

    var selected_topic_pk = $('#selected-import-topic').val();

    if (selected_topic_pk == "") {
        showToast("Please select a topic to import questions");
        return;
    }

    btn_element = $("#btn-import-question");
    btn_element_2 = $("#btn-delete-import-question");

    btn_element.addClass("disabled");
    btn_element_2.addClass("disabled");

    var CSRF_TOKEN = getCsrfToken();

    $("#preloader_div_import").show();
    $.ajax({
        url: "/manage-quiz/topic/import-topic-questions/",
        type: "POST",
        headers: {
           'X-CSRFToken': CSRF_TOKEN
        },
        data: {
            'source_topic_pk': selected_topic_pk,
            'destination_topic_pk': destination_topic_pk,
            'delete_and_import': delete_and_import,
        },
        success: function(response) {
            $("#preloader_div_import").hide();
            if (response["status"] == 200) {
                showToast("Questions Added Successfully.", 2000);
                setTimeout(function() {
                    console.log("success reloading")
                    window.location.reload();
                }, 2100);
            } else {
                showToast("Internal Server Error. Please try again later.", 2000);
            }
            btn_element.removeClass("disabled");
            btn_element_2.removeClass("disabled");
        },
        error: function(xhr, textstatus, errorthrown) {
            $("#preloader_div_import").hide();
            showToast("Internal Server Error. Please try again later.", 2000);
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
            btn_element.removeClass("disabled");
            btn_element_2.removeClass("disabled");
        }
    });
}

function toggle_range_search(){

    let selected_filters = $('#multiple-select-applicant-search').val();
    if(selected_filters.indexOf("13")!=-1){
        $('#div-quiz-assigned-range-filter').show();
    }
    else{
        $('#div-quiz-assigned-range-filter').hide();
    }
    if(selected_filters.indexOf("15")!=-1){
        $('#div-quiz-completed-range-filter').show();
    }
    else{
        $('#div-quiz-completed-range-filter').hide();
    }
    if(selected_filters.indexOf("16")!=-1){
        $('#div-registered-between-range-filter').show();
    }
    else{
        $('#div-registered-between-range-filter').hide();
    }

    if(selected_filters.indexOf("13")==-1 && selected_filters.indexOf("15")==-1 && selected_filters.indexOf("16")==-1){
        $('#no-range-filter').show();
    }
    else{
        $('#no-range-filter').hide();
    }
}






////////// TAGS Module Javascript Function ////////////////
function save_tag(tag_pk=-1){

    category = $('#selected-tag-category-'+tag_pk).val();
    title = $('#input-tag-title-'+tag_pk).val().trim();

    if(invalid_input(category)){
        showToast("Please select a category");
        return;
    }

    if(invalid_input(title)){
        showToast("Please enter tag title");
        return;
    }

    json_string = JSON.stringify({
        'category': category,
        'title': title,
        'tag_pk': tag_pk,
    })

    $.ajax({
       url: '/master-list/save-tag/',
       type: 'POST',
       headers: {
           'X-CSRFToken': getCsrfToken()
       },
       data: {
           data: json_string
       },
       success: function(response) {
           if (response["status_code"] == 200) {
               showToast("Tag saved successfully", 2000);
               setTimeout(function(){location.reload()},2000);
           }
           else if(response['status_code'] == 101){
               showToast(response['message'], 2000);
           }
           else{
               showToast("Unable to save due to some internal server error. Kindly report the same", 2000);
               console.log("Please report this. ", response["status_message"]);
           }
       },
       error: function(xhr, textstatus, errorthrown){
           console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
       }
    });

}

function change_topic_tag(topic_pk){

    tag_pk = $('#select-topic-tag').val()

    json_string = JSON.stringify({
        'topic_pk': topic_pk,
        'tag_pk': tag_pk,
    })

    $.ajax({
       url: '/manage-quiz/change-topic-tag/',
       type: 'POST',
       headers: {
           'X-CSRFToken': getCsrfToken()
       },
       data: {
           data: json_string
       },
       success: function(response) {
           if (response["status_code"] == 200) {
               showToast("Tag changed successfully", 2000);
           }
           else{
               showToast("Unable to save due to some internal server error. Kindly report the same", 2000);
               console.log("Please report this. ", response["status_message"]);
           }
       },
       error: function(xhr, textstatus, errorthrown){
           console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
       }
    });
}


function assign_tag_applicants(element){
    student_tag_pk = document.getElementById("selected-student-tag").value;
    selected_applicant_id_list = get_list_of_selected_applicants();

    json_string = JSON.stringify({
        student_tag_pk: student_tag_pk,
        selected_applicant_id_list:selected_applicant_id_list
    });

    var CSRF_TOKEN = getCsrfToken();
    element.innerHTML = "Assigning...";
    $.ajax({
       url: '/administrator/assign-tag/',
       type: 'POST',
       headers: {
           'X-CSRFToken': CSRF_TOKEN
       },
       data: {
           data: json_string
       },
       success: function(response) {
           if (response["status_code"] == 200) {
               showToast("Tag assigned successfully", 2000);
               window.location.reload();
           } else if(response["status_code"]==101) {
               showToast(response["status_message"], 2000);
               console.log("Please report this. ", response["status_message"]);
           }else{
               showToast("Unable to assign tag due to some internal server error. Kindly report the same", 2000);
               console.log("Please report this. ", response["status_message"]);
           }
            element.innerHTML = "Assign Task";
       },
       error: function(xhr, textstatus, errorthrown){
           console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
            element.innerHTML = "Assign Tag";
       }
   });
}

////////////// Assigning Tags to Applicants //////////////

function assign_tag_applicants(element){
    student_tag_pk = document.getElementById("selected-student-tag").value;
    selected_applicant_id_list = get_list_of_selected_applicants();

    json_string = JSON.stringify({
        student_tag_pk: student_tag_pk,
        selected_applicant_id_list:selected_applicant_id_list
    });

    var CSRF_TOKEN = getCsrfToken();
    element.innerHTML = "Assigning...";
    $.ajax({
       url: '/administrator/assign-tag/',
       type: 'POST',
       headers: {
           'X-CSRFToken': CSRF_TOKEN
       },
       data: {
           data: json_string
       },
       success: function(response) {
           if (response["status_code"] == 200) {
               showToast("Tag assigned successfully", 2000);
               window.location.reload();
           } else if(response["status_code"]==101) {
               showToast(response["status_message"], 2000);
               console.log("Please report this. ", response["status_message"]);
           }else{
               showToast("Unable to assign tag due to some internal server error. Kindly report the same", 2000);
               console.log("Please report this. ", response["status_message"]);
           }
            element.innerHTML = "Assign Task";
       },
       error: function(xhr, textstatus, errorthrown){
           console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
            element.innerHTML = "Assign Tag";
       }
   });
}
