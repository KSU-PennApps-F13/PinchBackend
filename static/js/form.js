function submit_inject(){
    $("#qform").on('submit', function() {
        var d = {"data":[{"name":"mac"}]}
        $.ajax({
            url: '/q',
            cache:false,
            type: 'POST',
            dataType: 'json',
            data: JSON.stringfy(d),
            success: function(data){
                var res = document.createTextNode(data);
                $("body").html(res);
            }
        });
    });
}

submit_inject()
