!function( $ ) {
    "use strict"; // js-hint screams if we don't include it ;_; (or use it's name...)
    var default_delay = {show: 200, hide: 200}
    var slow_delay = {show: 1000, hide: 200}

    function auto_placement($tip, element) {
        var offset = $(element).offset(),
            top = offset.top, left = offset.left,
            doc_width = $(document).outerWidth(),
            doc_height = $(document).outerHeight(),
            cen_x = doc_width / 2,
            cen_y = doc_height / 2
        var actualWidth = $tip.offsetWidth || 350, actualHeight = $tip.offsetHeight || 350

        var horiz = left > cen_x ? 'left' : 'right'
        var horiz_offset = left > cen_x ? left - actualWidth : left + actualWidth
        var vert = top > cen_y ? 'top' : 'bottom'
        var vert_offset = top > cen_y ? top - actualHeight : top + actualHeight 
        return Math.abs(cen_x -horiz_offset) > Math.abs(cen_y - vert_offset) ? horiz : vert
    }

    $('[rel="tooltip"]').tooltip({delay: default_delay})
    $('[rel="tooltip-table"]').tooltip({container: 'body', delay: default_delay})
    $('[rel="tooltip-slow"]').tooltip({delay: slow_delay})
    $('[rel="popover-html"]').popover({container: 'body', placement: auto_placement, delay: default_delay, html: true, content: function() { return $("#" + $(this).attr('data-rel')).html() }, template: '<div class="popover popover-html"><div class="arrow"></div><div class="popover-inner"><h3 class="popover-title"></h3><div class="popover-content"><p></p></div></div></div>'})

    var $popovers = $('[rel="popover"],[rel="popover-html"]')
    if ($popovers.length > 0) {
        $('html').on('click.popover.data-api', function(e) {
            var $target = $(e.target)
            var $parents = $($target.parents('[rel="popover"],[rel="popover-html"]').get(0))
            if ((typeof $target.attr('rel') !== 'undefined') && ($target.attr('rel').startsWith('popover'))) {
                $parents = $($target)
            }
            if ($parents.length > 0) {
                var popover = $parents.data('popover')
                var shown = popover && popover.tip().hasClass('in')
                $popovers.each(function(i) {
                    if ( $(this).get(0) == $parents.get(0) ) { return }
                    $(this).popover('hide')                 
                })
            }
            else {
                if ( $target.parents('.popover-content').length < 1 ) { // allow clicking on content
                    $popovers.popover('hide')
                }
            }
        })
    }

    $("input[name='csrfmiddlewaretoken']").each(function(){
        if( $(this).attr("value") != window.__csrf_token__) {
            $(this).attr("value", window.__csrf_token__);
        }
    })


    $.ajaxSetup({cache: false, surpressErrors: false})
    $(document).ajaxError(function(evt, xhr, settings) {
        if (settings.surpressErrors) {
            return;
        }
    })
}( window.jQuery );

var django = {
    "jQuery": window.jQuery
}

if (typeof String.prototype.startsWith != 'function') {
  // see below for better implementation!
  String.prototype.startsWith = function (str){
    return this.slice(0, str.length) === str;
  };
}
if (typeof Array.prototype.indexOf != 'function') {
    Array.prototype.indexOf = function(elt /*, from*/) {
        var len = this.length >>> 0;
        var from = Number(arguments[1]) || 0;
        from = (from < 0) ? Math.ceil(from) : Math.floor(from);
        if (from < 0) from += len;

        for (; from < len; from++)
        {
            if (from in this && this[from] === elt) return from;
        }
        return -1;
    };
}