

function showAlert(message,type,id) {
    let alerts = document.getElementById(id);
    if (alerts) {
        alerts.innerHTML = `<div class="${type}">${message}</div>`;
        setTimeout(() => {
            alerts.innerHTML = "";
        }, 6000);
    }
}

function weights_validation() {
    let weights_array = document.getElementById("weights").value.split(",").map(Number);
    for (let i = 0; i < weights_array.length; i++) {
        if (isNaN(weights_array[i]) || weights_array[i] <= 0) {
            return showAlert("Please enter valid weights. Use numbers greater than 0 separated by ','.","error","weights_alerts");
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