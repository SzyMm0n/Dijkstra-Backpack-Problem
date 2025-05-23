function showAlert(message,type,id) {
    let alerts = document.getElementById(id);
    if (alerts) {
        alerts.innerHTML = `<div class="${type}">${message}</div>`;
        setTimeout(() => {
            alerts.innerHTML = "";
        }, 6000);
    }
}

function volumes_validation() {
    let volumes_array = document.getElementById("volumes").value.split(",").map(Number);
    for (let i = 0; i < volumes_array.length; i++) {
        if (isNaN(volumes_array[i]) || volumes_array[i] <= 0) {
            return showAlert("Please enter valid weights. Use numbers greater than 0 separated by ','.","error","volumes_alerts");
        }
    }
}

function values_validation() {
    let values_array = document.getElementById("values").value.split(",").map(Number);
    for (let i = 0; i < values_array.length; i++) {
        if (isNaN(values_array[i]) || values_array[i] <= 0) {
            return showAlert("Please enter valid values. Use numbers greater than 0 separated by ','.","error","values_alerts");
        }
    }
}

function capacity_validation() {
    let capacity = document.getElementById("capacity").value;
    if (isNaN(capacity) || capacity <= 0) {
        return showAlert("Please enter a valid capacity. Use numbers greater than 0.","error","capacity_alerts");
    }
}
// function responsible for the passing of the values to the backend
// and invoking the function to draw the graph if the response is successful
async function solution(){
    event.preventDefault();

    const values = document.getElementById("values").value;
    const volumes = document.getElementById("volumes").value;
    const capacity = document.getElementById("capacity").value;

    const response = await fetch("solve", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({values: values, volumes: volumes, capacity: capacity}),
    })

    if (response.ok) {
        const data = await response.json();
        await drawGraph(data.data);
        await results(data.data, values, volumes);
        showAlert("Graph generated successfully!","success","general_alerts");
    } else {
        const error = await response.json();
        showAlert(error.message,"error","general_alerts");
    }
}
// function to draw the graph using vis.js
async function drawGraph(data) {
    showAlert("Graph generated successfully!","success","general_alerts");

    const containerDiv = await document.getElementById("mynetwork-container");
    containerDiv.style.display = "block";

    const container = await document.getElementById("mynetwork");
    container.innerHTML = "";

    const nodes = new vis.DataSet(data.nodes);
    const edges = new vis.DataSet(data.edges);

    const options = {
        layout: {hierarchical: {direction: "LR", sortMethod: "directed"}},
        physics: false
    };
    new vis.Network(container, {nodes, edges}, options);
}

async function generate_data(){
    const response = await fetch("generate");
    const data = await response.json();

    document.getElementById("values").value = data.values.join(",");
    document.getElementById("volumes").value = data.volumes.join(",");
    document.getElementById("capacity").value = data.capacity;

    showAlert("Data generated successfully!","success","general_alerts");
}

async function results(data, values, volumes) {
    const resultDiv = await document.getElementById("result");

    // Konwersja stringów na tablice liczb
    const valuesArray = values.split(',').map(Number);
    const volumesArray = volumes.split(',').map(Number);

    await fetch("results", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            data: data,
            values: valuesArray,
            volumes: volumesArray
        }),
    })
        .then(response => response.json())
        .then(data => {
            resultDiv.innerHTML = `<h2>Results:</h2>
            <p>Items: ${data.items }</p>
            <p>Value accumulated: ${data.value}</p>
            <p>Volumes accumulated: ${data.volume}</p>`
        })
}
async function show_item(id){
    const resultDiv = document.getElementById(id);
    if (resultDiv.style.display === "none") {
        resultDiv.style.display = "block";
    }
    else {
        resultDiv.style.display = "none";
    }
}
