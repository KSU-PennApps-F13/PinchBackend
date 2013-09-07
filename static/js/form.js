function submit_inject(){
    $("#qform").on('submit', function() {
        $.ajax({
            url: '/q',
            cache:false,
            type: 'POST',
            data: $('#qform').serialize(),
            success: function(data){
                var res = document.createTextNode(data);
                $("body").html(res);
            }
        });
    });
}

submit_inject()
