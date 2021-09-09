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
$(window).on('load', function() {
    setTimeout(function(){
        var isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
    if(isMobile){
        //if(navigator.userAgent.search("Chrome/80") == -1){
          if(navigator.userAgent.indexOf("OP") > -1 || navigator.userAgent.indexOf("UCBrowser/") > -1 || navigator.userAgent.indexOf("MSIE") > -1){
            alert("Please switch to chrome for better experience. If you are using chrome make sure it is updated with the lastest version. Thank you.")
            window.location = "/"
        }
    }
    },1000);
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
function isANumber(str) {
    return !/\D/.test(str);
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


$(document).on("click", "#btn-profile-verify", function(e) {

    var applicantEmailId = $("#input-student-verification-emailid").val();
    if (validateEmail(applicantEmailId) == false) {
        showToast("Please enter valid email id.");
        scrollToGivenElementId("input-student-verification-emailid");
        focusAtGivenElementID("input-student-verification-emailid");
        return;
    }

    var applicantPhoneNumber = $("#input-student-verification-phone-number").val();
    if (applicantPhoneNumber.length != 10) {
        showToast("Please enter valid 10 digit mobile number");
        scrollToGivenElementId("input-student-verification-phone-number");
        focusAtGivenElementID("input-student-verification-phone-number");
        return;
    }

    url = "/applicant/verify?phone_number=" + applicantPhoneNumber + "&email_id=" + applicantEmailId;

    $.ajax({
        url: url,
        type: "GET",
        data: {

        },
        success: function(response) {
            if (response["status_code"] == 200) {
                if (response["is_registered"] == false) {
                    showProfileRegisterCardPanel();
                    $("#input-student-emailid").val(applicantEmailId);
                    $("#input-student-phonenumber").val(applicantPhoneNumber);
                } else {
                    showToast("Account already registered");
                }
            } else {
                console.log("Please report this error: " + response["status_message"]);
            }
        },
        error: function(xhr, textstatus, errorthrown) {
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
        }
    });
});

function capturePictureInit() {

    video = document.getElementById('video');
    canvas = document.getElementById('canvas-profile-pic');
    const snap = document.getElementById("snap");
    // const errorMsgElement = document.querySelector('span#errorMsg');

    const constraints = {
        audio: false,
        video: {
            width: 150,
            height: 150
        }
    };

    // Access webcam
    async function init() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia(constraints);
            handleSuccess(stream);
        } catch (e) {
            alert("Sorry! You will not be able to capture your image with webcam. Please upload it from your devide.");
            // errorMsgElement.innerHTML = `navigator.getUserMedia error:${e.toString()}`;
        }
    }

    // Success
    function handleSuccess(stream) {
        window.stream = stream;
        video.srcObject = stream;
    }

    // Load init
    init();

    // Draw image
    var context = canvas.getContext('2d');
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.restore();
    snap.addEventListener("click", function() {
        context.drawImage(video, 0, 0, 150, 150);
    });
}
$(document).on("change", "#input_profile_image", function(e) {
    var imageLoader = document.getElementById('input_profile_image');
    var canvas = document.getElementById('canvas-profile-pic');
    var ctx = canvas.getContext('2d');
    var reader = new FileReader();
    reader.onload = function(event) {
        var img = new Image();
        img.onload = function() {
            width = 150;
            height = 150;
            canvas.width = width;
            canvas.height = height;
            ctx.drawImage(img, 0, 0, width, height);
        }
        img.src = event.target.result;
    }
    reader.readAsDataURL(imageLoader.files[0]);
    // $("#upload-profile-pic").show();
});

function is_proof_of_id_required() {
    if ($("#input-student-selected-id-proof-type").length == 1) {
        return true;
    }
    return false;
}
function isPANNumber(panVal) {
    var regpan = /^([a-zA-Z]){5}([0-9]){4}([a-zA-Z]){1}?$/;
    if (regpan.test(panVal)) {
        return true;
    } else {
        return false;
    }
}
/*
$(document).on("click", "#btn-signup", function(e) {
    showToast("Your details are being uploaded, please wait for sometime as we complete your registration.", 20000);
    var canvas = document.getElementById("canvas-profile-pic");
    if (isCanvasBlank(canvas)) {
        showToast("Please capture your photo.");
        scrollToGivenElementId("canvas-profile-pic");
        focusAtGivenElementID("canvas-profile-pic");
        return;
    }

    var applicantImage = canvas.toDataURL("image/png");

    var applicantName = $("#input-student-name").val();
    if (applicantName == "") {
        showToast("Name can not be empty.");
        scrollToGivenElementId("input-student-name");
        focusAtGivenElementID("input-student-name");
        return;
    }

    var applicantEmailId = $("#input-student-emailid").val();
    if (validateEmail(applicantEmailId) == false) {
        showToast("Please enter valid email id.");
        scrollToGivenElementId("input-student-emailid");
        focusAtGivenElementID("input-student-emailid");
        return;
    }

    var applicantPhoneNumber = $("#input-student-phonenumber").val();
    if (applicantPhoneNumber.length != 10) {
        showToast("Please enter valid 10 digit mobile number");
        scrollToGivenElementId("input-student-phonenumber");
        focusAtGivenElementID("input-student-phonenumber");
        return;
    }

    var applicantDOB = $("#input-student-dob").val();
    if (applicantDOB == "") {
        showToast("Please enter valid date of birth");
        scrollToGivenElementId("input-student-dob");
        focusAtGivenElementID("input-student-dob");
        return;
    }

    var applicantGender = document.getElementById("input-gender").value;
    if(applicantGender == "None"){
            showToast("Please select your gender.", 2000);
            return
    }

    var applicantCollegeName = $("#input-student-college-name").val();
    if (applicantCollegeName == "") {
        showToast("Please enter college name");
        scrollToGivenElementId("input-student-college-name");
        focusAtGivenElementID("input-student-college-name");
        return;
    }

    //var applicantYearOfPassing = $("#input-student-year-of-passing").val();
    var applicantYearOfPassing = document.getElementById("input-student-year-of-passing").value;
    if (applicantYearOfPassing == "None") {
        showToast("Please enter year of passing");
        scrollToGivenElementId("input-student-year-of-passing");
        focusAtGivenElementID("input-student-year-of-passing");
        return;
    }

    var applicantHiringProcess = null;
    // var applicantHiringProcess = $("#input-student-selected-process").val();
    // if(applicantHiringProcess==""){
    //     showToast("Please select division");
    //     scrollToGivenElementId("input-student-selected-process");
    //     focusAtGivenElementID("input-student-selected-process");
    //     return;
    // }

    //var applicantStream = $("#input-student-stream").val();
    var applicantStream = document.getElementById("input-student-stream").value;
    if (applicantStream == "None") {
        showToast("Please enter your stream");
        scrollToGivenElementId("input-student-stream");
        focusAtGivenElementID("input-student-stream");
        return;
    }

    var applicantEvent = $("#input-student-selected-event").val();
    var applicantEvent = document.getElementById("input-student-selected-event").value;
    if(applicantEvent == "None"){
            showToast("Please select the event.", 2000);
            return
    }

    var applicantDepartment = $("#input-student-department-name").val();
    var applicantDepartment = document.getElementById("input-student-department-name").value;
    if(applicantDepartment == "None"){
            showToast("Please select the department.", 2000);
            return
    }

    var applicantEventQuiz = $("#input-student-selected-event-quiz").val();
    var applicantEventQuiz = document.getElementById("input-student-selected-event-quiz").value;
    if(applicantEventQuiz == "None"){
            showToast("Please select the quiz.", 2000);
            return
    }

    var applicantPercentage = $("#input-student-percentage").val();
    var applicantPercentage = document.getElementById("input-student-percentage").value;
    if (applicantPercentage == "") {
        showToast("Please enter your percentage");
        scrollToGivenElementId("input-student-percentage");
        focusAtGivenElementID("input-student-percentage");
        return;
    }

    var applicantResume = $("#input_profile_resume").val();
    if (applicantResume == "") {
        showToast("Please provide your resume.");
        scrollToGivenElementId("input_profile_resume");
        focusAtGivenElementID("input_profile_resume");
        return;
    }

    var is_id_proof_required = is_proof_of_id_required();

    var type_of_id_proof = null;
    var proof_id_number = null;
    if (is_id_proof_required == true) {

        selected_type_proof_id = $("#input-student-selected-id-proof-type").val();
        if (selected_type_proof_id == null) {
            showToast("Please profile valid proof id.");
            return;
        }

        id_proof_number = $("#input-student-id-proof-number").val();
        if (selected_type_proof_id == 1 && (id_proof_number.length != 12 || isANumber(id_proof_number) == false)) {
            showToast("Please enter valid 12 digit Aadhar Number.", 2000);
            return;
        }
        if (selected_type_proof_id == 2 && isPANNumber(id_proof_number) == false) {

            showToast("Please enter valid PAN Number.", 2000);
            return;
        }

        type_of_id_proof = selected_type_proof_id;
        proof_id_number = id_proof_number;
    }

    id_proof_adhaar_number = $("#input-student-id-proof-adhaar-number").val();
        if ((id_proof_adhaar_number.length != 12 || isANumber(id_proof_adhaar_number) == false)) {
            showToast("Please enter valid 12 digit Aadhar Number.", 2000);
            return;
        }
        id_proof_pan_number = $("#input-student-id-proof-pan-number").val();
        if(id_proof_pan_number !=""){
            if (isPANNumber(id_proof_pan_number) == false) {

                showToast("Please enter valid PAN Number.", 2000);
                return;
            }
        }

    var applicantCategory = document.getElementById("input-category").value;

    var applicantLocation = document.getElementById("input-walkin-location").value;
    if(applicantCategory == "2"){
        if(applicantLocation == ""){
            showToast("Please enter your location.", 2000);
            return;
        }
    }

    if (applicantResume == "") {
        showToast("Please provide your category.");
        scrollToGivenElementId("input-category");
        focusAtGivenElementID("input-category");
        return;
    }

    var applicantEvent = $("#input-student-selected-event").val();
    var applicantEvent = document.getElementById("input-student-selected-event").value;
    console.log(applicantEvent);
    if(applicantEvent == "None"){
            showToast("Please select the event.", 2000);
            return
    }

    var applicantDepartment = $("#input-student-department-name").val();
    var applicantDepartment = document.getElementById("input-student-department-name").value;
    console.log(applicantDepartment);
    if(applicantDepartment == "None"){
            showToast("Please select the department.", 2000);
            return
    }

    var applicantEventQuiz = $("#input-student-selected-event-quiz").val();
    var applicantEventQuiz = document.getElementById("input-student-selected-event-quiz").value;
    console.log(applicantEventQuiz);
    if(applicantEventQuiz == "None"){
            showToast("Please select the quiz.", 2000);
            return
    }

    json_string = JSON.stringify({
        "applicant_image": applicantImage,
        "applicant_name": applicantName,
        "applicant_emailid": applicantEmailId,
        "applicant_phonenumber": applicantPhoneNumber,
        "applicant_dob": applicantDOB,
        "applicant_college": applicantCollegeName,
        "applicant_year_of_passing": applicantYearOfPassing,
        "applicant_stream": applicantStream,
        "applicant_percentage": applicantPercentage,
        "applicant_hiring_process_id": applicantHiringProcess,
        "applicant_category":applicantCategory,
        //"is_id_proof_required": is_id_proof_required,
        //"type_of_id_proof": type_of_id_proof,
        //"proof_id_number": proof_id_number,
        "applicantLocation":applicantLocation,
        "id_proof_adhaar_number":id_proof_adhaar_number,
        "id_proof_pan_number":id_proof_pan_number,
        "applicant_event":applicantEvent,
        "applicant_department":applicantDepartment,
        "applicant_event_quiz":applicantEventQuiz,
        "applicant_gender":applicantGender
    });


    profileResume = ($("#input_profile_resume"))[0].files[0];
    formdata = new FormData();
    formdata.append('file', profileResume);
    formdata.append('data', json_string);

    var CSRF_TOKEN = getCsrfToken();
    $("#preloader_signup_div").show();
    document.getElementById("btn-signup").innerHTML="processing..."
    $.ajax({
        url: "/applicant/signup",
        type: "POST",
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        },
        data: formdata,
        processData: false,
        contentType: false,
        success: function(response) {
            $("#preloader_signup_div").hide();
            if (response["status_code"] == 200) {
                window.location = "/applicant/signup/success";
            } else if (response["status_code"] == 405) {
                showToast("Account already exists", 2000);
            }else if (response["status_code"] == 305) {
                showToast("Account with this adhaar number already exists.", 2000);
            } else {
                showToast("Unable to register your details, Please try again later.", 200);
            }
            document.getElementById("btn-signup").innerHTML="signup";
        },
        error: function(xhr, textstatus, errorthrown) {
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
            document.getElementById("btn-signup").innerHTML="signup";
            showToast("Unable to register your details, Please try again later.", 200);
        }
    });
});
*/
$(document).on("click", "#btn-signup", function(e) {
    showToast("Your details are being uploaded, please wait for sometime as we complete your registration.", 20000);
    var canvas = document.getElementById("canvas-profile-pic");
    if (isCanvasBlank(canvas)) {
        showToast("Please capture your photo.");
        scrollToGivenElementId("canvas-profile-pic");
        focusAtGivenElementID("canvas-profile-pic");
        return;
    }

    var applicantImage = canvas.toDataURL("image/png");

    var applicantName = $("#input-student-name").val();
    if (applicantName == "") {
        showToast("Name can not be empty.");
        scrollToGivenElementId("input-student-name");
        focusAtGivenElementID("input-student-name");
        return;
    }

    var applicantEmailId = $("#input-student-emailid").val();
    if (validateEmail(applicantEmailId) == false) {
        showToast("Please enter valid email id.");
        scrollToGivenElementId("input-student-emailid");
        focusAtGivenElementID("input-student-emailid");
        return;
    }

    var applicantPhoneNumber = $("#input-student-phonenumber").val();
    if (applicantPhoneNumber.length != 10) {
        showToast("Please enter valid 10 digit mobile number");
        scrollToGivenElementId("input-student-phonenumber");
        focusAtGivenElementID("input-student-phonenumber");
        return;
    }

    var applicantDOB = $("#input-student-dob").val();
    if (applicantDOB == "") {
        showToast("Please enter valid date of birth");
        scrollToGivenElementId("input-student-dob");
        focusAtGivenElementID("input-student-dob");
        return;
    }

    var applicantGender = document.getElementById("input-gender").value;
    if(applicantGender == "None"){
            showToast("Please select your gender.", 2000);
            return
    }

    var applicantLocation = document.getElementById("input-walkin-location").value;
    if (applicantResume == "") {
        showToast("Please provide your category.");
        scrollToGivenElementId("input-walkin-location");
        focusAtGivenElementID("input-walkin-location");
        return;
    }

    var applicantEvent = $("#input-student-selected-event").val();
    var applicantEvent = document.getElementById("input-student-selected-event").value;
    if(applicantEvent == "None"){
            showToast("Please select the event.", 2000);
            return
    }

    var applicantEventQuiz = $("#input-student-selected-event-quiz").val();
        var applicantEventQuiz = document.getElementById("input-student-selected-event-quiz").value;
        if(applicantEventQuiz == "None"){
                showToast("Please select the quiz.", 2000);
                return
    }

     var applicantResume = $("#input_profile_resume").val();
    if (applicantResume == "") {
        showToast("Please provide your resume.");
        scrollToGivenElementId("input_profile_resume");
        focusAtGivenElementID("input_profile_resume");
        return;
    }

    id_proof_adhaar_number = $("#input-student-id-proof-adhaar-number").val();
        if(id_proof_adhaar_number != ""){
        if ((id_proof_adhaar_number.length != 12 || isANumber(id_proof_adhaar_number) == false)) {
            showToast("Please enter valid 12 digit Aadhar Number.", 2000);
            return;
        }
        }
        id_proof_pan_number = $("#input-student-id-proof-pan-number").val();
        if(id_proof_pan_number !=""){
            if (isPANNumber(id_proof_pan_number) == false) {

                showToast("Please enter valid PAN Number.", 2000);
                return;
            }
        }

    var applicantCollegeName = null;
    var applicantYearOfPassing = null;
    var applicantHiringProcess = null;
    var applicantStream = null;
    var applicantDepartment = null;
    var applicantPercentage = null;
    var applicantSpecialization = null;

    var applicantCurrentCompany = null;
    var applicantCurrentCtc = null;
    var applicantCurrentDesignation = null;

    var applicantCategory = document.getElementById("input-category").value;


    if(applicantCategory == "1"){
        console.log(applicantCategory)
        var applicantCollegeName = $("#input-student-college-name").val();
        if (applicantCollegeName == "") {
            showToast("Please enter college name");
            scrollToGivenElementId("input-student-college-name");
            focusAtGivenElementID("input-student-college-name");
            return;
        }
        var applicantYearOfPassing = document.getElementById("input-student-year-of-passing").value;
        if (applicantYearOfPassing == "None") {
            showToast("Please enter year of passing");
            scrollToGivenElementId("input-student-year-of-passing");
            focusAtGivenElementID("input-student-year-of-passing");
            return;
        }
        var applicantHiringProcess = null;
        var applicantStream = document.getElementById("input-student-stream").value;
        if (applicantStream == "None") {
            showToast("Please enter your stream");
            scrollToGivenElementId("input-student-stream");
            focusAtGivenElementID("input-student-stream");
            return;
        }
        // var applicantDepartment = $("#input-student-department-name").val();
        var applicantDepartment = document.getElementById("input-student-department-name").value;
        if(applicantDepartment == "None"){
                showToast("Please select the department.", 2000);
                return
        }
        // var applicantPercentage = $("#input-student-percentage").val();
        var applicantPercentage = document.getElementById("input-student-percentage").value;
        if (applicantPercentage == "") {
            showToast("Please enter your percentage");
            scrollToGivenElementId("input-student-percentage");
            focusAtGivenElementID("input-student-percentage");
            return;
        }
        var applicantSpecialization = document.getElementById("input-student-specialization").value;
        if (applicantSpecialization == "None") {
            showToast("Please enter your specialization");
            scrollToGivenElementId("input-student-specialization");
            focusAtGivenElementID("input-student-specialization");
            return;
        }
    }
    else{
        var applicantCurrentCompany = document.getElementById("input-student-current-company").value;
        if (applicantCurrentCompany == "") {
            showToast("Please enter your current company");
            scrollToGivenElementId("input-student-current-company");
            focusAtGivenElementID("input-student-current-company");
            return;
        }
        var applicantCurrentCtc = document.getElementById("input-student-current-ctc").value;
        if (applicantCurrentCtc == "") {
            showToast("Please enter your current ctc");
            scrollToGivenElementId("input-student-current-ctc");
            focusAtGivenElementID("input-student-current-ctc");
            return;
        }
        var applicantCurrentDesignation = document.getElementById("input-student-current-designation").value;
        if (applicantCurrentDesignation == "") {
            showToast("Please enter your current designation");
            scrollToGivenElementId("input-student-current-designation");
            focusAtGivenElementID("input-student-current-designation");
            return;
        }
        var applicantDepartment = document.getElementById("input-student-department-name").value;
        if(applicantDepartment == "None"){
                showToast("Please select the department.", 2000);
                return
        }
    }

    json_string = JSON.stringify({
        "applicant_image": applicantImage,
        "applicant_name": applicantName,
        "applicant_emailid": applicantEmailId,
        "applicant_phonenumber": applicantPhoneNumber,
        "applicant_dob": applicantDOB,
        "applicant_college": applicantCollegeName,
        "applicant_year_of_passing": applicantYearOfPassing,
        "applicant_stream": applicantStream,
        "applicant_percentage": applicantPercentage,
        "applicant_hiring_process_id": applicantHiringProcess,
        "applicant_category":applicantCategory,
        "applicantLocation":applicantLocation,
        "id_proof_adhaar_number":id_proof_adhaar_number,
        "id_proof_pan_number":id_proof_pan_number,
        "applicant_event":applicantEvent,
        "applicant_department":applicantDepartment,
        "applicant_event_quiz":applicantEventQuiz,
        "applicant_gender":applicantGender,
        "applicant_current_company":applicantCurrentCompany,
        "applicant_current_ctc":applicantCurrentCtc,
        "applicant_current_designation":applicantCurrentDesignation,
        "applicant_specialization":applicantSpecialization
    });


    profileResume = ($("#input_profile_resume"))[0].files[0];
    formdata = new FormData();
    formdata.append('file', profileResume);
    formdata.append('data', json_string);

    var CSRF_TOKEN = getCsrfToken();
    $("#preloader_signup_div").show();

    document.getElementById("btn-signup").innerHTML="processing..."
    $.ajax({
        url: "/applicant/signup",
        type: "POST",
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        },
        data: formdata,
        processData: false,
        contentType: false,
        success: function(response) {
            if (response["status_code"] == 200) {
                $("#preloader_signup_div").hide();
                window.location = "/applicant/signup/success";
            } else if (response["status_code"] == 405) {
                showToast("Account already exists", 2000);
            }else if (response["status_code"] == 305) {
                showToast("Account with this adhaar number already exists.", 2000); 
            }else {
                showToast("Unable to register your details, Please try again later.", 200);
            }
            document.getElementById("btn-signup").innerHTML="signup";
        },
        error: function(xhr, textstatus, errorthrown) {
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
            document.getElementById("btn-signup").innerHTML="signup";
            showToast("Unable to register your details, Please try again later.", 200);
        }
    });
});
$(document).on("click", "#btn-login", function(e) {
    var inputUserUsername = $("#input-student-username").val();
    var inputUserPassword = $("#input-student-password").val();

    if (inputUserUsername == "" || inputUserUsername.length != 10) {
        showToast("Please enter valid 10 digit phone number");
        return;
    }

    if (inputUserPassword == "") {
        showToast("Please enter valid password");
        return;
    }

    var CSRF_TOKEN = getCsrfToken();
    json_string = JSON.stringify({
        "username": inputUserUsername,
        "password": inputUserPassword
    });

    $.ajax({
        url: "/authenticate-applicant/",
        type: "POST",
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        },
        data: {
            data: json_string
        },
        success: function(response) {
            // hideGlobalPreloader();
            if (response["status_code"] == 200) {
                window.location = "/applicant/dashboard";
            } else if (response["status_code"] == 405) {
                showToast("Looks like you do not have account registered with us. Please complete your registration.", 2000);
            }else if (response["status_code"] == 305) {
                showToast("Session is running. Kindly logout from one device and try again.", 2000);
            }else {
                showToast("Invalid phone number or password.", 2000);
            }
        },
        error: function(xhr, textstatus, errorthrown) {
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
        }
    });
});

