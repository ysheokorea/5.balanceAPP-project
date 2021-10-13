const yearVal = document.getElementById("yearVal")
const monthVal = document.getElementById("monthVal")
const dateBtn = document.getElementById("dateBtn")

var ctx1 = document.getElementById('myChart1').getContext('2d');
var myChart1 = new Chart(ctx1, {
    type: 'bar',
    data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [{
            label: 'Last 6 months incomes',
            data: [500,400,300,200,100],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        plugins:{
            title : {
                display : true,
                text : "Incomes per sources",
            }
        }
    }
});
var ctx2 = document.getElementById('myChart2').getContext('2d');
var myChart2 = new Chart(ctx2, {
    type: 'doughnut',
    data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [{
            label: 'Last 6 months incomes',
            data: [500,400,300,200,100],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        plugins:{
            title : {
                display : true,
                text : "Incomes per sources",
            }
        }
    }
});
var ctx3 = document.getElementById('myChart3').getContext('2d');
var myChart3 = new Chart(ctx3, {
    type: 'line',
    data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [{
            label: 'Last 6 months incomes',
            data: [500,400,300,200,100],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        plugins:{
            title : {
                display : true,
                text : "Incomes per sources",
            }
        }
    }
});

const renderChart1 = (data, labels) => {
    myChart1.data.labels = labels;
    myChart1.data.datasets[0].data = data;
    myChart1.update();
}
const renderChart2 = (data, labels) => {
    myChart2.data.labels = labels;
    myChart2.data.datasets[0].data = data;
    myChart2.update();
}
const renderChart3 = (data, labels) => {
    myChart3.data.labels = labels;
    myChart3.data.datasets[0].data = data;
    myChart3.update();
}


// const getChartData = () =>{
//     console.log({'yearVal' : yearVal, 'monthVal': monthVal})
//     fetch('income-summary',{
//         body : JSON.stringify({yearVal : yearVal, monthVal:monthVal}),
//         method : 'POST',}).
//     then((res)=>res.json()).
//     then(results=>{
//         const source_data=results.income_source_data;
//         const [labels, data] = [Object.keys(source_data), Object.values(source_data)];

//         renderChart1(data, labels);
//         renderChart2(data, labels);
//         renderChart3(data, labels);
//     })
// }


// document.onload = getChartData()
dateBtn.addEventListener('click', ()=>{
    console.log({'yearVal' : yearVal.value, 'monthVal': monthVal.value})
    fetch('income-summary',{
        body : JSON.stringify({yearVal : yearVal.value, monthVal:monthVal.value}),
        method : 'POST',}).
    then((res)=>res.json()).
    then(results=>{
        const source_data=results.income_source_data;
        const [labels, data] = [Object.keys(source_data), Object.values(source_data)];

        renderChart1(data, labels);
        renderChart2(data, labels);
        renderChart3(data, labels);
    })
})



