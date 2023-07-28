console.log("Start");

var canvas = document.getElementById('myChart');

const data = {
  datasets: [{
    label: '',
    backgroundColor: 'rgb(255, 99, 132)',
    borderColor: 'rgb(255, 99, 132)',
    data: [{
        }],
        showLine: true,
  }]
};

//const config = {
//  type: 'line',
//  data: data,
//  options: {}
//};

var myChart = new Chart(canvas, {
  type: 'scatter',
  data: data,
  options: {
  responsive:true,
  maintainAspectRatio: false,
  animation: {
        duration: 0
    },
  scales: {
        y: {
            min: -1,
            max: 1,
            stepSize: 1,

        },
        x: {
            min: 0,
            max: 12,
            stepSize: 1,
            ticks: {
                callback: function(val, index) {

                    return Math.round(val,1);
                },

            },
        },
    }
    }
  }
);

once = true;

// function to update the chart
function addData(chart, data) {

  chart.data.datasets.forEach((dataset) => {
    if (once){
        dataset.data.shift();
        once = false;
    }

    dataset.data = dataset.data.filter(function( element ) {
        return element !== undefined;
    });

   if((dataset.data.length > 2) && ((dataset.data[dataset.data.length-1].x) > 12.0)){
        dataset.data.shift();
       chart.options.scales.x.min = dataset.data[0].x;
       chart.options.scales.x.max = dataset.data[dataset.data.length-1].x;
   }
   else if((dataset.data.length > 2) && ((dataset.data[dataset.data.length-1].x) < 12.0)){
       chart.options.scales.x.min = 0.;
       chart.options.scales.x.max = 12.;
   }
    dataset.data.push(data);

  });
  chart.update();
}

function fetch_ports(){
    $.get('api/ports', function(data){
        var optionsHtml = data.map(function(item) {
            return '<option value="' + item + '">' + item + '</option>';
        }).join('');

        $('#ports').html(optionsHtml);
    })
};

function fetch_data() {
    var result;

    $.ajax({
        url: 'api/read',
        type: 'get',
        async: false,  // make it synchronous
        success: function(data) {
            result = data;
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.log(textStatus, errorThrown);
        }
    });
    return result;
}

//window.onload = fetch_ports();

var interval_chart;

function discon(){
console.log($('#Connect').text() == 'Connect');
if ($('#Connect').text() == 'Connect'){
    $('#Connect').text('Disconnect');
    var port = $('#ports').val();
    $('#ports').prop('disabled', true);
    $.get('api/connect', {port: port}, function(data){
        console.log(data);
    });

    myChart.config.data.datasets.forEach((dataset) => {
        dataset.data = [];
        });

    myChart.update();

    interval_chart = setInterval(function() {
      const newData = fetch_data();
      addData(myChart, newData);
    }, 100);

    }
else{
    clearInterval(interval_chart);
    $('#ports').prop('disabled', false);
    $('#Connect').text('Connect');
    $.get('api/disconnect');
}
}

function scan(){
    fetch_ports();
}