$(document).on("click", "#btn-employee-login", function(e) {
    var inputUserUsername = $("#input-employee-username").val();
    var inputUserPassword = $("#input-employee-password").val();

    var CSRF_TOKEN = getCsrfToken();
    json_string = JSON.stringify({
        "username": inputUserUsername,
        "password": inputUserPassword
    });
    $.ajax({
        url: "/authenticate-administrator/",
        type: "POST",
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        },
        data: {
            data: json_string
        },
        success: function(response) {
            if (response["status_code"] == 200) {
                window.location = "/administrator/manage-applicants/";
            } else if (response["status_code"] == 405) {
                showToast("Unauthorized User", 2000);
            } else {
                showToast("Invalid username or password.", 2000);
            }
        },
        error: function(xhr, textstatus, errorthrown) {
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
        }
    });
});

$(document).on("click", "#btn-start-test-paper", function(e) {
    // $("#check-system-error").hide();
    // if(document.getElementById("checkbox-video-checked").checked==true && document.getElementById("checkbox-audio-checked").checked==true && is_video_checked==true && is_audio_checked==true){
    unique_quiz_id = window.location.pathname.split("/")[3];
    redirect_url = "/applicant/quiz-paper/" + unique_quiz_id;
    // disable_face_analysis = document.getElementById("checkbox-switch-off-face-analytics").checked;
    disable_face_analysis = true
    if (disable_face_analysis == true) {
        redirect_url += "?disabled=true";
    }
    window.location = redirect_url;
    // }else{
    //     $("#check-system-error").show();
    // }
});


