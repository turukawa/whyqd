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
    dlist = instruct + dlist + '</ul>';
    return dlist;
}
$(document).ready(function() {
    $('#downloadButton').on('click', function () {
        $.ajax({
           url: $('#downloadURL').val()
           }).done(function(data) {
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
            });           
        });
    $('#downloadButton').on('click', function () {
        $.ajax({
           url: $('#downloadURL').val()
           }).done(function(data) {
               var time = data.timer;
               var links = data.links;
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