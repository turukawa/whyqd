function getemaillist(form_text) {
    // http://scottdowne.wordpress.com/2010/07/13/javascript-array-split-on-multiple-characters/
    var textlist = form_text ? form_text.split(/[\s,;]+/) : 0;
    // http://stackoverflow.com/a/2507043 and http://www.w3.org/TR/html5/forms.html#valid-e-mail-address
    var regex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
    // http://stackoverflow.com/questions/4964456/make-javascript-do-list-comprehension
    var emails = jQuery.map(textlist, function(e) { if (regex.test(e)) { return e; } });
    return emails;
}
function setprice() {
    var count = parseInt($("#stripeCount").val());
    var discount = parseFloat($("#stripeDiscount").val());
    var volume = parseInt($("#stripeVolume").val());
    var fx_currency = $("#stripeCurrency").val().toLowerCase();
    var fx_price = parseFloat($('#forex_' + fx_currency).attr('data-value').trim()).toFixed(2);
    var base_price = parseFloat($('#basePrice').attr('value').trim()).toFixed(2);
    var bulk_price = base_price * fx_price;
    if (count) {
        bulk_price = bulk_price * count;
        if (count >= volume) {
            bulk_price = bulk_price / (1 + discount);
        }
    }
    $("#stripePrice").val(bulk_price.toFixed());
}
function getcurrencysymbol() {
    var forex_currency = $("#stripeCurrency").val();
    switch (forex_currency) {
        case 'GBP':
            return '&pound;';
        case 'EUR':
            return '&euro;';
        case 'USD':
            return '$';
        default:
            return '&pound;';
    }
}
function setcount(volume, discount) {
    var emails = getemaillist(this.value)
    var count = emails.length > 1 ? emails.length : 1;
    if (emails.length) {
        $('#stripeButton').prop('disabled', false);
    }
    else {
        $('#stripeButton').prop('disabled', true);
    }
    $("#stripeCount").val(count);
    $("#stripeDiscount").val(discount);
    $("#stripeVolume").val(volume);
    setprice();
    setbuttonprice();
}
function setbuttonprice() {
    var count = parseInt($("#stripeCount").val());
    var discount = $("#stripeDiscount").val();
    var volume = parseInt($("#stripeVolume").val());
    var currency = getcurrencysymbol();
    var price = $("#stripePrice").val();
    var d_text = "Buy " + count + " for " + currency + " " + (price/100).toFixed(2);
    //var cin = count >= volume ? 'btn-success' : 'btn-default';
    //var cout = count < volume ? 'btn-success' : 'btn-default';
    d_text = count >= volume ? d_text + " (" + Math.floor(discount*100) + "% discount)" : d_text;
    $('#stripeButton').html(d_text); //.addClass(cin).removeClass(cout);
    //$("#stripeCaret").addClass(cin).removeClass(cout);
}
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
    var instruct = '<p>Time remaining before links expire: <span id="timer"></span></p>';
    var dlist = '<ul class="redeem-token">';
    $.each(links, function(k, l) {
        dlist = dlist + '<li><a href=' + l + '>' + k + '</a></li>';
    });
    dlist = instruct + dlist + '</ul>';
    dlist += '<p>Guidance for reading ' +
    '<a href="https://www.amazon.com/gp/sendtokindle">Kindle/.mobi</a> ' +
    'and <a href="http://www.kobobooks.com/ade">Kobo/Nook/.epub</a>.</p>';
    return dlist;
}
$(document).ready(function() {
    $.ajax({
        url: $('#stripeSettings').val()
        }).done(function(data) {
            ns = data.settings;
            var handler = StripeCheckout.configure({
                key: ns.stripe_key,
                image: '/static/images/qwyre_logo_128pxBW.png',
                name: ns.novel_title,
                email: ns.user_email,
                token: function(token) {
                    // http://stackoverflow.com/a/22461608
                    // You can access the token ID with `token.id`
                    $.ajax({
                        url: $('#stripeBuy').val(),
                        type: 'post',
                        data: {
                            stripeToken: token.id,
                            stripeDescription: ns.description,
                            stripePrice: ns.price,
                            stripeCurrency: ns.currency,
                            stripeEmails: ns.emails,
                            selfPurchase: false,
                            template: 'gift_purchase'
                        },
                        success: function(data) {
                            if (data.response == 'success') {
                                $("#email_list").val("");
                                window.location.href = window.location.href;;
                            }
                            else {
                                $('#bulkbuyinfo').html(
                                    '<div class="alert alert-danger alert-dismissable">'+
                                        '<button type="button" class="close" ' + 
                                            'data-dismiss="alert" aria-hidden="true">' + '&times;' + 
                                        '</button>' + 
                                        '<strong>Sorry</strong>, something went wrong. ' +
                                        'You have not been charged. Please try again.' +
                                     '</div>');
                            }
                        },
                        error: function(data) {
                            $('#bulkbuyinfo').html(
                                '<div class="alert alert-danger alert-dismissable">'+
                                    '<button type="button" class="close" ' + 
                                        'data-dismiss="alert" aria-hidden="true">' + '&times;' + 
                                    '</button>' + 
                                    '<strong>Sorry</strong>, something went wrong. ' +
                                    'You have not been charged. Please try again.' +
                                 '</div>');
                        }
                      }); // end ajax call
                }
            });
            //https://mathiasbynens.be/notes/oninput
            var emaillist = document.getElementById("email_list");
            emaillist.oninput = function() {
                this.onkeyup = null;
                setcount.call(this, ns.bulk_volume, ns.bulk_discount);
            };
            emaillist.onkeyup = function() {
                setcount.call(this, ns.bulk_volume, ns.bulk_discount);
            };
            document.getElementById('stripeButton').addEventListener('click', function(e) {
                var emails = getemaillist($('#email_list').val());
                ns.emails = emails.toString();
                ns.price = $("#stripePrice").val();
                ns.description = ns.novel_title + " - " + $('#stripeButton').html();
                ns.currency = $('#stripeCurrency').val();
                // Open Checkout with further options
                handler.open({
                    name: "Whythawk Limited (Qwyre)",
                    description: ns.description,
                    amount: ns.price,
                    currency: ns.currency
                });
                e.preventDefault();
            });
        });
    $('#downloadButton').on('click', function () {
        $.ajax({
            url: $('#downloadURL').val(),
            success: function(data) {
                if (data.response == 'success') {
                    var time = data.timer;
                    var links = data.links;
                    // http://stackoverflow.com/a/5557728
                    var divclone = $('#download_ebook').clone(true, true);
                    $('#download_ebook').html(setlinks(links));
                    timer(
                        time*1000, // milliseconds
                        function(timeleft) { // called every step to update the visible countdown
                            document.getElementById('timer').innerHTML = timeleft + " seconds.";
                        },
                        function() { // what to do after
                            $('#download_ebook').replaceWith(divclone);
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
                            'Please try again.' +
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
                        'Please try again.' +
                    '</div>');
            }
        });           
    });
    $('[id^=refundToken_]').on('click', function (e) {
        var tid = this;
        var rid = tid.id.replace("refundToken_", "");
        $.ajax({
            url: tid.value
            }).done(function(data) {
                if (data.response == 'success') {
                    $('#refundForm_' + rid).remove();
                }
            });
        e.preventDefault();
        });
    $('[id^=resendToken_]').on('click', function (e) {
        var tid = this;
        var rid = tid.id.replace("resendToken_","");
        rid = "id_refund-" + rid + "-recipient";
        var recipient = $('#' + rid).val();
        $.ajax({
            url: tid.value,
            type: 'post',
            data: {
                recipient: recipient,
                template: 'gift_purchase'
            },
           }).done(function(data) {
                if (data.response == 'success') {
                    console.log(data.recipient)
                }
            });
        e.preventDefault();
        });
    $('[id^=forex_]').on('click', function (e) {
        var forex = this;
        switch (this.id) {
            case 'forex_usd':
                $("#stripeCurrency").val('USD');
                break;
            case 'forex_gbp':
                $("#stripeCurrency").val('GBP');
                break;
            case 'forex_eur':
                $("#stripeCurrency").val('EUR');
                break;
        }
        setprice();
        setbuttonprice();
        e.preventDefault();
        });
    $('#change_email').on('click', function (e) {
        var emails = getemaillist($('#user_email').val());
        emails = emails.toString();
        name = $('#facebookname').val().toString();
        optout = $('#optout').is(':checked').toString();
        $.ajax({
            url: $('#user_update').val(),
            type: 'post',
            data: {
                email: emails,
                name: name,
                optout: optout
            }
            });
        e.preventDefault();
        });
});