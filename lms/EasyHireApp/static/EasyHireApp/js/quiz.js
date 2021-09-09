var is_quiz_started = null;
var problemCounter = 0;
var totalProblems = 0;
var last_attempted_quiz_section_id = null;
var speech_synthesis_utterance_instance = null;
var speech_synthesis_instance = window.speechSynthesis;
var voices = null;
var socket = null;


function EnableWebSocket(){
    var unique_quiz_config_id = window.location.pathname.split("/")[3];
    var request_user = document.getElementById('request_user')

    //var url = `ws://localhost:8000/ws/sync/time/${unique_quiz_config_id}/${request_user.value}`
    var url = `wss://easyhire-uat.allincall.in/ws/sync/time/${unique_quiz_config_id}/${request_user.value}`
    console.log(url)
    socket = new WebSocket(url);
    socket.onopen = function (e) {console.log("Connected")}
    socket.onmessage = function (e) {console.log(e)};
    socket.onclose = function (e) {
    console.log('Socket closed')
    sync_remaining_time()
    }
}

window.onload = function(){
    document.addEventListener("visibilitychange", function()
    {
        if(document.hidden)
        {
            console.log("Tab change detected")
            window.location = "/applicant/dashboard/"
        }
    }, false);
}

function getCsrfToken() {
    var CSRF_TOKEN = $('input[name="csrfmiddlewaretoken"]').val();
    return CSRF_TOKEN;
}

function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m, key, value) {
        vars[key] = value;
    });
    return vars;
}

function disableF5(e) {
    if ((e.which || e.keyCode) == 116) e.preventDefault();
}

function preventCopyPasteWithID(element_id) {
    if ($("#" + element_id).length == 1) {
        console.log("element found");
        $(document).bind("cut copy paste", '#' + element_id, function(e) {
            console.log("cut copy paste is not allowed");
            e.preventDefault();
        });
    }
}

$(window).keyup(function(e){
      console.log(e.keyCode);
      if(e.keyCode == 27){
          e.preventDefault();
      }
});

function textToSpeech(message_to_be_spoken) {
    if (speech_synthesis_instance != null) {
        speech_synthesis_instance.cancel();
    }
    speech_synthesis_utterance_instance = new SpeechSynthesisUtterance(message_to_be_spoken);
    speech_synthesis_utterance_instance.lang = "hi";
    speech_synthesis_utterance_instance.rate = 0.95;
    speech_synthesis_utterance_instance.pitch = 1;
    speech_synthesis_utterance_instance.volume = 1;
    voices = speech_synthesis_instance.getVoices();
    speech_synthesis_instance.speak(speech_synthesis_utterance_instance);
}

function speakTheProblem() {
    problem = document.getElementById("problem-description").innerText;
    textToSpeech(problem);
}

function startGlobalVideoCapture() {
    $("#btn-start-recording").click();
    //startScreenShotTimer();
}

function stopGlobalVideoCapture() {
    $("#btn-stop-recording").click();
    //clearScreenShotTimer();
}

function takeScreenShot() {
    console.log("Image captured")
    $("#btn-take-screenshot").click();
}

var screen_shot_min_counter_timeout = null;
/*
function startScreenShotTimer() {
    screen_shot_min_counter_timeout = setInterval(takeScreenShot, 20000);
}

function clearScreenShotTimer() {
    if (screen_shot_min_counter_timeout != null) {
        clearInterval(screen_shot_min_counter_timeout);
    }
}*/

var sync_time_min_counter_timeout = null;

function startSyncTimeTimer(){
    sync_time_min_counter_timeout = setInterval(sync_remaining_time, 5000);
}

//$(document).on("click", "#btn-take-screenshot", function(e) {
//    quiz_uuid = window.location.pathname.split("/")[3];
//    video = document.getElementById('global-video-captured-response');
//    canvas = document.getElementById('global-canvas-video-capture');
//    img = document.getElementById('captured-image-from-video');
//
//    canvas.width = 200;
//    canvas.height = 150;
//    canvas.getContext('2d').drawImage(video, 0, 0, 200, 150);
//    img.src = canvas.toDataURL('image/png');
//    CSRF_TOKEN = getCsrfToken();
//    $.ajax({
//        url: "/applicant/save-screenshots/",
//        type: "POST",
//        headers: {
//            "X-CSRFToken": CSRF_TOKEN
//        },
//        data: {
//            applicant_image: img.src,
//            quiz_uuid:quiz_uuid
//        },
//        success: function(response) {
//            if (response["status_code"]==200){
//                /*if(response["is_multiple_faces"]){
//                    $("#modal-multiple-faces-detected").modal({
//                        onCloseEnd: function() {
//                            clearTimeout(completed_quiz_timeout);
//                            window.location = "/applicant/dashboard";
//                        }
//                    });
//                    $("#modal-multiple-faces-detected").modal('open');
//
//                    completed_quiz_timeout = setTimeout(function(e) {
//                        $("#modal-multiple-faces-detected").modal('close');
//                    }, 10000);
//                }*/
//                console.log("success")
//            }
//        },
//        error: function(xhr, textstatus, errorthrown) {
//            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
//        }
//    });
//});