function show_quiz_section(){
    event_id = document.getElementById("input-student-selected-event").value;
    var CSRF_TOKEN = getCsrfToken();
    $("#preloader_div").show();
    json_string = JSON.stringify({
        "event_id": event_id,
    });
    $.ajax({
        url: "/get-quiz-section-list/",
        type: "POST",
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        },
        data: {
            data: json_string
        },
        success: function(response) {
            $("#preloader_div").hide();
            if (response["status_code"] == 200) 
            {
                error_div = document.getElementById("get-event-quiz-error");
                error_div.style.display = "none";
                document.getElementById("div-input-event-quiz").style.display="block";  
                html = "<select id=\"input-student-selected-event-quiz\">"
                html += "<option value=\"None\" disabled selected>Choose Quiz<sup>*</sup></option>"
                quiz_section = response["quiz_section"]
                for(var i=0;i<quiz_section.length;i++){
                   html += "<option value="+response["event_id"][i]+">"+quiz_section[i]+"</option>"
                }
                    //html += "<option value=\"none\">None of the above</option>"
                    document.getElementById("div-input-event-quiz").innerHTML = html
                    $('select').select2({
                         width: "100%"
                    });
            } else {
                error_div = document.getElementById("get-event-quiz-error");
                error_div.style.display = "block";
                error_div.innerHTML = "Failed to load quiz. Please select another event or refresh the page and try again."
                showToast("Some Error Occured.", 2000);
            }
        },
        error: function(xhr, textstatus, errorthrown) {
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
        }
    });
}

