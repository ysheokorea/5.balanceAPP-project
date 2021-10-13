const progressBar = document.querySelector('.progress-test')
const progressBtn = document.querySelector('.progress-btn')
const progressRate = document.querySelector('.progress-rate')



progressBtn.addEventListener('click', ()=>{
    fetch('progress-bar').
        then((res)=>res.json()).
        then(data => {
            const source_data = data.income_source_data;
            const [l,d] = [Object.keys(source_data), Object.values(source_data)];
            var sumValue = 0;
            for (var i=0; i<d.length; i++){
               sumValue = sumValue + d[i];
            }
            console.log(source_data);
            rateVal = (sumValue/20000000)*100+'%';
            progressBar.style.width = rateVal;
            // progressBar.style.width = "30%";
            console.log(sumValue);
            progressRate.innerHTML = `<h4 class="small font-weight-bold">Server Migration 
                                    <span class="float-right">${rateVal}</span></h4>
                                    `
        })
})