$(document).on("click", "#btn-take-screenshot", function(e) {

    navigator.getMedia = (navigator.getUserMedia || // use the proper vendor prefix
    navigator.webkitGetUserMedia ||
    navigator.mozGetUserMedia ||
    navigator.msGetUserMedia);

    navigator.getMedia({
        video: true,
    }, function () {
        console.log("Webcam is on...");
        quiz_uuid = window.location.pathname.split("/")[3];
        video = document.getElementById('global-video-captured-response');
        canvas = document.getElementById('global-canvas-video-capture');
        img = document.getElementById('captured-image-from-video');

        canvas.width = 200;
        canvas.height = 150;
        canvas.getContext('2d').drawImage(video, 0, 0, 200, 150);
        img.src = canvas.toDataURL('image/png');
        CSRF_TOKEN = getCsrfToken();
        $.ajax({
            url: "/applicant/save-screenshots/",
            type: "POST",
            headers: {
                "X-CSRFToken": CSRF_TOKEN
            },
            data: {
                applicant_image: img.src,
                quiz_uuid:quiz_uuid
            },
            success: function(response) {
                if (response["status_code"]==200){
                    console.log("success")
                }
            },
            error: function(xhr, textstatus, errorthrown) {
                console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
            }
        });
    }, function () {
        alert("Please allow webcam and microphone access, post that kindly restart the quiz.");
		window.location = "/applicant/dashboard/";
    });

});

var last_uploaded_video_url = "";

function saveVideoAtServer(data_url, problem_id) {
    CSRF_TOKEN = getCsrfToken();
    $.ajax({
        url: "/applicant/save-video/",
        type: "POST",
        async: false,
        headers: {
            "X-CSRFToken": CSRF_TOKEN
        },
        data: {
            "video_data_url": data_url,
            "quiz_uuid":quiz_uuid,
             "problem_id":problem_id,
        },
        success: function(response) {
            last_uploaded_video_url = response["url"];
        },
        error: function(xhr, textstatus, errorthrown) {
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
        }
    });
}

var recorded_video_data_url = null;
var flag_video_url_saved = false;
var flag_video_recording_started = false;
function initializeCaptureVideo(video_element_id, video_captured_canvas, start_button_id, stop_button_id, preview_button_id, is_save = false, is_audio_required = false, is_speech_to_text_required = false) {
    // Store a reference of the preview video element and a global reference to the recorder instance
    video = document.getElementById(video_element_id);
    canvas = document.getElementById(video_captured_canvas);
    // When the user clicks on start video recording
    document.getElementById(start_button_id).addEventListener("click", function() {
        // Disable start recording button
        this.disabled = true;
        // Request access to the media devices
        navigator.mediaDevices.getUserMedia({
            audio: is_audio_required,
            video: true
        }).then(function(stream) {
            // Display a live preview on the video element of the page
            setSrcObject(stream, video);

            // Start to display the preview on the video element
            // and mute the video to disable the echo issue !
            video.play();
            video.muted = true;

            // Initialize the recorder
            recorder = new RecordRTCPromisesHandler(stream, {
                mimeType: 'video/webm',
                bitsPerSecond: 128000
            });

            // Start recording the video
            recorder.startRecording().then(function() {
                // console.info('Recording video ...');
            }).catch(function(error) {
                console.error('Cannot start video recording: ', error);
            });

            // release stream on stopRecording
            recorder.stream = stream;
            videoStarted = true;

            if (is_speech_to_text_required == true) {
                startSpeechToText(this);
            }

            // screenShotTimer();
            // Enable stop recording button
            document.getElementById(stop_button_id).disabled = false;
            document.getElementById(preview_button_id).disabled = true;
            if(start_button_id=="btn-start-video-recording") {
                 document.getElementById("btn-next-question").disabled = true;
		 flag_video_recording_started = true;
	   }
        }).catch(function(error) {
            alert("Please allow webcam and microphone access, post that kindly restart the quiz.");
            console.error("Cannot access media devices: ", error);
        });
    }, false);

    // When the user clicks on Stop video recording
    document.getElementById(stop_button_id).addEventListener("click", function() {
        var dfd = $.Deferred();
        this.disabled = true;
        recorder.stopRecording().then(function() {
            // console.info('stopRecording success');

            // Retrieve recorded video as blob and display in the preview element
            videoBlob = recorder.blob;
            // console.log("DataURL:", recorder.getDataURL());
            recorder.getDataURL().then(function(result) {
                recorded_video_data_url = result;
            });

            // video.src = URL.createObjectURL(videoBlob);
            // video.play();

            // Unmute video on preview
            // video.muted = false;

            if (is_speech_to_text_required == true) {
                stopSpeechToText(this);
            }

            // Stop the device streaming
            recorder.stream.stop();
            videoStopped = true;
            // stopSpeechToText(this);
            // clearTimeout(one_min_counter_timeout);
            // Enable record button again !
            //document.getElementById("btn-preview-video-recording").disabled = true;
            document.getElementById(start_button_id).disabled = false;
            document.getElementById(preview_button_id).disabled = false;
            if(stop_button_id=="btn-stop-video-recording")
                 document.getElementById("btn-next-question").disabled = false;   
             flag_video_url_saved = true;
        }).catch(function(error) {
            console.error('stopRecording failure', error);
        });
    }, false);

    document.getElementById(preview_button_id).addEventListener("click", function() {
        this.disabled = true;
        // recorder.previewRecording().then(function() 
        // {
            // Retrieve recorded video as blob and display in the preview element
        // videoBlob = recorder.blob;
        // recorder.getDataURL().then(function(result) {
        //     recorded_video_data_url = result;
        // });
        // video.src = recorded_video_data_url;
        // video.play();
        var new_window = window.open("");
        inner_video_html = "<video controls><source type='video/webm' src='"+recorded_video_data_url+"'></video>";
        new_window.document.write(inner_video_html);
        // window.open(recorded_video_data_url);
        // }).catch(function(error) {
        //     console.error('previewRecording failure', error);
        // });
        document.getElementById(stop_button_id).disabled = true;
        document.getElementById(start_button_id).disabled = false;
    }, false);
}

