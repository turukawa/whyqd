

    function getdocxreview(docxarray) {
        var newaction = '<p>The table is sortable. Anything below a checked title will be grouped together as content, including sub-headings. If you wish to delete anything, now is the time. Note that a proper cover page will be created, so delete anything unrelated to chapters (like title, author, dedication) at this stage.</p><span class="navinput-icon btn btn-default" role="button"><label id="process" for="inputprocess">Accept</label><input id="inputprocess" type="hidden" name="file"></span><hr />';
        var partlast = '<label><small>&nbsp; delete &nbsp;</small><input type="checkbox" name="delete" value="delete" /></label><label><small>chapter &nbsp;</small><input type="checkbox" name="chapter" value="chapter" /></label></li>';
        var partlastselect = '<label><small>&nbsp; delete &nbsp;</small><input type="checkbox" name="delete" value="delete" /></label><label><small>chapter &nbsp;</small><input type="checkbox" name="chapter" value="chapter" checked /></label></li>';
        var partfirst = '<li data-value="-';
        var partfirstselect = '<li data-value="T';
        var partmid = '"><span class="ui-icon ui-icon-arrowthick-2-n-s"></span>';
        var partmidselect = '" style="background-color: rgb(227, 218, 201);"><span class="ui-icon ui-icon-arrowthick-2-n-s"></span>';
        var sortable = newaction + '<ul id="sortable">';
        $.each(docxarray, function(i, c) {
            if(c[0].indexOf("<b>") >= 0) {
                sortable = sortable + partfirstselect + c[1] + partmidselect + c[0] + partlastselect;
            } else {
                sortable = sortable + partfirst + c[1] + partmid + c[0] + partlast;
            }
            
        });
        sortable = sortable + '</ul>';
        return sortable;
    }
    function strip(html) {
        var tmp = document.createElement("DIV");
        tmp.innerHTML = html;
        return tmp.textContent || tmp.innerText || "";
    }

    $(document).ready(function() {
        var editor = new MediumEditor('.editable', {
            buttons: ['bold', 'italic', 'quote']
        });
        // Image processing
        $(document).on('click', 'label', function(event){
            if (!$(this).attr('id')) {
                // We're going to assume that a checkbox was clicked...
                // li.label.input where this is the label
                // http://stackoverflow.com/a/2204253
                var that = $(this).children('input').is(":checked");
                var currentdata = $(this).parent().attr("data-value");
                var bone = "#E3DAC9";
                var ghost = "#F8F8FF";
                var colour = $(this).children('input').attr('name') == 'chapter' ? bone : ghost;
                var parse = $(this).children('input').attr('name') == 'chapter' ? "T" : "D";
                $(this).parent().css("background-color", function() {
                    return that ? colour : "";
                });
                //http://www.jquery4u.com/javascript/15-javascript-string-functions/
                $(this).parent().attr("data-value", function() {
                    return that ? parse + currentdata.substring(1) : '-' + currentdata.substring(1);
                });
                return true;
            }
            switch($(this).attr('id')) {
                case "getdocx":
                    $(function () {
                        $('#docxupload').fileupload({
                            url: '/my/docxtract/',
                            type: "POST",
                            dataType: 'json',
                            done: function (e, data) {
                                var dlist = getdocxreview(data.result);
                                localStorage.setItem('dlist', dlist);
                                $("#booksort").html(dlist);
                                $("#sortable").sortable();
                                $("#sortable").disableSelection();
                                // Strip function: http://stackoverflow.com/a/822486
                                //var novel_data = editor.serialize()
                                //novel_data.defaultprice = strip(novel_data.defaultprice)
                                // Using Django standard form for the moment since require publish
                                // dates ... and can't think of a way to get that as text just yet.
                                var novel_data = $('#noveldata').serialize();
                                var array_novel_data = $('#noveldata').serializeArray();
                                var array_data = {};
                                $(array_novel_data).each(function(index, obj){
                                    array_data[obj.name] = obj.value;
                                });
                                $.post(window.location.pathname, novel_data, function(data) {
                                    localStorage.setItem('book', data.novel);
                                    //$('#bookintro').empty();
                                    $('#charactercount').empty();
                                    editor.deactivate();
                                    //hidebookempties();
                                    $('#noveldata').hide();
                                    $('#this_title').text(array_data.title);
                                    $('#this_pitch').text(array_data.pitch);
                                });
                            }
                        });
                    }); 
                    break;
                case "process":
                    $(function () {
                        var chapters = $("#sortable").sortable('toArray', {attribute: 'data-value'});
                        var totalchapters = chapters.length;
                        if (!totalchapters) {
                            return true;
                        }
                        var j = 0;
                        var bookstructure = {'0': {}};
                        $("#booksort").empty();
                        $("#booksort").append('<p>Please review and submit if you\'re satisfied</p>');
                        $("#booksort").append('<span><a id="write-accept" href="" class="btn btn-default" role="button">Accept</a></span>');
                        $("#booksort").append('<span><a id="write-restart" href="" class="btn btn-default" role="button">Restart</a></span>');
                        var content = false;
                        var pagecontent = "";
                        var first = true;
                        $.each(chapters, function(i, c) {
                            var action = c.substring(0,1);
                            var booktext = c.substring(1);
                            if (action !== "D") {
                                if (action == "T") {
                                    if (content) {
                                        if (first) {
                                            $("#booksort").append("<hr/>");
                                            first = false;
                                        }
                                        $("#booksort").append(content);
                                        bookstructure[j+'']['content'] = content;
                                        content = false;
                                    }
                                    $("#booksort").append("<hr/>");
                                    $("#booksort").append(booktext);
                                    first = false;
                                    if (bookstructure[j+'']) {
                                        j = j + 1;
                                        bookstructure[j+''] = {};
                                    }
                                    bookstructure[j+'']['title'] = booktext;
                                } else {
                                    if (content) {
                                        content = content + booktext;
                                    } else {
                                        content = booktext;
                                        pagecontent = $(booktext).text().substring(0,80)+"...";
                                    }
                                }
                                
                            }
                        });
                        if (content) {
                            bookstructure[j+'']['content'] = content;
                            $("#booksort").append(content);
                        }
                        localStorage.setItem('bookstructure', JSON.stringify({'upload': bookstructure}));
                    });
                    break;
                default:
                    return true;
            }
        });
        // Text processing
        $(document).on('click', 'a', function(event){ 
            event.preventDefault();
            switch($(this).attr('id')) {
                case "edit":
                    break;
                case "view":
                    break;
                case "write":
                    $.post(window.location.pathname, editor.serialize(), function(data) {
                        window.location.href = $('#write').attr('href') + '?j=view&lw=' + data.novel;
                    });
                    break;
                case "write-accept":
                    $(function () {
                        var bookstructure = localStorage.getItem('bookstructure');
                        localStorage.removeItem('dlist');
                        localStorage.removeItem('bookstructure');
                        $.post('/my/organise/' + localStorage.getItem('book') + '/', bookstructure, function(data) {
                            window.location.href = '/my/pricing/' + localStorage.getItem('book') + '/';//data.wiqi.url;
                        });
                    });
                    break;
                case "write-restart":
                    $(function () {
                        var dlist = localStorage.getItem('dlist');
                        $("#booksort").html(dlist);
                        $( "#sortable" ).sortable();
                        $( "#sortable" ).disableSelection();                       
                    });
                    break;
                default:
                    window.location.href = $(this).attr('href');
            }
        });
    });