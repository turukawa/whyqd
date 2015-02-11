function timer(time,update,complete) {
    // http://stackoverflow.com/a/11336046
    var start = new Date().getTime();
    var interval = setInterval(function() {
        var now = time-(new Date().getTime()-start);
        if( now <= 0) {
            clearInterval(interval);
            complete();
        }
        else update(Math.floor(now/1000));
    },100); // the smaller this number, the more accurate the timer will be
}
function setlinks(links) {
    var instruct = '<p>Your token has been disabled. Time remaining before links expire: <span id="timer"></span></p>';
    var dlist = '<ul>';
    $.each(links, function(k, l) {
        dlist = dlist + '<li><a href=' + l + '>' + k + '</a></li>';
    });
    return '<div class="row text-center col-md-10 col-md-push-1">' + instruct + dlist + '</ul><p><br/></p></div>';
}
$(document).ready(function() {
    $('#downloadButton').on('click', function () {
        $.ajax({
            url: $('#downloadURL').val(),
            success: function(data) {
                if (data.response == 'success') {
                    var time = data.timer;
                    var links = data.links;
                    $('#refundForm').remove();
                    $('#download_ebook').html(setlinks(links));
                    timer(
                        time*1000, // milliseconds
                        function(timeleft) { // called every step to update the visible countdown
                            document.getElementById('timer').innerHTML = timeleft + " seconds.";
                        },
                        function() { // what to do after
                            document.getElementById('timer').innerHTML = "download period ended.";
                        }
                    );
                }
                else {
                    $('#downloadButton').after(
                        '<div class="alert alert-danger alert-dismissable">'+
                            '<button type="button" class="close" ' + 
                                'data-dismiss="alert" aria-hidden="true">' + '&times;' + 
                            '</button>' + 
                            '<strong>Sorry</strong>, something went wrong. ' +
                            'Your token is still valid. Please try again.' +
                        '</div>');
                }
            },
            error: function(data) {
                $('#downloadButton').after(
                    '<div class="alert alert-danger alert-dismissable">'+
                        '<button type="button" class="close" ' + 
                            'data-dismiss="alert" aria-hidden="true">' + '&times;' + 
                        '</button>' + 
                        '<strong>Sorry</strong>, something went wrong. ' +
                        'Your token is still valid. Please try again.' +
                    '</div>');
            }
        });           
    });
    $('#refundToken').on('click', function (e) {
        var tid = this;
        $.ajax({
            url: tid.value
            }).done(function(data) {
                if (data.response == 'success') {
                    window.location.href = '/';
                }
            });
        e.preventDefault();
        });
});