var global_time_remaining = null;

function startGlobalQuizTimer(time_in_minutes, time_in_seconds=0) {

    function time_remaining(endtime) {
        var t = Date.parse(endtime) - Date.parse(new Date());
        global_time_remaining = t;
        var seconds = Math.floor((t / 1000) % 60);
        var minutes = Math.floor((t / 1000 / 60) % 60);
        var hours = Math.floor((t / (1000 * 60 * 60)) % 24);
        var days = Math.floor(t / (1000 * 60 * 60 * 24));
        return {
            'total': t,
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds
        };
    }

    function run_clock(id, endtime) {
        var clock = document.getElementById(id);

        function update_clock() {
            var t = time_remaining(endtime);

            hours = t.hours;
            if(hours<10){
                hours="0"+hours;
            }

            minutes = t.minutes;
            if(minutes<10){
                minutes="0"+minutes;
            }

            seconds = t.seconds;
            if(seconds<10){
                seconds="0"+seconds;
            }

            clock.innerHTML = "<h5>Time remaining: "+ hours + ":" + minutes + ':' + seconds + "</h5>";
            if (t.total <= 0) {
                clearInterval(timeinterval);
            }

            if (t.hours<=0 && t.minutes <= 0 && t.seconds <= 0) {
                sync_remaining_time();
                setTimeout(end_test(true),3000);
            }
        }
        update_clock(); // run function once at first to avoid delay
        var timeinterval = setInterval(update_clock, 1000);
    }

    // var time_in_minutes = time_in_minutes;
    var current_time = Date.parse(new Date());
    var deadline = new Date(current_time + time_in_minutes * 60 * 1000 + time_in_seconds * 1000);
    $("#global-clockdiv").remove();
    $("#global-row-div-clock-div").html(`<div id="global-clockdiv" class="center"></div>`);
    run_clock('global-clockdiv', deadline);
}

var is_face_analysis_required = true;

if (window.location.pathname.indexOf("/applicant/quiz-paper") != -1) {
    if (performance.navigation.type == 1) {
        window.location = "/applicant/dashboard";
    } else {
        is_quiz_started = false;
        urlparams = getUrlVars();
        if ("disabled" in urlparams && urlparams["disabled"] == "true") {
            is_face_analysis_required = false;
        }

        $(document).bind("keydown", disableF5);
        render_quiz_config();
        $(window).bind('beforeunload', function() {
            sync_remaining_time();
        });
    }
} else {
    $(document).unbind("keydown", disableF5);
}

