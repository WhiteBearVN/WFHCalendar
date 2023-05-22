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
      events: 'https://fullcalendar.io/api/demo-feeds/events.json',
      dateClick: function(info) {
        //Create event
        var result = confirm("Confirm to leave office this date?");
  
          if (result) {
              var event = {
              title: '... Work from home',
              start: info.dateStr 
           };
              const body = {
              workday: info.dateStr
              };
              $.post("https://jsonplaceholder.typicode.com/todos", body, (data, status) => {
              console.log(data);
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