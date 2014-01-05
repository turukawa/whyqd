    // using jQuery
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection"
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    
    $(document).ready(function() {
        // Facebook details
          window.fbAsyncInit = function() {
            // init the FB JS SDK
            FB.init({
              appId      : '528916567204030',                        // App ID from the app dashboard
              status     : true,                                 // Check Facebook Login status
              xfbml      : true                                  // Look for social plugins on the page
            });
        
            // Additional initialization code such as adding Event Listeners goes here
          };
          // Load the SDK asynchronously
          (function(){
             // If we've already installed the SDK, we're done
             if (document.getElementById('facebook-jssdk')) {return;}
             // Get the first script element, which we'll use to find the parent node
             var firstScriptElement = document.getElementsByTagName('script')[0];
             // Create a new script element and set its id
             var facebookJS = document.createElement('script'); 
             facebookJS.id = 'facebook-jssdk';
             // Set the new script's source to the source of the Facebook JS SDK
             facebookJS.src = '//connect.facebook.net/en_US/all.js';
             // Insert the Facebook JS SDK into the DOM
             firstScriptElement.parentNode.insertBefore(facebookJS, firstScriptElement);
           }());
    });