function render_quiz_config() {

    quiz_uuid = window.location.pathname.split("/")[3];

    $.ajax({
        url: '/applicant/get-quiz-config/',
        type: 'GET',
        data: {
            quiz_uuid: quiz_uuid
        },
        success: function(response) {
            console.log(response)
           
            if (response["status_code"] == 200) {
                if (is_quiz_started == false || 1) {

                    if (response["remaining_time"] == -1) {
                        startGlobalQuizTimer(response["time"]);
                    } else {
                        var seconds = Math.floor(response["remaining_time"] / 1000);
                        var minutes = Math.floor(seconds/60);
                        seconds -= minutes * 60;
                        startGlobalQuizTimer(minutes, seconds);
                    }

                    //if (is_face_analysis_required == true) {
                        initializeCaptureVideo("global-video-captured-response", "global-canvas-video-capture", "btn-start-recording", "btn-stop-recording", "btn-preview-recording", false, false, false);
                        startGlobalVideoCapture();
                    //}

                    startSyncTimeTimer();
                    is_quiz_started = true;
                }

                quiz_sections = response["quiz_section"];
                quiz_id = response["quiz_uuid"];

                var quiz_config_html = "";
                for (var i = 0; i < quiz_sections.length; i++) {
                    quiz_config_html += '\
                            <div class="col s12 m4 l4">\
                              <div class="card">\
                                <div class="card-content black-text">\
                                <span class="card-title">' + quiz_sections[i]["topic_name"] + '</span>\
                                    <hr>\
                                    <p>No questions: ' + quiz_sections[i]["no_questions"] + '</p>\
                                    <p>Time: ' + quiz_sections[i]["time"] + ' mins</p>\
                                    <p>Type: ' + quiz_sections[i]["category"] + '</p>\
                                    <p>Weightage: ' + quiz_sections[i]["weightage"] + ' %</p>\
                                </div>\
                                <div class="card-action">';

                    if (quiz_sections[i]["is_completed"] == true) {
                        quiz_config_html += '<a href="javascript:void(0)" class="btn safe" onclick="start_quiz_section_paper(this, \'' + quiz_id + '\', \'' + quiz_sections[i]["id"] + '\')"\
                                        id="btn-start-quiz-section-' + quiz_sections[i]["id"] + '" disabled="disabled">\
                                            <i class="material-icons inline-icon">lock</i>\
                                        </a>';
                        
                        if(quiz_sections[i]['message']=='Completed'){
                            quiz_config_html += '<span class="green-text">Completed</span>';
                        }
                        else if(quiz_sections[i]['message']=='Pending'){
                            quiz_config_html += '<span class="red-text">Pending</span>';
                        }
                    } else {
                        quiz_config_html += '<a href="javascript:void(0)" class="btn safe" onclick="start_quiz_section_paper(this, \'' + quiz_id + '\', \'' + quiz_sections[i]["id"] + '\')"\
                                        id="btn-start-quiz-section-' + quiz_sections[i]["id"] + '">\
                                            <i class="material-icons inline-icon">lock_open</i> Start Now\
                                        </a>';
                    }

                    quiz_config_html += '</div>\
                                                  </div>\
                                                </div>';
                }

                document.getElementById("div-quiz-section-list").innerHTML = quiz_config_html;
            } else {
                window.location = "/";
            }
        },
        error: function(xhr, textstatus, errorthrown) {
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
        }
    });
}


function start_quiz_section_paper(element, quiz_uuid, quiz_section_id) {
    takeScreenShot();
    sync_remaining_time();
    clearInterval(sync_time_min_counter_timeout);
    $("#problem-render-preloader").show();
    $("#div-quiz-section-list").hide();
    $.ajax({
        url: '/applicant/get-quiz-section/',
        type: 'GET',
        data: {
            quiz_uuid: quiz_uuid,
            quiz_section_id: quiz_section_id
        },
        success: function(response) {
            console.log(response);
            if (response["status_code"] == 200) {
                last_attempted_quiz_section_id = quiz_section_id;
                if(response['is_sectional_timed']){
                    if (response["time_remaining"] == -1) {
                        startGlobalQuizTimer(response["time"]);
                    } else {
                        var seconds = Math.floor((response["time_remaining"]) / 1000);
                        var minutes = Math.floor(seconds/60);
                        seconds -= minutes * 60;
                        console.log(minutes, seconds);
                        startGlobalQuizTimer(minutes, seconds);
                    }
                }
                startSyncTimeTimer();
                totalProblems = response["total_problems"];
                problemCounter = response["no_questions_attempted"];
                fetch_problem(response);
            } else {
                window.location = "/";
            }
            $("#problem-render-preloader").hide();
            $("#div-quiz-section-list").show();
        },
        error: function(xhr, textstatus, errorthrown) {
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
        }
    });
}

