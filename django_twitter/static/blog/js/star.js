$('.star').click(function(){
    var id;
    id = $(this).attr("id");
    $.ajax({
        type: "GET",
        url: "/dupa",
        data: {post_id: id},
        success: function(data) {
            $(this).removeClass('btn-outline-warning');
            $(this).addClass('btn-warning');
        }
    });
});