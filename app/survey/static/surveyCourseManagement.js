/*
global
alertify: false
call: false
fCall: false
fields: false
users: false
*/

const table = $('#table').DataTable({
    language: {
        url: '/static/build/language/Vietnamese.json'
    }
}); // eslint-disable-line new-cap

/**
 * Add user to datatable or edit line.
 * @param {mode} mode - Create or edit.
 * @param {properties} properties - Properties of the user.
 */
function addUser(mode, properties) {

  let values = [];
  for (let i = 0; i < fields.length; i++) {
      if(fields[i] == 'lecturer') {
          values.push(`${properties[fields[i]].full_name}`);
      }
      else {
          values.push(`${properties[fields[i]]}`);
      }

  }
  values.push(
    `<button id="student_index" type="button" class="btn btn-info btn-xs"
    onclick="gen_survey('${properties.id}')">Khảo sát</button>`,
  );
  if (mode == 'edit') {
    table.row($(`#${properties.id}`)).data(values);
  } else {
    const rowNode = table.row.add(values).draw(false).node();
    $(rowNode).attr('id', `${properties.id}`);
  }
}

(function() {
  for (let i = 0; i < users.length; i++) {
    addUser('create', users[i]);
  }
})();

function gen_survey(id) { // eslint-disable-line no-unused-vars
    call(`/course/get/${id}`, function (properties) {
        var course_code = properties.course_code
        var course_name = properties.name
        var lecturer = properties.lecturer.full_name
        $('#cf_course_code').text('Mã môn học: ' + course_code)
        $('#cf_course_name').text('Tên môn học: ' + course_name)
        $('#cf_lecturer').text('Giảng viên: ' + lecturer)
    })
    $('#gen_survey_confirm').modal('show');
    $('#do_gen_survey').click(function () {
        do_gen_survey(id);
    })
}

function do_gen_survey(id) {
    call(`/survey/course/gen_survey/${id}`, function (success) {
        if(success=='Success') {
            $('#alert_message').text('Tạo khảo sát thành công!')
            $('#alert').modal('show');
        }
        else {
            $('#alert_message').text(success)
        }
    })
    $('#alert').modal('show');
    $('#gen_survey_confirm').modal('hide');
}

function gen_survey_for_all() {
    $('#gen_survey_for_all_confirm').modal('show');
    $('#do_gen_survey_for_all').click(function () {
        do_gen_survey_for_all();
    })
}

function do_gen_survey_for_all() {
    call(`/survey/course/gen_survey_for_all`, function (success) {
        if(success=='Success') {
            $('#alert_message').text('Thạo khảo sát thành công!')
            $('#alert').modal('show');
        }
        else {
            $('#alert_message').text(success)
        }
    })
    $('#alert').modal('show');
    $('#gen_survey_for_all_confirm').modal('hide');
}