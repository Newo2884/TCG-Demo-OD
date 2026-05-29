// the link to your model provided by Teachable Machine export panel
const URL = "/static/model/";

let model, webcam, labelContainer, maxPredictions, className;

// Load the image model and setup the webcam
async function init() {
    const modelURL = URL + "model.json";
    const metadataURL = URL + "metadata.json";

    // load the model and metadata
    // Refer to tmImage.loadFromFiles() in the API to support files from a file picker
    // or files from your local hard drive
    // Note: the pose library adds "tmImage" object to your window (window.tmImage)
    model = await tmImage.load(modelURL, metadataURL);
    maxPredictions = model.getTotalClasses();

    const constraints = {
        facingMode: "environment"
    };


    // Convenience function to setup a webcam
    const flip = false; // whether to flip the webcam
    webcam = new tmImage.Webcam(200, 200, flip); // width, height, flip
    await webcam.setup(constraints); // request access to the webcam
    await webcam.play();
    window.requestAnimationFrame(loop);

    // append elements to the DOM
    document.getElementById("webcam-container").appendChild(webcam.canvas);
    labelContainer = document.getElementById("label-container");
    className = document.getElementById("class-name");

    for (let i = 0; i < maxPredictions; i++) { // and class labels
        labelContainer.appendChild(document.createElement("div"));
    }

}

async function loop() {
    webcam.update(); // update the webcam frame
    await predict();
    window.requestAnimationFrame(loop);
}

// run the webcam image through the image model
async function predict() {
    let best_match = "None";

    // predict can take in an image, video or canvas html element
    const prediction = await model.predict(webcam.canvas);
    for (let i = 0; i < maxPredictions; i++) {
        const classPrediction =
            prediction[i].className + ": " + prediction[i].probability.toFixed(2);
        labelContainer.childNodes[i].innerHTML = classPrediction;
        if (prediction[i].probability.toFixed(2) > 0.95) {
            best_match = prediction[i].className;
        }
    }
    className.innerHTML = best_match;
    if (best_match != "None") {
        fetchCardDetails(best_match)
    }
}

function displayCard(card) {
    document.getElementById("card-name").innerText = card.name;
    document.getElementById("card-level").innerText = card.level;
    document.getElementById("card-race").innerText = card.race;
    document.getElementById("card-type").innerText = card.type;
    document.getElementById("card-desc").innerText = card.desc;
    document.getElementById("card-attack").innerText = card.attack;
    document.getElementById("card-defence").innerText = card.defence;
}

async function fetchCardDetails(detectedName) {
    try {
        const response = await fetch('/get_card_details', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ className: detectedName })
        });

        const result = await response.json();

        if (result.success) {
            displayCard(result.card);
        }
    } catch (error) {
        console.error("Error fetching card details:", error);
    }
}