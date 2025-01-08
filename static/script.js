console.log("App Is Running");

document.getElementById("btn").addEventListener("click", async () => {
    console.log("Entering..");
    const fileInput = document.getElementById('fileInput');
    if (!fileInput.files.length) {
        alert('Please select a file to upload.');
        return false;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('http://127.0.0.1:8000/predict/', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        console.log(result);

        // Show the prediction result on the back side
        const container = document.querySelector('.container');
        const uploadedImage = document.getElementById('uploadedImage');
        const prediction = document.getElementById('prediction');
        const score = document.getElementById('score');

        // Set the prediction text and image preview
        prediction.textContent = `${result.prediction}`;
        score.textContent = `${parseFloat(result.score).toFixed(2)}%`;
        const file = fileInput.files[0];
        const reader = new FileReader();
        reader.onload = () => {
            uploadedImage.src = reader.result;
        };
        reader.readAsDataURL(file);

        // Flip the container to show the back
        container.classList.add('flipped');
    } catch (error) {
        alert(`An error occurred: ${error.message}`);
        console.log(error);
    }
});