function initializeCaptureAudio() {
    // Store a reference of the preview video element and a global reference to the recorder instance
    audio = document.getElementById('audio-captured-response');

    // When the user clicks on start video recording
    document.getElementById('btn-start-audio-recording').addEventListener("click", function() {
        // Disable start recording button
        this.disabled = true;

        // Request access to the media devices
        navigator.mediaDevices.getUserMedia({
            audio: true,
            video: false
        }).then(function(stream) {
            // Display a live preview on the video element of the page
            setSrcObject(stream, audio);

            // Start to display the preview on the video element
            // and mute the video to disable the echo issue !
            audio.play();
            audio.muted = true;

            // Initialize the recorder
            recorder = new RecordRTCPromisesHandler(stream, {
                mimeType: 'audio/webm',
                bitsPerSecond: 128000
            });

            audioStarted = true;

            // Start recording the video
            recorder.startRecording().then(function() {
                console.info('Recording audio ...');
            }).catch(function(error) {
                console.error('Cannot start audio recording: ', error);
            });

            // release stream on stopRecording
            recorder.stream = stream;
            startSpeechToText(this);

            // Enable stop recording button
            document.getElementById('btn-stop-audio-recording').disabled = false;
        }).catch(function(error) {
            console.error("Cannot access media devices: ", error);
        });
    }, false);

    // When the user clicks on Stop video recording
    document.getElementById('btn-stop-audio-recording').addEventListener("click", function() {
        this.disabled = true;

        recorder.stopRecording().then(function() {
            console.info('stopRecording success');

            // Retrieve recorded video as blob and display in the preview element
            audioBlob = recorder.blob;

            audioStopped = true;

            // video.src = URL.createObjectURL(videoBlob);
            // video.play();

            // Unmute video on preview
            // video.muted = false;

            // Stop the device streaming
            recorder.stream.stop();
            stopSpeechToText(this);

            // Enable record button again !
            document.getElementById('btn-start-audio-recording').disabled = false;
        }).catch(function(error) {
            console.error('stopRecording failure', error);
        });
    }, false);
}
function fetch_problem(response) {

    // json_string = JSON.stringify({
    //     "problem_id": problem_id
    // });
    //
    // $("#problem-render-preloader").show();

    // $.ajax({
    //     url: "/fetch-problem/",
    //     type: "POST",
    //     data: {
    //         data: json_string
    //     },
    //     success: function(response) {
    //
    //         $("#problem-render-preloader").hide();
    //
    //         if (response["status_code"] == 200) {

    problemCounter += 1;

    console.log(response)

    problem_html = `
    <div class="card-panel col s12">
        <div class="row">
            <div class="col s12">
                <input type="hidden" name="testProblem" value="problem-id-` + response["problem_id"] + `">
                    <h6><p id="p-question-counter">Quiz: ` + problemCounter + `/` + totalProblems + `</p></h6>
                        <hr>`;

    if (response["problem_pdf"] != null && response["problem_pdf"]!="" && response["problem_pdf"]!="None"){
        problem_html += `<embed src="`+response["problem_pdf"]+`#toolbar=0&navpanes=0&scrollbar=0" width="100%" height="500"><br>`;
        problem_html += "<hr>";
    }

    if (response["problem_video"]!=null && response["problem_video"].length!=0) {
        for(var index=0;index<response["problem_video"].length;index++)
        {
            if (response['is_embed'][index]) {
                problem_html += `<iframe src="` + response["problem_video"][index] + `" frameborder="0" allowfullscreen style="width:25em;height:15em;padding:1em;"></iframe>`;
            } else {
                problem_html += `<video width="90%" height="30%" controls><source src="` + response["problem_video"][index] + `" type="video/mp4" style="padding:1em;"></video>`;
            }            
        }
        problem_html += "<hr>";
    }

    if (response["problem_image"] != null) {
        problem_html += `<img src="` + response["problem_image"] + `" class="responsive-img"><br>`;
        problem_html += "<hr>";
    }

    if (response["problem_graph"] != null){
        for(var index=0;index<response["problem_graph"].length;index++){
	       problem_html += `<iframe src="`+response["problem_graph"][index]+`" width="100%" height="400" frameborder="0"></iframe><br>`;
        }
        problem_html += "<hr>";
    }

    //problem_html += `<div id="problem-description" style="display:none; padding-bottom:20px !important;" >` + response["problem_description"] + `</div>`;
    if(response["problem_category"] == "5"){
        problem_html += `<div id="problem-description" style="display:none;margin-bottom:15px !important;">` + response["problem_description"] + `</div>`;
    }else{
    problem_html += `<div id="problem-description" style="margin-bottom:15px !important;"  >` + response["problem_description"] + `</div>`;
    }


    if (response["text_to_speech"] == true) {
        problem_html += `
        <div class="col s12">
          <a class="right" href="javascript:void(0)" onclick="speakTheProblem()" id="speak-the-problem">
            <i class="material-icons">surround_sound</i>
          </a>
        </div>`;
    }

    if (response["problem_category"] == "1") {
        problem_html += `
                  <div id="div-single-choice-section">`;

        problem_choices = response["problem_choices"];

        for (var i = 0; i < problem_choices.length; i++) {
            problem_html += `<p>
                    <label>
                        <input class="with-gap" name="input-single-choice" type="radio" value="` + problem_choices[i]["value"] + `" />
                        <span class="black-text">` + problem_choices[i]["display"] + `</span>
                    </label>
                </p>`;
        }
        problem_html += `</div>`;
    } else if (response["problem_category"] == "2") {
        problem_html += `
                  <div id="div-multiple-choice-section">`;

        problem_choices = response["problem_choices"];

        for (var i = 0; i < problem_choices.length; i++) {
            problem_html += `<p>
                    <label>
                      <input type="checkbox" name="input-multiple-choice" value="` + problem_choices[i]["value"] + `"/>
                      <span class="black-text">` + problem_choices[i]["display"] + `</span>
                    </label>
                  </p>`;
        }
        problem_html += `</div>`;
    } else if (response["problem_category"] == "3") {
        problem_html += `
              <div id="div-descriptive-section">
                <textarea id="textarea-descriptive-input" style="width:100%; height:10em;"></textarea>
                <br>Total Words: <span id="display_word_count">0</span>. Words left: <span id="display_word_left">200</span>
              </div>`;
    } else if (response["problem_category"] == "4") {
        problem_html += `
                <div id="div-audio-section">
                    <button id="btn-start-audio-recording">Start</button>
                    <button id="btn-stop-audio-recording" disabled="disabled">Stop</button>
                    <div class="col s12">
                        <br>
                        <div class="row">
                            <div class="col s12 m6 l6">
                                <br><br>
                                <span id="speech_to_text_span" class="final"></span>
                                <span id="interim_span" class="final"></span>
                            </div>
                            <div class="col s12 m6 l6">
                                <br>
                                <audio id="audio-captured-response" controls autoplay></audio>
                            </div>
                        </div>
                    </div>
                </div>`;
    } else if (response["problem_category"] == "5") {
        problem_html += `
              <div id="div-video-section" class="row">
                <div class="col s12">
                <p class="red-text" id="hide-info-text">Question will be visible once you click Start button.</p>
                  <button id="btn-start-video-recording" onclick="showQuestion()">Start</button>
                  <button id="btn-stop-video-recording" disabled="disabled">Stop</button>
                  <button id="btn-preview-video-recording" disabled="disabled" style="display:none;" >Preview</button>
                  <canvas style="display:none;" id="canvas-video-capture"></canvas>
                  <span id="video-counter" class="right"></span>
                </div>
                <div class="col s12">
                  <div class="row">
                    <div class="col s12 m6 l6">
                      <br><br>
                      <span id="speech_to_text_span" class="final" style="display:none;" ></span>
                      <span id="interim_span" class="final" style="display:none;" ></span>
                    </div>
                    <div class="col s12 m6 l6">
                      <br>
                      <video class="responsive-video" id="video-captured-response" controls autoplay style="height:10em;" type="video/webm"></video>
                    </div>
                  </div>
                </div>
              </div>`;
    }

    problem_html += `
            </div>
              <div class="col s12">
                <br>
                 <button id="btn-next-question" class="btn left" onclick="fetch_next_question('` + response["problem_id"] + `', 'false')">Next Question</button>
                <!-- <a class="btn right8887513372 modal-trigger" href="#modal-end-test">End Section</a> -->
              </div>
            </div>
        </div>
    <div id="modal-empty-answer-confirm" class="modal">
    <div class="modal-content">
        	Look's like you haven't selected valid options or answer, Are you sure you want to continue?
        </div>
        <div class="modal-footer">
                <a href="javascript:void(0)" class="modal-close btn" onclick="fetch_next_question('` + response["problem_id"] + `', 'true')">Yes</a>
            <a href="javascript:void(0)" class="modal-close btn">No</a>
        </div>
    </div>`;

    $("#div-quiz-section-list").html(problem_html);
    $(".modal").modal();

    if (response["problem_category"] == "3") {
        preventCopyPasteWithID("textarea-descriptive-input");

        $(document).ready(function() {
            $("#textarea-descriptive-input").on('keyup', function() {
                var words = this.value.match(/\S+/g).length;
                if (words > 200) {
                    // Split the string on first 200 words and rejoin on spaces
                    var trimmed = $(this).val().split(/\s+/, 200).join(" ");
                    // Add a space at the end to keep new typing making new words
                    $(this).val(trimmed + " ");
                }
                else {
                    $('#display_word_count').text(words);
                    $('#display_word_left').text(200-words);
                }
            });
        }); 
    } else if (response["problem_category"] == "4") {
        initializeCaptureAudio();
    } else if (response["problem_category"] == "5") {
        stopGlobalVideoCapture();
        initializeCaptureVideo("video-captured-response", "canvas-video-capture", "btn-start-video-recording", "btn-stop-video-recording", "btn-preview-video-recording", true, true, true);
    }

    if ($("#speak-the-problem").length == 1) {
        $("#speak-the-problem").click();
    }

    //         } else {
    //             window.location = "/";
    //         }
    //     },
    //     error: function(xhr, textstatus, errorthrown) {
    //         console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
    //         $("#problem-render-preloader").hide();
    //     }
    // });
}


