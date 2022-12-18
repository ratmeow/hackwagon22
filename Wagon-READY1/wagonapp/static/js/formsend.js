let sendbtn = document.querySelector(".aside__button_submit");

sendbtn.addEventListener("click", function (e) {
    e.preventDefault();

    //let file= document.getElementsByName("file")[0].value;
    //let file= document.getElementsByName("file").files[0];
    //console.log(file);

    let input = document.getElementById("file");
    let file = input.files[0];
    console.log(file);
    
    let formdata = new FormData();
    formdata.append('file', file);
    formdata.append('test', 'test is work');
    console.log(formdata);
    console.log(formdata.get('file'));
    console.log(formdata.get('test'));

    //formparse = JSON.parse(formdata);
    //let full = formparse["file"];
    //console.log(full);

    console.log(file);

    if (file!=null && file.type == "audio/wav") {
        document.querySelector(".table__dummy-text").innerHTML = `
            <img src="static/img/loading.png" alt="loading..." class="loading-img">
            <style>
                .loading-img {
                    width: 50px; 
                    height: 50px;
                    animation: move 0.5s infinite linear;
                }
                
                @keyframes move {
                    0% {
                    transform: rotate(0deg);
                    }
                    50% {
                    transform: rotate(180deg);
                    border-radius: 50%;
                    }
                    100% {
                    transform: rotate(360deg);
                    }
                }
            </style>
        `


        fetch("/api/file",
        {
            method: "POST",
            body: formdata,
            /*headers: {
                'Content-Type': 'multipart/form-data'
            }*/
        })
        .then( response => {
            response.blob().then(function(data) {
                console.log(data);
                console.log(data.type);
                
                document.getElementById("download").innerHTML = `
                    <a href=` + URL.createObjectURL(data) + ` download="` + (file.name).split('.wav')[0] + `.csv">
                        <input class="aside__button" type="button" value="Скачать">
                    </a>
                `;

                $.ajax({
                    url: URL.createObjectURL(data),
                    dataType: 'text',
                  }).done(successFunction);

                  function successFunction(data1) {
                    //const reader = new FileReader();

                    
                    //console.log(reader.readAsText(data1, "windows-1251"));
                    console.log(data1);

                    //document.getElementById("table").innerHTML = data1;

                    let mas = data1.split('\n');
                    
                    console.log(mas);
                    let mas2 = [];
                    for (let i =  0; i < mas.length; i=i+1){
                        //let str = mas[i];
                        //let pmas = str.split(',');
                        //mas2.push(pmas);
                        if(mas[i] != ""){
                            mas2.push(mas[i].split(','));
                            while(mas2[i].length > 5) {
                                console.log(mas2[i]);
                                mas2[i][4] = mas2[i][4] + "," + mas2[i].splice(5);
                                mas2[i][4] = mas2[i][4].split('\"').join('');
                            }
                        }

                        //while(mas2[i].length > 5){
                        //    mas2[i][4] += "," + mas2[i].splice(5);
                        //}

                    }
                    console.log(mas2);

                    document.getElementById("tablecontainer").innerHTML = `
                        <table id="table"></table>
                    `

                    let table = document.getElementById("table");

                    table.innerHTML += `
                            <tr>
                                <th>` + mas2[0][0] + `</th>
                                <th>` + mas2[0][1] + `</th>
                                <th>` + mas2[0][2] + `</th>
                                <th>` + mas2[0][3] + `</th>
                                <th>` + mas2[0][4] + `</th>
                            </tr>
                        `;

                    for (let i = 1; i<mas2.length; i=i+1){
                        table.innerHTML += `
                            <tr>
                                <td>` + mas2[i][0] + `</td>
                                <td>` + mas2[i][1] + `</td>
                                <td>` + mas2[i][2] + `</td>
                                <td>` + mas2[i][3] + `</td>
                                <td>` + mas2[i][4] + `</td>
                            </tr>
                        `;
                    }



                  }

            });
        })
        .catch( error => {
            alert(error);
            console.error('error:', error);
        });
        
    }
    else {

    }
});
