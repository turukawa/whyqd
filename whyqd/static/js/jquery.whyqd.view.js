    function hideheaderempties() {
        if (!$('#subtitle').html().trim()) {
            $('#subtitle').hide(); //animate({opacity:0.0},2000);
        }
        if (!$('#title').html().trim()) {
            $('#title').hide();
        }
    }

    $(document).ready(function() {
        if ($('#view').length) {
            hideheaderempties();
        }
        var nav_visible = true;
        // Text reading and getting out the way
        //http://stackoverflow.com/questions/3706957/reset-on-hover-jquery
        $("#navigation").hover(function() {
            nav_visible = true;
            $("#navigation").stop(true, true).animate({opacity:1.0},100); // You might not need to use clearQueue() but test it out
        },
        function() {
            nav_visible = false;
            $("#navigation").delay(10000).animate({opacity:0.0},2000);
        }).animate({opacity:1.0},100).delay(10000).animate({opacity:0.0},2000);
    });