function confirm_next_question() {
    $("#modal-empty-answer-confirm").modal();
    $("#modal-empty-answer-confirm").modal("open");
}

function fetch_next_question(problem_id, is_confirmed) {
    // var problem_id = $('input[name="testProblem"]').val().split("-")[2];
    var unique_quiz_config_id = window.location.pathname.split("/")[3];
    var quiz_status_obj = document.getElementById('quiz_status_obj')
    var response = {
        "problem_id": problem_id,
        "unique_quiz_config_id": unique_quiz_config_id,
        "quiz_section_id": last_attempted_quiz_section_id,
        "mode": "",
        "quiz_status_obj" : quiz_status_obj.value
    }

    if ($("#div-single-choice-section").length == 1) {
        response["mode"] = "1";
        response["choice"] = "";
        single_choice_input = document.getElementsByName("input-single-choice");
        for (var i = 0; i < single_choice_input.length; i++) {
            if (single_choice_input[i].checked) {
                response["choice"] = single_choice_input[i].value;
                break;
            }
        }

        if (is_confirmed == "false" && response["choice"] == "") {
            confirm_next_question();
            return;
        }
    } else if ($("#div-multiple-choice-section").length == 1) {
        response["mode"] = "2";
        response["choice_list"] = [];
        multiple_choice_input = document.getElementsByName("input-multiple-choice");
        for (var i = 0; i < multiple_choice_input.length; i++) {
            if (multiple_choice_input[i].checked) {
                response["choice_list"].push(multiple_choice_input[i].value);
            }
        }

        if (is_confirmed == "false" && response["choice_list"].length == 0) {
            confirm_next_question();
            return;
        }
    } else if ($("#div-descriptive-section").length == 1) {
        response["mode"] = "3"
        response["text"] = $("#textarea-descriptive-input").val();
        if (is_confirmed == "false" && response["text"] == "") {
            confirm_next_question();
            return;
        }
    } else if ($("#div-audio-section").length == 1) {
        response["mode"] = "4"
    } else if ($("#div-video-section").length == 1) {
        $("#btn-stop-video-recording").click();
        //saveVideoAtServer(recorded_video_data_url, problem_id);
	if(flag_video_recording_started){
            saveVideoAtServer(recorded_video_data_url, problem_id);
        }
        else{
            saveVideoAtServer("null", problem_id);
        }
	flag_video_recording_started = false;
        response["mode"] = "5";
        response["text"] = document.getElementById("speech_to_text_span").innerText;
        response["video_url"] = last_uploaded_video_url;

        //if (is_face_analysis_required == true) {
            initializeCaptureVideo("global-video-captured-response", "global-canvas-video-capture", "btn-start-recording", "btn-stop-recording", "btn-preview-recording",false, false, false);
            startGlobalVideoCapture();
        //}
    }
    get_next_question_for_applicant(response);
}

