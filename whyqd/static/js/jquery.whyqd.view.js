
    function getnavactions(nav, nav_active) {
        //nav is list of form [[nav_item, nav_url],...]
        var navtypes = {'view': '<span class="icon-eye"></span>',
                        'edit': '<span class="icon-quill"></span>',
                        'editing': '<span class="icon-disk"></span>',
                        'branch': '<span class="icon-branch"></span>',
                        'stack': '<span class="icon-stack"></span>',
                        'create': '<span class="icon-file"></span>',
                        //'image': '<li id="nav-image" class="navinput-icon"><label id="image" for="fileupload" class="navbar-text"><span class="icon-image"></span></label><input id="fileupload" type="file" name="file"></li>'
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
    
    function showheaderempties() {
        if (!$('#subtitle').html().trim()) {
            $('#subtitle').show(); //animate({opacity:1.0},100);
        }
        if (!$('#title').html().trim()) {
            $('#title').hide();
        }       
    }

    function hideheaderempties() {
        if (!$('#subtitle').html().trim()) {
            $('#subtitle').hide(); //animate({opacity:0.0},2000);
        }
        if (!$('#title').html().trim()) {
            $('#title').hide();
        }
    }
   
    function processAjaxData(response, urlPath){
        // http://stackoverflow.com/a/3354511
        document.getElementById("content").innerHTML = response.html;
        document.title = response.pageTitle;
        window.history.pushState({"html":response.html,"pageTitle":response.pageTitle},"", urlPath);
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
        // Text processing
        $(document).on('click', 'a', function(event){ 
            event.preventDefault(); 
            var page_wiqi = $.trim($("#header-wiqi-surl").html());
            switch($(this).attr('id')) {
                case "edit":
                    showheaderempties();
                    if ($('#nav-edit').attr('class')==='active') {
                        // http://stackoverflow.com/questions/2751566/jquery-on-click-event-send-post-request
                        console.log($("#working-on").data('surl'));
                        // http://stackoverflow.com/a/4406372
                        $.post(event.currentTarget.pathname + '?lw=' + $("#working-on").data('surl'), editor.serialize(), function(data) {
                            $("#nav-actions").html(getnavactions(data.nav, "edit"));
                            // Leave this for now...
                            //if (window.location.pathname != data.wiqi.wiqiurl ) {
                            //    http://stackoverflow.com/a/3354511
                            //    window.history.pushState({"html":response.html,"pageTitle":response.pageTitle},"", urlPath);
                            //}
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
                case "branch":
                    $.post(event.currentTarget.pathname, editor.serialize(), function(data) {
                        window.location.href = data.wiqi.wiqiurl;
                    });     
                    break;
                case "create":
                    window.location.href = $(this).attr('href') + '?j=view&lw=' + $("#working-on").data('surl');
                    break;
                default:
                    window.location.href = $(this).attr('href');
            }
        });
        // Text editing and getting out the way
        $("#content").keyup(function(e) {
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