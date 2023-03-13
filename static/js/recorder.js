const recordButton = document.getElementById('recordButton');
const recordingsList = document.getElementById('recordings');
const audioContext = new AudioContext();

let mediaRecorder;
let chunks = [];
const form = document.getElementById('chat-form');

const applyEventListeners = (button) => {
    button.addEventListener('click', function() {
        if (mediaRecorder.state == 'inactive') {
            mediaRecorder.start();
            button.innerHTML = 'Stop Recording';
        } else {
            mediaRecorder.stop();
            button.innerHTML = 'Record';
        }
    });
};

navigator.mediaDevices.getUserMedia({ audio: true })
    .then(function(stream) {
        audioContext.createMediaStreamSource(stream);
        mediaRecorder = new MediaRecorder(stream);

        applyEventListeners(recordButton);

        mediaRecorder.ondataavailable = function(e) {
            chunks.push(e.data);
        };

        mediaRecorder.onstop = function() {
            const blob = new Blob(chunks, { type: 'audio/ogg; codecs=opus' });
            chunks = [];
            
            // Send the audio data to the server
            const formData = new FormData();
            formData.append('audio', blob);
            fetch('/', {
                method: 'POST',
                body: formData
            })
            .then(response => response.text())
            .then(responseData => {
                // Update the page with the chat transcript
                document.body.innerHTML = responseData;

                // Re-initialize the eventListener
                const newRecordButton = document.getElementById('recordButton');
                applyEventListeners(newRecordButton);
            })
            .catch(error => {
                console.error('Error sending audio to server:', error);
            });
        };
    })
    .catch(function(err) {
        console.log('The following error occurred: ' + err);
    });


      