!(function ($) {
  "use strict";

  // Get CSRF
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  const csrftoken = getCookie('csrftoken')

  // Ajax requests
  function eventsAjax(
    event_type='',
    event_name='',
    time_spent='',
    message='',
  ) {
    var _path = window.location.origin + '/events/';
    var re = /.*kwp\/([\s\S]+?)$/;
    var document_name = window.location.href.match(re)[1].replaceAll("%20", " ");
    $.ajax({
      headers: {"X-CSRFToken": csrftoken},
      url: _path,
      method: "POST",
      data: {
        "event_type":event_type,
        "event_name":event_name,
        "time_spent": time_spent,
        "message":message,
        "document_name":document_name
      },
      dataType: "json"
    });
  }


  // Preloader
  $(window).on('load', function () {
    let preloader = document.getElementById('preloader');
    if ($(window).width() > 840) {
      $('#sidebarToggle').trigger('click');
    }
    setTimeout(function () {
      preloader.classList.add('loaded')
    }, 1000);

    var iframeInput = document.getElementById('pageNumber'),
      docContainer = document.getElementById('viewerContainer'),
      inputVal = $(iframeInput),
      valDict = {},
      startPage = new Date().getTime(),
      endPage,
      spentTime;


    valDict.oldVal = inputVal.val()
    eventsAjax('Interaction with Document', 'Opened page 1')

    $('.downloadMobile, .downloadDesktop').on('click', function () {
      eventsAjax('Interaction with Document', 'Download');
    })

    $(docContainer).scroll(function() {
      let docElem = docContainer,
        scrollTop = docElem['scrollTop'],
        scrollBottom = (docElem['scrollHeight']) - window.innerHeight,
        scrollPercent = scrollTop / scrollBottom * 100 + '%';

      document.getElementById('progress-bar').style.setProperty('--scrollAmount', scrollPercent);
      valDict.newVal = inputVal.val()

      if (valDict.newVal !== valDict.oldVal) {
        endPage = new Date().getTime()
        spentTime = ((endPage - startPage) / 1000)
        if (valDict.oldVal !== '0') {
          eventsAjax('Interaction with Document', 'Spent seconds on page number ' + valDict.oldVal, '' + spentTime)
          eventsAjax('Interaction with Document', "Opened page " + valDict.newVal);
        }
        valDict.oldVal = valDict.newVal
        startPage = new Date().getTime()
      }

    });
  });

  $(document).on('copy', function () {
    let selected_text = document.getSelection().toString().replace("\n", ' '),
      l = selected_text.length;
    if (l > 50) {
        selected_text = selected_text.substring(0, 20) + ' ... ' + selected_text.substring(l-20, l);
    }
    eventsAjax('Interaction with Document', 'Copied text: '+selected_text);
  });


})(jQuery);