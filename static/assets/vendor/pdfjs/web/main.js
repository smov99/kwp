!(function ($) {
  "use strict";

  // Get CSRF
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
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
  function eventsAjax(event_type, event_name, time_spent, message) {
    var _path = window.location.origin + '/events/';
    $.ajax({
      headers: {"X-CSRFToken": csrftoken},
      url: _path,
      method: "POST",
      data: {"event_type":event_type, "event_name":event_name, "time_spent": time_spent, "message":message},
      dataType: "json"
    });
  }

  // Preloader
  $(window).on('load', function () {
    let preloader = document.getElementById('preloader');
    setTimeout(function () {
      preloader.classList.add('loaded')
    }, 1000)

    var timeTracker = {};

    timeTracker['pageStart'] = new Date();
    var iframeInput = document.getElementById('pageNumber'),
      docContainer = document.getElementById('viewerContainer'),
      downloadBtn = document.getElementById('proposal-download-btn'),
      inputVal = $(iframeInput),
      valDict = {},
      startPage = new Date().getTime(),
      endPage,
      spentTime;


    valDict.oldVal = inputVal.val()
    eventsAjax('page_opened', 'PDF page 1')

    $(downloadBtn).on('click', function () {
      eventsAjax('download', 'PDF downloaded');
    })

    $(docContainer).scroll(function() {
      let docElem = docContainer,
        scrollTop = docElem['scrollTop'],
        scrollBottom = (docElem['scrollHeight']) - window.innerHeight,
        scrollPercent = scrollTop / scrollBottom * 100 + '%',
        downloadContainer = document.getElementById('download-container');

      document.getElementById('progress-bar').style.setProperty('--scrollAmount', scrollPercent);

      if ((scrollTop / scrollBottom) * 100 >= 50) {
        $(downloadContainer).removeClass('hide')
      } else {
        $(downloadContainer).addClass('hide')
      }
      valDict.newVal = inputVal.val()

      if (valDict.newVal !== valDict.oldVal) {
        endPage = new Date().getTime()
        spentTime = ((endPage - startPage) / 1000)
        if (valDict.oldVal !== '0') {
          eventsAjax('spent_time', 'Spent seconds on page number ' + valDict.oldVal, '' + spentTime)
          eventsAjax('page_opened', "PDF page " + valDict.newVal);
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
    eventsAjax('copying_in_pdf', 'Copied text: '+selected_text);
  });


})(jQuery);