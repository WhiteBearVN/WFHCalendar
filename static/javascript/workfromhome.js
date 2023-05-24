document.addEventListener('DOMContentLoaded', function () {
  var calendarEl = document.getElementById('calendar');

  var calendar = new FullCalendar.Calendar(calendarEl, {
    timeZone: 'UTC',
    themeSystem: 'bootstrap5',
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth'
    },
    hiddenDays: [ 0, 6 ],
    weekNumbers: true,
    dayMaxEvents: true, // allow "more" link when too many events
    events: {
      url: 'workdays',
      error: function() {
        $('#script-warning').show();
      }
    },
    dateClick: function(info) {
      //Create event
      var result = confirm("Confirm to work from home this date?");

if (result) {
  var event = {
    title: 'Registered, please refesh page',
    color: '#2b31db',
    start: info.dateStr 
  };
  
  var body = {
    workday: info.dateStr
  };
  
  fetch("https://whitebearvn-ideal-succotash-46pqvgp6v463vw6-5000.preview.app.github.dev/api/workday", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(body)
  });
} else {
  // Nothing
}

      // Add event to calendar, comment after done backend
      calendar.addEvent(event);
    }
    
  });

  calendar.render();
  
});