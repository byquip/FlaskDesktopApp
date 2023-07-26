console.log("Start");

//var canvas = document.getElementById('myChart');
//const canvas = component.find("myChart");
var canvas = document.getElementById('myChart');
//console.log(canvas);
//var canvas1 = document.getElementById('myChart').getContext('2d');
//console.log(canvas1);
//var canvas2 = $('#myChart');
//console.log(canvas2);
//var canvas3 = 'myChart';
//console.log(canvas3);
////const canvas = document.querySelector("myChart")
//const canvas4 = document.querySelector("myChart")
//console.log(canvas4);
//canvas.height = 75;

const labels = [
  'dju32',
  'ad6b2',
  '0f23f',
  'asd4c',
];

const data = {
  labels: labels,
  datasets: [{
    label: 'Test',
    backgroundColor: 'rgb(255, 99, 132)',
    borderColor: 'rgb(255, 99, 132)',
    data: [0, 10, 5, 4],
  }]
};

//const config = {
//  type: 'line',
//  data: data,
//  options: {}
//};

var myChart = new Chart(canvas, {
  type: 'line',
  data: data,
  options: {}
}
);

// function to update the chart
function addData(chart, label, data) {
  chart.data.labels.push(label);
  chart.data.datasets.forEach((dataset) => {
    dataset.data.push(data);
  });
  chart.update();
}

// randomly add new data
//setInterval(function() {
//    // time in seconds
////    fetch_data(function(data) {
//    // You can use your data here
////    console.log(data);
//    const newLabel = Math.floor(Math.random() * 10);
//    const val = fetch_data();
//    console.log(val);
//    addData(myChart, newLabel, val);
//
////    });
//
//}, 1000);
setInterval(function() {
  const newLabel = (Math.random() + 1).toString(36).substring(7);
  const newData = Math.floor(Math.random() * (10 - 1 + 1)) + 1;
  addData(myChart, newLabel, newData);
}, 1000);

function fetch_cpu_usage(){
    $.get('api/cpu', function(data){
        //console.log(data);
        $('#cpu_usage').html(data);
        $('#usage').val(data);
        //console.log('style.css path: ' + window.getComputedStyle(document.querySelector('link[rel=stylesheet]')).getPropertyValue('href'));
    })
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
    console.log(result);
    return result;
}

//function fetch_data(){
//    var data2;
//    $.get('api/read', function(data){
//        console.log(data);
//        callback(data);
////        data2 = data;
////        console.log(data);
//        //$('#plot').html(data);
////        $.get('api/plot.png', {data: data}, function(data2){
////            console.log(data2);
////            $("#myplot").attr("src", 'api/plot.png?data=' + data);
//
//        })
//};

window.onload = fetch_ports();

//setInterval(function(){
//    //fetch_cpu_usage();
//    //fetch_ports();
//}, 1000);

//setInterval(function(){
//    fetch_data();
//}, 1000);

// connect to the port by api call 'api/connect' by clicking on the button 'Connect'
$('#Connect').click(function(){
    var port = $('#ports').val();
    $.get('api/connect', {port: port}, function(data){
        console.log(data);
    })
})
