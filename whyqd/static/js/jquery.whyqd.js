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
    

    function getnavactions(nav, nav_active) {
        //nav is list of form [[nav_item, nav_url],...]
        var navtypes = {'view': '<span class="icon-eye"></span>',
                        'edit': '<span class="icon-quill"></span>',
                        'editing': '<span class="icon-disk"></span>',
                        'fork': '<span class="icon-fork"></span>',
                        'stack': '<span class="icon-stack"></span>',
                        'create': '<span class="icon-file"></span>',
                        'image': '<li id="nav-image"><label id="image" for="fileupload" class="navbar-text"><span class="icon-image"></span></label><input id="fileupload" type="file" name="file"></li>'
                        };
        htmlresponse = '';
        $.each(nav, function(index, item) {
            eachresponse ='<li id="nav-' + item[0] +'" ';
            if (item[0] === nav_active) {
                eachresponse = eachresponse + 'class="active" ';
            }
            eachresponse = eachresponse + '><a id="' + item[0] + '" title="' 
                           + item[0] + '" href="' + item[1] + '">';
            if (item[0] === nav_active && item[0] === "edit") {  
                eachresponse = eachresponse + navtypes['editing'] + '</a></li>';
            } else {
                eachresponse = eachresponse + navtypes[item[0]] + '</a></li>';
            }
            htmlresponse = htmlresponse + eachresponse;
            // Add in the image upload button after the edit button
            if (item[0] === "edit" && item[0] == nav_active) {
                htmlresponse = htmlresponse + navtypes['image'];
            }
        });
        return htmlresponse;
    }
    
    function getpagewiqi() {
        if ($('#view').length) {
            return $('#view').attr('href');
        } else {
            return "/";
        }
    }
 
     function getimageurl() {
        var image_wiqi = $.trim($("#header-image-surl").html());
        if (image_wiqi && image_wiqi !== "None") {
            return image_wiqi + "/";
        } else {
            return "";
        }
    }
            
    function getimagestackurl() {
        var imagestack_wiqi = $.trim($("#header-imagestack-surl").html());
        if (imagestack_wiqi && imagestack_wiqi !== "None") {
            return "/edit/image/" + imagestack_wiqi + "/";
        } else {
            return "/create/image" + getpagewiqi();
        }       
    }
    
    function showheaderempties() {
        if (!$('#source_attribution').html().trim()) {
            $('#source_attribution').show(); //animate({opacity:1.0},100);
        }
        if (!$('#subtitle').html().trim()) {
            $('#subtitle').show(); //animate({opacity:1.0},100);
        }         
    }

    function hideheaderempties() {
        if (!$('#source_attribution').html().trim()) {
            $('#source_attribution').hide(); //animate({opacity:0.0},2000);
        }
        if (!$('#subtitle').html().trim()) {
            $('#subtitle').hide(); //animate({opacity:0.0},2000);
        }         
    }
   
    $(document).ready(function() {
        var editor = new MediumEditor('.editable', {
            buttons: ['bold', 'italic', 'quote'],
        });
        if ($('#view').length) {
            editor.deactivate();
            hideheaderempties();
        }
        var nav_visible = true;
        // Image processing
        $(document).on('click', 'label', function(event){
            switch($(this).attr('id')) {
                case "image":
                    $(function () {
                        $('#fileupload').fileupload({
                            url: getimagestackurl(),
                            type: "POST",
                            formData: editor.serialize(),
                            dataType: 'json',
                            done: function (e, data) {
                                $("#page-header-image").html(data.result.image);
                                $("#header-image-surl").html(data.result.imagesurl);
                                $("#header-imagestack-surl").html(data.result.imagestacksurl);
                                $('div[class^="whyqd-text-"]').attr('class', 
                                    function(i, c) {
                                        return c.replace(/\bwhyqd-text-([a-z]*)/g, 
                                        "whyqd-text-" + data.result.color + " ");
                                        });
                            }
                        });
                    }); 
                    break;
                default:
            }
        });
        // Text processing
        $(document).on('click', 'a', function(event){ 
            event.preventDefault(); 
            var page_wiqi = $.trim($("#header-wiqi-surl").html());
            switch($(this).attr('id')) {
                case "edit":
                    showheaderempties();
                    if ($('#nav-edit').attr('class')==='active') {
                        // http://stackoverflow.com/questions/2751566/jquery-on-click-event-send-post-request
                        $.post(event.currentTarget.pathname + getimageurl(), editor.serialize(), function(data) {
                            $("#nav-actions").html(getnavactions(data.nav, "edit"));
                        });                   
                    } else {
                        editor.activate();
                        $.ajax({
                           url: "/nav/edit" + getpagewiqi()
                        }).done(function(data) {
                            $("#nav-actions").html(getnavactions(data.nav, "edit"));
                        });
                    } 
                    break;
                case "view":
                    hideheaderempties();
                    if ($('#nav-stack').attr('class')==='active') {
                        window.location.href = $(this).attr('href');
                        break;
                    }
                    if ($('#nav-view').attr('class')!=='active') {
                        editor.deactivate();
                        $.ajax({
                           url: "/nav/view" + getpagewiqi()
                        }).done(function(data) {
                            $("#nav-actions").html(getnavactions(data.nav, "view"));
                        });
                        break;
                    } else {
                        window.location.href = $(this).attr('href');
                        break;
                    }
                case "fork":
                    $.post(event.currentTarget.pathname, editor.serialize(), function(data) {
                        console.log(data.view);
                        window.location.href = data.view;
                    });     
                    break;        
                default:
                    window.location.href = $(this).attr('href');
            }
        });
        // Text editing and getting out the way
        $("#content").keyup(function(e) {
            console.log(nav_visible);
            if (nav_visible === true) {
                $("#navigation").animate({opacity:0.0},2000);
                nav_visible = false;        
            }
        });
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
    /*
        $("#navigation").hover(function() {
            $("#navigation").animate({opacity:1.0},100);
            nav_visible = true;
        });
     */