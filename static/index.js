$(document).ready(function() {
    listing();
    bsCustomFileInput.init()
    bsCustomFileInput.init()

})

// listing ini untuk mengecek di consolelog apakah sudh berhasil
function listing(){
    $.ajax ({
        Type : 'GET',
        url : '/dairy',
        data : {},
        success : function(response){
            let articles = response['articles'];
            let temp_html =''
            for (i = 0; i < articles.length; i++){
                let title = articles[i]['title'];
                let content = articles[i]['content'];
                let file = articles[i]['file'];
                let time = articles[i]['time'] || '???.??.??';
                let profile = articles[i]['profile'];
                temp_html = `
                <div class="col-4">
          <div class="card">
          <img src="../static/${file}" class="img-fluid rounded-start" alt="...">
            <div class="card-body">
              <h5 class="card-title">${title}</h5>
              <p class="card-text">${content}</p>
              <img src="../static/${profile}" class="img" alt="..."> 
                                <h6 class="card-subtitle mb-2 text-muted"><small class="text-muted">${time}</small>
                                </h6>
            
            </div>
          </div>
        </div> `;
                        $('#card-box').append(temp_html);
            }
        }
    })
}
// Kita harus mengirimkan data title dan content ke server 
// Kita harus menunjukkan kepada user respons dari server sebagai suatu alert, dan lalu refresh lamannya
function posting(){
    let title = $('#image-title').val();
    if (!title){
        return alert('heyy, your forgot the title')
    }
    let content = $('#image-content').val();
    if (!content){
        return alert('heyy, your forgot the description')
    }

    // mengirimkan file ke server
    let file = $("#image").prop("files")[0];
    let profile = $("#profile").prop("files")[0];

    let form_data = new FormData();
    form_data.append("file_give", file);
    form_data.append("profile_give", profile);
    form_data.append("title_give", title);
    form_data.append("content_give", content);

    $.ajax({
        type : 'POST',
        url : '/dairy',
        data : form_data, // agar request tidak bingung permintaan form data // kita ubah dengan form data, karena telah mewakili semua variable dari valuenya
        contentType: false,
        processData: false,
        success : function(response){
            alert(response['msg'])
            window.location.reload();
            // console.log(response["msg"])
        }
    })
}