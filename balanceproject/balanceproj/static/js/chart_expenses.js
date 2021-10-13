const yearVal_ex = document.getElementById("yearVal_ex")
const monthVal_ex = document.getElementById("monthVal_ex")
const dateBtn_ex = document.getElementById("dateBtn_ex")

var ctx1_ex = document.getElementById('myChart1_ex').getContext('2d');
var myChart1_ex = new Chart(ctx1_ex, {
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
                text : "Expenses per Category",
            }
        }
    }
});
var ctx2_ex = document.getElementById('myChart2_ex').getContext('2d');
var myChart2_ex = new Chart(ctx2_ex, {
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
                text : "Expenses per Category",
            }
        }
    }
});
var ctx3_ex = document.getElementById('myChart3_ex').getContext('2d');
var myChart3_ex = new Chart(ctx3_ex, {
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
                text : "Expenses per Category",
            }
        }
    }
});

const renderChart1_ex = (data, labels) => {
    myChart1_ex.data.labels = labels;
    myChart1_ex.data.datasets[0].data = data;
    myChart1_ex.update();
}
const renderChart2_ex = (data, labels) => {
    myChart2_ex.data.labels = labels;
    myChart2_ex.data.datasets[0].data = data;
    myChart2_ex.update();
}
const renderChart3_ex = (data, labels) => {
    myChart3_ex.data.labels = labels;
    myChart3_ex.data.datasets[0].data = data;
    myChart3_ex.update();
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
dateBtn_ex.addEventListener('click', ()=>{
    console.log({'yearVal' : yearVal_ex.value, 'monthVal': monthVal_ex.value})
    fetch('expense-summary',{
        body : JSON.stringify({yearVal : yearVal_ex.value, monthVal:monthVal_ex.value}),
        method : 'POST',}).
    then((res)=>res.json()).
    then(results=>{
        const source_data=results.expense_category_data;
        const [labels, data] = [Object.keys(source_data), Object.values(source_data)];

        renderChart1_ex(data, labels, );
        renderChart2_ex(data, labels);
        renderChart3_ex(data, labels);
    })
})



