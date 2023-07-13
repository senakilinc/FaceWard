let camera_button = document.querySelector("#start-camera");
let video = document.querySelector("#video");
let start_button = document.querySelector("#start-record");
let stop_button = document.querySelector("#stop-record");
let submit_button = document.querySelector("#submit-video");
let download_link = document.querySelector("#download-video");

let camera_stream = null;
let media_recorder = null;
let blobs_recorded = [];

// Disable the stop and submit buttons initially
stop_button.disabled = true;
submit_button.disabled = true;

camera_button.addEventListener('click', async function() {
    camera_stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
    video.srcObject = camera_stream;
});

start_button.addEventListener('click', function() {
    // Set MIME type of recording as video/webm
    media_recorder = new MediaRecorder(camera_stream, { mimeType: 'video/webm' });
    video.style.border = "3px solid red";
    // Event: new recorded video blob available
    media_recorder.addEventListener('dataavailable', function(e) {
        blobs_recorded.push(e.data);
    });

    // Event: recording stopped & all blobs sent
    media_recorder.addEventListener('stop', function() {
        // Create local object URL from the recorded video blobs
        let video_local = URL.createObjectURL(new Blob(blobs_recorded, { type: 'video/webm' }));
        download_link.href = video_local;

        // Re-enable the start, camera, and submit buttons, and disable the stop button
        start_button.disabled = false;
        camera_button.disabled = false;
        submit_button.disabled = false;
        stop_button.disabled = true;
    });

    // Disable the start, camera, and submit buttons, and enable the stop button
    start_button.disabled = true;
    camera_button.disabled = true;
    submit_button.disabled = true;
    stop_button.disabled = false;

    // Start recording with each recorded blob having 1 second video
    media_recorder.start(1000);
});

stop_button.addEventListener('click', function() {
    media_recorder.stop();
    $('#confirmation-modal').modal('show');
    
});

submit_button.addEventListener('click', function() {
    // Send the recorded video blob to the server
    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log(xhr.responseText);
        }
    }
    xhr.open('POST', '/save_video', true);
    xhr.setRequestHeader('Content-Type', 'application/octet-stream');
    xhr.send(new Blob(blobs_recorded, { type: 'video/webm' }));

    // Disable the submit button
    submit_button.disabled = true;
});
