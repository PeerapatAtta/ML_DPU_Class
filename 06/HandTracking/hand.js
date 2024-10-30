//Hand.js
const videoElement = document.getElementById('video');
const canvasElement = document.getElementById('canvas');
const canvasCtx = canvasElement.getContext('2d');
const scoreElement = document.getElementById('score');
const drawingUtils = window;
const holistic = new Holistic({
    locateFile: (file) => {
        return `https://cdn.jsdelivr.net/npm/@mediapipe/holistic@0.5.1635989137/${file}`;
    }
});

holistic.setOptions({
    modelComplexity: 1,
    smoothLandmarks: true,
    minDetectionConfidence: 0.5,
    minTrackingConfidence: 0.5
});

//Page 7-9

holistic.onResults(onResults);

const camera = new Camera(videoElement, {
    onFrame: async () => {
        await holistic.send({ image: videoElement });
    },
    width: 640,
    height: 480
});
camera.start();

function onResults(results) {
    canvasCtx.save();
    canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
    // Flip the video horizontally
    canvasCtx.translate(canvasElement.width, 0);
    canvasCtx.scale(-1, 1);
    canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);
    const hands = [
        { landmarks: results.leftHandLandmarks, label: 'Left' },
        { landmarks: results.rightHandLandmarks, label: 'Right' }
    ];
    let textResultContent = '';

    // FOR LOOP RENDER
    for (const hand of hands) {
        if (hand.landmarks) {
            // Draw hand landmarks
            drawingUtils.drawConnectors(canvasCtx, hand.landmarks, HAND_CONNECTIONS, { color: '#00FF00', lineWidth: 2 });
            for (const landmark of hand.landmarks) {
                drawingUtils.drawLandmarks(canvasCtx, [landmark], { color: '#00FF00', lineWidth: 2 });
            }
            // Add hand label to textResult
            // textResultContent += `${hand.label} Hand Detected\n`;
            const gesture = detectGesture(hand.landmarks);
            // Add hand label to textResult
            textResultContent += `${hand.label} Hand: ${gesture}\n`;
        }
    }

    document.getElementById('textResult').textContent = textResultContent;
    canvasCtx.restore();
}

//Page 10
function detectGesture(landmarks) {
    console.log(landmarks);
    // Check if all fingers are extended (Paper)
    const allFingersExtended = landmarks.slice(8, 21).every(landmark => landmark.y < landmarks[5].y);
    if (allFingersExtended) return 'Paper';
    // Check if only index and middle fingers are extended (Scissors)
    const onlyIndexAndMiddleExtended =
        landmarks[8].y < landmarks[6].y &&  // Index finger extended
        landmarks[12].y < landmarks[10].y && // Middle finger extended
        landmarks[16].y > landmarks[14].y && // Ring finger not extended
        landmarks[20].y > landmarks[18].y;    // Pinky finger not extended
    if (onlyIndexAndMiddleExtended) return 'Scissors';
    // Otherwise, assume it's Rock
    return 'Rock';
}







