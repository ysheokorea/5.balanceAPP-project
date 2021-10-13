// Incomes Field
const searchField_incomes = document.getElementById("searchField_incomes");
const tableBody_incomes = document.querySelector('.table-body_incomes');
const appTable_incomes = document.querySelector("#dataTable_incomes");
const tableOutput_incomes = document.querySelector(".table-output-incomes");
const noResults_incomes = document.querySelector(".no-results_incomes");
//Sorting System
const tableOutput_incomes_sort = document.querySelector(".table-output-incomes_sort")
const tableBody_incomes_sort = document.querySelector(".table-body_incomes_sort")
tableOutput_incomes_sort.style.display = "none";
noResults_incomes.style.display = "none";
tableOutput_incomes.style.display="none";

// const tableHead = document.getElementById("test-th");
searchField_incomes.addEventListener('keyup', (e)=>{
    const searchValue = e.target.value;

    if(searchValue.trim().length > 0) {
        tableBody_incomes.innerHTML = "";
        fetch('search-incomes', {
            body : JSON.stringify({searchText : searchValue}),
            method : 'POST',
        })
            .then((res) => res.json())
            .then((data) => {
                console.log({'data' : data});
                appTable_incomes.style.display = "none";
                tableOutput_incomes.style.display = "block";

                if(data.length === 0){
                    noResults_incomes.style.display = "block";
                    tableOutput_incomes.style.display = "none";
                }
                else{
                    noResults_incomes.style.display = "none";
                    data.forEach(item =>{
                        tableBody_incomes.innerHTML += `
                            <tr>
                                <td>${item.date}</td>
                                <td>${item.source}</td>
                                <td>${item.amount}</td>
                                <td>${item.description}</td>
                            </tr>
                        `;
                    })

                }
            })
    }
    else{
        tableOutput_incomes.style.display="none";
        appTable_incomes.style.display = "block";
        noResults_incomes.style.display = "none";
    }
});

$('th').on('click', function(){
    var column=$(this).data('column');
    var order=$(this).data('order');
    var text=$(this).html()
    text=text.substring(0, text.length -1)

    $(this).text("");
    tableBody_incomes_sort.innerHTML="";
    if(order == 'desc'){
        $(this).data('order', "asc");
        fetch('sort-incomes-desc',{
            body : JSON.stringify({column:column}),
            method : 'POST',
        }).
        then((res) => res.json()).
        then(results=>{
            appTable_incomes.style.display = "none";
            tableOutput_incomes_sort.style.display = "block";
            results.forEach(item=>{
                tableBody_incomes_sort.innerHTML += `
                            <tr>
                                <td>${item.date}</td>
                                <td>${item.source}</td>
                                <td>${item.amount}</td>
                                <td>${item.description}</td>
                            </tr>
                        `;
            })
            $(this).html(column+'&#9650')
        })
    }else if(order == "asc"){
        $(this).data('order', "desc");
        fetch('sort-incomes-asc',{
            body : JSON.stringify({column:column}),
            method : 'POST',
        }).
        then((res) => res.json()).
        then(results=>{
            appTable_incomes.style.display = "none";
            tableOutput_incomes_sort.style.display = "block";
            results.forEach(item=>{
                tableBody_incomes_sort.innerHTML += `
                            <tr>
                                <td>${item.date}</td>
                                <td>${item.source}</td>
                                <td>${item.amount}</td>
                                <td>${item.description}</td>
                            </tr>
                        `;
            })
            $(this).html(column+'&#9660')

        })
    }
})




