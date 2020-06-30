$('.star').click(function(){
    var id;
    id = $(this).attr("post-id");
    $.ajax({
        type: "GET",
        url: "star",
        data: {post_id: id},
        success: function(data) {
            $('#star' + id).toggleClass("btn-outline-warning btn-warning");
        }
    });
});