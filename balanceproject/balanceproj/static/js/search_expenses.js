// Expenses Field
const searchField_expenses = document.querySelector("#searchField_expenses");
const tableBody_expenses = document.querySelector(".table-body_expenses");
const appTable_expenses = document.querySelector("#dataTable_expenses");
const tableOutput_expenses = document.querySelector(".table-output_expenses");
const noResults_expenses = document.querySelector(".no-results_expenses");
noResults_expenses.style.display = "none";
tableOutput_expenses.style.display = "none";
//Sorting System
const tableOutput_expenses_sort = document.querySelector(".table-output-expenses_sort")
tableOutput_expenses_sort.style.display = "none";
const tableBody_expenses_sort = document.querySelector(".table-body_expenses_sort")


searchField_expenses.addEventListener('keyup', (e)=>{
    const searchValue = e.target.value;
    
    if(searchValue.trim().length > 0){
        tableBody_expenses.innerHTML = "";
        fetch('search-expenses',{
            body : JSON.stringify({searchText : searchValue}),
            method : 'POST',
        }).
        then((res)=>res.json()).
        then(data=>{
            console.log({'data' : data})
            appTable_expenses.style.display = "none";
            tableOutput_expenses.style.display = "block";

            if(data.length === 0){
                noResults_expenses.style.display = "block";
                tableOutput_expenses.style.display = "none";
            }
            else{
                noResults_expenses.style.display = "none";
                data.forEach(item=>{
                    tableBody_expenses.innerHTML += `
                    <tr>
                        <th>${item.date}</th>
                        <th>${item.category}</th>
                        <th>${item.amount}</th>
                        <th>${item.description}</th>
                    </tr>
                    `;
                })
            }
        })
    }
    else{
        appTable_expenses.style.display ="block";
        noResults_expenses.style.display = "none";
        tableOutput_expenses.style.display = "none";
    }
})
$('th').on('click', function(){
    var column=$(this).data('column');
    var order=$(this).data('order');
    var text=$(this).html()
    text=text.substring(0, text.length -1)

    
    $(this).text("");
    tableBody_expenses_sort.innerHTML="";
    if(order == 'desc'){
        $(this).data('order', "asc");
        fetch('sort-expenses-desc',{
            body : JSON.stringify({column:column}),
            method : 'POST',
        }).
        then((res) => res.json()).
        then(results=>{
            appTable_expenses.style.display = "none";
            tableOutput_expenses_sort.style.display = "block";
            results.forEach(item=>{
                tableBody_expenses_sort.innerHTML += `
                            <tr>
                                <td>${item.date}</td>
                                <td>${item.category}</td>
                                <td>${item.amount}</td>
                                <td>${item.description}</td>
                            </tr>
                        `;
            })
            $(this).html(column+'&#9650')
        })
    }else if(order == "asc"){
        $(this).data('order', "desc");
        fetch('sort-expenses-asc',{
            body : JSON.stringify({column:column}),
            method : 'POST',
        }).
        then((res) => res.json()).
        then(results=>{
            appTable_expenses.style.display = "none";
            tableOutput_expenses_sort.style.display = "block";
            results.forEach(item=>{
                tableBody_expenses_sort.innerHTML += `
                            <tr>
                                <td>${item.date}</td>
                                <td>${item.category}</td>
                                <td>${item.amount}</td>
                                <td>${item.description}</td>
                            </tr>
                        `;
            })
            $(this).html(column+'&#9660')

        })
    }
})
