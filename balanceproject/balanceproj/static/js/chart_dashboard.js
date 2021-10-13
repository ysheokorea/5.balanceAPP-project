
var dashboard1 = document.getElementById('myAreaChart-dash').getContext('2d');
var myChart4 = new Chart(dashboard1, {
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


var dashboard2 = document.getElementById('myPieChart-dash').getContext('2d');
var myChart5 = new Chart(dashboard2, {
    type: 'pie',
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
const renderChart4 = (data, labels) => {
    myChart4.data.labels = labels;
    myChart4.data.datasets[0].data = data;
    myChart4.update();
}
const renderChart5 = (data, labels) => {
    myChart5.data.labels = labels;
    myChart5.data.datasets[0].data = data;
    myChart5.update();
}


const getCharData=() =>{
    fetch('dashboard-incomes-summary').
    then((res)=>res.json()).
    then(results=>{
        const source_data=results.income_source_data;
        const [labels, data] = [Object.keys(source_data), Object.values(source_data)];
        renderChart4(data, labels);
    })
    fetch('dashboard-expenses-summary').
    then((res)=>res.json()).
    then(results=>{
        const source_data=results.expense_category_data;
        const [labels, data] = [Object.keys(source_data), Object.values(source_data)];
        renderChart5(data, labels);
    })
}


document.onload = getCharData();