function get_next_question_for_applicant(response) {

    json_string = JSON.stringify(response);
    $("#problem-render-preloader").show();
    $("#div-quiz-section-list").hide();
    $.ajax({
        url: "/applicant/fetch-next-problem/",
        type: "POST",
        headers:{
            "X-CSRFToken":getCsrfToken()
        },
        data: {
            data: json_string
        },
        success: function(response) {
            if (response["status_code"] == 200) {
                if (response["problem_id"] == -1) {
                    end_test();
                } else {
                    fetch_problem(response);
                    $("#current_topic").html(response["topic_name"]);
                }
            } else {
                window.location = "/";
            }
            $("#problem-render-preloader").hide();
            $("#div-quiz-section-list").show();
            last_uploaded_video_url = null
        },
        error: function(xhr, textstatus, errorthrown) {
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
            $("#problem-render-preloader").hide();
            window.location = "/";
        }
    });
}


function end_test(time_up = false) {
    takeScreenShot();
    var CSRF_TOKEN = getCsrfToken();
    var unique_quiz_config_id = window.location.pathname.split("/")[3];
    $("#problem-render-preloader").show();
    takeScreenShot();
    $.ajax({
        url: "/applicant/test-complete/",
        type: "POST",
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        },
        data: {
            "unique_quiz_config_id": unique_quiz_config_id,
            "quiz_section_id": last_attempted_quiz_section_id,
            "time_up": time_up,
        },
        success: function(response) {
            if (response["status_code"] == 200 && response["is_quiz_ended"] == true) {

                stopGlobalVideoCapture();

                $("#modal-timeout-test").modal({
                    onCloseEnd: function() {
                        clearTimeout(completed_quiz_timeout);
                        window.location = "/applicant/dashboard";
                    }
                });

                $("#modal-timeout-test").modal('open');

                completed_quiz_timeout = setTimeout(function(e) {
                    $("#modal-timeout-test").modal('close');
                }, 10000);

            } else if (response["status_code"] == 200 && response["is_quiz_ended"] == false) {
                clearInterval(sync_time_min_counter_timeout);
                $("#modal-completed-quiz-section").modal({
                    onCloseEnd: function() {
                        clearTimeout(completed_quiz_section_timeout);
                        render_quiz_config();
                        last_attempted_quiz_section_id = null;
                        startSyncTimeTimer();
                    }
                });
                $("#modal-completed-quiz-section").modal('open');
                completed_quiz_section_timeout = setTimeout(function(e) {
                    $("#modal-completed-quiz-section").modal('close');
                }, 10000);
            }
            $("#problem-render-preloader").hide();
        },
        error: function(xhr, textstatus, errorthrown) {
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
            $("#problem-render-preloader").hide();
        }
    });
}

var final_transcript = '';
var recognizing = false;
var ignore_onend;
var start_timestamp;

