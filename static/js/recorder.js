const recordButton = document.getElementById('recordButton');
const recordingsList = document.getElementById('recordings');
const audioContext = new AudioContext();

let mediaRecorder;
let chunks = [];

navigator.mediaDevices.getUserMedia({ audio: true })
    .then(function(stream) {
        audioContext.createMediaStreamSource(stream);
        mediaRecorder = new MediaRecorder(stream);

        recordButton.addEventListener('click', function() {
            if (mediaRecorder.state == 'inactive') {
                mediaRecorder.start();
                recordButton.innerHTML = 'Stop Recording';
            } else {
                mediaRecorder.stop();
                recordButton.innerHTML = 'Record';
            }
        });

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
            .then(chatTranscript => {
                // Update the page with the chat transcript
                const transcriptElement = document.createElement('p');
                transcriptElement.textContent = chatTranscript;
                document.body.appendChild(transcriptElement);
            })
            .catch(error => {
                console.error('Error sending audio to server:', error);
            });
        };
    })
    .catch(function(err) {
        console.log('The following error occurred: ' + err);
    });


      