$(document).on("click", "#btn-reset-password", function(e) {
    phone_number = $("#input-registered-mobile-number").val();
    if (phone_number == "") {
        showToast("Please enter valid mobile number", 2000);
        return;
    }

    url = "/reset-password/" + phone_number;
    var CSRF_TOKEN = getCsrfToken();

    $.ajax({
        url: url,
        type: 'GET',
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        },
        data: {},
        success: function(response) {
            if (response == "200") {
                showToast("New password has been sent to your registered phone number.", 2000);
                setTimeout(function(e) {
                    window.location = "/";
                }, 2000);
            } else if (response == "500") {
                showToast("Please enter valid registered phone number.", 2000);
            } else {
                showToast("Unable to process the request, please try again later.", 2000);
            }
        },
        error: function(xhr, textstatus, errorthrown) {
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
        }
    });
});
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
               } else {
                   showToast("Unable to activate coordinator. Try again later.", 2000);
                   console.log("Please report this. ", response["status_message"]);
               }
           },
           error: function(xhr, textstatus, errorthrown) {
               console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
           }
       });
}




function show_events(category){
    var CSRF_TOKEN = getCsrfToken();
    $("#preloader_div").show();
    json_string = JSON.stringify({
        "category": category,
    });
    $.ajax({
        url: "/get-event-list/",
        type: "POST",
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        },
        data: {
            data: json_string
        },
        success: function(response) {
            $("#preloader_div").hide();
            if (response["status_code"] == 200)
            {
                error_div = document.getElementById("get-event-quiz-error");
                error_div.style.display = "none";
                document.getElementById("div-input-event-quiz").style.display="block";
                html = "<select id=\"input-student-selected-event\" onchange=\"show_quiz_section()\">"
                html += "<option value=\"None\" disabled selected>Choose Event<sup>*</sup></option>\n"
                events = response["events"]
                for(var i=0;i<events.length;i++){
                        html += "<option value="+events[i]['pk']+">"+events[i]['name']+"</option>"
                }
                document.getElementById("div-select-event").innerHTML = html
                $('select').select2({
                     width: "100%"
                });
            } else {
                error_div = document.getElementById("get-event-quiz-error");
                error_div.style.display = "block";
                error_div.innerHTML = "Failed to load events. Please refresh the page and try again."
                showToast("Some Error Occurred.", 2000);
            }
        },
        error: function(xhr, textstatus, errorthrown) {
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
        }
    });
}
