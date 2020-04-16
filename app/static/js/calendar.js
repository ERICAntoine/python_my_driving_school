function parseObject(json){
    for(let i = 0; i < json.length; i++){
        for(let key in json[i]){
            if(key === 'pk'){
                console.log()
                json[i]["fields"]["idPlanning"] = json[i][key];
            }
        }
        json[i] = json[i]["fields"];
    }
    return json;
}

function updatePlanning(json){
    const csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    return new Promise(function(resolve, reject){
        $.ajaxSetup({headers: { "X-CSRFToken": csrftoken }});
        $.post('/app/planning/update', json)
        .done(function() {
            resolve(true);
        })
        .fail(function(e) {
            console.log(e)
            reject(false)
            alert( e.responseJSON.message );
        })
    })
}

function deletePlanning(id){
    const csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    return new Promise(function(resolve, reject){
        $.ajaxSetup({headers: { "X-CSRFToken": csrftoken }});
        $.post('/app/planning/delete', {id: id})
        .done(function(res) {
            console.log(res)
            resolve(true);
        })
        .fail(function(e) {
            console.log(e)
            reject(false)
            alert( "Tu es un eleve, tu ne peux pas supprimer un event." );
        })
    })
}

function calendar(e){

    document.addEventListener('DOMContentLoaded', function() {
          const events = parseObject(JSON.parse(e));
          var calendarEl = document.getElementById('calendar');
  
          var calendar = new FullCalendar.Calendar(calendarEl, {
                plugins: [ 'dayGrid','interaction', 'timeGrid', 'list' ],
                locale: 'fr',
                header: {
                  left: 'prev, next today',
                  center: 'title',
                  right: 'dayGridMonth, timeGridWeek, list'
                },
                defaultView: 'timeGridWeek',
                events: events,
                nowIndicator: true,
                editable: true,
                eventDrop: (date) => {
                    if(!confirm("Etes vous sur de vouloir déplacer cette evenement")){
                        date.revert()
                    } else {
                        const start = moment(new Date(date.event.start)).format('YYYY-MM-DDTHH:mm:ss')
                        const end = moment(new Date(date.event.end)).format('YYYY-MM-DDTHH:mm:ss')
                        const eventData = {
                        "id": date.event.extendedProps.idPlanning,
                        "start": start,
                        "end": end,
                        "title": date.event.title,
                        "instructor": date.event.extendedProps.instructor,
                        "student": date.event.extendedProps.student
                        }
                        const update = updatePlanning(eventData);
                        update.then((res) => {
                            return true;
                        })
                        .catch((err) => {
                            console.log('revert')
                            date.revert()
                        })
                    }
                },
                eventResize: (date) => {
                    if(!confirm("Etes vous sur de vouloir déplacer cette evenement")){
                        date.revert()
                    } else {
                        const start = moment(new Date(date.event.start)).format('YYYY-MM-DDTHH:mm:ss')
                        const end = moment(new Date(date.event.end)).format('YYYY-MM-DDTHH:mm:ss')
                        const eventData = {
                        "id": date.event.extendedProps.idPlanning,
                        "start": start,
                        "end": end,
                        "title": date.event.title,
                        "instructor": date.event.extendedProps.instructor,
                        "student": date.event.extendedProps.student
                        }
                        console.log(eventData)
                        update.then((res) => {
                            return true;
                        })
                        .catch((err) => {
                            console.log('revert')
                            date.revert()
                        })
                    }
                },
                eventConstraint: {
                    start: moment().format('YYYY-MM-DD'),
                    end: '2100-01-01'
                },
                eventClick: function(info){
                    let id = info.event.extendedProps.idPlanning
                    let input = document.createElement("input");
                    input.value = info.event.title;
                    input.type = 'text';
                    input.className = 'swal-content__input';
                    swal({
                        text: "Mettre à jour le titre ou retirer l'event",
                        content: input,
                        value: info.event.title,
                        buttons: {
                            cancel: true,
                            delete: {
                                text: "Retirer",
                                className: "btn-danger"
                            },
                            confirm: {
                                text: "Mettre à jour"
                            }
                        },
                      })
                      .then((value) => {
                        switch (value) {
                            case "delete":
                                deletePlanning(id)
                            break;
                            case true:
                                swal("Gotcha!", "Pikachu was caught!", "success");
                            break;
                            }
                      });
                }
          });
          calendar.render();
        });
}
