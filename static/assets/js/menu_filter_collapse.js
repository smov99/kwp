!(function($){ $(document).ready(function(){
    $('#changelist-filter style, #changelist-filter link, #changelist-filter script, #changelist-filter .admindatefilter').wrapAll('<ul />')

    // Start with a filter list showing only its h3 subtitles; clicking on any
    // displays that filter content; clicking again collapses the list:
    $('#changelist-filter > h3').each(function(){
        var $title = $(this);
        $title.next().toggle();
        $title.css("cursor","pointer");
        $title.click(function(){
            $title.next().slideToggle();
        });
    });
  });
})(jQuery);