if (!('webkitSpeechRecognition' in window)) {
    console.log("----------- EasySTEP ------------");
    console.log("warning: Speech to Text is not supported in this. Please update it");
} else {
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onstart = function() {
        recognizing = true;
    };

    recognition.onerror = function(event) {
        if (event.error == 'no-speech') {
            ignore_onend = true;
        }

        if (event.error == 'audio-capture') {
            ignore_onend = true;
        }

        if (event.error == 'not-allowed') {
            if (event.timeStamp - start_timestamp < 100) {
                alert("Blocked access to microphone");
            } else {
                alert("Denied access to microphone");
            }
            ignore_onend = true;
        }
    };

    recognition.onend = function() {
        if (ignore_onend) {
            return;
        }

        if (!final_transcript) {
            return;
        }

        if (window.getSelection) {
            window.getSelection().removeAllRanges();
            var range = document.createRange();
            range.selectNode(document.getElementById('speech_to_text_span'));
            window.getSelection().addRange(range);
        }
    };

    recognition.onresult = function(event) {
        var interim_transcript = '';
        for (var i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                final_transcript += event.results[i][0].transcript;
            } else {
                interim_transcript += event.results[i][0].transcript;
            }
        }
        final_transcript = capitalize(final_transcript);
        speech_to_text_span.innerHTML = linebreak(final_transcript);
        interim_span.innerHTML = linebreak(interim_transcript);


        checkbox_audio_check_element = document.getElementById("checkbox-audio-checked");
        if (checkbox_audio_check_element != null && checkbox_audio_check_element != undefined && document.getElementById('speech_to_text_span').innerHTML != "") {
            is_audio_checked = true;
            checkbox_audio_check_element.checked = true;
            stopSpeechToText();
        }
    };
}

var two_line = /\n\n/g;
var one_line = /\n/g;

function linebreak(s) {
    return s.replace(two_line, '<p></p>').replace(one_line, '<br>');
}

var first_char = /\S/;

function capitalize(s) {
    return s.replace(first_char, function(m) {
        return m.toUpperCase();
    });
}

function startSpeechToText(event) {
    if (recognizing) {
        stopSpeechToText(event);
    }
    final_transcript = '';
    recognition.lang = "en-US";
    recognition.start();
    ignore_onend = false;
    speech_to_text_span.innerHTML = '';
    interim_span.innerHTML = '';
    start_timestamp = event.timeStamp;
}

function stopSpeechToText(event) {
    if (recognizing != null) {
        recognition.stop();
        recognizing = false;
        return;
    }
}

// ADDED SOCKET CONFIG HERE 

//  END HERE 


function sync_remaining_time() {

    var unique_quiz_config_id = window.location.pathname.split("/")[3];
    var request_user = document.getElementById('request_user')
    var s = socket
    
    json_string = JSON.stringify({
        quiz_section_id: last_attempted_quiz_section_id,
        quiz_config_id: unique_quiz_config_id,
        remaining_time: global_time_remaining
    });
   

    s.send(JSON.stringify({'data' :{
        quiz_section_id: last_attempted_quiz_section_id,
        quiz_config_id: unique_quiz_config_id,
        remaining_time: global_time_remaining
    }}))

   

   

    // $.ajax({
    //     url: "/applicant/sync-remaining-quiz-time/",
    //     type: "POST",
    //     headers: {
    //         "X-CSRFToken": getCsrfToken()
    //     },
    //     async: false,
    //     data: {
    //         data: json_string
    //     },
    //     success: function(response) {},
    //     error: function(xhr, textstatus, errorthrown) {
    //         console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
    //     }
    // });
}


//  Constant checking of Access to Webcam and Micropone permission for 5 seconds

  navigator.getMedia = (navigator.getUserMedia || // use the proper vendor prefix
	navigator.webkitGetUserMedia ||
	navigator.mozGetUserMedia ||
	navigator.msGetUserMedia);

  const interval = setInterval(function () {
    console.log("in set interval");
  navigator.getMedia({
		video: true,
                audio: true
	}, function () {
		console.log("Webcam is on...");
	}, function () {
		alert("Please allow webcam and microphone access, post that kindly restart the quiz.");
		window.location = "/applicant/dashboard/";
	});
}, 5000);



// for capturing login logout time on August 18th 2020

$(window).bind('beforeunload', function(){
    return save_logout_time(window.location.pathname.split('/')[3]);
});

function save_logout_time(quiz_uuid){
    CSRF_TOKEN = getCsrfToken();
    $.ajax({
        url: "/applicant/save-logout-time/",
        type: "POST",
        headers: {
            "X-CSRFToken": CSRF_TOKEN
        },
        data: {
            'quiz_uuid': quiz_uuid,
        },
        success: function(response) {
        },
        error: function(xhr, textstatus, errorthrown) {
            console.log("Please report this error: " + errorthrown + xhr.status + xhr.responseText);
        }
    });
}


function showQuestion(){
    var element = document.querySelector('#problem-description')
    var hide_info_text = document.querySelector('#hide-info-text')
    element.style.display = 'block'
    hide_info_text.style.display ='none'
}


//function changeQuestion(){
//    console.log("")
//    var element = document.getElementById('btn-next-question').click()
//    console.log(element)
//    console.log("element clicked")
//}
