function odswiezDane() {
    let buttonText = document.getElementById('napis');
    let buttonImage = document.getElementById('obrazek');

    $.ajax({
        url: '/sensor_data_json',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            $('#czas').text(data.hour);
            $('#dzien').text(data.dataa);
            $('#slon').text(data.sensor + ' %');
            $('#gleba').text(data.soil_hum + ' %');
            $('#temperatura').text(data.temperature + ' °C');
            $('#wilg_pow').text(data.humidity + ' %');
            $('#water_time').text(data.last_water);
            
            if (data.light_state == 1) {
                $('#napis').text('WYŁĄCZ');
                buttonImage.src = '../static/idea2.png';
            } else {
                buttonText.textContent = 'WŁĄCZ';
                buttonImage.src = '../static/idea1.png';
            }
        },
        complete: function () {
            // Odśwież dane co 1 sekund
            setTimeout(odswiezDane, 1000);
        }
    });
    
}

let light_state = 'off';

function light_change() {

    let button = document.getElementById('button-light');
    let buttonText = document.getElementById('napis');
    let buttonImage = document.getElementById('obrazek');

    if (light_state === 'off') {
        light_state = 'on';
        buttonText.textContent = 'WYŁĄCZ';
        buttonImage.src = '../static/idea2.png';
    } else {
        light_state = 'off';
        buttonText.textContent = 'WŁĄCZ';
        buttonImage.src = '../static/idea1.png';
    }

    $.ajax({
        url: '/light_change',
        type: 'POST',
        data: { state: light_state },
        success: function (data) {
            console.log('Zmieniono stan diody.');
        },
        error: function (xhr, status, error) {
            console.error('Wystąpił błąd podczas zmiany stanu diody:', error);
        }
    });
}

function podlej() {
    $.ajax({
        url: '/podlej',
        type: 'POST',
        success: function (data) {
            console.log('Podlano.');
            $('#water_time').text(data.last_water);
        },
        error: function (xhr, status, error) {
            console.error('Wystąpił błąd podczas podlewania:', error);
        }
    });
}

$(document).ready(function () {
    odswiezDane();
});