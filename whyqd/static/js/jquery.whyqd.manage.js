function getemaillist(form_text) {
    // http://scottdowne.wordpress.com/2010/07/13/javascript-array-split-on-multiple-characters/
    var textlist = form_text ? form_text.split(/[\s,;]+/) : 0;
    // http://stackoverflow.com/a/2507043 and http://www.w3.org/TR/html5/forms.html#valid-e-mail-address
    var regex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
    // http://stackoverflow.com/questions/4964456/make-javascript-do-list-comprehension
    var emails = jQuery.map(textlist, function(e) { if (regex.test(e)) { return e; } });
    return emails;
}
function setchapterstructure() {
        $.ajax({
            url: $('#chapterFormat').val(),
            }).done(function(data) {
                var chapterformat = $.parseJSON(data.chapterformat);
                for (var c = 0; c < chapterformat.len; c++) {
                    var i = chapterformat.chapters[c].id;
                    if (chapterformat.chapters[c].is_section) {
                        $('#structureSection_'+i).prop('checked', true);
                    }
                    if (chapterformat.chapters[c].is_callout) {
                        $('#structureCallOut_'+i).prop('checked', true);
                    }
                }
            });        
}
$(document).ready(function() {
    setchapterstructure();
    $('#market_tokens').on('click', function (e) {
        var emails = getemaillist($('#market_list').val());
        emails = emails.toString();
        var custom_email = "";
        var custom_subject = "";
        if ($('#send_individual').is(':checked')) {
            custom_email = $('#custom_email').val();
            custom_subject = $('#custom_subject').val();
        }
        $.ajax({
            url: $('#marketTokens').val(),
            type: 'post',
            data: {
                recipients: emails,
                subject: custom_subject,
                custom: custom_email
            }
            }).done(function(data) {
                $("#market_list").val("");
                $('#custom_email').val("");
                $('#custom_subject').val("");
            });
        e.preventDefault();
        });
    $('#set_structure').on('click', function (e) {
        var len = $('#structureLength').val();
        var response = {
            len: 0,
            chapters: {}
        };
        for (var i = 0; i <= len; i++) {
            // http://stackoverflow.com/a/2204253
            var is_section = $('#structureSection_'+i).is(":checked");
            var is_callout = $('#structureCallOut_'+i).is(":checked");
            response.chapters[response.len] = {
                title: $('#structureTitle_'+i).val(),
                url: $('#structureURL_'+i).val(),
                read: $('#structureReadIf_'+i).val(),
                id: i,
                is_section: is_section,
                is_callout: is_callout,
            }
            response.len++;
        }
        console.log(JSON.stringify(response));
        $.ajax({
            url: $('#chapterFormat').val(),
            type: 'post',
            data: {
                chapterformat: JSON.stringify(response)
            }
            }).done(function(data) {
                console.log(data);
            });
        e.preventDefault();
    });
});