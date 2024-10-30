const videoElement = document.getElementById('video');
const canvasElement = document.getElementById('canvas');
const canvasCtx = canvasElement.getContext('2d');

const faceMesh = new FaceMesh({
    locateFile: (file) => {
        return `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${file}`;
    }
});

const drawingUtils = window;

// ค่าคงที่สำหรับ landmark ของริมฝีปาก
const FACEMESH_LIPS = [
    0, 13, 14, 17, 37, 39, 40, 61, 78, 80, 81, 82, 84, 87, 88, 91, 95, 146, 178, 181, 185, 191, 267, 269, 270, 291, 308, 310, 311, 312, 314, 317, 318, 321, 324, 375, 402, 405, 409, 415
];

// ค่าคงที่สำหรับ landmark ของดวงตาขวา
const FACEMESH_RIGHT_EYE = [
    33, 7, 133, 144, 145, 153, 154, 155, 157, 158, 159, 160, 161, 163, 173, 246
];

// ค่าคงที่สำหรับ landmark ของดวงตาซ้าย
const FACEMESH_LEFT_EYE = [
    263, 249, 362, 373, 374, 380, 381, 382, 384, 385, 386, 387, 388, 390, 398, 466
];

// ค่าคงที่สำหรับ landmark ของจมูก
const FACEMESH_NOSE = [1, 2, 3];

faceMesh.setOptions({
    maxNumFaces: 3, // ตรวจจับใบหน้าสูงสุด 1 ใบหน้า
    refineLandmarks: true, // เปิดใช้งานการตรวจจับ landmark ที่ละเอียดขึ้น
    minDetectionConfidence: 0.5,
    minTrackingConfidence: 0.5
});

faceMesh.onResults(onResults);
const camera = new Camera(videoElement, {
    onFrame: async () => {
        await faceMesh.send({ image: videoElement });
    },
    width: 640,
    height: 480
});
camera.start();

function onResults(results) {
    canvasCtx.save();
    canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
    canvasCtx.drawImage(
        results.image, 0, 0, canvasElement.width, canvasElement.height);

    if (results.multiFaceLandmarks) {
        for (const landmarks of results.multiFaceLandmarks) {
            drawLandmarkWithLabel(canvasCtx, landmarks, FACEMESH_RIGHT_EYE, 'Right Eye', '#FFF');
            drawLandmarkWithLabel(canvasCtx, landmarks, FACEMESH_LEFT_EYE, 'Left Eye', '#FFF');
            drawLandmarkWithLabel(canvasCtx, landmarks, FACEMESH_NOSE, 'Nose', '#FFF');
            drawLandmarkWithLabel(canvasCtx, landmarks, FACEMESH_LIPS, 'Mouth', '#FFF');
        }
    }
    canvasCtx.restore();
}

// ฟังก์ชันสำหรับวาด landmark และ label
function drawLandmarkWithLabel(ctx, landmarks, landmarkIndices, labelText, color) {
    if (landmarks && landmarkIndices.length > 0 && landmarks[landmarkIndices[0]]) {
        const landmark = landmarks[landmarkIndices[0]];
        const x = landmark.x * canvasElement.width;
        const y = landmark.y * canvasElement.height;
        // วาดเส้น
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(x + 15, y - 30);
        ctx.strokeStyle = color;
        ctx.lineWidth = 2;
        ctx.stroke();
        // วาดข้อความ
        ctx.font = '28px Arial';
        ctx.fillStyle = color;
        ctx.fillText(labelText, x, y - 35);
    }
}

