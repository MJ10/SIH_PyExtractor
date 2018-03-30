var departments = ['Geology', 'Astromony', 'Physics'];


$(document).ready(function (){
    var optionsList = $('select');
    // fill options
    for (var i = 0; i < departments.length; ++i) {
        $('select').append($("<option></option>").attr("value", i).text(departments[i]));
    }
    $('select').formSelect();


    $('#upload').click(function() {
        if ($('select').val() == null || !$('input[type="file"]').val()) {
                
            M.toast({html: 'Please complete all fields'}, 1);            
        }

        setTimeout(function() {
            M.Toast.dismissAll();
        }, 1000);

        var formData = new FormData();
        formData.append('file', $('input[type=file]')[0].files[0]);
        console.log(formData);
        console.log($('select').val());
    });
   
});



