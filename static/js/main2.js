$(document).ready(function() {
    let doc = $(document).height();
    let win = $(window).height();
    if (doc > win) {
        $("#footer").removeClass("fixed-bottom");
    }
})