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
    let _path = window.location.origin + '/events/';
    let re = /.*kwp\/([\s\S]+?)$/;
    let document_name = window.location.href.match(re)[1].replaceAll("%20", " ");
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

    let iframeInput = document.getElementById('pageNumber'),
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
    });

    let eventTimer = {'click': 0}

    $('body').on('DOMSubtreeModified', '.page', function () {
      $('.linkAnnotation a').on('click', function (e) {
        e.preventDefault()
        let eventStart = new Date().getTime()
        if (((eventStart - eventTimer.click)/1000) > 2) {
        eventsAjax('Interaction with Document', 'Following a link ' + $(this).attr('title') + ': ' + $(this).attr('href'))
        let tab = window.open(''+$(this).attr('href'), '_blank');
        if (tab) {
          tab.focus();
        }
        eventTimer.click = new Date().getTime()
        }
      });
    });

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